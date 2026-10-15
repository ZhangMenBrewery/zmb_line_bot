from django.db import models

# Create your models here.
class hmi_event(models.Model):  #警報事件
    time = models.TimeField() #時間
    event = models.CharField(max_length=100, blank=True) #事件
    def __str__(self):
        return self.event

class TMP(models.Model):  #TMP
    date = models.DateField() #日期
    time = models.TimeField() #時間
    name = models.CharField(max_length=20) #設備名稱
    realtmp = models.FloatField(max_length=10) #實際溫度
    settmp = models.FloatField(max_length=10) #設定溫度
    def __str__(self):
        return self.name