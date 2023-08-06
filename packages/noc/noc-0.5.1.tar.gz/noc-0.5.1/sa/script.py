# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Copyright (C) 2007-2009 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
"""
"""
from __future__ import with_statement
from noc.lib.fsm import StreamFSM
from noc.lib.registry import Registry
from noc.lib.nbsocket import PTYSocket,UDPSocket,SocketTimeoutError
from noc.lib.debug import format_frames,get_traceback_frames
from noc.lib.text import replace_re_group
from noc.sa.protocols.sae_pb2 import TELNET,SSH,HTTP
from noc.sa.profiles import profile_registry
from noc.settings import config
import logging,re,threading,Queue,urllib,httplib,random,base64,hashlib,cPickle,sys,time,datetime

try:
    from pysnmp.carrier.asynsock.dispatch import AsynsockDispatcher
    from pysnmp.carrier.asynsock.dgram import udp
    from pyasn1.codec.ber import encoder, decoder
    from pysnmp.proto import api
    HAS_SNMP=True
except ImportError:
    HAS_SNMP=False


##
##
##
scheme_id={
    "telnet" : TELNET,
    "ssh"    : SSH,
    "http"   : HTTP,
}
##
class TimeOutError(Exception): pass
class LoginError(Exception): pass
class CLISyntaxError(Exception): pass
##
##
##
class ScriptProxy(object):
    def __init__(self,parent):
        self._parent=parent
    def __getattr__(self,name):
        return ScriptCallProxy(self._parent,self._parent.profile.scripts[name])
    def has_script(self,name):
        return self._parent.profile.scripts.has_key(name)

class ScriptCallProxy(object):
    def __init__(self,parent,script):
        self.parent=parent
        self.script=script
        
    def __call__(self,**kwargs):
        s=self.script(self.parent.profile,self.parent.activator,self.parent.access_profile,parent=self.parent,**kwargs)
        return s.guarded_run()
##
##
##
class ScriptRegistry(Registry):
    name="ScriptRegistry"
    subdir="profiles"
    classname="Script"
    apps=["noc.sa"]
    exclude=["highlight"]
    def register_generics(self):
        for c in [c for c in self.classes.values() if c.name and c.name.startswith("Generic.")]:
            g,name=c.name.split(".")
            for p in profile_registry.classes:
                s_name=p+"."+name
                # Do not register generic when specific exists
                if s_name in self.classes:
                    continue
                to_register=True
                for r_name,r_interface in c.requires:
                    rs_name=p+"."+r_name
                    if rs_name not in self.classes or not self.classes[rs_name].implements_interface(r_interface):
                        to_register=False
                        break
                if to_register:
                    logging.debug("Script Registry: Register generic %s"%s_name)
                    self.classes[s_name]=c
                    profile_registry[p].scripts[name]=c
    def register_all(self):
        super(ScriptRegistry,self).register_all()
        self.register_generics()

script_registry=ScriptRegistry()
##
##
##
class ScriptBase(type):
    def __new__(cls,name,bases,attrs):
        m=type.__new__(cls,name,bases,attrs)
        m.implements=[c() for c in m.implements]
        script_registry.register(m.name,m)
        if m.name and not m.name.startswith("Generic."):
            pv,pos,sn=m.name.split(".",2)
            profile_registry["%s.%s"%(pv,pos)].scripts[sn]=m
        return m
##
## Configuration context manager to use with "with" statement
##
class ConfigurationContextManager(object):
    def __init__(self,script):
        self.script=script
    def __enter__(self):
        self.script.enter_config()
    def __exit__(self,exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.script.leave_config()
        else:
            raise exc_type, exc_val
##
##
##
class Script(threading.Thread):
    __metaclass__=ScriptBase
    name=None
    description=None
    # Interfaces list. Each element of list must be Interface subclass
    implements=[]
    # Scripts required by generic script.
    # For common scripts - empty list
    # For generics - list of pairs (script_name,interface)
    requires=[]
    # Constants
    TELNET=scheme_id["telnet"]
    SSH=scheme_id["ssh"]
    HTTP=scheme_id["http"]
    TIMEOUT=120 # 2min by default
    #
    LoginError=LoginError
    CLISyntaxError=CLISyntaxError

    def __init__(self,profile,activator,access_profile,parent=None,**kwargs):
        self.start_time=time.time()
        self.to_cancel=False
        self.parent=parent
        self.access_profile=access_profile
        if self.access_profile.address:
            p=self.access_profile.address
        elif self.access_profile.path:
            p=self.access_profile.path
        else:
            p="<unknown>"
        self.debug_name="script-%s-%s"%(p,self.name)
        super(Script,self).__init__(name=self.debug_name,kwargs=kwargs)
        self.activator=activator
        self.servers=activator.servers
        self.profile=profile
        self.cli_provider=None
        self.http=HTTPProvider(self.access_profile)
        if HAS_SNMP:
            self.snmp=SNMPProvider(self)
        else:
            self.snmp=None
        self.status=False
        self.result=None
        self.error_traceback=None
        self.login_error=None
        self.strip_echo=True
        self.kwargs=kwargs
        self.scripts=ScriptProxy(self)
        self.need_to_save=False
        self.to_disable_pager=not self.parent and self.profile.command_disable_pager
        self.log_cli_sessions_path=None # Path to log CLI session
        if self.parent:
            self.log_cli_sessions_path=self.parent.log_cli_sessions_path
        elif self.activator.log_cli_sessions\
            and self.activator.log_cli_sessions_ip_re.search(self.access_profile.address)\
            and self.activator.log_cli_sessions_script_re.search(self.name):
            self.log_cli_sessions_path=self.activator.log_cli_sessions_path
            for k,v in [
                ("ip",self.access_profile.address),
                ("script",self.name),
                ("ts",datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))]:
                self.log_cli_sessions_path=self.log_cli_sessions_path.replace("{{%s}}"%k,v)
            self.cli_debug("IP: %s SCRIPT: %s"%(self.access_profile.address,self.name),"!")
    ##
    ##
    ##
    def cli_debug(self,msg,chars=None):
        if not self.log_cli_sessions_path:
            return
        m=datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
        if chars:
            m+=chars*50
        m+="\n"
        m+=msg+"\n"
        with open(self.log_cli_sessions_path,"a") as f:
            f.write(m)
    ##
    ## Checks script is stale and must be terminated
    ##
    def is_stale(self):
        return time.time()-self.start_time > self.TIMEOUT
    
    @classmethod
    def implements_interface(cls,interface):
        for i in cls.implements:
            if type(i)==interface:
                return True
        return False
        
    def debug(self,msg):
        logging.debug("[%s] %s"%(self.debug_name,msg))
    
    def error(self,msg):
        logging.error("[%s] %s"%(self.debug_name,msg))
        
    def guarded_run(self):
        self.debug("Guarded run")
        # Enforce interface type checking
        for i in self.implements:
            self.kwargs=i.script_clean_input(self.profile,**self.kwargs)
        # Calling script body
        result=self.execute(**self.kwargs)
        # Enforce interface result checking
        for i in self.implements:
            result=i.script_clean_result(self.profile,result)
        self.debug("Script returns with result: %s"%result)
        return result
        
    def serialize_result(self,result):
        return cPickle.dumps(result)
        
    def run(self):
        self.debug("Running")
        result=None
        try:
            result=self.guarded_run()
            self.result=self.serialize_result(result)
            if self.parent is None and self.need_to_save and self.profile.command_save_config:
                self.debug("Saving config")
                self.cli(self.profile.command_save_config)
        except TimeOutError:
            self.error("Timed out")
        except self.LoginError,why:
            self.login_error=why.args[0]
            self.error("Login failed: %s"%self.login_error)
        except:
            t,v,tb=sys.exc_info()
            r=[str(t),str(v)]
            r+=[format_frames(get_traceback_frames(tb))]
            self.error_traceback="\n".join(r)
            self.debug("Script traceback:\n%s"%self.error_traceback)
        self.debug("Closing")
        if self.activator.to_save_output and result:
            self.activator.save_result(result,self.motd)
        if self.cli_provider:
            self.activator.request_call(self.cli_provider.close)
        if self.snmp:
            self.snmp.close()
        self.activator.on_script_exit(self)
        
    def execute(self,**kwargs):
        return None
    ##
    ## Request CLI provider's queue
    ## Handle cancel condition
    ##
    def cli_queue_get(self):
        while True:
            try:
                return self.cli_provider.queue.get(block=True,timeout=1)
            except Queue.Empty:
                if self.to_cancel:
                    self.error("Canceled")
                    raise TimeOutError()
                else:
                    continue
    
    def request_cli_provider(self):
        if self.parent:
            self.cli_provider=self.parent.request_cli_provider()
        elif self.cli_provider is None:
            self.debug("Running new provider")
            if self.access_profile.scheme==TELNET:
                s_class=CLITelnetSocket
            elif self.access_profile.scheme==SSH:
                s_class=CLISSHSocket
            else:
                raise Exception("Invalid access scheme '%d' for CLI"%self.access_profile.scheme)
            self.cli_provider=s_class(self.activator.factory,self.profile,self.access_profile)
            self.cli_queue_get()
            self.debug("CLI Provider is ready")
            # Disable pager when necessary
            if self.to_disable_pager:
                self.debug("Disable paging")
                self.to_disable_pager=False
                self.cli(self.profile.command_disable_pager)
        return self.cli_provider
    ##
    ## Execute CLI command and return a result
    ## if list_re is None, return a string
    ## if list_re is regular expression object, return a list of dicts (group name -> value), one dict per matched line
    ##
    def cli(self,cmd,command_submit=None,bulk_lines=None,list_re=None):
        #
        self.debug("cli(%s)"%cmd)
        self.cli_debug(cmd,">")
        # Submit command
        command_submit=self.profile.command_submit if command_submit is None else command_submit
        if self.activator.use_canned_session:
            data=self.activator.cli(cmd)
        else:
            self.request_cli_provider()
            self.cli_provider.submit(cmd,command_submit=command_submit,bulk_lines=bulk_lines)
            data=self.cli_queue_get()
        # Save canned output if requested
        if self.activator.to_save_output:
            self.activator.save_interaction("cli",cmd,data)
        if isinstance(data,Exception):
            # Exception captured
            raise data
        # Check for syntax error
        if self.profile.pattern_syntax_error and re.search(self.profile.pattern_syntax_error,data):
            raise self.CLISyntaxError()
        # Echo cancelation
        if self.strip_echo and data.lstrip().startswith(cmd):
            data=data.lstrip()
            if data.startswith(cmd+"\n"):
                # Remove first line
                data=self.strip_first_lines(data.lstrip())
            else:
                # Some switches, like ProCurve do not send \n after the echo
                data=data[len(cmd):]
        # Convert to list when required
        if list_re:
            r=[]
            for l in data.splitlines():
                match=list_re.match(l.strip())
                if match:
                    r+=[match.groupdict()]
            data=r
        self.debug("cli(%s) returns:\n---------\n%s\n---------"%(cmd,repr(data)))
        self.cli_debug(data,"<")
        return data
    ##
    ## Clean up config from all unnecessary trash
    ##
    def cleaned_config(self,config):
        return self.profile.cleaned_config(config)
    ##
    ##
    ##
    def strip_first_lines(self,text,lines=1):
        t=text.split("\n")
        if len(t)<=lines:
            return ""
        else:
            return "\n".join(t[lines:])
    ##
    ## Expands expressions like "1,2,5-7" to [1,2,5,6,7]
    ##
    def expand_rangelist(self,s):
        result={}
        for x in s.split(","):
            x=x.strip()
            if x=="":
                continue
            if "-" in x:
                l,r=[int(y) for y in x.split("-")]
                if l>r:
                    x=r
                    r=l
                    l=x
                for i in range(l,r+1):
                    result[i]=None
            else:
                result[int(x)]=None
        return sorted(result.keys())
    ##
    ## Convert a 6-octet string to MAC address
    ##
    def hexstring_to_mac(self,s):
        return ":".join(["%02X"%ord(x) for x in s])
    ##
    ## Cancel script
    ##
    def cancel_script(self):
        self.to_cancel=True
        
    ## Returns configuration context
    def configure(self):
        return ConfigurationContextManager(self)
        
    # Enter configuration mote
    def enter_config(self):
        if self.profile.command_enter_config:
            self.cli(self.profile.command_enter_config)
    # Leave configuration mode
    def leave_config(self):
        if self.profile.command_leave_config:
            self.cli(self.profile.command_leave_config)
            self.cli("") # Guardian empty command to wait until configuration is finally written
    # Save current config
    def save_config(self,immediately=False):
        if immediately:
            if self.profile.command_save_config:
                self.cli(self.profile.command_save_config)
        else:
            self.schedule_to_save()
    #
    def schedule_to_save(self):
        self.need_to_save=True
        if self.parent:
            self.parent.schedule_to_save()
    
    def motd(self):
        if self.activator.use_canned_session:
            return self.activator.get_motd()
        if not self.cli_provider:
            self.request_cli_provider()
        return self.cli_provider.motd
    motd=property(motd)

##
##
##
class TimeOutError(Exception): pass
##
##
##
class CLI(StreamFSM):
    FSM_NAME="CLI"
    DEFAULT_STATE="START"
    STATES={
        "START":{
            "USERNAME"            : "USERNAME",
            "PASSWORD"            : "PASSWORD",
            "UNPRIVELEGED_PROMPT" : "UNPRIVELEGED_PROMPT",
            "PROMPT"              : "PROMPT",
            "PAGER"               : "START",
        },
        "USERNAME":{
            "USERNAME"            : "FAILURE",
            "PASSWORD"            : "PASSWORD",
            "UNPRIVELEGED_PROMPT" : "UNPRIVELEGED_PROMPT",
            "PROMPT"              : "PROMPT"
        },
        "PASSWORD":{
            "USERNAME"            : "FAILURE",
            "PASSWORD"            : "FAILURE",
            "UNPRIVELEGED_PROMPT" : "UNPRIVELEGED_PROMPT",
            "PROMPT"              : "PROMPT",
            "PAGER"               : "PASSWORD",
        },
        "SUPER_PASSWORD" : {
            "UNPRIVELEGED_PROMPT" : "FAILURE",
            "PASSWORD"            : "FAILURE",
            "PROMPT"              : "PROMPT",
            "PAGER"               : "SUPER_PASSWORD"
        },
        "UNPRIVELEGED_PROMPT":{
            "PASSWORD"            : "SUPER_PASSWORD",
            "PROMPT"              : "PROMPT",
        },
        "PROMPT":{
            "PROMPT"      : "PROMPT",
            "PAGER"       : "PROMPT",
            "CLOSE"       : "CLOSED",
        },
        "FAILURE":{
        },
        "CLOSED":{
        }
    }
    
    def __init__(self,profile,access_profile):
        self.profile=profile
        self.access_profile=access_profile
        self.queue=Queue.Queue()
        self.is_ready=False
        self.collected_data=""
        self.submitted_data=[]
        self.submit_lines_limit=None
        self.motd="" # Message of the day storage
        self.pattern_prompt=None # Set when entering PROMPT state
        if isinstance(self.profile.pattern_more,basestring):
            self.more_patterns=[self.profile.pattern_more]
            self.more_commands=[self.profile.command_more]
        else:
            # .more_patterns is a list of (pattern,command)
            self.more_patterns=[x[0] for x in self.profile.pattern_more]
            self.more_commands=[x[1] for x in self.profile.pattern_more]
        self.pager_patterns="|".join([r"(%s)"%p for p in self.more_patterns])
        StreamFSM.__init__(self)
    
    def on_read(self,data):
        self.debug("on_read: %s"%repr(data))
        if self.profile.rogue_chars:
            for rc in self.profile.rogue_chars:
                try:
                    data=rc.sub("",data) # rc is compiled regular expression
                except AttributeError:
                    data=data.replace(rc,"") # rc is a string
        self.feed(data,cleanup=self.profile.cleaned_input)
        self.__flush_submitted_data()
    ##
    ## Feed pending submitted data
    ##
    def __flush_submitted_data(self):
        if self.submitted_data:
            self.debug("%d lines to submit"%len(self.submitted_data))
            sd="\n".join(self.submitted_data[:self.submit_lines_limit])+"\n"
            self.submitted_data=self.submitted_data[self.submit_lines_limit:]
            self.write(sd)
    
    def submit(self,msg,command_submit=None,bulk_lines=None):
        self.debug("submit(%s,bulk_lines=%s)"%(repr(msg),bulk_lines))
        self.submit_lines_limit=bulk_lines
        if bulk_lines:
            self.submitted_data=msg.splitlines()
            self.__flush_submitted_data()
        else:
            self.write(msg+(self.profile.command_submit if command_submit is None else command_submit))
    ##
    def on_START_enter(self):
        # username/password match
        p=[
            (self.profile.pattern_username,"USERNAME"),
            (self.profile.pattern_password,"PASSWORD"),
        ]
        # Match unpriveleged prompt when given
        if self.profile.pattern_unpriveleged_prompt:
            p+=[(self.profile.pattern_unpriveleged_prompt,"UNPRIVELEGED_PROMPT")]
        # Match priveleged prompt when given
        p+=[(self.profile.pattern_prompt,"PROMPT")]
        # Match pager
        p+=[(self.pager_patterns,"PAGER")]
        self.set_patterns(p)
    
    def on_USERNAME_enter(self):
        self.motd="" # Reset MoTD
        self.set_patterns([
            (self.profile.pattern_password, "PASSWORD"),
            (self.profile.pattern_prompt,   "PROMPT"),
        ])
        self.submit(self.access_profile.user)
        
    def on_PASSWORD_enter(self):
        self.motd="" # Reset MoTD
        p=[(self.profile.pattern_prompt, "PROMPT")]
        if self.profile.pattern_unpriveleged_prompt:
            p+=[(self.profile.pattern_unpriveleged_prompt,"UNPRIVELEGED_PROMPT")]
        p+=[
            (self.profile.pattern_username, "USERNAME"),
            (self.profile.pattern_password, "PASSWORD")
            ]
        p+=[(self.pager_patterns,"PAGER")]
        self.set_patterns(p)
        self.submit(self.access_profile.password)
        
    def on_UNPRIVELEGED_PROMPT_enter(self):
        self.set_patterns([
            (self.profile.pattern_prompt,   "PROMPT"),
            (self.profile.pattern_password, "PASSWORD")
        ])
        self.submit(self.profile.command_super)
    
    def on_SUPER_PASSWORD_enter(self):
        self.set_patterns([
            (self.profile.pattern_prompt, "PROMPT"),
            (self.profile.pattern_password, "PASSWORD"),
            (self.pager_patterns,"PAGER")
        ])
        sp=self.access_profile.super_password
        if not sp:
            sp=""
        self.submit(sp)
        
    def on_PROMPT_enter(self):
        self.debug("on_PROMPT_enter")
        if not self.is_ready:
            self.pattern_prompt=self.profile.pattern_prompt
            # Refine prompt pattern when necessary
            for k,v in self.match.groupdict().items():
                v=re.escape(v)
                self.pattern_prompt=replace_re_group(self.pattern_prompt,"(?P<%s>"%k,v)
                self.pattern_prompt=replace_re_group(self.pattern_prompt,"(?P=%s"%k,v)
            self.debug("Using prompt pattern: %s"%self.pattern_prompt)
            self.queue.put(None) # Signal provider passing into PROMPT state
            self.is_ready=True
        p=[
            (self.pattern_prompt, "PROMPT"),
            (self.pager_patterns, "PAGER"),
            ]
        self.set_patterns(p)
        
    def on_PROMPT_match(self,data,match):
        if match.re.pattern in self.pager_patterns:
            self.collected_data+=data
        elif match.re.pattern==self.pattern_prompt:
            self.queue.put(self.collected_data+data)
            self.collected_data=""
        
    def on_PROMPT_PAGER(self):
        pg=self.match.group(0)
        for p,c in zip(self.more_patterns,self.more_commands):
            if re.search(p,pg,re.DOTALL|re.MULTILINE):
                self.write(c)
                return
        raise Exception("Unexpected pager pattern")
    on_START_PAGER=on_PROMPT_PAGER
    on_PASSWORD_PAGER=on_PROMPT_PAGER
    
    def on_FAILURE_enter(self):
        self.set_patterns([])
        if not self.is_ready:
            self.queue.put(None)
        self.queue.put(Script.LoginError(self.motd))

    def on_START_match(self,data,match):
        self.motd+=data
    on_USERNAME_match=on_START_match
    on_PASSWORD_match=on_START_match
##
##
##
class ScriptSocket(object):pass
#
##
##
class CLITelnetSocket(ScriptSocket,CLI,PTYSocket):
    TTL=30
    def __init__(self,factory,profile,access_profile):
        logging.debug("CLITelnetSocket connecting '%s'"%access_profile.address)
        cmd_args=[config.get("path","telnet"),access_profile.address]
        if access_profile.port and access_profile.port!=23:
            cmd_args+=[str(access_profile.port)]
        CLI.__init__(self,profile,access_profile)
        PTYSocket.__init__(self,factory,cmd_args)
        ScriptSocket.__init__(self)
##
##
##
class CLISSHSocket(ScriptSocket,CLI,PTYSocket):
    TTL=30
    def __init__(self,factory,profile,access_profile):
        logging.debug("CLISSHSocket connecting '%s'"%access_profile.address)
        cmd_args=[config.get("path","ssh"),"-o","StrictHostKeyChecking=no","-o","UserKnownHostsFile=/dev/null","-l",access_profile.user]
        if access_profile.port and access_profile.port!=22:
            cmd_args+=["-p",str(access_profile.port)]
        cmd_args+=[access_profile.address]
        CLI.__init__(self,profile,access_profile)
        PTYSocket.__init__(self,factory,cmd_args)
        ScriptSocket.__init__(self)
##
##
##
class HTTPProvider(object):
    def __init__(self,access_profile):
        self.access_profile=access_profile
        self.authorization=None
    
    def request(self,method,path,params=None,headers={}):
        if self.authorization:
            headers["Authorization"]=self.authorization
        conn=httplib.HTTPConnection(self.access_profile.address)
        conn.request(method,path,params,headers)
        response=conn.getresponse()
        try:
            if response.status==200:
                return response.read()
            elif response.status==401 and self.authorization is None:
                self.set_authorization(response.getheader("www-authenticate"),method,path)
                return self.request(method,path,params,headers)
            else:
                raise Exception("HTTP Error: %s"%response.status)
        finally:
            conn.close()
            
    def set_authorization(self,auth,method,path):
        scheme,data=auth.split(" ",1)
        scheme=scheme.lower()
        d={}
        for s in data.split(","):
            s=s.strip()
            if "=" in s:
                k,v=s.split("=",1)
                if v.startswith("\"") and v.endswith("\""):
                    v=v[1:-1]
                d[k]=v
            else:
                d[s]=None
        if scheme=="basic":
            self.authorization="Basic %s"%base64.b64encode("%s:%s"%(self.access_profile.user,self.access_profile.password)).strip()
        elif scheme=="digest":
            H = lambda x: hashlib.md5(x).hexdigest()
            KD= lambda x,y: H("%s:%s"%(x,y))
            A1="%s:%s:%s"%(self.access_profile.user,d["realm"],self.access_profile.password)
            A2="%s:%s"%(method,path)
            f={
                "username": self.access_profile.user,
                "realm"   : d["realm"],
                "nonce"   : d["nonce"],
                "uri"     : path,
            }
            if "qop" not in d:
                noncebit="%s:%s"%(d["nonce"],H(A2))
            elif d["qop"]=="auth":
                nc="00000001"
                cnonce=H(str(random.random()))
                f["nc"]=nc
                f["cnonce"]=cnonce
                f["qop"]=d["qop"]
                noncebit="%s:%s:%s:%s:%s"%(d["nonce"],nc,cnonce,d["qop"],H(A2))
            else:
                raise Exception("qop not supported: %s"%d["qop"])
            f["response"]=KD(H(A1),noncebit)
            self.authorization="Digest "+", ".join(["%s=\"%s\""%(k,v) for k,v in f.items()])
        else:
            raise Exception("Unknown auth method: %s"%scheme)
    
    def get(self,path,params=None,headers={}):
        return self.request("GET",path)
    
    def post(self,path,params=None,headers={}):
        if params:
            params=urllib.urlencode(params)
            headers["Content-Type"]="application/x-www-form-urlencoded"
        return self.request("POST",path,params,headers)
##
##
##
class SNMPGetSocket(UDPSocket):
    TTL=3
    def __init__(self,provider,oid):
        super(SNMPGetSocket,self).__init__(provider.factory)
        self.provider=provider
        self.oid=oid
        self.address=self.provider.access_profile.address
        self.got_result=False
        self.is_failed=False
        self.sendto(self.get_snmp_request(),(self.address,161))
    ##
    ## Build full community, appending suffix when necessary
    ##
    def get_community(self):
        c=self.provider.access_profile.snmp_ro
        if self.provider.community_suffix:
            c+=self.provider.community_suffix
        return c
    ##
    ## Convert oid from string to a list of integers
    ##
    def oid_to_tuple(self,oid):
        return [int(x) for x in oid.split(".")]
    ##
    ## Returns string containing SNMP GET requests to self.oids
    ##
    def get_snmp_request(self):
        self.provider.script.debug("%s SNMP GET %s"%(self.address,self.oid))
        p_mod=api.protoModules[api.protoVersion2c]
        req_PDU =  p_mod.GetRequestPDU()
        p_mod.apiPDU.setDefaults(req_PDU)
        p_mod.apiPDU.setVarBinds(req_PDU,[(self.oid_to_tuple(self.oid),p_mod.Null())])
        req_msg = p_mod.Message()
        p_mod.apiMessage.setDefaults(req_msg)
        p_mod.apiMessage.setCommunity(req_msg, self.get_community())
        p_mod.apiMessage.setPDU(req_msg, req_PDU)
        self.req_PDU=req_PDU
        return encoder.encode(req_msg)
    ##
    ## Read and parse reply.
    ## Call set_data for all returned values
    ##
    def on_read(self,data,address,port):
        p_mod=api.protoModules[api.protoVersion2c]
        while data:
            rsp_msg, data = decoder.decode(data, asn1Spec=p_mod.Message())
            rsp_pdu = p_mod.apiMessage.getPDU(rsp_msg)
            if p_mod.apiPDU.getRequestID(self.req_PDU)==p_mod.apiPDU.getRequestID(rsp_pdu):
                errorStatus = p_mod.apiPDU.getErrorStatus(rsp_pdu)
                if errorStatus:
                    self.provider.script.error("%s SNMP GET ERROR: %s"%(self.address,errorStatus.prettyPrint()))
                    break
                else:
                    for oid, val in p_mod.apiPDU.getVarBinds(rsp_pdu):
                        self.provider.script.debug('%s SNMP GET REPLY: %s %s'%(self.address,oid.prettyPrint(),val.prettyPrint()))
                        self.got_result=True
                        self.provider.queue.put(str(val))
                        break
        self.close()
    ##
    ##
    ##
    def on_close(self):
        if not self.got_result:
            self.provider.script.debug("SNMP Timeout")
            self.provider.queue.put(None)
        elif self.is_failed:
            self.provider.script.debug("Stale SNMP Operation")
            self.provider.queue.put(None)
        super(SNMPGetSocket,self).on_close()
    ##
    ## Raise timeout error when in stale
    ##
    def is_stale(self):
        r=super(SNMPGetSocket,self).is_stale()
        if r:
            self.is_failed=True
        return r
##
##
##
class SNMPGetNextSocket(SNMPGetSocket):
    TTL=5
    
    def __init__(self,provider,oid,bulk=False,min_index=None,max_index=None):
        self.bulk=bulk
        self.min_index=min_index
        self.max_index=max_index
        super(SNMPGetNextSocket,self).__init__(provider,oid)
    ##
    ## Returns string containing SNMP GET requests to self.oids
    ##
    def get_snmp_request(self):
        self.provider.script.debug("%s SNMP %s %s"%(self.address,"GETBULK" if self.bulk else "GETNEXT",str(self.oid)))
        p_mod=api.protoModules[api.protoVersion2c]
        req_PDU =  p_mod.GetBulkRequestPDU() if self.bulk else p_mod.GetNextRequestPDU()
        self.api_pdu=p_mod.apiBulkPDU if self.bulk else p_mod.apiPDU
        self.api_pdu.setDefaults(req_PDU)
        if self.bulk:
            self.api_pdu.setNonRepeaters(req_PDU,0)   # <!>
            self.api_pdu.setMaxRepetitions(req_PDU,20)# <!>
        self.api_pdu.setVarBinds(req_PDU,[(p_mod.ObjectIdentifier(self.oid_to_tuple(self.oid)),p_mod.Null())])
        req_msg = p_mod.Message()
        p_mod.apiMessage.setDefaults(req_msg)
        p_mod.apiMessage.setCommunity(req_msg, self.get_community())
        p_mod.apiMessage.setPDU(req_msg, req_PDU)
        self.req_PDU=req_PDU
        self.req_msg=req_msg
        return encoder.encode(req_msg)

    def on_read(self,data,address,port):
        self.update_status()
        p_mod=api.protoModules[api.protoVersion2c]
        while data:
            self.provider.script.debug("SNMP PDU RECEIVED")
            rsp_msg, data = decoder.decode(data, asn1Spec=p_mod.Message())
            rsp_pdu = p_mod.apiMessage.getPDU(rsp_msg)
            # Match response to request
            if self.api_pdu.getRequestID(self.req_PDU)==p_mod.apiPDU.getRequestID(rsp_pdu):
                # Check for SNMP errors reported
                errorStatus = self.api_pdu.getErrorStatus(rsp_pdu)
                if errorStatus and errorStatus != 2:
                    raise errorStatus
                # Format var-binds table
                var_bind_table = self.api_pdu.getVarBindTable(self.req_PDU, rsp_pdu)
                # Report SNMP table
                for table_row in var_bind_table:
                    for name, val in table_row:
                        if val is None:
                            continue
                        oid=name.prettyPrint()
                        if not oid.startswith(self.oid):
                            self.close()
                            self.provider.queue.put(None)
                            return
                        # Check index range if given
                        if self.min_index is not None or self.max_index is not None:
                            index=int(oid.split(".")[-1])
                            if self.min_index is not None and index<self.min_index:
                                # Skip values below min_index
                                continue
                            if self.max_index and index>self.max_index:
                                # Finish processing
                                self.close()
                                self.provider.queue.put(None)
                                return
                        if self.bulk:
                            self.provider.script.debug("SNMP BULK DATA: %s %s"%(oid,str(val)))
                        else:
                            self.provider.script.debug('%s SNMP GETNEXT REPLY: %s %s'%(self.address,oid,str(val)))
                        self.provider.queue.put((oid,str(val)))
                        self.got_result=True
                # Stop on EOM
                for oid, val in var_bind_table[-1]:
                    if val is not None:
                        break
                    else:
                        self.close()
                        return
                self.api_pdu.setVarBinds(self.req_PDU, map(lambda (x,y),n=p_mod.Null(): (x,n), var_bind_table[-1]))
                self.api_pdu.setRequestID(self.req_PDU, p_mod.getNextRequestID())
                self.sendto(encoder.encode(self.req_msg),(self.address,161))
##
##
##
class SNMPProvider(object):
    TimeOutError=SocketTimeoutError
    def __init__(self,script):
        self.script=script
        self.access_profile=self.script.access_profile
        self.factory=script.activator.factory
        self.queue=Queue.Queue(maxsize=1)
        self.getnext_socket=None
        self.community_suffix=None
        self.to_save_output=self.script.activator.to_save_output
    
    def get(self,oid,community_suffix=None):
        if self.script.activator.use_canned_session:
            r=self.script.activator.snmp_get(oid)
            if r is None:
                raise self.TimeOutError()
            return r
        self.community_suffix=community_suffix
        s=SNMPGetSocket(self,oid)
        try:
            r=self.queue.get(block=True)
            if r is None:
                if self.script.activator.to_save_output:
                    self.script.activator.save_snmp_get(oid,None)
                raise self.TimeOutError()
        finally:
            s.close()
        if self.to_save_output:
            self.script.activator.save_snmp_get(oid,r)
        return r
    ##
    ## getnext generator.
    ## USAGE:
    ## for oid,v in self.getnext("xxxxx"):
    ##      ....
    ##
    def getnext(self,oid,community_suffix=None,bulk=False,min_index=None,max_index=None):
        if self.script.activator.use_canned_session:
            r=self.script.activator.snmp_getnext(oid)
            if r is None:
                raise self.TimeOutError()
            for l in r:
                yield l
            raise StopIteration
        if self.to_save_output:
            out=[]
        self.community_suffix=community_suffix
        if self.getnext_socket:
            self.getnext_socket.close()
        self.getnext_socket=SNMPGetNextSocket(self,oid,bulk=bulk,min_index=min_index,max_index=max_index)
        # Flush queue
        while not self.queue.empty():
            self.queue.get()
        while True:
            r=self.queue.get(block=True)
            if r is None:
                if self.getnext_socket.is_failed:  # Stale socket killed
                    if self.to_save_output:
                        self.script.activator.save_snmp_getnext(oid,None)
                    raise self.TimeOutError()
                elif self.getnext_socket.got_result: # Stop Iteration in case of success
                    if self.to_save_output:
                        self.script.activator.save_snmp_getnext(oid,out)
                    raise StopIteration
                else: # Socket closed by Timeout
                    if self.to_save_output:
                        self.script.activator.save_snmp_getnext(oid,None)
                    raise self.TimeOutError()
            else:
                if self.script.activator.to_save_output:
                    out+=[r]
                yield r
    ##
    ## getnext wrapper
    ## returns a hash of {index,value}
    ##
    def get_table(self,oid,community_suffix=None,bulk=False,min_index=None,max_index=None):
        r={}
        for o,v in self.getnext(oid,community_suffix=community_suffix,bulk=bulk,min_index=min_index,max_index=max_index):
            r[int(o.split(".")[-1])]=v
        return r
    ##
    ## Generator returning a rows of two snmp tables joined by index
    ##
    def join_tables(self,oid1,oid2,community_suffix=None,bulk=False,min_index=None,max_index=None):
        t1=self.get_table(oid1,community_suffix=community_suffix,bulk=bulk,min_index=min_index,max_index=max_index)
        t2=self.get_table(oid2,community_suffix=community_suffix,bulk=bulk,min_index=min_index,max_index=max_index)
        for k1,v1 in t1.items():
            try:
                yield (v1,t2[k1])
            except KeyError:
                pass
    ##
    ## Close all UDP sockets
    ##
    def close(self):
        if self.getnext_socket:
            self.getnext_socket.close()
            del self.getnext_socket
