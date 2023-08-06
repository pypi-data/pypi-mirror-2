# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## IP Address space management application
##----------------------------------------------------------------------
## Copyright (C) 2007-2010 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
from django.shortcuts import get_object_or_404
from django import forms
from noc.lib.app import Application,URL,HasPerm
from noc.ip.models import *
from noc.vc.models import VC,VCBindFilter
from noc.lib.colors import get_colors
from noc.lib.validators import is_cidr,is_ipv4,is_fqdn
from noc.lib.ip import normalize_prefix,contains,in_range,free_blocks,prefix_to_size
from noc.lib.widgets import AutoCompleteTags,AutoCompleteTextInput
from noc.lib.forms import NOCForm
from noc.sa.interfaces.base import MACAddressParameter,InterfaceTypeError
from noc.sa.models import ManagedObject,ReduceTask
##
## IP Address Space Management
##
class IPManageAppplication(Application):
    title="Assigned Addresses"
    ##
    ## Display VRF list
    ##
    def view_index(self,request):
        # Check only one active VRF exists
        if VRF.objects.count()==1:
            vrf=VRF.objects.all()[0]
            return self.response_redirect("ip:ipmanage:vrf_index",vrf.id,"0.0.0.0/0")
        #
        groups=[]
        for vg in VRFGroup.objects.all():
            vrfs=vg.vrf_set.all()
            if len(vrfs)>0:
                groups+=[(vg,vrfs.order_by("name"))]
        return self.render(request,"index.html",{"groups":groups})
    view_index.url=r"^$"
    view_index.menu="Assigned Addresses"
    view_index.access=HasPerm("view")
    ##
    ## Display assigned addresses and blocks
    ##
    def view_vrf_index(self,request,vrf_id,prefix="0.0.0.0/0"):
        if not is_cidr(prefix):
            return self.response_not_found("Prefix '%s' is not found"%prefix)
        vrf_id=int(vrf_id)
        vrf=get_object_or_404(VRF,id=vrf_id)
        parents=vrf.prefix(prefix).parents
        prefixes=vrf.prefixes(prefix)
        can_allocate=IPv4BlockAccess.check_write_access(request.user,vrf,prefix)
        prefix=vrf.prefix(prefix)
        has_children=prefix.has_children
        total=prefix.size
        block_info=[
            ("Net",         prefix.prefix),
            ("Netmask",     prefix.netmask),
            ("Broadcast",   prefix.broadcast),
            ("Wildcard",    prefix.wildcard),
            ("Size",        total),
        ]
        ranges=None
        range_colors=None
        all_addresses=None
        can_ping=False
        if has_children:
            orphaned_addresses=prefix.orphaned_addresses
        else:
            orphaned_addresses=None
            used=prefix.address_count
            free=total-used
            block_info+=[
                ("Addresses Used",used),
                ("Addresses Free",free),
            ]
            # Prepare range colors
            ranges=list(prefix.ranges)
            range_colors=zip(ranges,get_colors(len(ranges)))
            # Bind addresses to ranges
            all_addresses=[]
            for a in prefix.all_addresses:
                try:
                    ip=a.ip
                    if a.managed_object:
                        can_ping=True
                except:
                    ip=a
                ar=None
                for r in ranges:
                    if in_range(ip,r.from_ip,r.to_ip):
                        ar=r
                        break
                all_addresses+=[(ar,a)]
        return self.render(request,"vrf_index.html",{"vrf":vrf,"parents":parents,"prefixes":prefixes,"prefix":prefix,
                            "can_allocate":can_allocate,"block_info":block_info,"has_children":has_children,
                            "ranges":ranges,"range_colors":range_colors,"all_addresses":all_addresses,
                            "orphaned_addresses":orphaned_addresses,
                            "has_bookmark":prefix.has_bookmark(request.user),"can_ping":can_ping,
                            "my_networks":IPv4BlockBookmark.user_bookmarks(request.user,vrf)})
    view_vrf_index.url=r"(?P<vrf_id>\d+)/(?P<prefix>\S+)/$"
    view_vrf_index.url_name="vrf_index"
    view_vrf_index.access=HasPerm("view")
    ##
    ## Quick jump to most suitable block
    ##
    class QuickJumpForm(forms.Form):
        jump=forms.RegexField(regex=r"^\d+(\.\d+){0,3}$")
    def view_quickjump(self,request,vrf_id):
        vrf=get_object_or_404(VRF,id=vrf_id)
        if request.POST:
            form=self.QuickJumpForm(request.POST)
            if form.is_valid():
                parts=form.cleaned_data["jump"].split(".")
                # Fill missed octets with '0'
                if len(parts)<4:
                    parts+=["0"]*(4-len(parts))
                ip=".".join(parts)
                # Check address
                if not is_ipv4(ip):
                    self.message_user(request,"Invalid address %s"%ip)
                    return self.response_redirect_to_referrer(request)
                # Find covering block
                b=vrf.find_ipv4block(ip)
                self.message_user(request,"Redirected to %s"%b.prefix)
                return self.response_redirect("ip:ipmanage:vrf_index",vrf.id,b.prefix)
        return self.response_redirect_to_referrer(request)
    view_quickjump.url=r"(?P<vrf_id>\d+)/quickqump/"
    view_quickjump.url_name="quickjump"
    view_quickjump.access=HasPerm("view")
    ##
    ## Allocate new block form
    ##
    class AllocateBlockForm(NOCForm):
        prefix=forms.CharField(label="Prefix",required=True)
        description=forms.CharField(label="Description",required=True)
        asn=forms.ModelChoiceField(label="ASN",queryset=AS.objects.all(),required=True)
        tags=forms.CharField(widget=AutoCompleteTags,required=False)
        tt=forms.IntegerField(label="TT #",required=False)
        def __init__(self,data=None,initial=None,vrf=None,block_id=None):
            NOCForm.__init__(self,data=data,initial=initial)
            self.vrf=vrf
            self.block_id=block_id
        def clean_prefix(self):
            if not is_cidr(self.cleaned_data["prefix"]):
                raise forms.ValidationError("Invalid prefix")
            prefix=normalize_prefix(self.cleaned_data["prefix"])
            # Check for duplication
            q=IPv4Block.objects.filter(prefix=prefix)
            if self.vrf.vrf_group.unique_addresses:
                q=q.filter(vrf__in=self.vrf.vrf_group.vrf_set.all())
            else:
                q=q.filter(vrf=self.vrf)
            if self.block_id:
                q=q.exclude(id=self.block_id)
            if q.count()>0:
                raise forms.ValidationError("Block is already present")
            return prefix
    ##
    ## Allocate Block
    ##
    def view_allocate_block(self,request,vrf_id,prefix=None):
        rx_referer_prefix=re.compile(r"^.+/(?P<prefix>\d+\.\d+\.\d+\.\d+/\d+)/$")
        vrf=get_object_or_404(VRF,id=int(vrf_id))
        suggestions=[]
        parent=prefix
        block_id=None
        initial={}
        if prefix:
            assert is_cidr(prefix)
            block=get_object_or_404(IPv4Block,vrf=vrf,prefix=prefix)
            initial={
                "prefix"      : block.prefix,
                "description" : block.description,
                "asn"         : block.asn.id,
                "tags"        : block.tags,
                "tt"          : block.tt
            }
            p="/"+prefix
            block_id=block.id
        else:
            # Fetch prefix from referrer
            match=rx_referer_prefix.match(request.META.get("HTTP_REFERER",""))
            if match and is_cidr(match.group(1)):
                # Suggest blocks of different sizes
                parent=match.group(1)
                free=[(x.split("/")[0],int(x.split("/")[1])) for x in free_blocks(parent,[p.prefix for p in vrf.prefixes(top=parent)])]
                free=sorted(free,lambda x,y: -cmp(x[1],y[1]))
                for m in range(int(parent.split("/")[1])+1,31):
                    for fp,fm in free:
                        if fm<=m:
                            p="%s/%d"%(fp,m)
                            suggestions+=[(p,prefix_to_size(p))]
                            break
                # Fill initial prefix
                prefix=parent.split("/")[0]
                while prefix.endswith(".0"):
                    prefix=prefix[:-2]
                initial["prefix"]=prefix
            p=""
        if request.POST:
            # Process post request
            form=self.AllocateBlockForm(request.POST,vrf=vrf,block_id=block_id)
            if form.is_valid():
                if not IPv4BlockAccess.check_write_access(request.user,vrf,form.cleaned_data["prefix"]):
                    return self.respone_forbidden("Permission denied")
                if prefix:
                    block.prefix=form.cleaned_data["prefix"]
                    block.description=form.cleaned_data["description"]
                    block.asn=form.cleaned_data["asn"]
                    block.tags=form.cleaned_data["tags"]
                    block.tt=form.cleaned_data["tt"]
                    status="changed"
                else:
                    block=IPv4Block(vrf=vrf,prefix=form.cleaned_data["prefix"],
                        description=form.cleaned_data["description"],
                        asn=form.cleaned_data["asn"],
                        tags=form.cleaned_data["tags"],
                        tt=form.cleaned_data["tt"])
                    status="created"
                block.save()
                self.message_user(request,"Block '%s' in VRF '%s' %s successfully"%(block.prefix,str(vrf),status))
                # Redirect depenging on submit button pressed
                if "_continue" in request.POST:
                    return self.response_redirect("ip:ipmanage:change_block",vrf.id,block.prefix)
                if "_addanother" in request.POST:
                    return self.response_redirect("ip:ipmanage:allocate_block",vrf.id)
                
                return self.response_redirect("%s%d/%s/"%(self.base_url,vrf.id,block.prefix))
        else:
            # Display form
            form=self.AllocateBlockForm(initial=initial)
        return self.render(request,"allocate_block.html",{"vrf":vrf,"form":form,"p":p,"suggestions":suggestions,"parent":parent})
    view_allocate_block.url=[
        URL(r"^(?P<vrf_id>\d+)/allocate_block/",name="allocate_block"),
        URL(r"^(?P<vrf_id>\d+)/(?P<prefix>\S+)/allocate_block/$",name="change_block")
        ]
    view_allocate_block.access=HasPerm("allocate")
    ##
    ## Deallocate block handler
    ##
    def view_deallocate_block(self,request,vrf_id,prefix):
        assert is_cidr(prefix)
        vrf_id=int(vrf_id)
        vrf=get_object_or_404(VRF,id=vrf_id)
        block=get_object_or_404(IPv4Block,vrf=vrf,prefix=prefix)
        if not IPv4BlockAccess.check_write_access(request.user,vrf,prefix):
            return self.response_forbidden("Permission denied")
        parents=vrf.prefix(prefix).parents
        parent=parents[-1].prefix
        block.delete()
        self.message_user(request,"Block %s in VRF %s deallocated successfully"%(prefix,str(vrf)))
        return self.response_redirect("%s%d/%s/"%(self.base_url,vrf_id,parent))
    view_deallocate_block.url=r"^(?P<vrf_id>\d+)/(?P<prefix>\S+)/deallocate_block/$"
    view_deallocate_block.url_name="deallocate_block"
    view_deallocate_block.access=HasPerm("deallocate")
    ##
    ##
    ## Assign new IP address form
    ##
    class AssignAddressForm(NOCForm):
        fqdn=forms.CharField(label="FQDN",required=True)
        ip=forms.CharField(label="IP",required=True)
        mac=forms.CharField(label="MAC",required=False)
        auto_update_mac=forms.BooleanField(label="Auto Update MAC",required=False)
        managed_object=forms.CharField(label="Managed Object",required=False,widget=AutoCompleteTextInput("sa:managedobject:lookup"))
        description=forms.CharField(label="Description",required=False)
        tags=forms.CharField(label="Tags",widget=AutoCompleteTags,required=False)
        tt=forms.IntegerField(label="TT #",required=False)
        def __init__(self,data=None,initial=None,vrf=None,address_id=None):
            NOCForm.__init__(self,data=data,initial=initial)
            #forms.Form.__init__(self,data=data,initial=initial)
            self.vrf=vrf
            self.address_id=address_id
        def clean_fqdn(self):
            if not is_fqdn(self.cleaned_data["fqdn"]):
                raise forms.ValidationError("Invalid FQDN")
            return self.cleaned_data["fqdn"].strip()
        def clean_ip(self):
            if not is_ipv4(self.cleaned_data["ip"]):
                raise forms.ValidationError("Invalid IP Address")
            if IPv4AddressRange.is_range_locked(self.vrf,self.cleaned_data["ip"]):
                raise forms.ValidationError("IP Address Range is locked")
            # Check for duplications
            ip=self.cleaned_data["ip"]
            q=IPv4Address.objects.filter(ip=ip)
            if self.vrf.vrf_group.unique_addresses:
                q=q.filter(vrf__in=self.vrf.vrf_group.vrf_set.all())
            else:
                q=q.filter(vrf=self.vrf)
            if self.address_id:
                q=q.exclude(id=self.address_id)
            if q.count()>0:
                raise forms.ValidationError("IPv4 Address is already present")
            return ip
        def clean_mac(self):
            if not self.cleaned_data["mac"]:
                return ""
            try:
                return MACAddressParameter().clean(self.cleaned_data["mac"])
            except InterfaceTypeError:
                raise forms.ValidationError("Invalid MAC address")
    ##
    ## Assign IP address
    ##
    def view_assign_address(self,request,vrf_id,ip=None,new_ip=None):
        rx_url_cidr=re.compile(r"^.*/(\d+\.\d+\.\d+\.\d+/\d+)/$")
        vrf=get_object_or_404(VRF,id=int(vrf_id))
        parents=[]
        address_id=None
        can_delete=False
        if ip:
            assert is_ipv4(ip)
            address=get_object_or_404(IPv4Address,vrf=vrf,ip=ip)
            address_id=address.id
            initial={
                "fqdn"            : address.fqdn,
                "ip"              : address.ip,
                "mac"             : address.mac,
                "auto_update_mac" : address.auto_update_mac,
                "description"     : address.description,
                "tags"            : address.tags,
                "tt"              : address.tt,
            }
            if address.managed_object:
                initial["managed_object"]=address.managed_object.name
            p="/"+ip
            parents=list(address.parent.parents)+[address.parent]
            can_delete=True
        elif new_ip:
            assert is_ipv4(new_ip)
            initial={"ip":new_ip}
            p=""
        else:
            initial={}
            p=""
        if request.POST:
            form=self.AssignAddressForm(request.POST,vrf=vrf,address_id=address_id)
            if form.is_valid():
                if not IPv4BlockAccess.check_write_access(request.user,vrf,form.cleaned_data["ip"]+"/32"):
                    return self.response_forbidden("Permission denied")
                managed_object=None
                if "managed_object" in form.cleaned_data and form.cleaned_data["managed_object"]:
                    managed_object=get_object_or_404(ManagedObject,name=form.cleaned_data["managed_object"])
                if ip:
                    address.fqdn=form.cleaned_data["fqdn"]
                    address.ip=form.cleaned_data["ip"]
                    address.mac=form.cleaned_data["mac"]
                    address.auto_update_mac="auto_update_mac" in form.cleaned_data and form.cleaned_data["auto_update_mac"]
                    address.managed_object=managed_object
                    address.description=form.cleaned_data["description"]
                    address.tags=form.cleaned_data["tags"]
                    address.tt=form.cleaned_data["tt"]
                    status="changed"
                else:
                    # Check no duplicated IPs
                    if IPv4Address.objects.filter(vrf=vrf,ip=form.cleaned_data["ip"]).count()>0:
                        return render_failure(request,"Duplicated IP address","Address %s is already present in VRF %s"%(form.cleaned_data["ip"],vrf.name))
                    address=IPv4Address(vrf=vrf,fqdn=form.cleaned_data["fqdn"],
                        ip=form.cleaned_data["ip"],mac=form.cleaned_data["mac"],
                        auto_update_mac="auto_update_mac" in form.cleaned_data and form.cleaned_data["auto_update_mac"],
                        managed_object=managed_object,description=form.cleaned_data["description"],
                        tags=form.cleaned_data["tags"],tt=form.cleaned_data["tt"])
                    status="created"
                address.save()
                self.message_user(request,"IP Address %s in VRF %s %s successfully"%(form.cleaned_data["ip"],str(vrf),status))
                # Redirect depenging on submit button pressed
                if "_continue" in request.POST:
                    return self.response_redirect("ip:ipmanage:change_address",vrf.id,address.ip)
                if "_addanother" in request.POST:
                    return self.response_redirect("ip:ipmanage:assign_address",vrf.id)
                return self.response_redirect("ip:ipmanage:vrf_index",vrf.id,address.parent.prefix)
        else:
            if "ip" not in initial:
                # Try to calculate ip address from referer
                referer=request.META.get("HTTP_REFERER",None)
                if referer:
                    match=rx_url_cidr.match(referer)
                    if match and is_cidr(match.group(1)):
                        block=match.group(1)
                        # Find first free IP address
                        c=self.cursor()
                        c.execute("SELECT free_ip(%s,%s)",[vrf.id,block])
                        ip=c.fetchall()[0][0]
                        if ip:
                            initial["ip"]=ip
                        else:
                            initial["ip"]="NO FREE IP"
            form=self.AssignAddressForm(initial=initial)
        return self.render(request,"assign_address.html",{
            "vrf":vrf,"form":form,"p":p,"parents":parents,"can_delete":can_delete,"ip":initial.get("ip",None)})
    view_assign_address.url=[
        URL(r"^(?P<vrf_id>\d+)/assign_address/$",name="assign_address"),
        URL(r"^(?P<vrf_id>\d+)/(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3})/assign_address/$",name="change_address"),
        URL(r"^(?P<vrf_id>\d+)/(?P<new_ip>\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3})/assign_address/new/$",name="assign_new_address")
    ]
    view_assign_address.access=HasPerm("allocate")
    ##
    ## Deallocate ip address handler
    ##
    def view_revoke_address(self,request,vrf_id,ip):
        assert is_ipv4(ip)
        vrf_id=int(vrf_id)
        vrf=get_object_or_404(VRF,id=vrf_id)
        address=get_object_or_404(IPv4Address,vrf=vrf,ip=ip)
        if not IPv4BlockAccess.check_write_access(request.user,vrf,ip+"/32"):
            return self.response_forbidden("Permission denied")
        address.delete()
        self.message_user(request,"IP address %s in VRF %s successfully deleted"%(ip,str(vrf)))
        return self.response_redirect("%s%d/%s/"%(self.base_url,vrf.id,address.parent.prefix))
    view_revoke_address.url=r"^(?P<vrf_id>\d+)/(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/revoke_address/$"
    view_revoke_address.url_name="revoke_address"
    view_revoke_address.access=HasPerm("deallocate")
    ##
    ## Bind VC to Prefix
    ##
    def view_bind_vc(self,request,vrf_id,prefix):
        def get_bind_vc_form(prefix):
            class BindVCForm(forms.Form):
                vc=forms.ChoiceField(label="VC",choices=VCBindFilter.get_choices(prefix),required=True)
            return BindVCForm
        vrf=get_object_or_404(VRF,id=int(vrf_id))
        p=get_object_or_404(IPv4Block,vrf=vrf,prefix=prefix)
        if not IPv4BlockAccess.check_write_access(request.user,vrf,prefix):
            return self.response_forbidden("Permission denied")
        initial={"vc":p.vc}
        if request.POST:
            form=get_bind_vc_form(p)(request.POST,initial=initial)
            if form.is_valid():
                # Bind to vc
                p.vc=get_object_or_404(VC,id=form.cleaned_data["vc"])
                p.save()
                self.message_user(request,"Prefix %s is succesfully bind to VC %s"%(prefix,str(p.vc)))
                return self.response_redirect("%s%d/%s/"%(self.base_url,vrf.id,prefix))
        else:
            form=get_bind_vc_form(p)(initial=initial)
        return self.render(request,"bind_vc.html",{"form":form,"prefix":p})
    view_bind_vc.url=r"(?P<vrf_id>\d+)/(?P<prefix>\S+)/bind_vc/$"
    view_bind_vc.url_name="bind_vc"
    view_bind_vc.access=HasPerm("bind_vc")
    ##
    ## Toggle bookmark
    ##
    def view_toogle_bookmark(self,request,vrf_id,prefix):
        vrf=get_object_or_404(VRF,id=int(vrf_id))
        p=get_object_or_404(IPv4Block,vrf=vrf,prefix=prefix)
        p.toggle_bookmark(request.user)
        self.message_user(request,"Bookmark %s on %s"%({True:"set",False:"removed"}[p.has_bookmark(request.user)],prefix))
        return self.response_redirect("ip:ipmanage:vrf_index",vrf_id,prefix)
    view_toogle_bookmark.url=r"(?P<vrf_id>\d+)/(?P<prefix>\S+)/toggle_bookmark/$"
    view_toogle_bookmark.url_name="toggle_bookmark"
    view_toogle_bookmark.access=HasPerm("view")
    ##
    ## AJAX handler to run ping_task
    ##
    def view_ping_check(self,request,vrf_id,prefix):
        vrf=get_object_or_404(VRF,id=int(vrf_id))
        p=get_object_or_404(IPv4Block,vrf=vrf,prefix=prefix)
        # Detect managed objects in block
        addresses=p.addresses
        r=[a for a in addresses if a.managed_object]
        if not r:
            return self.render_json(None)
        activator_name=r[0].managed_object.activator.name
        addresses=list(generate_ips(p.network,p.broadcast))
        if len(addresses)>2:
            addresses=addresses[1:-1]
        t=ReduceTask.create_task(["SAE"],"pyrule:get_single_result",{},
            "ping_check",{"activator_name":activator_name,"addresses":addresses},60)
        return self.render_json(t.id)
    view_ping_check.url=r"^(?P<vrf_id>\d+)/(?P<prefix>\S+)/ping_check/$"
    view_ping_check.url_name="ping_check"
    view_ping_check.access=HasPerm("view")
    ##
    ## Ping check task result
    ##
    def view_ping_check_task(self,request,vrf_id,prefix,task_id):
        vrf=get_object_or_404(VRF,id=int(vrf_id))
        p=get_object_or_404(IPv4Block,vrf=vrf,prefix=prefix)
        task=get_object_or_404(ReduceTask,id=int(task_id))
        try:
            result=task.get_result(block=False)
        except ReduceTask.NotReady:
            return self.render_json(None) # Waiting
        r={}
        for s in result:
            r[s["ip"]]=s["status"]
        return self.render_json(r)
    view_ping_check_task.url=r"^(?P<vrf_id>\d+)/(?P<prefix>\S+)/ping_check/(?P<task_id>\d+)/$"
    view_ping_check_task.url_name="ping_check_task"
    view_ping_check_task.access=HasPerm("view")
    ##
    ## Return a list of user access
    ##
    def user_access_list(self,user):
        return ["%s: %s"%(a.vrf.name,a.prefix) for a in IPv4BlockAccess.objects.filter(user=user)]
    ##
    def user_access_change_url(self,user):
        return self.site.reverse("ip:ipv4blockaccess:changelist",QUERY={"user__id__exact":user.id})
