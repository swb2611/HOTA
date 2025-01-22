import React from "react";
import { Flex, Descriptions, Divider, Badge, Segmented } from "antd";
import { useState, useEffect } from "react";
import myPicture from "../pic/1.jpg";
import { Line } from "@ant-design/plots";

import { datasecond } from "./testdata";
import { Typography } from "antd";

const { Title } = Typography;

const randomIntFromInterval = (min, max) => {
  return Math.floor(Math.random() * (max - min + 1) + min);
};

const DemoLine = () => {
  const data = [
    { 日期: "2024-12-24", 输送量: 1205 },
    { 日期: "2024-12-25", 输送量: 1211 },
    { 日期: "2024-12-26", 输送量: 1226 },
    { 日期: "2024-12-27", 输送量: 1235 },
    { 日期: "2024-12-28", 输送量: 1214 },
    { 日期: "2024-12-29", 输送量: 1223 },
    { 日期: "2024-12-30", 输送量: 1212 },
    { 日期: "2024-12-31", 输送量: 1211 },
  ];
  const config1 = {
    data,
    xField: "日期",
    yField: "输送量",
    point: {
      shapeField: "square",
      sizeField: 4,
    },
    interaction: {
      tooltip: {
        marker: false,
      },
    },
    scale: {
      y: {
        type: "linear",
        domain: [1000, 1500],
        range: [0.1, 0.9],
      },
    },
    style: {
      lineWidth: 2,
    },
  };
  return <Line {...config1} />;
};

const Bucket = () => {
  const [tishengliang, setTishengliang] = useState(0);
  const [wendo, setWendo] = useState(0);
  const [zhuansu, setZhuansu] = useState(0);
  const [zhuansuzhuangtai, setZhuansuzhuangtai] = useState("success");
  const [wendozhuangtai, setWendozhuangtai] = useState("success");
  const [segvalue, setSegValue] = useState("线体状态");

  useEffect(() => {
    const interval = setInterval(() => {
      setTishengliang(String(randomIntFromInterval(1500, 1600)) + " t/h");
      const tempwendo = randomIntFromInterval(100, 110);
      setWendo(String(tempwendo) + " 摄氏度");
      if (tempwendo > 105) {
        setWendozhuangtai("error");
      } else {
        setWendozhuangtai("success");
      }
      const temp = randomIntFromInterval(20, 25);
      setZhuansu(String(temp) + " RPM");
      if (temp > 22) {
        setZhuansuzhuangtai("error");
      } else {
        setZhuansuzhuangtai("success");
      }
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  const descriptionItems = [
    {
      key: "1",
      label: "设备名称",
      children: "粮食输送提升机测试机",
    },
    {
      key: "2",
      label: "提升量",
      children: "1600t/h",
    },
    {
      key: "3",
      label: "提升物料",
      children: "大豆、大米、玉米等",
    },
    {
      key: "4",
      label: "设备型号",
      children: " NBL1600 ",
    },
    {
      key: "5",
      label: "设备地址",
      children: "和泰机电江东厂区测试区域",
    },
  ];
  const collectionItems = [
    {
      key: "1",
      label: "线体状态",
      children: <Badge status="processing" text="启用" />,
      span: 3,
    },
    {
      key: "2",
      label: "实时提升量",
      children: <Badge status="success" text={tishengliang} />,

      span: 3,
    },
    {
      key: "3",
      label: "头部轴承测温",
      children: <Badge status={wendozhuangtai} text={wendo} />,
      span: 3,
    },
    {
      key: "4",
      label: "头部传动转速",
      children: <Badge status={zhuansuzhuangtai} text={zhuansu} />,
      span: 3,
    },
    {
      key: "4",
      label: "头部轴承座震动",
      children: <Badge status="success" text="23 mm/s" />,
      span: 3,
    },
    {
      key: "4",
      label: "链条伸长量检测",
      children: <Badge status="success" text="53 mm" />,
      span: 3,
    },
  ];

  const page2 = (
    <div>
      <p></p>
      <p></p>
      <Title level={3}>粮食输送提升机测试机提升量统计(吨/小时)</Title>
      <DemoLine />
    </div>
  );

  const page1 = (
    <Flex style={{ width: "100%" }} vertical={false} justify="center">
      <Flex style={{ width: "30%" }} vertical={true}>
        <p></p>
        <p></p>
        <Descriptions
          layout="vertical"
          //   title="和泰测试提升机数据采集:"
          items={collectionItems}
        />
      </Flex>
      <img style={{ width: "40%" }} src={myPicture} alt="bucket elevator" />
    </Flex>
  );

  const page3 = <div></div>;

  const pageselect = () => {
    if (segvalue === "线体状态") {
      return page1;
    } else if (segvalue === "输送量检测") {
      return page2;
    } else if (segvalue === "故障报警") {
      return page3;
    } else {
      return page1;
    }
  };

  return (
    <Flex vertical={true} align="center">
      <Title level={3}>粮食输送提升机测试机实时数据采集显示</Title>
      <p></p>
      {/* <Descriptions title="和泰测试提升机数据采集" items={descriptionItems} /> */}
      <Segmented
        options={["线体状态", "输送量检测", "故障报警"]}
        value={segvalue}
        onChange={setSegValue}
      />
      <p></p>
      <p></p>
      {segvalue === "线体状态" ? page1 : null}
      {segvalue === "输送量检测" ? page2 : null}
      {segvalue === "故障报警" ? page3 : null}
      <Divider />
    </Flex>
  );
};

export default Bucket;
