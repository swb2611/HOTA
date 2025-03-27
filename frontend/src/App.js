import {useState, useEffect} from "react";
import {
    AppstoreOutlined,
    SettingOutlined,
    QuestionCircleOutlined,
    SyncOutlined,
} from "@ant-design/icons";
import {
    Breadcrumb,
    Layout,
    Menu,
    theme,
    Image,
    Row,
    Col,
    FloatButton,
} from "antd";
import {NavLink, Outlet, useLocation} from "react-router-dom";

const {Header, Content, Footer} = Layout;

const items = [
    {
        label: <NavLink to="/Home"
                        style={({isActive}) => ({
                            color: isActive ? "#FFFFFF" : "#A09F9F",
                            textDecoration: "none",
                        })}>Home</NavLink>,
        key: "/Home",
        icon: <AppstoreOutlined/>,
    },
    {
        label: <NavLink to="/Links"
                        style={({isActive}) => ({
                            color: isActive ? "#FFFFFF" : "#A09F9F",
                            textDecoration: "none",
                        })}>和泰加工设备监控-车床线</NavLink>,
        key: "/Links",
        icon: <SettingOutlined/>,
    },
    {
        label: <NavLink to="/L2Links"
                        style={({isActive}) => ({
                            color: isActive ? "#FFFFFF" : "#A09F9F",
                            textDecoration: "none",
                        })}>和泰加工设备监控-滚子套筒线</NavLink>,
        key: "/L2Links",
        icon: <SettingOutlined/>,
    },
    {
        label: <NavLink to="/Stats"
                        style={({isActive}) => ({
                            color: isActive ? "#FFFFFF" : "#A09F9F",
                            textDecoration: "none",
                        })}>和泰加工数据统计-车床线</NavLink>,
        key: "/Stats",
        icon: <SettingOutlined/>,
    },
    {
        label: <NavLink to="/Bucket"
                        style={({isActive}) => ({
                            color: isActive ? "#FFFFFF" : "#A09F9F",
                            textDecoration: "none",
                        })}>和泰测试提升机数据采集</NavLink>,
        key: "/Bucket",
        icon: <SettingOutlined/>,
    },
];

const App = () => {
    const {
        token: {colorBgContainer, borderRadiusLG},
    } = theme.useToken();
    const [current, setCurrent] = useState({});
    // 定义selectedKeys，来控制菜单选中状态和切换页面
    const [selectedKeys, setSelectedKeys] = useState([]);
    // useLocation react-router自带hook，能获取到当前路由信息
    const location = useLocation();
    // 每次切换路由，获取当前最新的pathname,并赋给menu组件
    useEffect(() => {
        // location.pathname对应路由数据中的path属性
        setSelectedKeys([location.pathname]);
        // store current menu
        setCurrent(items.find((item) => item.key === location.pathname));
        console.log("rendered");
    }, [location]);

    return (
        <Layout>
            <Header style={{display: "flex", alignItems: "center"}}>
                <div className="demo-logo"/>
                <Menu
                    theme="dark"
                    mode="horizontal"
                    selectedKeys={[current]}
                    items={items}
                    style={{flex: 1, minWidth: 0}}
                />
            </Header>
            <Content style={{padding: "0 48px"}}>
                {/* <Breadcrumb style={{ margin: "16px 0" }}>
          <Breadcrumb.Item>Home</Breadcrumb.Item>
          <Breadcrumb.Item>List</Breadcrumb.Item>
          <Breadcrumb.Item>App</Breadcrumb.Item>
        </Breadcrumb> */}
                <div
                    style={{
                        background: colorBgContainer,
                        minHeight: 280,
                        padding: 24,
                        borderRadius: borderRadiusLG,
                    }}
                >
                    <Outlet/>
                </div>
            </Content>
            <Footer style={{textAlign: "center"}}>
                和泰机电数采平台 ©{new Date().getFullYear()} Created by wenbo
            </Footer>
            <FloatButton.Group shape="square" style={{insetInlineEnd: 94}}>
                <FloatButton icon={<QuestionCircleOutlined/>}/>
                <FloatButton/>
                <FloatButton icon={<SyncOutlined/>}/>
                <FloatButton.BackTop visibilityHeight={0}/>
            </FloatButton.Group>
        </Layout>
    );
};

export default App;


