from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
from rest_framework import status
from .models import User,CNCMachine,MachineRealtimeStatus
from .serializer import UserSerializer,CNCMachineSerializer,MachineRealtimeStatusSerializer

from asyncua.sync import Client
from concurrent.futures import ThreadPoolExecutor


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
    # return [
    #     key, url, status, actMainProgramName, TotalPartCount, ActFeedrate,
    #     ToolId, FeedHold, ActSpeed, ActLoad, ActTorque, ActOverride, CurrentAlarm
    # ]


# 0:Root,0:Objects,3:JH2301=PLC,3:DataBlocksGlobal,3:MS组,3:Static_1,3:回火炉1区温控
# ns=3;s="MS组"."Static_1"."回火炉1区温控"

# 0:Root,0:Objects,1:CNCInterface,1:CncChannelList0,1:CncChannel1,1:ActProgramStatus0
# ns=1;s=CNCInterface/CncChannelList0/CncChannel1/ActProgramStatus0

@api_view(['GET'])
def get_l2_machine_status(request):
    machine_ip_map = {
        65: "opc.tcp://192.168.31.65:4840",
        66: "opc.tcp://192.168.31.66:4840",
        67: "opc.tcp://192.168.31.67:4840",
        68: "opc.tcp://192.168.31.68:4840",
        69: "opc.tcp://192.168.31.69:4840",
        70: "opc.tcp://192.168.31.70:4840",
        71: "opc.tcp://192.168.31.71:4840",
        72: "opc.tcp://192.168.31.72:4840",
        73: "opc.tcp://192.168.31.73:4840",
        74: "opc.tcp://192.168.31.74:4840",
        75: "opc.tcp://192.168.31.75:4840",
        76: "opc.tcp://192.168.31.76:4840",
    }

    # 使用线程池并行执行
    with ThreadPoolExecutor(max_workers=len(machine_ip_map)) as executor:
        # 提交所有任务
        futures = [executor.submit(fetch_machine_data, key, url) for key, url in machine_ip_map.items()]
        # 按原始顺序获取结果
        res = [future.result() for future in futures]

    return Response(res)

@api_view(['GET'])
def get_l1_machine_status(request):
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


@api_view(['GET'])
def get_all_machine_status(request):
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


@api_view(['GET'])
def get_user(request, pk):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
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
        "machineId": pk,
        "url": target_url,
        "status": status,
    }]
    return Response(res)


# @api_view(['GET'])
# def get_all_machine_status2(request):
#     machine_ip_map = {
#         22: "opc.tcp://192.168.31.22:4840",
#         21: "opc.tcp://192.168.31.21:4840",
#         20: "opc.tcp://192.168.31.20:4840",
#         19: "opc.tcp://192.168.31.19:4840",
#         18: "opc.tcp://192.168.31.18:4840",
#         17: "opc.tcp://192.168.31.17:4840",
#         28: "opc.tcp://192.168.31.28:4840",
#         27: "opc.tcp://192.168.31.27:4840",
#         26: "opc.tcp://192.168.31.26:4840",
#         25: "opc.tcp://192.168.31.25:4840",
#         24: "opc.tcp://192.168.31.24:4840",
#         23: "opc.tcp://192.168.31.23:4840",
#     }
#     res = []
#     for key in machine_ip_map:
#         status = "未知"
#         actMainProgramName = "未知"
#         TotalPartCount = "未知"
#         ActFeedrate = "未知"
#         ToolId = "未知"
#         FeedHold = "未知"
#         ActSpeed = "未知"
#         ActLoad = "未知"
#         ActTorque = "未知"
#         ActOverride = "未知"
#         CurrentAlarm = "未知"
#         try:
#             with Client(machine_ip_map[key]) as client:
#                 ActProgramStatus0 = client.get_node("ns=1;s=CNCInterface/CncChannelList0/CncChannel1/ActProgramStatus0")
#                 if ActProgramStatus0.read_value():
#                     status = "运行中"
#                 else:
#                     status = "未在运行"
#                 try:
#                     actMainProgramName = client.get_node(
#                         "ns=1;s=CNCInterface/CncChannelList0/CncChannel1/ActProgramName0").read_value()
#                     # 当前主加工程式名称
#                     TotalPartCount = client.get_node(
#                         "ns=1;s=CNCInterface/CncChannelList0/CncChannel1/TotalPartCount0").read_value()
#                     # 加工总工件数
#                     CmdFeedrate = client.get_node(
#                         "ns=1;s=CNCInterface/CncChannelList0/CncChannel1/CmdFeedrate0").read_value()
#                     # 进给倍率改变命令
#                     ToolId = client.get_node("ns=1;s=CNCInterface/CncChannelList0/CncChannel1/ToolId0").read_value()
#                     # 系统主轴刀号
#                     FeedHold = client.get_node("ns=1;s=CNCInterface/CncChannelList0/CncChannel1/FeedHold0").read_value()
#                     # 是否加工暂停
#                     ActSpeed = client.get_node("ns=1;s=CNCInterface/CncSpindleList0/CncSpindle1/ActSpeed0").read_value()
#                     # 系统实际的主轴转速
#                     ActLoad = client.get_node("ns=1;s=CNCInterface/CncSpindleList0/CncSpindle1/ActLoad0").read_value()
#                     # 系统主轴负载率 ns=1;s=CNCInterface/CncSpindleList0/CncSpindle2/ActLoad0
#                     ActTorque = client.get_node(
#                         "ns=1;s=CNCInterface/CncSpindleList0/CncSpindle1/ActTorque0").read_value()
#                     # 主轴实际输出扭矩 ns=1;s=CNCInterface/CncSpindleList0/CncSpindle2/ActTorque0
#                     ActOverride = client.get_node(
#                         "ns=1;s=CNCInterface/CncSpindleList0/CncSpindle1/ActOverride0").read_value()
#                     # 实际转速百分比 ns=1;s=CNCInterface/CncSpindleList0/CncSpindle2/ActOverride0
#                     CurrentAlarm = client.get_node("ns=1;s=CNCInterface/CurrentAlarm0").read_value()
#                     # 系统警报展示
#                 except:
#                     status = status
#         except:
#             status = "连接失败"
#
#         res.append(
#             [key,
#              machine_ip_map[key],
#              status,
#              actMainProgramName,
#              TotalPartCount,
#              ActFeedrate,
#              ToolId,
#              FeedHold,
#              ActSpeed,
#              ActLoad,
#              ActTorque,
#              ActOverride,
#              CurrentAlarm]
#         )
#     return Response(res)


@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_CNCMachine(request):
    serializer = CNCMachineSerializer(data=request.data)
    print(request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def create_CNCMachine_batch(request):
    res_list = []
    for each in request.data:
        serializer = CNCMachineSerializer(data=each)
        if serializer.is_valid():
            serializer.save()
            res_list.append(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(res_list, status=status.HTTP_201_CREATED)




@api_view(['GET'])
def get_CNCMachine(request):
    serializer = CNCMachineSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_MachineRealtimeStatus(request):
    machineRealtimeStatus = MachineRealtimeStatus.objects.all()
    serializer = MachineRealtimeStatusSerializer(machineRealtimeStatus, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_CNCMachine(request, machine_id):
    try:
        cncMachine = CNCMachine.objects.get(pk=machine_id)
    except CNCMachine.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = CNCMachineSerializer(cncMachine)
    return Response(serializer.data)


@api_view(['GET'])
def get_all_CNCMachine(request):
    cncMachine = CNCMachine.objects.all()
    serializer = CNCMachineSerializer(cncMachine, many=True)
    return Response(serializer.data)
    
# 测试用数据
# {
# "machine_id": "1",
# "machine_name": "车削中心",
# "model": "BC20P",
# "workshop": "销轴线",
# "ip_address": "192.168.31.22",
# "is_online": 1
# }