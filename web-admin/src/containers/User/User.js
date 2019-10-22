import React from 'react';
import { Button, Switch } from 'antd';
import { connect } from 'react-redux';
import refresh from '../../images/refresh.svg';
import TableHeader from '../../components/TableHeader/TableHeader';
import UserTable from '../../components/UserTable/UserTable';
import { switchUserList, getVolunteerList, getDisabledList, updateUsers } from '../../actions';
import {USER_LIST_TYPE} from '../../constants';

import './User.less';

class User extends React.Component {  
  
  componentDidMount(){
    this.props.refreshTable(this.props.isVolunteer);
  }

  render() {  
    let isVolunteer = this.props.isVolunteer ;
    return (
        <div className="user">
            <TableHeader right={<span>
                      <Button loading={this.props.loading} onClick={this.props.onClickAuditAction.bind(null, this.props.selectedUsers, isVolunteer, "approved")}>同意</Button>
                      <Button loading={this.props.loading} onClick={this.props.onClickAuditAction.bind(null, this.props.selectedUsers, isVolunteer, "rejected")} type="danger">拒绝</Button>
                      <img 
                        width={25}
                        alt="refresh"
                        src={refresh}
                        onClick = {this.props.refreshTable.bind(null, isVolunteer, this.props.loading)}
                      />
                      </span>}
                      
                      left={<span>
                        <Switch loading={this.props.loading} checkedChildren="志愿者" unCheckedChildren="视障人士" checked={isVolunteer} onChange={this.props.onChangeType.bind(null, isVolunteer)}/>
                        </span>}/>
            <UserTable/>
        </div>
    );
  }
}

const mapStateToProps = (state, ownProps) => ({
  loading: state.ui.loading,
  type: state.ui.userListType,
  isVolunteer: state.ui.userListType === USER_LIST_TYPE.VOLUNTEER,
  selectedUsers: state.ui.selectedUsers
});

const mapDispatchToProps = (dispatch, ownProps) => ({
  onClickAuditAction : (users, isVolunteer, audit_status) => {
    if( !users || users.length === 0){
      return;
    }
    let selectedUsers = [];
    users.forEach((user)=>{
      selectedUsers.push({
        openid: user.openid,
        audit_status
      });
    });
    dispatch(updateUsers(selectedUsers,
    isVolunteer));
  },
  onChangeType: (isVolunteer) => {
    dispatch(switchUserList());
    if(!isVolunteer){
      dispatch(getVolunteerList());
    }else{
      dispatch(getDisabledList());
    }
  },
  refreshTable: (isVolunteer, isLoading)=>{
    if(isLoading){
      return;
    }
    if(isVolunteer){
      dispatch(getVolunteerList());
    }else{
      dispatch(getDisabledList());
    }
  }
})

export default connect(mapStateToProps, mapDispatchToProps)(User)