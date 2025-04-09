from django.db import models

# Create your models here.


class User(models.Model):
    age = models.IntegerField()
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class CNCMachine(models.Model):
    machine_id = models.CharField(max_length=32, primary_key=True, verbose_name="设备编号")
    machine_name = models.CharField(max_length=64, blank=True, verbose_name="设备名称")
    model = models.CharField(max_length=64, verbose_name="设备型号")
    workshop = models.CharField(max_length=32, blank=True, verbose_name="所属车间")
    ip_address = models.GenericIPAddressField(protocol='IPv4', blank=True, null=True, verbose_name="IP地址")
    is_online = models.BooleanField(default=False,blank=True, verbose_name="启用状态")

    def __str__(self):
        return self.machine_id



class MachineRealtimeStatus(models.Model):
    STATUS_CHOICES = [
        ('运行中', 'ON'),
        ('未在运行', 'OFF'),
        ("连接失败",'FAIL'),
        ("未知",'UNKNOWN')
    ]
    

    machine = models.ForeignKey(CNCMachine, on_delete=models.PROTECT, verbose_name="设备")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="时间戳")

    ActProgramStatus0 = models.CharField(max_length=7, choices=STATUS_CHOICES, verbose_name="电源状态")
    actMainProgramName = models.CharField(max_length=64, verbose_name="当前主加工程式名称")
    TotalPartCount = models.IntegerField(max_length=64, verbose_name="加工总工件数")
    CmdFeedrate = models.CharField(max_length=64, verbose_name="进给倍率改变命令")
    ToolId = models.CharField(max_length=64, verbose_name="系统主轴刀号")
    FeedHold = models.BooleanField(max_length=64, verbose_name="是否加工暂停")
    ActSpeed = models.FloatField(max_length=64, verbose_name="系统实际的主轴转速")
    ActLoad = models.FloatField(max_length=64, verbose_name="系统主轴负载率")
    ActTorque = models.FloatField(max_length=64, verbose_name="主轴实际输出扭矩")
    ActOverride = models.FloatField(max_length=64, verbose_name="实际转速百分比")
    CurrentAlarm = models.CharField(max_length=128, blank=True, verbose_name="系统警报展示")

    def __str__(self):
        return self.timestamp
    


