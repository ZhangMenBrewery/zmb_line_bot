from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from django.db.models import Case, When, Value, IntegerField
from django.utils.html import escape, format_html
from callback.models import beer, can, usage_log, line_user


def _line_card_html(obj, image_url):
    abv_icons = '🍺🍺🍺🍺🍺' if obj.ABV >= 10 else '🍺' * int(obj.ABV / 2)
    ibu_icons = '🌿🌿🌿🌿🌿' if obj.IBU >= 60 else '🌿' * int(obj.IBU / 12)
    award = ''
    if obj.AwardRecord:
        award = '<div class="lc-award">🏆' + escape(obj.AwardRecord).replace('\n', '<br>🏆') + '</div>'
    badge = '<div class="lc-badge">' + escape(obj.time or '') + '</div>'
    if image_url:
        img_tag = '<img id="card-preview-img" src="' + escape(image_url) + '" />'
    else:
        img_tag = ('<img id="card-preview-img" style="display:none;" />'
                   '<div id="card-preview-placeholder" class="lc-placeholder">尚未上傳圖片</div>')
    return (
        '<div id="line-card-preview">'
        '<div class="lc-img-wrap">' + img_tag + '</div>'
        '<div class="lc-body">'
        '<div class="lc-badge-wrap">' + badge + '</div>'
        '<div class="lc-cname">' + escape(obj.cName or '') + '</div>'
        '<div class="lc-ename">' + escape(obj.eName or '') + '</div>'
        '<div class="lc-style">' + escape(obj.Style or '') + '</div>'
        '<div class="lc-meta">酒精 ' + abv_icons + '　苦度 ' + ibu_icons + '</div>'
        '<div class="lc-meta2">ABV : ' + str(obj.ABV) + '%　IBU : ' + str(obj.IBU) + '　SRM : ' + str(obj.SRM) + '</div>'
        + award +
        '<div class="lc-text"><b>特色：</b>' + escape(obj.Feature or '') + '</div>'
        '<div class="lc-text"><b>說明：</b>' + escape(obj.Description or '') + '</div>'
        '<div class="lc-copy">Copyright@掌門精釀啤酒 2026</div>'
        '</div></div>'
    )


class beerAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('beer_thumb', 'beer_name', 'Style', 'time', 'validity_period', 'ABV', 'IBU', 'SRM', 'keyword_short', 'award_short')
    list_display_links = ('beer_name',)
    list_filter = ('time', 'Style')
    search_fields = ('cName', 'eName', 'Style', 'Keyword', 'AwardRecord')
    list_per_page = 20
    readonly_fields = ('card_preview',)
    change_form_template = 'callback/beer_change_form.html'
    ordering = ['position']

    fieldsets = (
        ('基本資料', {'fields': ('cName', 'eName', 'Style', 'time', 'Validity_period')}),
        ('風味與數據', {'fields': ('ABV', 'IBU', 'SRM', 'Malt', 'Hop', 'Adj')}),
        ('價格與搜尋', {'fields': ('NT_29L', 'NT_330ml', 'Keyword')}),
        ('介紹內容', {'fields': ('Feature', 'Description', 'AwardRecord')}),
        ('圖片與預覽', {'fields': ('card_preview', 'image'), 'description': '建議 4:3 橫式 1200x900、JPEG/PNG、1MB 以內'}),
    )

    @admin.display(description='效期')
    def validity_period(self, obj):
        return escape(obj.Validity_period or '')

    @admin.display(description='圖')
    def beer_thumb(self, obj):
        if obj.image:
            return format_html('<img src="' + escape(obj.image.url) + '" style="height:40px;border-radius:4px;" />')
        return '—'

    @admin.display(description='酒款')
    def beer_name(self, obj):
        return format_html('<b>' + escape(obj.cName) + '</b><br><span style="color:#777;">' + escape(obj.eName or '') + '</span>')

    @admin.display(description='關鍵字')
    def keyword_short(self, obj):
        return escape((obj.Keyword or '')[:30])

    @admin.display(description='得獎')
    def award_short(self, obj):
        return escape((obj.AwardRecord or '')[:30])

    @admin.display(description='LINE 圖卡預覽')
    def card_preview(self, obj):
        image_url = obj.image.url if obj.image else ''
        return format_html(_line_card_html(obj, image_url))


class canAdmin(admin.ModelAdmin):
    list_display = ('can_thumb', 'cName', 'eName', 'ABV', 'NT_330ml', 'Description')
    list_display_links = ('cName',)
    search_fields = ('cName', 'eName')
    list_per_page = 20

    @admin.display(description='圖')
    def can_thumb(self, obj):
        if obj.image_url:
            return format_html('<img src="' + escape(obj.image_url) + '" style="height:40px;border-radius:4px;" />')
        return '—'


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

admin.site.register(beer, beerAdmin)
admin.site.register(can, canAdmin)
admin.site.register(usage_log, usage_logAdmin)
admin.site.register(line_user, line_userAdmin)
