from django.contrib import admin
from callback.models import beer, can
# Register your models here.

class beerAdmin(admin.ModelAdmin):
    list_display=('id','Style','eName','cName','ABV','IBU','SRM','Keyword','Description'
    )
    ordering=('id',)

class canAdmin(admin.ModelAdmin):
    list_display=('cName','eName','ABV','NT_330ml','Description'
    )
    ordering=('id',)

admin.site.register(beer,beerAdmin)
admin.site.register(can,canAdmin)