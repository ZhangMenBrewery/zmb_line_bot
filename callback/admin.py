from django.contrib import admin
from django.db.models import Case, When, Value, IntegerField
from django.utils.html import escape, format_html
from callback.models import beer, can, usage_log, line_user

class beerAdmin(admin.ModelAdmin):
    list_display = ('id', 'position', 'time', 'Validity_period', 'Style', 'eName', 'cName', 'ABV', 'IBU', 'SRM', 'Keyword', 'Description')
    
    # 使用Case和When來定義排序條件，將time為'停產'的放在最後面
    ordering = (
        Case(
            When(time='停產', then=Value(1)),
            default=Value(0),
            output_field=IntegerField()
        ),
        'position',
    )

class canAdmin(admin.ModelAdmin):
    list_display = ('cName', 'eName', 'ABV', 'NT_330ml', 'Description')
    ordering = ('id',)

admin.site.register(beer, beerAdmin)
admin.site.register(can, canAdmin)

class usage_logAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'log_user', 'event_type', 'content')
    list_filter = ('event_type',)
    search_fields = ('user_id', 'user_name', 'content')
    date_hierarchy = 'timestamp'
    list_per_page = 25
    ordering = ['-timestamp']

    @admin.display(description='使用者')
    def log_user(self, obj):
        if obj.user_name:
            return format_html('<b>' + escape(obj.user_name) + '</b><br><span style="color:#777;">' + escape(obj.user_id) + '</span>')
        return escape(obj.user_id)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class line_userAdmin(admin.ModelAdmin):
    list_display = ('display_name_col', 'user_id', 'first_seen', 'last_seen')
    list_display_links = ('display_name_col',)
    search_fields = ('user_id', 'display_name')
    ordering = ['-last_seen']
    list_per_page = 25

    @admin.display(description='使用者')
    def display_name_col(self, obj):
        if obj.display_name:
            return format_html('<b>' + escape(obj.display_name) + '</b><br><span style="color:#777;">' + escape(obj.user_id) + '</span>')
        return escape(obj.user_id)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


admin.site.site_header = '掌門精釀啤酒 管理後台'
admin.site.site_title = '掌門精釀啤酒'
admin.site.index_title = '管理後台'

admin.site.register(usage_log, usage_logAdmin)
admin.site.register(line_user, line_userAdmin)
