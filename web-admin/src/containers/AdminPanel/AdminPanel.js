import React from 'react';
import AdminForm from '../../components/AdminForm/AdminForm';
import AdminList from '../../components/AdminList/AdminList';
import AdminDetail from '../../components/AdminDetail/AdminDetail';
import './AdminPanel.css';
import addIcon from '../../images/add.svg';
import removeIcon from '../../images/delete.svg';
import { removeAdmin, switchAdminPanel, switchAdminFormType} from '../../actions';
import { ADMIN_PANEL_TYPE, ADMIN_FORM_TYPE } from "../../constants";
import { message } from 'antd';
import { connect } from 'react-redux';

class AdminPanel extends React.Component {

  onClickRemove = (e) => {
    if(this.props.mode === ADMIN_PANEL_TYPE.ADD){
      return;
    }
    this.props.removeAdmin(this.props.admin);
  }

  getDetail = ()=>{
    switch(this.props.mode){
      case ADMIN_PANEL_TYPE.ADD: return <div className="admin-form-wrapper"><AdminForm/></div>;
      default: return <div className="admin-detail-wrapper"><AdminDetail/></div>
    }
  }

  render() {
    let detail = this.getDetail();
    return (
        <div className="admin-panel">
          <div className="admin-display">
            <AdminList/>
            <div className="admin-detail">{detail}</div>
          </div>
          <div className="admin-side-bar">
            <img
                className="admin-action-icon"
                width={50}
                alt="addUser"
                src={addIcon}
                onClick={this.props.onClickAdd}
            />
            {(this.props.admin && this.props.admin.type) === "root"? null:
            <img
                className="admin-action-icon"
                width={50}
                alt="deleteUser"
                src={removeIcon}
                onClick={this.onClickRemove}
            />}
          </div>
        </div>
    );
  }
}

const mapStateToProps = (state, ownProps) => ({
  mode: state.ui.adminPanelType,
  admin: state.ui.admin
});

const mapDispatchToProps = (dispatch, ownProps) => ({
  onClickAdd : () => {
    dispatch(switchAdminPanel(ADMIN_PANEL_TYPE.ADD));
    dispatch(switchAdminFormType(ADMIN_FORM_TYPE.CREATE));
  },
  removeAdmin: (admin)=>{
    if(admin.type === "root"){
      message.error("无法删除超级用户");
    }
    dispatch(removeAdmin(admin.id));
  }
})

export default connect(mapStateToProps, mapDispatchToProps)(AdminPanel)