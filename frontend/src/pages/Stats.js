import React from "react";
import { Base } from "@ant-design/plots";
import { datatest, descriptionItems } from "./testdata";
import { Flex, Descriptions, Divider } from "antd";

const dataTransformed = datatest.map(({ date, ...d }) => ({
  ...d,
  date: new Date(date).getMonth() + "",
}));

const StatsData = () => {
  const config = {
    type: "repeatMatrix",
    width: 800,
    height: 720,
    autoFit: true,
    paddingLeft: 60,
    paddingBottom: 60,
    data: dataTransformed,
    encode: { y: ["设备综合效率", "主轴转速", "加工数量"], x: "date" },
    children: [
      {
        type: "line",
        encode: { color: "location" },
        transform: [{ type: "groupX", y: "mean" }],
        scale: { y: { zero: true } },
      },
    ],
  };
  return <Base {...config} />;
};

const Stats = () => {
  return (
    <Flex vertical={true} align="start">
      <Descriptions title="销轴生产车床线实时监控" items={descriptionItems} />
      <Divider />
      <p>销轴生产车床线实时监控数据统计：OEE统计等</p>
      <StatsData />
    </Flex>
  );
};

export default Stats;
