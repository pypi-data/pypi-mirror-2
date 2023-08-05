"""
A second, custom AdminSite -- see tests.CustomAdminSiteTests.
"""
from django.conf.urls.defaults import patterns
from django.contrib import admin
from django.http import HttpResponse

import models

class Admin2(admin.AdminSite):
    login_template = 'custom_admin/login.html'
    index_template = 'custom_admin/index.html'

    # A custom index view.
    def index(self, request, extra_context=None):
        return super(Admin2, self).index(request, {'foo': '*bar*'})

    def get_urls(self):
        return patterns('',
            (r'^my_view/$', self.admin_view(self.my_view)),
        ) + super(Admin2, self).get_urls()

    def my_view(self, request):
        return HttpResponse("Django is a magical pony!")

site = Admin2(name="admin2")

site.register(models.Article, models.ArticleAdmin)
site.register(models.Section, inlines=[models.ArticleInline])
site.register(models.Thing, models.ThingAdmin)
site.register(models.Fabric, models.FabricAdmin)
