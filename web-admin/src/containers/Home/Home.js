import React from 'react';
import Header from '../../components/Header/Header.js';
import Login from '../Login/Login.js';
import Drawer from '../Drawer/Drawer.js';
import AdminPanel from '../AdminPanel/AdminPanel.js';
import User from '../User/User.js';
import Activity from '../Activity/Activity.js';
import ActivityList from '../../components/ActivityList/ActivityList.js';
import Profile from '../Profile/Profile.js';
import { HOME_TAG_TYPE } from "../../constants";
import { connect } from 'react-redux';
import { Spin,Menu } from 'antd';
import { Router, Route, Link } from "react-router-dom";
import { createBrowserHistory } from 'history';

import './Home.less';

const history = createBrowserHistory();

class Home extends React.Component {
    getNavContent(history){
        const currentTagType = () => {
            switch(history.location.pathname){
                // case '/changePassword':
                case '/users': return HOME_TAG_TYPE.USER;
                case '/profile': return HOME_TAG_TYPE.PROFILE;
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
                {this.props.user && this.props.user.type === "root"? <Menu.Item key={HOME_TAG_TYPE.ADMIN}>管理员<Link to="/admins" /></Menu.Item> : null}
                <Menu.Item key={HOME_TAG_TYPE.PROFILE}>
                个人信息管理
                <Link to="/profile" />
                </Menu.Item>
                
            </Menu>
        )
    }
  
    render() {
        return (
            <Router history={history}>
                <div className="home" >
                    <Header/>
                    {this.getNavContent(history)}
                    <div className="content-wrapper" >
                        <Route exact path="/" component={ActivityList}/>
                        <Route path="/users" component={User}/>
                        <Route path="/profile" component={Profile}/>
                        {this.props.user && this.props.user.type === "root"?<Route path="/admins" component={AdminPanel}/>: null}
                    </div>
                    <Login/>
                    <Activity/>
                    <Drawer/>
                    {this.props.loading? <Spin size="large" />: null}
                </div>
            </Router>   
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

export default connect(mapStateToProps, mapDispatchToProps)(Home)
  