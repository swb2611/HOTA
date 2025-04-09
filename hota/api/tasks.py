from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
from rest_framework import status
from .models import User,CNCMachine,MachineRealtimeStatus
from .serializer import UserSerializer,CNCMachineSerializer,MachineRealtimeStatusSerializer
from asyncua.sync import Client
from concurrent.futures import ThreadPoolExecutor
from celery import Celery, shared_task
from celery.schedules import crontab

app = Celery()


def fetch_machine_data(key, url):
    """获取单台机器数据"""
    status = "未知"
    actMainProgramName = "未知"
    TotalPartCount = -1
    ActFeedrate = "未知"
    ToolId = "未知"
    FeedHold = 0
    ActSpeed = 0
    ActLoad = 0
    ActTorque = 0
    ActOverride = 0
    CurrentAlarm = "未知"

    try:
        with Client(url) as client:
            ActProgramStatus0 = client.get_node("ns=1;s=CNCInterface/CncChannelList0/CncChannel1/ActProgramStatus0")
            status = "运行中" if ActProgramStatus0.read_value() else "未在运行"

            try:
                # 获取所有需要读取的节点值
                actMainProgramName = client.get_node(
                    "ns=1;s=CNCInterface/CncChannelList0/CncChannel1/ActProgramName0").read_value()
                TotalPartCount = client.get_node(
                    "ns=1;s=CNCInterface/CncChannelList0/CncChannel1/TotalPartCount0").read_value()
                ActFeedrate = client.get_node(  # 注意这里修正了变量名匹配
                    "ns=1;s=CNCInterface/CncChannelList0/CncChannel1/CmdFeedrate0").read_value()
                ToolId = client.get_node(
                    "ns=1;s=CNCInterface/CncChannelList0/CncChannel1/ToolId0").read_value()
                FeedHold = client.get_node(
                    "ns=1;s=CNCInterface/CncChannelList0/CncChannel1/FeedHold0").read_value()
                ActSpeed = client.get_node(
                    "ns=1;s=CNCInterface/CncSpindleList0/CncSpindle1/ActSpeed0").read_value()
                ActLoad = client.get_node(
                    "ns=1;s=CNCInterface/CncSpindleList0/CncSpindle1/ActLoad0").read_value()
                ActTorque = client.get_node(
                    "ns=1;s=CNCInterface/CncSpindleList0/CncSpindle1/ActTorque0").read_value()
                ActOverride = client.get_node(
                    "ns=1;s=CNCInterface/CncSpindleList0/CncSpindle1/ActOverride0").read_value()
                CurrentAlarm = client.get_node(
                    "ns=1;s=CNCInterface/CurrentAlarm0").read_value()
            except Exception as e:
                # 部分节点读取失败时保持已有状态
                pass
    except Exception as e:
        status = "连接失败"

    """记录写入数据库"""
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    
    record = {
        "machine": key,
        "timestamp": timestamp,
        "ActProgramStatus0": status,
        "actMainProgramName": actMainProgramName,
        "TotalPartCount": int(TotalPartCount),
        "CmdFeedrate": ActFeedrate,
        "ToolId": ToolId,
        "FeedHold": FeedHold,
        "ActSpeed": ActSpeed,
        "ActLoad": ActLoad,
        "ActTorque": ActTorque,
        "ActOverride": ActOverride,
        "CurrentAlarm": CurrentAlarm,
    }
    
    serializer = MachineRealtimeStatusSerializer(data=record)
    print(record)
    if serializer.is_valid():
            serializer.save()
    else:
        print("储存出错：")
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return {
        "id": key,
        "url": url,
        "status": status,
        "actMainProgramName": actMainProgramName,
        "TotalPartCount": TotalPartCount,
        "ActFeedrate": ActFeedrate,
        "ToolId": ToolId,
        "FeedHold": FeedHold,
        "ActSpeed": ActSpeed,
        "ActLoad": ActLoad,
        "ActTorque": ActTorque,
        "ActOverride": ActOverride,
        "CurrentAlarm": CurrentAlarm,
    }
    
def get_l1_machine_status():
    machine_ip_map = {
        22: "opc.tcp://192.168.31.22:4840",
        21: "opc.tcp://192.168.31.21:4840",
        20: "opc.tcp://192.168.31.20:4840",
        19: "opc.tcp://192.168.31.19:4840",
        18: "opc.tcp://192.168.31.18:4840",
        17: "opc.tcp://192.168.31.17:4840",
        28: "opc.tcp://192.168.31.28:4840",
        27: "opc.tcp://192.168.31.27:4840",
        26: "opc.tcp://192.168.31.26:4840",
        25: "opc.tcp://192.168.31.25:4840",
        24: "opc.tcp://192.168.31.24:4840",
        23: "opc.tcp://192.168.31.23:4840",
    }

    # 使用线程池并行执行
    with ThreadPoolExecutor(max_workers=len(machine_ip_map)) as executor:
        # 提交所有任务
        futures = [executor.submit(fetch_machine_data, key, url) for key, url in machine_ip_map.items()]
        # 按原始顺序获取结果
        res = [future.result() for future in futures]
    return Response(res)


@shared_task
def monitor_l1():
    get_l1_machine_status()


@shared_task
def test(arg):
    print(arg)