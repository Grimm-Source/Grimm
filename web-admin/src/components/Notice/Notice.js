import React from 'react';
import { showDrawer, setNoticeUsers} from '../../actions';
import notice from '../../images/notice.svg';
import { connect } from 'react-redux';
import { socketHelper } from '../../utils/socketHelper.js';
import { storage } from '../../utils/localStorageHelper.js';

import './Notice.less';

class Notice extends React.Component {

    constructor(props) {
        super(props);
        this.io = null;
    }

    componentWillReceiveProps(nextProps, prevState){
        if(!this.io && nextProps.hasLogined){
            let io = socketHelper.getNewUsersSockect();
            io.on('new-users', function (data) {
                if( !data.users || data.users.length === 0 ){
                    return;
                }
                let users = data.users;//received users
                let newUsers = users.concat( this.props.users );

                storage.setItem("notice-new-users", newUsers);
                this.props.onUpdateNewUser(newUsers);

                io.emit("new-users", { data: {
                    users
                }});
            });
        }
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
        hasLogined: state.account.user && state.account.user.id
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