import React from 'react';
import Header from '../../components/Header/Header.js';
import Login from '../Login/Login.js';
import AdminPanel from '../AdminPanel/AdminPanel.js';
import Activity from '../Activity/Activity.js';
import ActivityList from '../../components/ActivityList/ActivityList.js';
import { HOME_TAG_TYPE } from "../../constants";
import { connect } from 'react-redux';
import { Spin } from 'antd';
// import client from 'socket.io-client';
import './Home.css';

class Home extends React.Component {
    getContent = () => {
        switch(this.props.tab){
            case HOME_TAG_TYPE.ADMIN: return <AdminPanel/>;
            default: return <ActivityList/>;
        }
    }

    componentDidMount(){
        // let io = client.connect("http://127.0.0.1:5000");
        // io.on('connect',function() {
        //     io.emit("test",{data: 'I\'m connected!'});
        // });
    }
  
    render() {        
        let content = this.getContent();
        return (
            <div>
                <Header/>
                <div className="content-wrapper">{content}</div>
                <Login/>
                <Activity/>
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
  