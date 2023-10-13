from django.contrib import admin
from callback.models import beer, can
# Register your models here.

class beerAdmin(admin.ModelAdmin):
    list_display=('id','tapNum',
    'Style','eName','cName','ABV','IBU','SRM','Keyword'
    )
    ordering=('id',)

class beerAdmin(admin.ModelAdmin):
    list_display=('cName','eName','ABV','NT_330ml','Description'
    )
    ordering=('id',)

admin.site.register(beer,beerAdmin)
admin.site.register(can,beerAdmin)