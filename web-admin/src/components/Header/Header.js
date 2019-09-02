import React from 'react';
import { PageHeader, Tag, Tabs, Button, Menu, Dropdown, Icon } from 'antd';
import { switchHomeTag, logout , login, showActivityModal} from '../../actions';
import { connect } from 'react-redux';
import './Header.css';

const { TabPane } = Tabs;

class Header extends React.Component {
    onClickCreateActivity = () =>{
        this.props.onClickCreateActivity();
    }

    render() {  
        const menu = (
          <Menu>
            <Menu.Item>
              {this.props.user && this.props.user.username?(<span onClick={this.props.onClickLogout}>
                退出
              </span>): (<span onClick={this.props.onClickLogin}>
                登录
              </span>)}
            </Menu.Item>
          </Menu>
        );      

        return (
            <PageHeader
                  title="助盲管理"
                  subTitle="Grimm Administration System"
                  tags={<Tag color="red">Beta</Tag>}
                  extra={[
                    <Dropdown key="user-menu" overlay={menu}>
                      <a className="ant-dropdown-link" href="#">
                        {this.props.user && this.props.user.username ||"未登陆"}<Icon type="down" />
                      </a>
                    </Dropdown>,
                    <Button key="new-activity" type="primary" onClick={this.props.onClickCreateActivity}>
                      发布新活动
                    </Button>,
                  ]}
                  footer={
                    <Tabs defaultActiveKey="activity" onChange={this.props.onChangeTab}>
                      <TabPane tab="志愿者活动" key="activity" />
                      <TabPane tab="管理员" key="admin" />
                    </Tabs>
                  }
                >
            </PageHeader>
        );
    }
  }

  const mapStateToProps = (state, ownProps) => ({
    user: state.account.user
  });
  
  const mapDispatchToProps = (dispatch, ownProps) => ({
    onChangeTab: (activeKey) => {
      dispatch(switchHomeTag(activeKey));
    },
    onClickLogin: () => {
      // dispatch(login());
    },
    onClickLogout: () => {
      sessionStorage.clear();
      dispatch(logout());
    },
    onClickCreateActivity: () => {
      dispatch(showActivityModal());
    }
  });

export default connect(mapStateToProps, mapDispatchToProps)(Header);