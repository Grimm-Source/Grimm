import React from 'react';
import { PageHeader, Tag, Button, Menu, Dropdown, Icon } from 'antd';
import { switchHomeTag, logout , showActivityModal, switchAdminFormType} from '../../actions';
import Notice from '../Notice/Notice.js';
import { HOME_TAG_TYPE, ADMIN_FORM_TYPE, ACTIVITY_DETAIL_TYPE } from '../../constants';
import { storage } from '../../utils/localStorageHelper';
import { withRouter} from "react-router-dom";
import { connect } from 'react-redux';

import './Header.less';

class Header extends React.Component {
    onClickCreateActivity = () => {
        this.props.onClickCreateActivity();
    }

    onClickLogout = ()=> {
        this.props.history.push('/');
        this.props.onClickLogout();
    }

    render() {  
        const menu = (
          <Menu className="header-menu">
            <Menu.Item>
              {this.props.user && this.props.user.email?(<div className="header-menu-button" onClick={this.onClickLogout}>
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
                    <Notice key="notice"/>]}
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
    onClickLogout: () => {
      dispatch(switchAdminFormType(ADMIN_FORM_TYPE.LOGIN));
      dispatch(switchHomeTag(HOME_TAG_TYPE.ACTIVITY));//incase login form in 2 modes
      storage.clearItems();
      dispatch(logout());
    },
    onClickCreateActivity: () => {
      dispatch(showActivityModal(null, ACTIVITY_DETAIL_TYPE.EDIT));
    }
  });

export default connect(mapStateToProps, mapDispatchToProps)(withRouter(Header));