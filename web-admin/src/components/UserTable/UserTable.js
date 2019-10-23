import { Table, Divider, Modal } from 'antd';
import React from 'react';
import { showUserDetail, hideUserDetail, updateUsers, setSelectedUsers } from '../../actions';
import UserDetail from '../UserDetail/UserDetail';
import { connect } from 'react-redux';
import {USER_LIST_TYPE, AUDIT_STATUS} from '../../constants';
import './UserTable.less';

class UserTable extends React.Component {
    render() {
        let isVolunteer = this.props.type === USER_LIST_TYPE.VOLUNTEER ;

        const columns = [
            {
            title: '姓名',
            dataIndex: 'name',
            render: (text, user) => (
              <span className="button" onClick={this.props.showUserDetail.bind(null, user)}>{text}</span>
              ),
            },
            {
            title: '身份证号',
            dataIndex: 'idcard',
            key: 'idcard'
            },
            {
            title: '残疾人证',
            dataIndex: 'disabledID',
            key: 'disabledID',
            className: 'disabled-id'
            },
            {
            title: '性别',
            dataIndex: 'gender',
            key: 'gender'
            },
            {
            title: '注册手机',
            dataIndex: 'tel',
            key: 'tel',
            },
            {
            title: '联系地址',
            dataIndex: 'linkaddress',
            key: 'linkaddress',
            },
            {
            title: '注册时间',
            dataIndex: 'registrationDate',
            key: 'registrationDate',
            },
            {
            title: '操作',
            key: 'action',
            render: (text, user) => (
                  user.audit_status !== "pending"? AUDIT_STATUS[user.audit_status]:
                  <span>
                    <span className="action-button" onClick={this.props.onClickApprove.bind(null, user, isVolunteer)}>同意</span>
                    <Divider type="vertical" />
                    <span className="action-button danger" onClick={this.props.onClickReject.bind(null, user, isVolunteer)}>拒绝</span>
                  </span> 
            )
            }
        ];

        const rowSelection = {
            onChange: (selectedRowKeys, selectedRows) => {
              this.props.updateSelectedUsers(selectedRows);
            }
        };

        return (<div className="user-table-wrapper" >
                  <Table  rowKey={item => item.openid} loading={this.props.loading} className={`user-table ${isVolunteer? "volunteer-table":"disabled-table"}`} rowSelection={rowSelection} columns={columns} dataSource={this.props.users} />
                  <Modal className="user-detail-modal"
                    title={this.props.user.name}
                    visible={this.props.isUserDetailVisible}
                    destroyOnClose={true}
                    onCancel = {this.props.hideUserDetail}
                    maskClosable={true}
                    cancelButtonProps={{ disabled: true }}
                    okButtonProps={{ disabled: true }}
                    ><UserDetail/>
                  </Modal>
                </div>
        );
    }
}

const mapStateToProps = (state, ownProps) => ({
  loading: state.ui.loading,
  isUserDetailVisible: state.ui.isShowUserDetail,
  user: state.ui.user,
  type: state.ui.userListType,
  users: state.user.users
});

const mapDispatchToProps = (dispatch, ownProps) => ({
  onClickReject : (user, isVolunteer) => {
    dispatch(updateUsers([{
      openid: user.openid,
      audit_status: "rejected"
    }],
    isVolunteer));
  },
  onClickApprove: (user, isVolunteer)=>{
    dispatch(updateUsers([{
      openid: user.openid,
      audit_status: "approved"
    }],
    isVolunteer));
  },
  showUserDetail: (user) => {
    dispatch(showUserDetail(user));
  },
  hideUserDetail: () => {
    dispatch(hideUserDetail());
  },
  updateSelectedUsers: (users) => {
    dispatch(setSelectedUsers(users));
  }
})

export default connect(mapStateToProps, mapDispatchToProps)(UserTable)