from django.contrib import admin

from unesco.models import Site, Category, Region, States, ISO

admin.site.register(Site)
admin.site.register(Category)
admin.site.register(Region)
admin.site.register(States)
admin.site.register(ISO)
