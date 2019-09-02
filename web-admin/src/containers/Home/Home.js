import React from 'react';
import Header from '../../components/Header/Header.js';
import Login from '../Login/Login.js';
import AdminPanel from '../AdminPanel/AdminPanel.js';
import Activity from '../Activity/Activity.js';
import ActivityList from '../../components/ActivityLIst/ActivityList.js';
import { connect } from 'react-redux';
import { Spin } from 'antd';
import './Home.css';

class Home extends React.Component {
    getContent = () => {
        switch(this.props.tab){
            case "admin": return <AdminPanel/>;
            default: return <ActivityList/>;
        }
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
    tab: state.ui.activeHomeTagKey,
    loading: state.ui.loading
})

const mapDispatchToProps = (dispatch, ownProps) => ({

})

export default connect(mapStateToProps, mapDispatchToProps)(Home)
  