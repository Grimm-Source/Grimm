import React from 'react';
import AdminForm from '../../components/AdminForm/AdminForm';
import AdminList from '../../components/AdminList/AdminList';
import AdminDetail from '../../components/AdminDetail/AdminDetail';
import './AdminPanel.css';
import addIcon from './add.svg';
import removeIcon from './delete.svg';
import { removeAdmin, switchAdminPanel, switchAdminFormType} from '../../actions';
import { connect } from 'react-redux';

class AdminPanel extends React.Component {

  onClickRemoveAdmin = (e) => {
    if(this.props.mode === "add"){
      return;
    }
    this.props.removeAdmin(this.props.adminId);
  }

  getDetail = ()=>{
    switch(this.props.mode){
      case "add": return <div className="admin-form-wrapper"><AdminForm type="create"/></div>;
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
                onClick={this.props.onClickRemove}
            />
          </div>
        </div>
    );
  }
}

const mapStateToProps = (state, ownProps) => ({
  mode: state.ui.activeAdminKey,
  adminId: state.ui.admin && state.ui.admin.id
});

const mapDispatchToProps = (dispatch, ownProps) => ({
  onClickAdd : () => {
    dispatch(switchAdminPanel("add"));
    dispatch(switchAdminFormType("create"));
  },
  removeAdmin: (adminId)=>{
    dispatch(removeAdmin(adminId));
  }
})

export default connect(mapStateToProps, mapDispatchToProps)(AdminPanel)