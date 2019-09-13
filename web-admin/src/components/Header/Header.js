import React from 'react';
import { PageHeader, Tag, Tabs, Button, Menu, Dropdown, Icon } from 'antd';
import { switchHomeTag, logout , showActivityModal, switchAdminFormType} from '../../actions';
import { HOME_TAG_TYPE, ADMIN_FORM_TYPE } from "../../constants";
import { connect } from 'react-redux';
import './Header.css';

const { TabPane } = Tabs;

class Header extends React.Component {
    onClickCreateActivity = () =>{
        this.props.onClickCreateActivity();
    }

    render() {  
        const menu = (
          <Menu className="header-menu">
            <Menu.Item>
              {this.props.user && this.props.user.email?(<div className="header-menu-button" onClick={this.props.onClickLogout}>
                退出
              </div>): (<div className="header-menu-button"  onClick={this.props.onClickLogin}>
                登录
              </div>)}
            </Menu.Item>
          </Menu>
        );      

        return (
            <PageHeader
                  title="助盲管理"
                  className="header"
                  subTitle="Grimm Administration System"
                  tags={<Tag color="red">Beta</Tag>}
                  extra={[
                    <Dropdown key="user-menu" overlay={menu}>
                      <span className="ant-dropdown-link">
                        {(this.props.user && this.props.user.email) || "未登陆"}<Icon type="down" />
                      </span>
                    </Dropdown>,
                    <Button key="new-activity" type="primary" onClick={this.props.onClickCreateActivity}>
                      发布新活动
                    </Button>,
                  ]}
                  footer={
                    <Tabs  onChange={this.props.onChangeTab} activeKey={this.props.activeKey}>
                      <TabPane tab="志愿者活动" key={HOME_TAG_TYPE.ACTIVITY} />
                      <TabPane tab="管理员" key={HOME_TAG_TYPE.ADMIN} />
                    </Tabs>
                  }
                >
            </PageHeader>
        );
    }
  }

  const mapStateToProps = (state, ownProps) => ({
    user: state.account.user,
    activeKey: state.ui.homeTagType
  });
  
  const mapDispatchToProps = (dispatch, ownProps) => ({
    onChangeTab: (activeKey) => {
      dispatch(switchHomeTag(activeKey));
    },
    onClickLogin: () => {
      // dispatch(login());
    },
    onClickLogout: () => {
      dispatch(switchAdminFormType(ADMIN_FORM_TYPE.LOGIN));
      dispatch(switchHomeTag(HOME_TAG_TYPE.ACTIVITY));//incase login form in 2 modes
      sessionStorage.clear();
      dispatch(logout());
    },
    onClickCreateActivity: () => {
      dispatch(showActivityModal());
    }
  });

export default connect(mapStateToProps, mapDispatchToProps)(Header);