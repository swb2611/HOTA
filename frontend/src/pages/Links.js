import React from "react";
import axios from "axios";
import { useState, useEffect } from "react";
import {
  Descriptions,
  Spin,
  Tag,
  Flex,
  Card,
  Divider,
  Badge,
  Popover,
} from "antd";
import {
  CloseCircleOutlined,
  LoadingOutlined,
  SyncOutlined,
  StockOutlined,
  WarningOutlined,
  SwapOutlined,
  SettingOutlined,
  EllipsisOutlined,
} from "@ant-design/icons";
import { Col, Row, Statistic } from "antd";

const Links = () => {
  const [loading, setLoading] = useState(true);
  const [mstatus, setMstatus] = useState([]);
  const [mstatuscount, setMstatuscount] = useState([0, 0, 0, 0]);
  const [num, setNum] = useState(0);
  const connectionFail = "连接失败";
  const working = "运行中";
  const notWorking = "未在运行";
  const mCodeMapToName = {
    17: "HT-3006双主轴",
    18: "HT-3007车床",
    19: "HT-3008车床",
    20: "HT-3009车床",
    21: "HT-3010车床",
    22: "HT-3011车床",
    23: "HT-3012双主轴",
    24: "HT-3013车床",
    25: "HT-3014车床",
    26: "HT-3015车床",
    27: "HT-3016车床",
    28: "HT-3017车床",
  };

  // useEffect(() => {
  //   const getData = async () => {
  //     setLoading(true);
  //     var fetchedData = [];
  //     try {
  //       fetchedData = await axios
  //         .get(`http://127.0.0.1:8000/api/machine-status/`)
  //         .then((res) => {
  //           setMstatus(res.data);
  //           console.log(res.data);
  //
  //           var jianceshebei = 0;
  //           var shebeilianjie = 0;
  //           var kaijiyunxing = 0;
  //           var guzhangbaojing = 0;
  //
  //           res.data.map((key) => {
  //             if (key[2] === connectionFail) {
  //               jianceshebei = jianceshebei + 1;
  //             }
  //             if (key[2] === working) {
  //               jianceshebei = jianceshebei + 1;
  //               shebeilianjie = shebeilianjie + 1;
  //               kaijiyunxing = kaijiyunxing + 1;
  //             }
  //             if (key[2] === notWorking) {
  //               jianceshebei = jianceshebei + 1;
  //               shebeilianjie = shebeilianjie + 1;
  //               guzhangbaojing = guzhangbaojing + 1;
  //             }
  //             setMstatuscount([
  //               jianceshebei,
  //               shebeilianjie,
  //               kaijiyunxing,
  //               guzhangbaojing,
  //             ]);
  //             return null;
  //           });
  //         });
  //     } catch (error) {
  //       //error handler
  //     } finally {
  //       setLoading(false);
  //     }
  //     return await fetchedData;
  //   };
  //
  //   getData();
  // }, []);

  useEffect(() => {
    const abortController = new AbortController();

    const COUNT_INDEX = {
      MONITORED: 0,
      CONNECTED: 1,
      RUNNING: 2,
      FAULT: 3,
    };

    const fetchData = async () => {
      try {
        setLoading(true);

        const response = await axios.get(
          "http://127.0.0.1:8000/api/l1-machine-status/",
          { signal: abortController.signal } // 绑定取消信号
        );

        if (!response.data || !Array.isArray(response.data)) {
          throw new Error("Invalid data format");
        }

        const rawData = response.data;

        const counts = rawData.reduce(
          (acc, current) => {
            console.log(current);
            const status = current["status"];

            // 监测设备计数（所有状态都计数）
            acc[COUNT_INDEX.MONITORED] += 1;

            switch (status) {
              case working:
                acc[COUNT_INDEX.CONNECTED] += 1;
                acc[COUNT_INDEX.RUNNING] += 1;
                break;
              case notWorking:
                acc[COUNT_INDEX.CONNECTED] += 1;
                acc[COUNT_INDEX.FAULT] += 1;
                break;
              case connectionFail:
                // 不需要额外处理
                break;
              default:
                console.warn("未知状态:", status);
            }

            return acc;
          },
          [0, 0, 0, 0]
        ); // 初始值对应四个计数器

        setMstatus(rawData);
        setMstatuscount(counts);
        setNum(counts[0]);

        if (process.env.NODE_ENV === "development") {
          console.log("Processed data:", {
            rawData,
            counts,
          });
        }
      } catch (error) {
        if (!abortController.signal.aborted) {
          console.error("数据请求失败:", error);
          // 可以添加状态更新显示错误信息
          // setError(error.message);
        }
      } finally {
        if (!abortController.signal.aborted) {
          setLoading(false);
        }
      }
    };

    fetchData();

    return () => {
      abortController.abort();
    };
  }, []);

  const statusToTagMap = (statusToTag) => {
    if (statusToTag === connectionFail) {
      return (
        <Tag icon={<CloseCircleOutlined />} color="error">
          断线
        </Tag>
      );
    }
    if (statusToTag === working) {
      return (
        <Tag icon={<SyncOutlined spin />} color="success">
          运行
        </Tag>
      );
    }
    if (statusToTag === notWorking) {
      return (
        <Tag icon={<LoadingOutlined spin />} color="processing">
          调试
        </Tag>
      );
    }
    return (
      <Tag icon={<CloseCircleOutlined />} color="error">
        未知
      </Tag>
    );
  };

  const contentStyle = {
    margin: 0,
    minheight: "400px",
    width: "100%",
    color: "#fff",
    background: "#001529",
  };
  const cardStyle = {
    margin: "15px",
    width: "180px",
  };

  const descriptionItems = [
    {
      key: "1",
      label: "线体名称",
      children: "宝鸡车床线A1A2",
    },
    {
      key: "2",
      label: "从属设备",
      children: "双主轴车床;车削中心,自动连线",
    },
    {
      key: "3",
      label: "加工产品",
      children: "和泰标准链条销轴 φ63*229",
    },
    {
      key: "4",
      label: "设备型号",
      children: " BC20P x 2, BC3751-HY x 5 ",
    },
    {
      key: "5",
      label: "设备地址",
      children: "和泰机电益农厂区一楼车床加工线AB",
    },
    {
      key: "5",
      label: "线体状态",
      children: <Badge status="processing" text="启用" />,
    },
  ];

  return (
    <Flex vertical={true}>
      <Flex vertical={true}>
        <Descriptions title="销轴生产车床线实时监控" items={descriptionItems} />
        <Divider />
        <Row gutter={16}>
          <Col span={6}>
            <Card bordered={false}>
              <Statistic
                prefix={<StockOutlined />}
                title="监测设备数量"
                suffix={"/" + num}
                value={mstatuscount[0]}
                loading={loading}
              />
            </Card>
          </Col>
          <Col span={6}>
            <Card bordered={false}>
              <Statistic
                prefix={<SwapOutlined />}
                title="设备连接状态"
                value={mstatuscount[1]}
                suffix={"/" + num}
                loading={loading}
              />
            </Card>
          </Col>
          <Col span={6}>
            <Card bordered={false}>
              <Statistic
                title="开机运行状态"
                value={mstatuscount[2]}
                suffix={"/" + num}
                prefix={<SyncOutlined />}
                loading={loading}
              />
            </Card>
          </Col>
          <Col span={6}>
            <Card bordered={false}>
              <Statistic
                title="设备故障报警"
                suffix={"/" + num}
                value={mstatuscount[3]}
                prefix={<WarningOutlined />}
                loading={loading}
              />
            </Card>
          </Col>
        </Row>
        <Divider />
        <Flex
          style={contentStyle}
          align="center"
          justify="space-evenly"
          wrap="wrap"
        >
          {loading ? (
            <Spin indicator={<LoadingOutlined spin />} size="large" />
          ) : (
            mstatus.map((key) => {
              const mName = mCodeMapToName[String(key["id"])];
              const actions = [
                <Popover
                  content={
                    // <div>
                    //     <p>当前主加工程式名称: {key[3]}</p>
                    //     <p>加工总工件数: {key[4]}</p>
                    //     <p>系统实际的进给倍率: {key[5]}</p>
                    //     <p>系统主轴刀号: {key[6]}</p>
                    //     <p>是否加工暂停: {key[7] ? " 是 " : " 否 "}</p>
                    //     <p>系统实际的主轴转速: {key[8]}</p>
                    //     <p>系统主轴负载率: {key[9]}</p>
                    //     <p>主轴实际输出扭矩: {key[10]}</p>
                    //     <p>实际转速百分比: {key[11]}</p>
                    //     <p>系统警报: {key[12] ? "无报警" : key[12]}</p>
                    // </div>
                    <div>
                      <p>当前主加工程式名称: {key["actMainProgramName"]}</p>
                      <p>加工总工件数: {key["TotalPartCount"]}</p>
                      <p>系统实际的进给倍率: {key["ActFeedrate"]}</p>
                      <p>系统主轴刀号: {key["ToolId"]}</p>
                      <p>是否加工暂停: {key["FeedHold"] ? " 是 " : " 否 "}</p>
                      <p>系统实际的主轴转速: {key["ActSpeed"]}</p>
                      <p>系统主轴负载率: {key["ActLoad"]}</p>
                      <p>主轴实际输出扭矩: {key["ActTorque"]}</p>
                      <p>实际转速百分比: {key["ActOverride"]}</p>
                      <p>
                        系统警报:{" "}
                        {key["CurrentAlarm"] ? "无报警" : key["CurrentAlarm"]}
                      </p>
                    </div>
                  }
                  title={mName}
                  trigger="click"
                  key={"11" + key["id"]}
                >
                  <EllipsisOutlined key="setting" />
                </Popover>,
              ];

              return (
                <Card style={cardStyle} actions={actions} bordered={true}>
                  <Card.Meta
                    key={key["id"]}
                    title={mName}
                    description={
                      <>
                        {statusToTagMap(key["status"])}
                        {key["actMainProgramName"]}
                      </>
                    }
                  />
                </Card>
              );
            })
          )}
        </Flex>
      </Flex>
    </Flex>
  );
};

export default Links;
