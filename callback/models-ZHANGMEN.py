from django.db import models
from django.db.models import Max

# Create your models here.
class beer(models.Model):
    time = models.CharField(max_length=10, null=False) #時間
    Style = models.CharField(max_length=40, null=False) #酒款類型
    eName = models.CharField(max_length=40, blank=True, default='') #英文名稱
    cName = models.CharField(max_length=40, null=False) #中文名稱
    ABV = models.FloatField(max_length=10, null=False) #酒精度
    IBU = models.FloatField(max_length=10, null=False) #苦度
    SRM = models.IntegerField(null=False) #色度
    NT_29L = models.IntegerField(null=False) #價格
    NT_330ml = models.IntegerField(null=False) #價格
    AwardRecord = models.CharField(max_length=200, blank=True) #得獎紀錄
    Malt = models.CharField(max_length=200, blank=True) #麥芽
    Hop = models.CharField(max_length=200, blank=True) #啤酒花
    Adj = models.CharField(max_length=200, blank=True) #其他
    Feature = models.CharField(max_length=200) #特色
    Description = models.CharField(max_length=500, blank=True) #描述
    Keyword = models.CharField(max_length=50, blank=True) #關鍵字
    Validity_period = models.CharField(max_length=50, blank=True) #有效期限
    image = models.ImageField(upload_to='beer_images/', blank=True, null=True) #酒款圖片
    position = models.PositiveIntegerField(default=0, db_index=True) #顯示順序（後台拖拉決定）

    class Meta:
        ordering = ['position']

    def save(self, *args, **kwargs):
        if self.time == '停產':  #停產的排到停產區間最後
            max_dis = beer.objects.filter(time='停產').aggregate(m=Max('position'))['m']
            self.position = max(max_dis or 999, 999) + 1
        elif self.position >= 1000 or self.position == 0:  #非停產但排序在停產區間，重新排到非停產區間最後
            max_active = beer.objects.exclude(time='停產').aggregate(m=Max('position'))['m']
            self.position = (max_active or 0) + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.cName

class can(models.Model):
    time = models.CharField(max_length=10, null=False) #時間
    eName = models.CharField(max_length=40, blank=True, default='') #英文名稱
    cName = models.CharField(max_length=40, null=False) #中文名稱
    ABV = models.FloatField(max_length=10, null=False) #酒精度
    NT_330ml = models.IntegerField(null=False) #價格
    Description = models.CharField(max_length=150, null=False) #描述
    image_url = models.CharField(max_length=100, null=False) #圖片
    order_url = models.CharField(max_length=100, null=False) #訂購
    order_text = models.CharField(max_length=20, null=False) #訂購文字

    def __str__(self):
        return self.cName

class usage_log(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True) #時間
    user_id = models.CharField(max_length=50, db_index=True, default='') #LINE使用者
    user_name = models.CharField(max_length=100, blank=True) #使用者名稱
    event_type = models.CharField(max_length=20, default='message') #事件類型
    content = models.CharField(max_length=100, blank=True) #內容摘要

    class Meta:
        indexes = [models.Index(fields=['-timestamp'])]

    def __str__(self):
        return self.user_id + ' ' + self.event_type + ' ' + self.content

class line_user(models.Model):
    user_id = models.CharField(max_length=50, unique=True) #LINE使用者ID
    display_name = models.CharField(max_length=100, blank=True) #顯示名稱
    picture_url = models.CharField(max_length=300, blank=True) #頭像
    first_seen = models.DateTimeField(auto_now_add=True) #首次使用
    last_seen = models.DateTimeField(auto_now=True) #最後使用

    def __str__(self):
        return self.display_name or self.user_id
