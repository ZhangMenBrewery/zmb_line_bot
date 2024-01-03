from django.db import models

# Create your models here.
class beer(models.Model):
    tapNum = models.IntegerField()    #酒頭順序
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
