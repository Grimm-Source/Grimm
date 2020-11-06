import React from 'react';
import { Button, Select, Table, Divider} from 'antd';
import { connect } from 'react-redux';
import TableHeader from '../TableHeader/TableHeader';
import { switchUserList, getRegisteredVolunteers, getDisabledList} from '../../actions';
import {USER_LIST_TYPE} from '../../constants';

import './ActivityRegistrationList.less';

const { Option } = Select;

class ActivityRegistrationList extends React.Component {  
  componentDidMount(){
    if(!this.props.activityId){
      return;
    }

    this.props.refreshTable(this.props.activityId, this.props.isVolunteer);
  }

  onChange = (value)=>{
    this.props.onChangeType(this.props.activityId, value==="volunteers");
  }

  onClickDownload = () => {
    if(this.props.loading){
      return;
    }

    const header = "\ufeff"+"姓名,身份类型,注册手机,联系地址,需要接送,愿意接送\n";
    const rows = [];
    this.props.volunteers.forEach(function(item) {
          rows.push(item.name + ',' + (item.role==="0"?"志愿者":"视障人士")
          +',' + item.phone + ',' + item.address + ',' 
          + (item.needpickup?"是":"否") +',' 
          + (item.topickup?"是": "否"));
        })
    const csvString = header + rows.join('\n');
    const link = window.document.createElement('a');
    document.body.appendChild(link);
    link.href = window.URL.createObjectURL(new Blob([csvString], { type: "text/plain;charset=utf-8" }));
    link.download = '活动名单.csv';
    link.click();
    document.body.removeChild(link);
  }

  render() {  
    let isVolunteer = this.props.isVolunteer ;
      const columns = [
        {
          title: '姓名',
          dataIndex: 'name',
          key: 'name',
        },
        {
          title: '身份类型',
          dataIndex: 'role',
          render: (role) => {
            return role === 0 ? '志愿者' : '视障人士'
          }
        },
        {
          title: '注册手机',
          dataIndex: 'phone',
          key: 'phone',
        },
        {
          title: '联系地址',
          dataIndex: 'address',
          key: 'address',
        },
        {
          title: '需要接送',
          dataIndex: 'needpickup',
          render: (needpickup) => {
            return needpickup === 1 ? '是' : '否'
          }
        },
        {
          title: '愿意接送',
          dataIndex: 'topickup',
          render: (topickup) => {
            return topickup === 1 ? '是' : '否'
          }
        },
        // {
        //   title: '操作',
        //   key: 'action',
        //   render: (text, user) => (
        //         user.accepted !== "pending"? AUDIT_STATUS[user.audit_status]:
        //         <span>
        //           <span className="action-button" onClick={this.props.onClickApprove.bind(null, user, isVolunteer)}>同意</span>
        //           <Divider type="vertical" />
        //           <span className="action-button danger" onClick={this.props.onClickReject.bind(null, user, isVolunteer)}>拒绝</span>
        //         </span> 
        //   )
        // }
    ];

    // const rowSelection = {
    //     onChange: (selectedRowKeys, selectedRows) => {
    //       this.props.updateSelectedUsers(selectedRows);
    //     }
    // };

    return (<div className="activity-registration" >
              {/* <TableHeader 
                right={<span>
                      <Button disabled={this.props.loading} onClick={this.props.onClickAuditAction.bind(null, this.props.selectedUsers, isVolunteer, "approved")} type="primary">同意</Button>
                      <Button disabled={this.props.loading} onClick={this.props.onClickAuditAction.bind(null, this.props.selectedUsers, isVolunteer, "rejected")} type="danger">拒绝</Button>
                </span>}
                      
                left={<span>
                        <Select defaultValue={this.props.isVolunteer?"volunteers":"disabled"} style={{ width: 120 }}  onChange={this.onChange}>
                          <Option value="volunteers">志愿者</Option>
                        </Select>
                </span>}
              /> */}
              <Table rowKey={item => item.openid} loading={this.props.loading} size="small" columns={columns} dataSource={this.props.volunteers} 
                  footer={() => <Button type="link" onClick={this.onClickDownload}>下载名单</Button>}
                  pagination={{  
                    pageSize: this.props.activityId? 10:15,
                    showTotal: (total, range) => this.props.activityId?<span>{`${range[0]}-${range[1]}项，共${total}项`}</span>:<span style={{color:"white"}}>{`${range[0]}-${range[1]}项，共${total}项`}</span>
                  }}
              />
            </div>
    );
  }
}

const mapStateToProps = (state, ownProps) => ({
  loading: state.ui.loading,
  activityId: state.ui.activityId,
  type: state.ui.userListType,
  isVolunteer: state.ui.userListType === USER_LIST_TYPE.VOLUNTEER,
  volunteers: state.activity.volunteers,
});

const mapDispatchToProps = (dispatch, ownProps) => ({
  // onClickReject : (user, isVolunteer) => {
  //   dispatch(updateUsers([{
  //     openid: user.openid,
  //     audit_status: "rejected"
  //   }],
  //   isVolunteer));
  // },

  // onClickApprove: (user, isVolunteer)=>{
  //   dispatch(updateUsers([{
  //     openid: user.openid,
  //     audit_status: "approved"
  //   }],
  //   isVolunteer));
  // },

  // onClickAuditAction : (users, isVolunteer, audit_status) => {
  //   if( !users || users.length === 0){
  //     return;
  //   }
  //   let selectedUsers = [];
  //   users.forEach((user)=>{
  //     selectedUsers.push({
  //       openid: user.openid,
  //       audit_status
  //     });
  //   });
  //   dispatch(updateUsers(selectedUsers, isVolunteer));
  // },

  onChangeType: (activityId, isVolunteer) => {
    dispatch(switchUserList());
    if(isVolunteer){
      dispatch(getRegisteredVolunteers(activityId));
    }else{
      // TODO: dispatch to get registeredDisabled
    }
  },

  refreshTable: (activityId, isVolunteer, isLoading)=>{
    if(isLoading){
      return;
    }
    if(isVolunteer){
      dispatch(getRegisteredVolunteers(activityId));
    }else{
      // TODO: dispatch to get registeredDisabled
    }
  }
})

export default connect(mapStateToProps, mapDispatchToProps)(ActivityRegistrationList)