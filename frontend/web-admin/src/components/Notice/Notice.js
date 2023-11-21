import React from 'react';
import { showDrawer, setNoticeUsers} from '../../actions';
import notice from '../../images/notice.svg';
import { connect } from 'react-redux';
import { socketHelper } from '../../utils/socketHelper.js';
import { message } from 'antd';

import './Notice.less';

class Notice extends React.Component {

    constructor(props) {
        super(props);
        this.io = null;
        if(this.props.hasLogined){
            // this.initNewUsersSocket();
        }
    }

    componentWillReceiveProps(nextProps, prevState){
        if(!this.io && nextProps.hasLogined){
            // this.initNewUsersSocket();
        }
    }

    initNewUsersSocket(){
        this.io = socketHelper.getNewUsersSockect();
        
        this.io.on('new-users', (users) => {
            if( !users || users.length === 0 ){
                return;
            }
            message.success(`${users.length}位新用户注册，请及时处理`);
            let newUsers = users.concat( this.props.users );
            this.props.onUpdateNewUser(newUsers);
            this.io.emit("new-users", { data: {
                users
            }});
        });
    }

    render() {   
        return (
            <span className="notice" onClick={this.props.onClickNotice}>
                <img 
                    width={25}
                    alt="notice"
                    src={notice}
                />
                {this.props.users.length > 0? <span className="notice-count"/> : null }
            </span>
        );
    }
  }

  const mapStateToProps = (state, ownProps) => ({
        users: state.notice.newUsers,
        hasLogined: !!(state.account.user && state.account.user.email),
        user: state.account.user && state.account.user
  });
  
  const mapDispatchToProps = (dispatch, ownProps) => ({
    onClickNotice: () => {
        dispatch(showDrawer());
    },
    onUpdateNewUser: (users) => {
        dispatch(setNoticeUsers(users));
    }
  });

export default connect(mapStateToProps, mapDispatchToProps)(Notice);