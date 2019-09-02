
import React from 'react';
import { Modal } from 'antd';
import { loginAccount } from '../../actions';
import { connect } from 'react-redux';
import AdminForm from '../../components/AdminForm/AdminForm';

import './Login.css';

class Login extends React.Component {  

  render() {
    return (
        <Modal
          className="register-modal"
          title="登录"
          visible={!this.props.user ||!this.props.user.username}
          destroyOnClose={true}
          closable={false}
          maskClosable={false}
          cancelButtonProps={{ disabled: true }}
          okButtonProps={{ disabled: true }}
        >
          <AdminForm/>
        </Modal>
    );
  }
}

const mapStateToProps = (state, ownProps) => ({
  user: state.account.user,
  loading: state.ui.loading
});

export default connect(mapStateToProps)(Login)