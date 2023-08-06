# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Service Activation Engine Daemon
##----------------------------------------------------------------------
## Copyright (C) 2007-2011 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
"""
"""
## Python modules
from __future__ import with_statement
import os
import time
import datetime
import threading
import logging
import random
import cPickle
## Django modules
from django.db import reset_queries
## NOC modules
from noc.sa.models import Activator, ManagedObject, TaskSchedule, MapTask, periodic_registry, script_registry, profile_registry
from noc.fm.models import Event, EventData, EventPriority, EventClass, EventCategory, IgnoreEventRules
from noc.sa.rpc import RPCSocket, file_hash, get_digest, get_nonce
from noc.pm.models import TimeSeries
from noc.sa.protocols.sae_pb2 import *
from noc.lib.fileutils import read_file
from noc.lib.daemon import Daemon
from noc.lib.debug import error_report, DEBUG_CTX_CRASH_PREFIX
from noc.lib.nbsocket import ListenTCPSocket, AcceptedTCPSocket, AcceptedTCPSSLSocket, SocketFactory, Protocol, HAS_SSL

##
## Additions to MANIFEST-ACTIVATfOR file
##
ACTIVATOR_MANIFEST=[
    "sa/profiles/",
    "sa/interfaces/",
]

##
##
##
class Service(SAEService):
    def get_controller_activator(self,controller):
        return Activator.objects.get(name=self.sae.factory.get_name_by_socket(controller.stream))
    ##
    ## RPC interfaces
    ##
    def ping(self,controller,request,done):
        done(controller,response=PingResponse())
    
    def register(self,controller,request,done):
        try:
            activator=Activator.objects.get(name=request.name)
        except Activator.DoesNotExist:
            logging.error("Unknown activator '%s'"%request.name)
            e=Error()
            e.code=ERR_UNKNOWN_ACTIVATOR
            e.text="Unknown activator '%s'"%request.name
            done(controller,error=e)
            return
        logging.info("Requesting digest for activator '%s'"%request.name)
        r=RegisterResponse()
        r.nonce=get_nonce()
        controller.stream.nonce=r.nonce
        done(controller,response=r)
        
    def auth(self,controller,request,done):
        try:
            activator=Activator.objects.get(name=request.name)
        except Activator.DoesNotExist:
            logging.error("Unknown activator '%s'"%request.name)
            e=Error()
            e.code=ERR_UNKNOWN_ACTIVATOR
            e.text="Unknown activator '%s'"%request.name
            done(controller,error=e)
            return
        logging.info("Authenticating activator '%s'"%request.name)
        if controller.stream.nonce is None or get_digest(request.name,activator.auth,controller.stream.nonce)!=request.digest:
            e=Error()
            e.code=ERR_AUTH_FAILED
            e.text="Authencication failed for activator '%s'"%request.name
            done(controller,error=e)
            return
        r=AuthResponse()
        controller.stream.set_name(request.name)
        controller.stream.is_authenticated=True
        done(controller,response=r)
        
    def manifest(self,controller,request,done):
        if not controller.stream.is_authenticated:
            e=Error()
            e.code=ERR_AUTH_REQUIRED
            e.text="Authentication required"
            done(controller,error=e)
            return
        done(controller,response=self.sae.activator_manifest)
        
    def software_upgrade(self,controller,request,done):
        if not controller.stream.is_authenticated:
            e=Error()
            e.code=ERR_AUTH_REQUIRED
            e.text="Authentication required"
            done(controller,error=e)
            return
        r=SoftwareUpgradeResponse()
        for n in request.names:
            if n not in self.sae.activator_manifest_files:
                e=Error()
                e.code=ERR_INVALID_UPGRADE
                e.text="Invalid file requested for upgrade: %s"%n
                done(controller,error=e)
                return
            u=r.codes.add()
            u.name=n
            u.code=read_file(n)
        done(controller,response=r)
    ##
    ## Retrieve event filters
    ##
    def event_filter(self,controller,request,done):
        if not controller.stream.is_authenticated:
            e=Error()
            e.code=ERR_AUTH_REQUIRED
            e.text="Authentication required"
            done(controller,error=e)
            return
        activator=self.get_controller_activator(controller)
        r=EventFilterResponse()
        r.expire=self.sae.config.getint("sae","refresh_event_filter")
        # Build source filter
        for c in ManagedObject.objects.filter(activator=activator,trap_source_ip__isnull=False):
            r.sources.append(c.trap_source_ip)
        # Build event filter
        for ir in IgnoreEventRules.objects.filter(is_active=True):
            i=r.ignore_rules.add()
            i.left_re=ir.left_re
            i.right_re=ir.right_re
        done(controller,response=r)
        
    def event(self,controller,request,done):
        if not controller.stream.is_authenticated:
            e=Error()
            e.code=ERR_AUTH_REQUIRED
            e.text="Authentication required"
            done(controller,error=e)
            return
        activator=self.get_controller_activator(controller)
        try:
            mo=ManagedObject.objects.get(activator=activator,trap_source_ip=request.ip) if request.ip else None
        except ManagedObject.DoesNotExist:
            e=Error()
            e.code=ERR_UNKNOWN_EVENT_SOURCE
            e.text="Unknown event source '%s'"%request.ip
            done(controller,error=e)
            return
        self.sae.write_event(
            data=[(b.key,b.value) for b in request.body],
            timestamp=datetime.datetime.fromtimestamp(request.timestamp),
            managed_object=mo
        )
        done(controller,EventResponse())
    ##
    ## Performance management collected data stream
    ##
    def pm_data(self,controller,request,done):
        if not controller.stream.is_authenticated:
            e=Error()
            e.code=ERR_AUTH_REQUIRED
            e.text="Authentication required"
            done(controller,error=e)
            return
        for d in request.result:
            timestamp=datetime.datetime.fromtimestamp(d.timestamp)
            self.sae.write_event([
                    ("source",      "system"),
                    ("type",        "pm probe"),
                    ("probe_name",  d.probe_name),
                    ("probe_type",  d.probe_type),
                    ("service",     d.service),
                    ("result",      d.result),
                    ("message",     d.message),
                ],
                timestamp=timestamp)
        for d in request.data:
            value=d.value if not d.is_null else None
            TimeSeries.register(d.name,d.timestamp,value)
        done(controller,PMDataResponse())
##
## AcceptedTCPSocket with RPC Protocol
##
class SAESocket(RPCSocket,AcceptedTCPSocket):
    def __init__(self,factory,socket):
        AcceptedTCPSocket.__init__(self,factory,socket)
        RPCSocket.__init__(self,factory.sae.service)
        self.nonce=None
        self.is_authenticated=True
        
    @classmethod
    def check_access(cls,address):
        return Activator.check_ip_access(address)
    
    def close(self):
        # Rollback all active transactions
        e=Error()
        e.code=ERR_ACTIVATOR_LOST
        e.text="Connection with activator lost"
        self.transactions.rollback_all_transactions(e) # Close all active transactions
        super(AcceptedTCPSocket,self).close()
##
## SSL version of SAE socket
##
class SAESSLSocket(RPCSocket,AcceptedTCPSSLSocket):
    def __init__(self,factory,socket,cert):
        AcceptedTCPSSLSocket.__init__(self,factory,socket,cert)
        RPCSocket.__init__(self,factory.sae.service)
        self.nonce=None
        self.is_authenticated=True
        
    @classmethod
    def check_access(cls,address):
        return Activator.check_ip_access(address)

    def close(self):
        # Rollback all active transactions
        e=Error()
        e.code=ERR_ACTIVATOR_LOST
        e.text="Connection with activator lost"
        self.transactions.rollback_all_transactions(e) # Close all active transactions
        super(AcceptedTCPSSLSocket,self).close()
##
## SAE Supervisor
##
class SAE(Daemon):
    daemon_name="noc-sae"
    def __init__(self):
        Daemon.__init__(self)
        logging.info("Running SAE")
        #
        self.service=Service()
        self.service.sae=self
        #
        self.factory=SocketFactory(tick_callback=self.tick)
        self.factory.sae=self
        #
        self.sae_listener=None
        self.sae_ssl_listener=None
        # Periodic tasks
        self.active_periodic_tasks={}
        self.periodic_task_lock=threading.Lock()
        #
        self.activator_manifest=None
        self.activator_manifest_files=None
        #
        t=time.time()
        self.last_task_check=t
        self.last_crashinfo_check=t
        self.last_mrtask_check=t
        # Activator interface implementation
        self.servers=None
        self.to_save_output=False
        self.use_canned_session=False
        self.log_cli_sessions=False
        self.script_threads={}
        self.script_lock=threading.Lock()
    ##
    ## Create missed Task Schedules
    ##
    def update_task_schedules(self):
        for pt in periodic_registry.classes:
            if TaskSchedule.objects.filter(periodic_name=pt).count()==0:
                logging.info("Creating task schedule for %s"%pt)
                TaskSchedule(periodic_name=pt).save()
    ##
    ## Build activator manifest
    ##
    def build_manifest(self):
        logging.info("Building manifest")
        manifest=read_file("MANIFEST-ACTIVATOR").split("\n")+ACTIVATOR_MANIFEST
        manifest=[x.strip() for x in manifest if x]
        self.activator_manifest=ManifestResponse()
        self.activator_manifest_files=set()
        
        files=set()
        for f in manifest:
            if f.endswith("/"):
                for dirpath,dirnames,filenames in os.walk(f):
                    for f in [f for f in filenames if f.endswith(".py")]:
                        files.add(os.path.join(dirpath,f))
            else:
                files.add(f)
        for f in files:
            self.activator_manifest_files.add(f)
            cs=self.activator_manifest.files.add()
            cs.name=f
            cs.hash=file_hash(f)
            
    def start_listeners(self):
        # SAE Listener
        sae_listen=self.config.get("sae","listen")
        sae_port=self.config.getint("sae","port")
        if self.sae_listener and (self.sae_listener.address!=sae_listen or self.sae_listener.port!=sae_port):
            self.sae_listener.close()
            self.sae_listener=None
        if self.sae_listener is None:
            logging.info("Starting SAE listener at %s:%d"%(sae_listen,sae_port))
            self.sae_listener=self.factory.listen_tcp(sae_listen,sae_port,SAESocket)
        # SAE SSL Listener
        if HAS_SSL:
            sae_ssl_listen=self.config.get("sae","ssl_listen")
            sae_ssl_port=self.config.getint("sae","ssl_port")
            sae_ssl_cert=self.config.get("sae","ssl_cert")
            if self.sae_ssl_listener and (self.sae_ssl_listener.address!=sae_ssl_listen or self.sae_ssl_listener.port!=sae_ssl_port):
                self.sae_ssl_listener.close()
                self.sae_ssl_listener=None
            if self.sae_ssl_listener is None:
                logging.info("Starting SAE SSL listener at %s:%d"%(sae_ssl_listen,sae_ssl_port))
                self.sae_ssl_listener=self.factory.listen_tcp(sae_ssl_listen,sae_ssl_port,SAESSLSocket,cert=sae_ssl_cert)
    ##
    ## Run SAE event loop
    ##
    def run(self):
        self.update_task_schedules()
        self.build_manifest()
        self.start_listeners()
        self.factory.run(run_forever=True)
    ##
    ## Called every second
    ##
    def tick(self):
        t=time.time()
        if time.time()-self.last_task_check>=10:
            with self.periodic_task_lock:
                tasks = TaskSchedule.get_pending_tasks(exclude=self.active_periodic_tasks.keys())
            self.last_task_check=t
            if tasks:
                for task in tasks:
                    self.run_periodic_task(task)
        if t-self.last_crashinfo_check>=60:
            self.collect_crashinfo()
            self.last_crashinfo_check=time.time()
        reset_queries() # Clear debug SQL log
        if t-self.last_mrtask_check>=1:
            # Check Map/Reduce task status
            self.process_mrtasks()
            self.last_mrtask_check=t
    
    ##
    ## Write event.
    ## data is a list of (left,right)
    ##
    def write_event(self,data,timestamp=None,managed_object=None):
        if managed_object is None:
            managed_object=ManagedObject.objects.get(name="SAE")
        if timestamp is None:
            timestamp=datetime.datetime.now()
        e=Event(
            timestamp=timestamp,
            event_priority=EventPriority.objects.get(name="DEFAULT"),
            event_class=EventClass.objects.get(name="DEFAULT"),
            event_category=EventCategory.objects.get(name="DEFAULT"),
            managed_object=managed_object
            )
        e.save()
        for l,r in data:
            d=EventData(event=e,key=l,value=r)
            d.save()
    ##
    ## Collect crashinfo and write as FM events
    ##
    def collect_crashinfo(self):
        if not self.config.get("main","logfile"):
            return
        c_d=os.path.dirname(self.config.get("main","logfile"))
        if not os.path.isdir(c_d):
            return
        for fn in [fn for fn in os.listdir(c_d) if fn.startswith(DEBUG_CTX_CRASH_PREFIX)]:
            path=os.path.join(c_d,fn)
            if not os.access(path,os.R_OK|os.W_OK): # Wait for noc-launcher to fix permissions
                continue
            try:
                with open(path,"r") as f:
                    data=cPickle.loads(f.read())
            except:
                logging.error("Cannot import crashinfo: %s"%path)
                continue
            ts=data["ts"]
            del data["ts"]
            self.write_event(data=data.items(),timestamp=datetime.datetime.fromtimestamp(ts))
            os.unlink(path)
    ##
    ## Periodic tasks
    ##
    def run_periodic_task(self,task):
        # Check no wait_for task running
        pc=task.periodic_class
        if pc.wait_for:
            with self.periodic_task_lock:
                for t in self.active_periodic_tasks.values():
                    if t.name in pc.wait_for:
                        logging.info("Periodic task '%s' cannot be launched when '%s' is active"%(task.periodic_name,t.name))
                        return
        # Run task
        logging.debug(u"New task running: %s"%unicode(task))
        t=threading.Thread(name=task.periodic_name,target=self.periodic_wrapper,kwargs={"task":task})
        with self.periodic_task_lock:
            self.active_periodic_tasks[task.id]=t
        t.start()
    ##
    ## Wrap periodic task handler and generate "periodic status"
    ## events with completion status
    ##
    def periodic_wrapper(self,task):
        logging.info(u"Periodic task=%s status=running"%unicode(task))
        cwd=os.getcwd()
        try:
            status=task.periodic_class(sae=self, timeout=task.timeout).execute()
        except:
            error_report()
            status=False
        logging.info(u"Periodic task=%s status=%s"%(unicode(task),"completed" if status else "failed"))
        if status:
            timeout=task.run_every
        else:
            timeout=max(60,task.run_every/4)
        task.next_run=datetime.datetime.now()+datetime.timedelta(seconds=timeout)
        task.save()
        with self.periodic_task_lock:
            try:
                del self.active_periodic_tasks[task.id]
            except:
                pass
        # Write task complete status event
        self.write_event([
            ("source","system"),
            ("type",  "periodic status"),
            ("task",  unicode(task)),
            ("status",{True:"success",False:"failure"}[status]),
        ])
        # Current path may be implicitly changed by periodic. Restore old value
        # to prevent further bugs
        new_cwd=os.getcwd()
        if cwd!=new_cwd:
            logging.error("CWD changed by periodic '%s' ('%s' -> '%s'). Restoring old cwd"%(unicode(task),cwd,new_cwd))
            os.chdir(cwd)

    def on_stream_close(self,stream):
        self.streams.unregister(stream)
        
    def register_activator(self,name,stream):
        self.streams.register(stream,name)
        
    def get_activator_stream(self,name):
        try:
            return self.factory.get_socket_by_name(name)
        except KeyError:
            raise Exception("Activator not available: %s"%name)
    
    def script(self,object,script_name,callback,**kwargs):
        def script_callback(transaction,response=None,error=None):
            if error:
                logging.error("script(%s,%s,**%s) failed: %s"%(script_name,object,kwargs,error.text))
                callback(error=error)
                return
            result=response.result
            result=cPickle.loads(str(result)) # De-serialize
            callback(result=result)
        logging.info("script %s(%s)"%(script_name,object))
        if object.profile_name!="NOC.SAE":
            # Validate activator is present
            try:
                stream=self.get_activator_stream(object.activator.name)
            except:
                e=Error()
                e.code=ERR_ACTIVATOR_NOT_AVAILABLE
                e.text="Activator '%s' not available"%object.activator.name
                logging.error(e.text)
                callback(error=e)
                return
        r=ScriptRequest()
        r.script=script_name
        r.access_profile.profile           = object.profile_name
        r.access_profile.scheme            = object.scheme
        r.access_profile.address           = object.address
        if object.port:
            r.access_profile.port          = object.port
        if object.user:
            r.access_profile.user          = object.user
        if object.password:
            r.access_profile.password      = object.password
        if object.super_password:
            r.access_profile.super_password= object.super_password
        if object.remote_path:
            r.access_profile.path          = object.remote_path
        if object.snmp_ro:
            r.access_profile.snmp_ro       = object.snmp_ro
        if object.snmp_rw:
            r.access_profile.snmp_rw       = object.snmp_rw
        attrs=[(a.key,a.value) for a in object.managedobjectattribute_set.all()]
        for k,v in attrs:
            a=r.access_profile.attrs.add()
            a.key=str(k)
            a.value=v
        for k,v in kwargs.items():
            a=r.kwargs.add()
            a.key=str(k)
            a.value=cPickle.dumps(v)
        if object.profile_name=="NOC.SAE":
            self.run_sae_script(r,script_callback)
        else:
            stream.proxy.script(r,script_callback)
    ##
    ## Send a list of addresses to activator
    ## and generate fault events for unreachable ones
    ##
    def ping_check(self,activator,addresses):
        def ping_check_callback(transaction,response=None,error=None):
            def save_probe_result(u,result):
                mo=ManagedObject.objects.filter(activator=activator,trap_source_ip=u).order_by("id")
                if len(mo)<1:
                    logging.error("Unknown object in ping_check: %s"%u)
                    return
                mo=mo[0] # Fetch first-created object in case of multiple objects with same trap_source_ip
                self.write_event(
                    data=[("source","system"),
                        ("activator",activator_name),
                        ("probe","ping"),
                        ("ip",u),
                        ("result",result)],
                    managed_object=mo,
                    timestamp=ts)
            if error:
                logging.error("ping_check failed: %s"%error.text)
                return
            ts=datetime.datetime.now()
            activator_name=activator.name
            for u in response.unreachable:
                save_probe_result(u,"failed")
            for u in response.reachable:
                save_probe_result(u,"success")
        logging.debug("ping_check(%s)"%activator.name)
        try:
            stream=self.get_activator_stream(activator.name)
        except:
            e=Error()
            e.code=ERR_ACTIVATOR_NOT_AVAILABLE
            e.text="Activator '%s' not available"%activator.name
            logging.error(e.text)
            return
        r=PingCheckRequest()
        for a in addresses:
            r.addresses.append(a)
        stream.proxy.ping_check(r,ping_check_callback)

    ##
    ## Map/Reduce task logging
    ##
    def log_mrt(self, level, task, status, args=None, **kwargs):
        r=[u"MRT task=%d/%d object=%s(%s) script=%s status=%s"%(task.task.id, task.id, task.managed_object.name,
            task.managed_object.address, task.map_script, status)]
        if args:
            a=repr(args)
            if level<=logging.INFO and len(a)>45:
                a=a[:20]+u" ... "+a[-20:]
            r+=[u"args=%s"%a]
        if kwargs:
            for k in kwargs:
                r+=[u"%s=%s"%(k, kwargs[k])]
        logging.log(level, u" ".join(r))
        
    ##
    ## Process Map/Reduce tasks
    ##
    def process_mrtasks(self):
        def map_callback(mt_id,result=None,error=None):
            try:
                mt=MapTask.objects.get(id=mt_id)
            except MapTask.DoesNotExist:
                logging.error("Map task %d suddently disappeared",mt_id)
                return
            if error:
                # Process non-fatal reasons
                TIMEOUTS={
                    ERR_ACTIVATOR_NOT_AVAILABLE: 10,
                    ERR_OVERLOAD:                10,
                    ERR_DOWN:                    30,
                }
                if error.code in TIMEOUTS: # Any of non-fatal reasons require retry
                    timeout=TIMEOUTS[error.code]
                    variation=10
                    timeout=random.randint(-timeout/variation,timeout/variation)
                    next_try=datetime.datetime.now()+datetime.timedelta(seconds=timeout)
                    if error.code==ERR_OVERLOAD:
                        next_retries=mt.retries_left
                    else:
                        next_retries=mt.retries_left-1
                    if mt.retries_left and next_try<mt.task.stop_time: # Check we're still in task time and have retries left
                        self.log_mrt(logging.INFO, task=mt, status="retry")
                        mt.next_try=next_try
                        mt.retries_left=next_retries
                        mt.status="W"
                        mt.save()
                        return
                mt.status="F"
                mt.script_result=dict(code=error.code,text=error.text)
                self.log_mrt(logging.INFO, task=mt, status="failed", code=error.code, error=error.text)
            else:
                mt.status="C"
                mt.script_result=result
                self.log_mrt(logging.INFO, task=mt, status="completed")
            mt.save()
        # Additional stack frame to store mt_id in a closure
        def exec_script(mt):
            kwargs={}
            if mt.script_params:
                kwargs=mt.script_params
            self.log_mrt(logging.INFO, task=mt, status="running", args=kwargs)
            self.script(mt.managed_object,mt.map_script,
                    lambda result=None,error=None: map_callback(mt.id,result,error),
                    **kwargs)
        t=datetime.datetime.now()
        for mt in MapTask.objects.filter(status="W",next_try__lte=t):
            if mt.task.stop_time<t: # Task timeout
                mt.status="F"
                mt.script_result=dict(code=ERR_TIMEOUT, text="Timed out")
                mt.save()
                self.log_mrt(logging.INFO, task=mt, status="failed", msg="timed out")
                continue
            mt.status="R"
            mt.save()
            exec_script(mt)
    ##
    ##
    ##
    def run_sae_script(self,request,callback):
        kwargs={}
        for a in request.kwargs:
            kwargs[str(a.key)]=cPickle.loads(str(a.value))
        script=script_registry[request.script](profile_registry[request.access_profile.profile],self,request.access_profile,**kwargs)
        script.sae=self
        with self.script_lock:
            self.script_threads[script]=callback
            logging.info("%d script threads"%(len(self.script_threads)))
        script.start()
    ##
    ##
    ##
    def on_script_exit(self,script):
        logging.info("Script %s(%s) completed"%(script.name,script.access_profile.address))
        with self.script_lock:
            cb=self.script_threads.pop(script)
            logging.info("%d script threads left"%(len(self.script_threads)))
        if script.result:
            r=ScriptResponse()
            r.result=script.result
            cb(None,response=r)
        else:
            e=Error()
            e.code=ERR_SCRIPT_EXCEPTION
            e.text=script.error_traceback
            cb(None,error=e)
    ##
    ## Called after config reloaded by SIGHUP.
    ##
    def on_load_config(self):
        self.start_listeners()
    # Signal handlers

    # SIGUSR1 returns process info
    def SIGUSR1(self,signo,frame):
        s=[
            ["factory.sockets",len(self.factory)],
        ]
        logging.info("STATS:")
        for n,v in s:
            logging.info("%s: %s"%(n,v))
        for sock in [s for s in self.factory.sockets.values() if issubclass(s.__class__,RPCSocket)]:
            try:
                logging.info("Activator: %s"%self.factory.get_name_by_socket(sock))
            except KeyError:
                logging.info("Unregistred activator")
            for n,v in sock.stats:
                logging.info("%s: %s"%(n,v))
