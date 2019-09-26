import React from 'react';
import Header from '../../components/Header/Header.js';
import Login from '../Login/Login.js';
import HomeSider from '../HomeSider/HomeSider.js';
import AdminPanel from '../AdminPanel/AdminPanel.js';
import User from '../User/User.js';
import Activity from '../Activity/Activity.js';
import ActivityList from '../../components/ActivityList/ActivityList.js';
import { HOME_TAG_TYPE } from "../../constants";
import { connect } from 'react-redux';
import { Spin } from 'antd';

import './Home.css';

class Home extends React.Component {
    getContent = () => {
        switch(this.props.tab){
            case HOME_TAG_TYPE.ADMIN: return <AdminPanel/>;
            case HOME_TAG_TYPE.USER: return <User/>;
            default: return <ActivityList/>;
        }
    }


  
    render() {        
        let content = this.getContent();
        return (
            <div className="home" >
                <Header/>
                <div className="content-wrapper" >{content}</div>
                <Login/>
                <Activity/>
                <HomeSider/>
                {this.props.loading? <Spin size="large" />: null}
            </div>
        );
    }
  }

const mapStateToProps = (state, ownProps) => ({
    tab: state.ui.homeTagType,
    loading: state.ui.loading
})

const mapDispatchToProps = (dispatch, ownProps) => ({
})

export default connect(mapStateToProps, mapDispatchToProps)(Home)
  