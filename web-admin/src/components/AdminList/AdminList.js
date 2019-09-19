import { List, Skeleton } from 'antd';
import React from 'react';
import { getAdminList, getAdmin, removeAdmin, switchAdminPanel} from '../../actions';
import { ADMIN_PANEL_TYPE } from "../../constants";
import { connect } from 'react-redux';
import './AdminList.css';

class AdminList extends React.Component {
  componentDidMount(){
    this.props.getAdminList();
  }

  render() {
    return (
            <List
                className="admin-list"
                loading={this.props.loading}
                itemLayout="horizontal"
                dataSource={this.props.admins}
                renderItem={item => (
                <List.Item
                    actions={[<span key="delete"  style={{display: (item.type==="root") ? "none" : "inline-block"}} className="list-item-button" onClick={this.props.onClickRemoveAdmin.bind(this, item)}>删除</span>]}
                    onClick={this.props.onClickAdmin.bind(this, item)}
                >
                    <Skeleton title={false} loading={this.props.loading} active>
                    <List.Item.Meta
                        title={<span className="admin-name">{item.email}</span>}
                    />
                    </Skeleton>
                </List.Item>
                )}
            />
    );
  }
}

const mapStateToProps = (state, ownProps) => ({
  admins: state.admin.admins,
  loading: state.ui.loading
});

const mapDispatchToProps = (dispatch, ownProps) => ({
  onClickAdmin : (adminInfo) => {
    dispatch(switchAdminPanel(ADMIN_PANEL_TYPE.DETAIL));
    dispatch(getAdmin(adminInfo.id));
  },
  onClickRemoveAdmin: (adminInfo)=>{
    dispatch(removeAdmin(adminInfo.id));
  },
  getAdminList : () => {
    dispatch(getAdminList());
  }
})

export default connect(mapStateToProps, mapDispatchToProps)(AdminList)