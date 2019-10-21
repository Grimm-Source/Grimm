import React from 'react';
import { PageHeader, Tag, Tabs, Button, Menu, Dropdown, Icon } from 'antd';
import { switchHomeTag, logout , showActivityModal, switchAdminFormType, showDrawer} from '../../actions';
import { HOME_TAG_TYPE, ADMIN_FORM_TYPE } from "../../constants";
import notice from '../../images/notice.svg';
import { connect } from 'react-redux';
import { BrowserRouter as Link } from "react-router-dom";

// import client from 'socket.io-client';

import './Header.less';

const { TabPane } = Tabs;

class Header extends React.Component {

    componentDidMount(){
        // let io = client.connect("http://127.0.0.1:5000");
        // io.on('connect',function() {
        //     io.emit("test",{data: 'I\'m connected!'});
        // });
    }

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
                    <span key="notice" className="notice" onClick={this.props.onClickNotice}>
                      <img 
                        width={25}
                        alt="notice"
                        src={notice}
                      />
                      {this.props.notices.length > 0? <span className="notice-count"/> : null }
                    </span>]}
                  // footer={
                  //   // <Tabs  onChange={this.props.onChangeTab} activeKey={this.props.activeKey}>
                  //   //   <TabPane tab="志愿者活动" key={HOME_TAG_TYPE.ACTIVITY} />
                  //   //   <TabPane tab="微信用户" key={HOME_TAG_TYPE.USER}/>
                  //   //   <TabPane tab="个人信息管理" key={HOME_TAG_TYPE.PROFILE}/>
                  //   //   {this.props.user && this.props.user.type === "root"? <TabPane tab="管理员" key={HOME_TAG_TYPE.ADMIN} />: null}
                  //   // </Tabs>
                  // }
                >
            </PageHeader>
        );
    }
  }

  const mapStateToProps = (state, ownProps) => ({
    user: state.account.user,
    activeKey: state.ui.homeTagType,
    notices: [1] || state.notice.notices //temp
  });
  
  const mapDispatchToProps = (dispatch, ownProps) => ({
    onChangeTab: (activeKey) => {
      dispatch(switchHomeTag(activeKey));
    },
    onClickLogin: () => {
      // dispatch(login());
    },
    onClickNotice: () =>{
      dispatch(showDrawer());
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