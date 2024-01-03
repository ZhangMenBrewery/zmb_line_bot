from django.contrib import admin
from django.db.models import Case, When, Value, IntegerField
from callback.models import beer, can

class beerAdmin(admin.ModelAdmin):
    list_display = ('id', 'tapNum', 'time', 'Validity_period', 'Style', 'eName', 'cName', 'ABV', 'IBU', 'SRM', 'Keyword', 'Description')
    
    # 使用Case和When來定義排序條件，將time為'停產'的放在最後面
    ordering = (
        Case(
            When(time='停產', then=Value(1)),
            default=Value(0),
            output_field=IntegerField()
        ),
        'tapNum',
    )

class canAdmin(admin.ModelAdmin):
    list_display = ('cName', 'eName', 'ABV', 'NT_330ml', 'Description')
    ordering = ('id',)

admin.site.register(beer, beerAdmin)
admin.site.register(can, canAdmin)
