import React from 'react';
import Header from '../../components/Header/Header.js';
import Login from '../Login/Login.js';
import Drawer from '../Drawer/Drawer.js';
import AdminPanel from '../AdminPanel/AdminPanel.js';
import User from '../User/User.js';
import Activity from '../Activity/Activity.js';
import ActivityPanel from '../ActivityPanel/ActivityPanel.js';
import Profile from '../Profile/Profile.js';
import Report from '../Report/Report.js';
import ResetPassword from '../ResetPassword/ResetPassword'
import AdminEmailVerify from '../../containers/AdminEmailVerify/AdminEmailVerify.js';
import { HOME_TAG_TYPE } from "../../constants";
import { connect } from 'react-redux';
import { Spin,Menu } from 'antd';
import { Switch } from "react-router";
import { Router, Route, Link, withRouter } from "react-router-dom";
import { createBrowserHistory } from 'history';


import './Home.less';


const history = createBrowserHistory();

class Home extends React.Component {
    getNavContent(){
        const currentTagType = () => {
            let currentUrlPath = this.props.location.pathname;
            if(currentUrlPath.includes('/profile')) currentUrlPath = '/profile'
            switch(currentUrlPath){
                case '/users': return HOME_TAG_TYPE.USER;
                case '/profile': return HOME_TAG_TYPE.PROFILE;
                case '/report': return HOME_TAG_TYPE.REPORT;
                case '/admins': return HOME_TAG_TYPE.ADMIN;
                default: return HOME_TAG_TYPE.ACTIVITY;
            }
        }

        return(
            <Menu className="nav-bar" selectedKeys={[`${currentTagType()}`]} mode="horizontal">
                <Menu.Item key={HOME_TAG_TYPE.ACTIVITY}>
                公益活动
                <Link to="/" />
                </Menu.Item>
                <Menu.Item key={HOME_TAG_TYPE.USER}>
                微信用户
                <Link to="/users" />
                </Menu.Item>
                {this.props.user && this.props.user.type === "root"? <Menu.Item key={HOME_TAG_TYPE.ADMIN}>管理员<Link to="/admins" /></Menu.Item> : null}
                <Menu.Item key={HOME_TAG_TYPE.PROFILE}>
                设置
                <Link to="/profile/base-info" />
                </Menu.Item>
            </Menu>
        )
    }

    render() {
        return (

            <div className="home" >
                <Header/>
                {this.getNavContent()}
                <div className="content-wrapper" >
                <Switch>
                    <Route exact path="/" component={ActivityPanel}/>
                    <Route path="/report" component={Report}/>
                    <Route path="/users" component={User}/>
                    <Route path="/profile" component={Profile}/>
                    {this.props.user && this.props.user.type === "root"?<Route path="/admins" component={AdminPanel}/>: null}
                </Switch>
                </div>
                {this.props.showLogin ? <Login /> : null}
                {this.props.showReset ? <ResetPassword /> : null}
                {this.props.showEmailVerify ? <AdminEmailVerify /> : null}
                <Login/>
                <Activity/>
                <Drawer/>
                <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'white'
                }}>
                    上海闵行区古美仁品社区为残服务中心©版权所有&emsp;<a target="_blank" style={{color: "white"}} href="https://beian.miit.gov.cn/">沪ICP备15045950号-1</a>
                </div>

                {this.props.loading? <Spin size="large" />: null}
            </div>
        );
    }
  }

const mapStateToProps = (state, ownProps) => ({
    tab: state.ui.homeTagType,
    loading: state.ui.loading,
    user: state.account.user,
    showLogin: !state.account.user || !state.account.user.email,
    showReset: state.ui.isShowResetPassword,
    showEmailVerify: state.ui.isShowEmailVerify,
})

const mapDispatchToProps = (dispatch, ownProps) => ({
})

export default connect(mapStateToProps, mapDispatchToProps)(withRouter(Home))
