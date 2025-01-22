from django.shortcuts import render


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializer import UserSerializer

from asyncua.sync import Client


@api_view(['GET'])
def get_user(request,pk):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    machine_ip_map  = {
        22:"opc.tcp://192.168.31.22:4840",
        21:"opc.tcp://192.168.31.21:4840",
        20:"opc.tcp://192.168.31.20:4840",
        19:"opc.tcp://192.168.31.19:4840",
        18:"opc.tcp://192.168.31.18:4840",
        17:"opc.tcp://192.168.31.17:4840",
        28:"opc.tcp://192.168.31.28:4840",
        27:"opc.tcp://192.168.31.27:4840",
        26:"opc.tcp://192.168.31.26:4840",
        25:"opc.tcp://192.168.31.25:4840",
        24:"opc.tcp://192.168.31.24:4840",
        23:"opc.tcp://192.168.31.23:4840",
    }
    target_url = machine_ip_map[pk]
    status = "未知"
    try:
        with Client(target_url) as client:
            var = client.get_node("ns=1;s=CNCInterface/CncChannelList0/CncChannel1/ActProgramStatus0")
            
            if var.read_value():
                status = "运行中"
            else:
                status = "未在运行"
            
    except:
        status = "连接失败"

    res = [{
        "machineId":pk,
        "url":target_url,
        "status":status,
    }]
    return Response(res)

# 0:Root,0:Objects,3:JH2301=PLC,3:DataBlocksGlobal,3:MS组,3:Static_1,3:回火炉1区温控
# ns=3;s="MS组"."Static_1"."回火炉1区温控"

# 0:Root,0:Objects,1:CNCInterface,1:CncChannelList0,1:CncChannel1,1:ActProgramStatus0
# ns=1;s=CNCInterface/CncChannelList0/CncChannel1/ActProgramStatus0


@api_view(['GET'])
def get_all_machine_status(request):
    machine_ip_map  = {
        22:"opc.tcp://192.168.31.22:4840",
        21:"opc.tcp://192.168.31.21:4840",
        20:"opc.tcp://192.168.31.20:4840",
        19:"opc.tcp://192.168.31.19:4840",
        18:"opc.tcp://192.168.31.18:4840",
        17:"opc.tcp://192.168.31.17:4840",
        28:"opc.tcp://192.168.31.28:4840",
        27:"opc.tcp://192.168.31.27:4840",
        26:"opc.tcp://192.168.31.26:4840",
        25:"opc.tcp://192.168.31.25:4840",
        24:"opc.tcp://192.168.31.24:4840",
        23:"opc.tcp://192.168.31.23:4840",
    }
    res = []
    for key in machine_ip_map:
        status = "未知"
        actMainProgramName = "未知"
        TotalPartCount = "未知"
        ActFeedrate = "未知"
        ToolId = "未知"
        FeedHold = "未知"
        ActSpeed = "未知"
        ActLoad = "未知"
        ActTorque = "未知"
        ActOverride = "未知"
        CurrentAlarm = "未知"
        try:
            with Client(machine_ip_map[key]) as client:
                ActProgramStatus0 = client.get_node("ns=1;s=CNCInterface/CncChannelList0/CncChannel1/ActProgramStatus0")
                if ActProgramStatus0.read_value():
                    status = "运行中"
                else:
                    status = "未在运行"
                try:
                    actMainProgramName = client.get_node("ns=1;s=CNCInterface/CncChannelList0/CncChannel1/ActProgramName0").read_value()
                    # 当前主加工程式名称
                    TotalPartCount = client.get_node("ns=1;s=CNCInterface/CncChannelList0/CncChannel1/TotalPartCount0").read_value()
                    # 加工总工件数
                    CmdFeedrate = client.get_node("ns=1;s=CNCInterface/CncChannelList0/CncChannel1/CmdFeedrate0").read_value()
                    # 进给倍率改变命令
                    ToolId = client.get_node("ns=1;s=CNCInterface/CncChannelList0/CncChannel1/ToolId0").read_value()
                    # 系统主轴刀号
                    FeedHold = client.get_node("ns=1;s=CNCInterface/CncChannelList0/CncChannel1/FeedHold0").read_value()
                    # 是否加工暂停
                    ActSpeed = client.get_node("ns=1;s=CNCInterface/CncSpindleList0/CncSpindle1/ActSpeed0").read_value()
                    # 系统实际的主轴转速 
                    ActLoad = client.get_node("ns=1;s=CNCInterface/CncSpindleList0/CncSpindle1/ActLoad0").read_value()
                    # 系统主轴负载率 ns=1;s=CNCInterface/CncSpindleList0/CncSpindle2/ActLoad0
                    ActTorque = client.get_node("ns=1;s=CNCInterface/CncSpindleList0/CncSpindle1/ActTorque0").read_value()
                    # 主轴实际输出扭矩 ns=1;s=CNCInterface/CncSpindleList0/CncSpindle2/ActTorque0
                    ActOverride = client.get_node("ns=1;s=CNCInterface/CncSpindleList0/CncSpindle1/ActOverride0").read_value()
                    # 实际转速百分比 ns=1;s=CNCInterface/CncSpindleList0/CncSpindle2/ActOverride0
                    CurrentAlarm = client.get_node("ns=1;s=CNCInterface/CurrentAlarm0").read_value()
                    # 系统警报展示
                except:
                    status = status
        except:
            status = "连接失败"
        
        
        res.append(
            [key,
             machine_ip_map[key],
             status,
             actMainProgramName,
             TotalPartCount,
             ActFeedrate,
             ToolId,
             FeedHold,
             ActSpeed,
             ActLoad,
             ActTorque,
             ActOverride,
             CurrentAlarm]
            )
    return Response(res)


@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status = status.HTTP_201_CREATED)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


