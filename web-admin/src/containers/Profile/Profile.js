import React from 'react';
import { Layout, Menu, Icon } from 'antd';
import { connect } from 'react-redux';
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import './Profile.less';

import BaseInfo from '../../components/BaseInfo/BaseInfo';
import ChangePassword from '../../components/ChangePassword/ChangePassword';

const { SubMenu } = Menu;
const { Content, Sider } = Layout;

class Profile extends React.Component {  
  render() {
    return (
        <Router>
            <Content style={{ padding: '0 50px' }}>
                <Layout style={{ padding: '24px 0', background: '#fff' }}>
                    <Sider width={200} style={{ background: '#fff' }}>
                        <Menu
                            mode="inline"
                            defaultSelectedKeys={['base-info']}
                            style={{ height: '100%' }}
                        >
                            <Menu.Item key="base-info">
                                <Icon type="user" />
                                基本信息
                                <Link to="/profile" />
                            </Menu.Item>
                            <Menu.Item key="change-password">
                                <Icon type="laptop" />
                                密码修改
                                <Link to="/changePassword" />
                            </Menu.Item>
                            <SubMenu key="sub3"
                            title={
                                <span>
                                <Icon type="notification" />
                                个人消息
                                </span>
                            }
                            >
                                <Menu.Item key="9">option3</Menu.Item>
                                <Menu.Item key="10">option4</Menu.Item>
                            </SubMenu>
                        </Menu>
                    </Sider>
                    <Content style={{ padding: '0 24px', minHeight: 280 }}>
                        <Route exact path="/profile" component={BaseInfo} />
                        <Route path="/changePassword" component={ChangePassword} />
                    </Content>
                </Layout>
            </Content>
        </Router>
    );
  }
}

const mapStateToProps = (state, ownProps) => ({
  loading: state.ui.loading
});

export default connect(mapStateToProps)(Profile)