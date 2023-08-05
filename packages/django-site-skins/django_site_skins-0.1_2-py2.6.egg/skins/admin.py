from django.contrib import admin
from django.contrib.sites.models import Site
from django.contrib.sites.admin import SiteAdmin
from skins.models import Skin

class skin_inline(admin.TabularInline):
    model = Skin
    extra = 1

admin.site.unregister(Site)
SiteAdmin.inlines = [skin_inline,]
admin.site.register(Site, SiteAdmin)
