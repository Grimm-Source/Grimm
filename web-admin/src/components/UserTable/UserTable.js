import { Table, Divider, Modal } from 'antd';
import React from 'react';
import { showUserDetail, hideUserDetail, getVolunteerList } from '../../actions';
import UserDetail from '../UserDetail/UserDetail';
import { connect } from 'react-redux';
import './UserTable.css';


class UserTable extends React.Component {
    componentDidMount(){
        this.props.getVolunteerList();
    }
  
    render() {
        const columns = [
            {
            title: '姓名',
            dataIndex: 'name',
            render: (text, user) => (
              <a onClick={this.props.showUserDetail.bind(null, user)}>{text}</a>
              ),//pop up detail
            },
            {
            title: '身份证号',
            dataIndex: 'idCard',
            key: 'idCard'
            },
            {
            title: '性别',
            dataIndex: 'gender',
            key: 'gender'
            },
            {
            title: '手机',
            dataIndex: 'tel',
            key: 'tel',
            },
            {
            title: '联系地址',
            dataIndex: 'linkAddress',
            key: 'linkAddress',
            },
            {
            title: '注册时间',
            dataIndex: 'registerDate',
            key: 'registerDate',
            },
            {
            title: '操作',
            key: 'action',
            render: (text, user) => (
                <span>
                    <span className="action-button" onClick={this.props.onClickApprove.bind(null, user)}>同意</span>
                    <Divider type="vertical" />
                    <span className="action-button danger" onClick={this.props.onClickDeny.bind(null, user)}>拒绝</span>
                </span>
            )
            }
        ];

        const rowSelection = {
            onChange: (selectedRowKeys, selectedRows) => {
              console.log(`selectedRowKeys: ${selectedRowKeys}`, 'selectedRows: ', selectedRows);
            }
        };

        return (<div className="user-table-wrapper" >
                  <Table className="user-table" rowSelection={rowSelection} columns={columns} dataSource={this.props.users} />
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
  // users: state.user.users
  users: [{
    name: "打马话",
    idCard: "310111111111111111",
    linkAddress: "上海市人民广场",
    registerDate: "2019-01-21",
    linkTel: "13811111111",
    tel: "13811111111",
    gender: "女",
    id: 1,
    key: 1
  },{
    name: "大佬住",
    idCard: "310222222222222222",
    linkAddress: "上海市人民广场",
    registerDate: "2019-01-21",
    linkTel: "19811111111",
    tel: "19811111111",
    gender: "女",
    id: 2,
    key: 2
  },{
    name: "寄卖",
    idCard: "310333333333333333",
    linkAddress: "上海市人民广场",
    registerDate: "2019-01-21",
    linkTel: "15511111111",
    tel: "15511111111",
    gender: "男",
    id: 3,
    key: 3
  }]
});

const mapDispatchToProps = (dispatch, ownProps) => ({
  onClickDeny : (user) => {
    // dispatch(denyUser(user.id));
  },
  onClickApprove: (user)=>{
    // dispatch(approveUser(user.id));
  },
  getVolunteerList : () => {
    // dispatch(getVolunteerList());
  },
  showUserDetail: (user) => {
    dispatch(showUserDetail(user));
  },
  hideUserDetail: () => {
    dispatch(hideUserDetail());
  }
})

export default connect(mapStateToProps, mapDispatchToProps)(UserTable)