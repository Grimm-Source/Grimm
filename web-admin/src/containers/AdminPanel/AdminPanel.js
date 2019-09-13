import React from 'react';
import AdminForm from '../../components/AdminForm/AdminForm';
import AdminList from '../../components/AdminList/AdminList';
import AdminDetail from '../../components/AdminDetail/AdminDetail';
import './AdminPanel.css';
import addIcon from './add.svg';
import removeIcon from './delete.svg';
import { removeAdmin, switchAdminPanel, switchAdminFormType} from '../../actions';
import { ADMIN_PANEL_TYPE, ADMIN_FORM_TYPE } from "../../constants";
import { connect } from 'react-redux';

class AdminPanel extends React.Component {

  onClickRemove = (e) => {
    if(this.props.mode === ADMIN_PANEL_TYPE.ADD){
      return;
    }
    this.props.removeAdmin(this.props.adminId);
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
            <img
                className="admin-action-icon"
                width={50}
                alt="deleteUser"
                src={removeIcon}
                onClick={this.onClickRemove}
            />
          </div>
        </div>
    );
  }
}

const mapStateToProps = (state, ownProps) => ({
  mode: state.ui.adminPanelType,
  adminId: state.ui.admin && state.ui.admin.id
});

const mapDispatchToProps = (dispatch, ownProps) => ({
  onClickAdd : () => {
    dispatch(switchAdminPanel(ADMIN_PANEL_TYPE.ADD));
    dispatch(switchAdminFormType(ADMIN_FORM_TYPE.CREATE));
  },
  removeAdmin: (adminId)=>{
    dispatch(removeAdmin(adminId));
  }
})

export default connect(mapStateToProps, mapDispatchToProps)(AdminPanel)