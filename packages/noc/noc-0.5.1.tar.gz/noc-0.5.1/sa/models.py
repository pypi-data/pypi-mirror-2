# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Copyright (C) 2007-2009 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
"""
"""
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User,Group
import datetime,random,cPickle,time,types
from noc.main.models import PyRule
from noc.sa.profiles import profile_registry
from noc.sa.periodic import periodic_registry
from noc.sa.script import script_registry
from noc.sa.protocols.sae_pb2 import TELNET,SSH,HTTP
from noc.lib.search import SearchResult
from noc.lib.fields import PickledField,INETField,AutoCompleteTagsField
from noc.lib.app.site import site
from tagging.models import TaggedItem
from django.utils.translation import ugettext_lazy as _
import marshal,base64,csv

profile_registry.register_all()
periodic_registry.register_all()
script_registry.register_all()
scheme_choices=[(TELNET,"telnet"),(SSH,"ssh"),(HTTP,"http")]
##
##
##
class AdministrativeDomain(models.Model):
    class Meta:
        verbose_name=_("Administrative Domain")
        verbose_name_plural=_("Administrative Domains")
    name=models.CharField(_("Name"),max_length=32,unique=True)
    description=models.TextField(_("Description"),null=True,blank=True)
    def __unicode__(self):
        return self.name
##
##
##
class Activator(models.Model):
    class Meta:
        verbose_name=_("Activator")
        verbose_name_plural=_("Activators")
    name=models.CharField(_("Name"),max_length=32,unique=True)
    ip=models.IPAddressField(_("From IP"))
    to_ip=models.IPAddressField(_("To IP"))
    auth=models.CharField(_("Auth String"),max_length=64)
    is_active=models.BooleanField(_("Is Active"),default=True)
    tags=AutoCompleteTagsField(_("Tags"),null=True,blank=True)
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return self.reverse("sa:activator:change",self.id)
    ##
    ## Returns true if IP can belong to any activator
    ##
    @classmethod
    def check_ip_access(self,ip):
        return Activator.objects.filter(ip__gte=ip,to_ip__lte=ip).count()>0
##
##
##
class ManagedObject(models.Model):
    class Meta:
        verbose_name=_("Managed Object")
        verbose_name_plural=_("Managed Objects")
    name=models.CharField(_("Name"),max_length=64,unique=True)
    is_managed=models.BooleanField(_("Is Managed?"),default=True)
    administrative_domain=models.ForeignKey(AdministrativeDomain,verbose_name=_("Administrative Domain"))
    activator=models.ForeignKey(Activator,verbose_name=_("Activator"))
    profile_name=models.CharField(_("Profile"),max_length=128,choices=profile_registry.choices)
    description=models.CharField(_("Description"),max_length=256,null=True,blank=True)
    # Access
    scheme=models.IntegerField(_("Scheme"),choices=scheme_choices)
    address=models.CharField(_("Address"),max_length=64)
    port=models.PositiveIntegerField(_("Port"),blank=True,null=True)
    user=models.CharField(_("User"),max_length=32,blank=True,null=True)
    password=models.CharField(_("Password"),max_length=32,blank=True,null=True)
    super_password=models.CharField(_("Super Password"),max_length=32,blank=True,null=True)
    remote_path=models.CharField(_("Path"),max_length=32,blank=True,null=True)
    trap_source_ip=INETField(_("Trap Source IP"),null=True,blank=True,default=None)
    trap_community=models.CharField(_("Trap Community"),blank=True,null=True,max_length=64)
    snmp_ro=models.CharField(_("RO Community"),blank=True,null=True,max_length=64)
    snmp_rw=models.CharField(_("RW Community"),blank=True,null=True,max_length=64)
    # CM
    is_configuration_managed=models.BooleanField(_("Is Configuration Managed?"),default=True)
    repo_path=models.CharField(_("Repo Path"),max_length=128,blank=True,null=True)
    #
    tags=AutoCompleteTagsField(_("Tags"),null=True,blank=True)
    
    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return self.reverse("sa:managedobject:change",self.id)
        
    # Returns object's profile
    def _profile(self):
        try:
            return self._cached_profile
        except AttributeError:
            self._cached_profile=profile_registry[self.profile_name]()
            return self._cached_profile
    profile=property(_profile)
    ##
    ## queryset returning objects for user
    ##
    @classmethod
    def user_objects(cls,user):
        return cls.objects.filter(UserAccess.Q(user))
    ##
    ##
    ##
    def has_access(self,user):
        return self.user_objects(user).filter(id=self.id).count()>0
    ##
    ## Returns a list of users granted access to object
    ##
    def _granted_users(self):
        return [u for u in User.objects.filter(is_active=True) if ManagedObject.objects.filter(UserAccess.Q(u)&Q(id=self.id)).count()>0]
    granted_users=property(_granted_users)
    ##
    ## Returns a list of groups granted access to object
    ##
    def _granted_groups(self):
        return [g for g in Group.objects.filter() if ManagedObject.objects.filter(GroupAccess.Q(g)&Q(id=self.id)).count()>0]
    granted_groups=property(_granted_groups)
    ##
    ## Override model's save()
    ## Change related Config object as well
    ##
    def save(self):
        super(ManagedObject,self).save()
        try:
            config=self.config # self.config is OneToOne field created by Config
        except:
            config=None
        if config is None: # No related Config object
            if self.is_configuration_managed: # Object is configuration managed, create related object
                from noc.cm.models import Config
                config=Config(managed_object=self,repo_path=self.repo_path,pull_every=86400)
                config.save()
        else: # Update existing config entry when necessary
            if self.repo_path!=self.config.repo_path: # Repo path changed
                config.repo_path=self.repo_path
            if self.is_configuration_managed and config.pull_every is None: # Device is configuration managed but not on periodic pull
                config.pull_every=86400
            elif not self.is_configuration_managed and config.pull_every: # Reset pull_every for unmanaged devices
                config.pull_every=None
            config.save()
    
    def delete(self):
        try:
            config=self.config
        except:
            config=None
        if config:
            config.delete()
        super(ManagedObject,self).delete()
    ##
    ## Search engine
    ##
    @classmethod
    def search(cls,user,query,limit):
        q=Q(repo_path__icontains=query)|Q(name__icontains=query)|Q(address__icontains=query)|Q(user__icontains=query)|Q(description__icontains=query)
        for o in [o for o in cls.objects.filter(q) if o.has_access(user)]:
            relevancy=1.0
            yield SearchResult(
                url=("sa:managedobject:change",o.id),
                title="SA: "+unicode(o),
                text=unicode(o),
                relevancy=relevancy
            )
    ##
    ## Returns True if Managed Object presents in more than one networks
    ##
    def is_router(self):
        return self.ipv4address_set.count()>1
    is_router=property(is_router)
##
##
##
class TaskSchedule(models.Model):
    periodic_name=models.CharField(_("Periodic Task"),max_length=64,choices=periodic_registry.choices)
    is_enabled=models.BooleanField(_("Enabled?"),default=False)
    run_every=models.PositiveIntegerField(_("Run Every (secs)"),default=86400)
    retries=models.PositiveIntegerField(_("Retries"),default=1)
    retry_delay=models.PositiveIntegerField(_("Retry Delay (secs)"),default=60)
    timeout=models.PositiveIntegerField(_("Timeout (secs)"),default=300)
    next_run=models.DateTimeField(_("Next Run"),auto_now_add=True)
    retries_left=models.PositiveIntegerField(_("Retries Left"),default=1)

    def __unicode__(self):
        return self.periodic_name

    def _periodic_class(self):
        return periodic_registry[self.periodic_name]
    periodic_class=property(_periodic_class)

    @classmethod
    def get_pending_tasks(cls,exclude=None):
        if exclude:
            TaskSchedule.objects.filter(next_run__lte=datetime.datetime.now(),is_enabled=True).exclude(id__in=exclude).order_by("-next_run")
        else:
            return TaskSchedule.objects.filter(next_run__lte=datetime.datetime.now(),is_enabled=True).order_by("-next_run")
    ##
    ## Reschedule an execution of task after specified time
    ##
    @classmethod
    def reschedule(cls,periodic_name,days=0,minutes=0,seconds=0):
        try:
            t=cls.objects.get(periodic_name=periodic_name)
            t.next_run=datetime.datetime.now()+datetime.timedelta(days=days,minutes=minutes,seconds=seconds)
            t.save()
        except TaskSchedule.DoesNotExist:
            pass
##
## Object Selector
##
class ManagedObjectSelector(models.Model):
    class Meta:
        verbose_name=_("Managed Object Selector")
        verbose_name_plural=_("Managed Object Selectors")
        ordering=["name"]
    name=models.CharField(_("Name"),max_length=64,unique=True)
    description=models.TextField(_("Description"),blank=True,null=True)
    is_enabled=models.BooleanField(_("Is Enabled"),default=True)
    filter_id=models.IntegerField(_("Filter by ID"),null=True,blank=True)
    filter_name=models.CharField(_("Filter by Name (REGEXP)"),max_length=256,null=True,blank=True)
    filter_profile=models.CharField(_("Filter by Profile"),max_length=64,null=True,blank=True,choices=profile_registry.choices)
    filter_address=models.CharField(_("Filter by Address (REGEXP)"),max_length=256,null=True,blank=True)
    filter_administrative_domain=models.ForeignKey(AdministrativeDomain,verbose_name=_("Filter by Administrative Domain"),null=True,blank=True)
    filter_activator=models.ForeignKey(Activator,verbose_name=_("Filter by Activator"),null=True,blank=True)
    filter_user=models.CharField(_("Filter by User (REGEXP)"),max_length=256,null=True,blank=True)
    filter_remote_path=models.CharField(_("Filter by Remote Path (REGEXP)"),max_length=256,null=True,blank=True)
    filter_description=models.CharField(_("Filter by Description (REGEXP)"),max_length=256,null=True,blank=True)
    filter_repo_path=models.CharField(_("Filter by Repo Path (REGEXP)"),max_length=256,null=True,blank=True)
    filter_tags=AutoCompleteTagsField(_("Filter By Tags"),null=True,blank=True)
    source_combine_method=models.CharField(_("Source Combine Method"),max_length=1,default="O",choices=[("A","AND"),("O","OR")])
    sources=models.ManyToManyField("ManagedObjectSelector",verbose_name=_("Sources"),symmetrical=False,null=True,blank=True)
    
    def __unicode__(self):
        return self.name
    ##
    ## Returns a Q object
    ##
    def _Q(self):
        # Apply restrictions
        q=Q(is_managed=True)&~Q(profile_name="NOC")
        if self.filter_id:
            q&=Q(id=self.filter_id)
        if self.filter_name:
            q&=Q(name__regex=self.filter_name)
        if self.filter_profile:
            q&=Q(profile_name=self.filter_profile)
        if self.filter_address:
            q&=Q(address__regex=self.filter_address)
        if self.filter_administrative_domain:
            q&=Q(administrative_domain=self.filter_administrative_domain)
        if self.filter_activator:
            q&=Q(activator=self.filter_activator)
        if self.filter_user:
            q&=Q(user__regex=self.filter_user)
        if self.filter_remote_path:
            q&=Q(remote_path__regex=self.filter_remote_path)
        if self.filter_description:
            q&=Q(description__regex=self.filter_description)
        if self.filter_repo_path:
            q&=Q(repo_path__regex=self.filter_repo_path)
        # Restrict to tags when necessary
        t_ids=TaggedItem.objects.get_intersection_by_model(ManagedObject,self.filter_tags).values_list("id",flat=True)
        if t_ids:
            q&=Q(id__in=t_ids)
        # Apply filters
        r=ManagedObject.objects.filter(q)
        # Restrict to sources
        if self.sources.count():
            if self.source_combine_method=="A":
                # AND
                for s in self.sources.all():
                    q&=s.Q
            else:
                # OR
                ql=list(self.sources.all())
                q=ql.pop(0).Q
                for qo in ql:
                    q|=qo.Q
        return q
    Q=property(_Q)
    ##
    ## Returns queryset containing managed objects
    ##
    def _managed_objects(self):
        return ManagedObject.objects.filter(self.Q)
    managed_objects=property(_managed_objects)
    ##
    ## Check Managed Object matches selector
    ##
    def match(self,managed_object):
        return self.managed_objects.filter(id=managed_object.id).count()>0
    ##
    ## Returns queryset containing managed objects supporting scripts
    ##
    def objects_with_scripts(self,scripts):
        sp=set()
        for p in profile_registry.classes:
            skip=False
            for s in scripts:
                if s not in profile_registry[p].scripts:
                    skip=True
                    continue
            if not skip:
                sp.add(p)
        return self.managed_objects.filter(profile_name__in=sp)
##
## Managed objects access for user
##
class UserAccess(models.Model):
    class Meta:
        verbose_name=_("User Access")
        verbose_name_plural=_("User Access")
    user=models.ForeignKey(User,verbose_name=_("User"))
    selector=models.ForeignKey(ManagedObjectSelector,verbose_name=_("Object Selector"))
    
    def __unicode__(self):
        return u"(%s,%s)"%(self.user.username,self.selector.name)
    ##
    ## Return Q object for user access
    ##
    @classmethod
    def Q(cls,user):
        if user.is_superuser:
            return Q() # All objects
        # Build Q for user access
        uq=[a.selector.Q for a in UserAccess.objects.filter(user=user)]
        if uq:
            q=uq.pop(0)
            while uq:
                q|=uq.pop(0)
        else:
            q=Q(id__in=[]) # False
        # Enlarge with group access
        for gq in [GroupAccess.Q(g) for g in user.groups.all()]:
            q|=gq
        return q
##
## Managed objects access for group
##
class GroupAccess(models.Model):
    class Meta:
        verbose_name=_("Group Access")
        verbose_name_plural=_("Group Access")
    group=models.ForeignKey(Group,verbose_name=_("Group"))
    selector=models.ForeignKey(ManagedObjectSelector,verbose_name=_("Object Selector"))
    
    def __unicode__(self):
        return u"(%s,%s)"%(self.group.name,self.selector.name)
    ##
    ## Return Q object
    ##
    @classmethod
    def Q(cls,group):
        gq=[a.selector.Q for a in GroupAccess.objects.filter(group=group)]
        if gq:
            # Combine selectors
            q=gq.pop(0)
            while gq:
                q|=gp.pop(0)
            return q
        else:
            return Q(id__in=[]) # False
##
## Reduce Tasks
##
class ReduceTask(models.Model):
    class Meta:
        verbose_name=_("Map/Reduce Task")
        verbose_name_plural=_("Map/Reduce Tasks")
    start_time=models.DateTimeField(_("Start Time"))
    stop_time=models.DateTimeField(_("Stop Time"))
    script=models.TextField(_("Script"))
    script_params=PickledField(_("Params"),null=True,blank=True)
    
    class NotReady(Exception): pass
    
    def __unicode__(self):
        if self.id:
            return u"%d"%(self.id)
        else:
            return u"New: %s"%id(self)
    ##
    ##
    ##
    def save(self,**kwargs):
        if callable(self.script):
            # Make bootstrap from callable
            self.script="import marshal,base64\n"\
            "@pyrule\n"\
            "def rule(*args,**kwargs): pass\n"\
            "rule.func_code=marshal.loads(base64.decodestring('%s'))\n"%(base64.encodestring(marshal.dumps(self.script.func_code)).replace("\n","\\n"))
        elif self.script.startswith("pyrule:"):
            # Reference to existing pyrule
            r=PyRule.objects.get(name=self.script[7:],interface="IReduceTask")
            self.script=r.text
        # Check syntax
        PyRule.compile_text(self.script)
        # Save
        super(ReduceTask,self).save(**kwargs)
    ##
    ## Check all map tasks are completed
    ##
    def _complete(self):
        return self.stop_time<=datetime.datetime.now()\
            or (self.maptask_set.all().count()==self.maptask_set.filter(status__in=["C","F"]).count())
    complete=property(_complete)
    ##
    ## Create map/reduce tasks
    ##
    ## object_selector must be either of ManagedObjectSelector instance or of list type
    ## map_script can be string or list.
    ## If map string is a list, map_string_params may be a list too, or it will be replicated for
    ## each kind of map task
    ##
    @classmethod
    def create_task(self,object_selector,reduce_script,reduce_script_params,map_script,map_script_params,timeout):
        # Create reduce task
        start_time=datetime.datetime.now()
        r_task=ReduceTask(
            start_time=start_time,
            stop_time=start_time+datetime.timedelta(seconds=timeout),
            script=reduce_script,
            script_params=reduce_script_params if reduce_script_params else {},
        )
        r_task.save()
        # Normalize map scripts to a list
        if type(map_script) in [types.ListType,types.TupleType]:
            # list of map scripts
            map_script_list=map_script
            if type(map_script_params) in [types.ListType,types.TupleType]:
                if len(map_script_params)!=len(map_script):
                    raise Exception("Mismatched parameter list size")
                map_script_params_list=map_script_params
            else:
                # Expand to list
                map_script_params_list=[map_script_params]*len(map_script_list)
        else:
            # Single map script
            map_script_list=[map_script]
            map_script_params_list=[map_script_params]
        # Normalize a name of map scripts and join with parameters
        msp=[]
        for ms,p in zip(map_script_list,map_script_params_list):
            s=ms.split(".")
            if len(s)==3:
                ms=s[-1]
            elif len(s)!=1:
                raise Exception("Invalid map script: '%s'"%ms)
            msp+=[(ms,p)]
        # Convert object_selector to a list of objects
        if type(object_selector) in (types.ListType,types.TupleType):
            objects=object_selector
        elif isinstance(object_selector,ManagedObjectSelector):
            objects=object_selector.managed_objects
        else:
            objects=list(object_selector)
        # Resolve strings to managed objects, if returned by selector
        objects=[ManagedObject.objects.get(name=x) if isinstance(x,basestring) else x for x in objects]
        # Run map task for each object
        for o in objects:
            for ms,p in msp:
                # Set status to "F" if script not found
                status="W" if ms in o.profile.scripts else "F"
                # Build full map script name
                msn="%s.%s"%(o.profile_name,ms)
                #
                MapTask(
                    task=r_task,
                    managed_object=o,
                    map_script=msn,
                    script_params=p,
                    next_try=start_time,
                    status=status
                ).save()
        return r_task
    ##
    ## Perform reduce script and execute result
    ##
    def reduce(self):
        return PyRule.compile_text(self.script)(self,**self.script_params)
    ##
    ## Get task result
    ##
    def get_result(self,block=True):
        while True:
            if self.complete:
                result=self.reduce()
                self.delete()
                return result
            else:
                if block:
                    time.sleep(3)
                else:
                    raise ReduceTask.NotReady
    ##
    ## Wait untill all task complete
    ##
    @classmethod
    def wait_for_tasks(cls,tasks):
        while tasks:
            time.sleep(3)
            rest=[]
            for t in tasks:
                if t.complete:
                    t.reduce() # delete task and trigger reduce task
                    t.delete()
                else:
                    rest+=[t]
                tasks=rest
##
## Map Tasks
##
class MapTask(models.Model):
    class Meta:
        verbose_name=_("Map/Reduce Task Data")
        verbose_name=_("Map/Reduce Task Data")
    task=models.ForeignKey(ReduceTask,verbose_name=_("Task"))
    managed_object=models.ForeignKey(ManagedObject,verbose_name=_("Managed Object"))
    map_script=models.CharField(_("Script"),max_length=256)
    script_params=PickledField(_("Params"),null=True,blank=True)
    next_try=models.DateTimeField(_("Next Try"))
    retries_left=models.IntegerField(_("Retries Left"),default=1)
    status=models.CharField(_("Status"),max_length=1,choices=[("W",_("Wait")),("R",_("Running")),("C",_("Complete")),("F",_("Failed"))],default="W")
    script_result=PickledField(_("Result"),null=True,blank=True)
    def __unicode__(self):
        if self.id:
            return u"%d: %s %s"%(self.id,self.managed_object,self.map_script)
        else:
            return u"New: %s %s"%(self.managed_object,self.map_script)
