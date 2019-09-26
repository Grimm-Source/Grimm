import React from 'react';
import {  } from 'antd';
import { connect } from 'react-redux';
import { hideHomeSider, setNoticeUsers} from '../../actions';
import NoticeUserList from '../../components/NoticeUserList/NoticeUserList';

import user from '../../images/user.svg';

import './HomeSider.css';

class HomeSider extends React.Component {  
    render() {
        const contents = [{key: 1, title: "新注册用户", component: <NoticeUserList/>, icon: <img 
                            width={18}
                            alt="user"
                            src={user}
                        />}];
        const contentList = contents.map((item) => {
                return <div className="content-block" key={item.key }><div className="title"><span className="left" >{item.title}{item.icon}</span><span className="remove-all" onClick={this.props.onClickRemoveAll}>清空用户消息</span></div><div className="list">{item.component}</div></div>
            }
        )
        return  (this.props.isSiderVisible?<div className="home-sider" onClick={this.props.onClickHomeSider}>
                    <div className="content"> 
                    <div className="notice-title">通知</div>
                    
                    {contentList}
                    </div>
                </div>: null)
    }
  }
  
  const mapStateToProps = (state, ownProps) => ({
    isSiderVisible: state.ui.isShowHomeSider
  });

  const mapDispatchToProps = (dispatch, ownProps) => ({
    onClickHomeSider: (event)=>{
        if(event.target && event.target.className === "home-sider" ){
            dispatch(hideHomeSider());
        }  
    },
    onClickRemoveAll: ()=>{
        dispatch(setNoticeUsers([]));
        dispatch(hideHomeSider());
    }
})
  
  export default connect(mapStateToProps, mapDispatchToProps)(HomeSider)