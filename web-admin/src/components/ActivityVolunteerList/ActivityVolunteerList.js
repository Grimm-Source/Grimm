import React from 'react';
import { Button, Select } from 'antd';
import { connect } from 'react-redux';
import TableHeader from '../../components/TableHeader/TableHeader';
import UserTable from '../../components/UserTable/UserTable';
import { switchUserList, getVolunteerList, getDisabledList, updateUsers } from '../../actions';
import {USER_LIST_TYPE} from '../../constants';

import './ActivityVolunteerList.less';

const { Option } = Select;

class ActivityVolunteerList extends React.Component {  
  componentDidMount(){
    this.props.refreshTable(this.props.isVolunteer);
  }

  onChange = (value)=>{
    this.props.onChangeType(value==="volunteers");
  }

  render() {  
    let isVolunteer = this.props.isVolunteer ;
    return (
        <div className="activity-volunteer">
            <TableHeader right={<span>
                      <Button disabled={this.props.loading} onClick={this.props.onClickAuditAction.bind(null, this.props.selectedUsers, isVolunteer, "approved")} type="primary">同意</Button>
                      <Button disabled={this.props.loading} onClick={this.props.onClickAuditAction.bind(null, this.props.selectedUsers, isVolunteer, "rejected")} type="danger">拒绝</Button>
                      </span>}
                      
                      left={<span>
                        <Select defaultValue={this.props.isVolunteer?"volunteers":"disabled"} style={{ width: 120 }}  onChange={this.onChange}>
                          <Option value="volunteers">志愿者</Option>
                        </Select>
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
    if(isVolunteer){
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

export default connect(mapStateToProps, mapDispatchToProps)(ActivityVolunteerList)