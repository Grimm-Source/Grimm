import React from 'react';
import Header from '../../components/Header/Header.js';
import Login from '../Login/Login.js';
import Drawer from '../Drawer/Drawer.js';
import AdminPanel from '../AdminPanel/AdminPanel.js';
import User from '../User/User.js';
import Activity from '../Activity/Activity.js';
import ActivityList from '../../components/ActivityList/ActivityList.js';
import Profile from '../Profile/Profile.js';
import Report from '../Report/Report.js';
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
                志愿者活动
                <Link to="/" />
                </Menu.Item>
                <Menu.Item key={HOME_TAG_TYPE.USER}>
                微信用户
                <Link to="/users" />
                </Menu.Item>
                <Menu.Item key={HOME_TAG_TYPE.REPORT}>
                活动签到统计
                <Link to="/report" />
                </Menu.Item>
                {this.props.user && this.props.user.type === "root"? <Menu.Item key={HOME_TAG_TYPE.ADMIN}>管理员<Link to="/admins" /></Menu.Item> : null}
                <Menu.Item key={HOME_TAG_TYPE.PROFILE}>
                个人信息管理
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
                    <Route exact path="/" component={ActivityList}/>
                    <Route path="/users" component={User}/>
                    <Route path="/report" component={Report}/>
                    <Route path="/profile" component={Profile}/>
                    {this.props.user && this.props.user.type === "root"?<Route path="/admins" component={AdminPanel}/>: null}
                </Switch>
                </div>
                <Login/>
                <Activity/>
                <Drawer/>
                {this.props.loading? <Spin size="large" />: null}
            </div>
        );
    }
  }

const mapStateToProps = (state, ownProps) => ({
    tab: state.ui.homeTagType,
    loading: state.ui.loading,
    user: state.account.user
})

const mapDispatchToProps = (dispatch, ownProps) => ({
})

export default connect(mapStateToProps, mapDispatchToProps)(withRouter(Home))
  