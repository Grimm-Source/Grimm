
import React from 'react';
import { showLogin, showResetPassword } from "../../actions";
import { Modal, Button } from 'antd';
import { connect } from 'react-redux';
import AdminForm from '../../components/AdminForm/AdminForm';

import './Login.less';
import Footer from "../../components/Footer";

class Login extends React.Component {

  handleForgotPassword = e => {
    this.props.forgotPassword();
  };

  render() {
    return (
      <Modal
        className="register-modal"
        title="登录"
        visible= {this.props.visible}
        destroyOnClose={true}
        closable={false}
        maskClosable={false}
        cancelButtonProps={{ disabled: true }}
        okButtonProps={{ disabled: true}}
        footer={<Footer color={'blank'} />}
      >
        <AdminForm />
        <Button type="link" className="admin-forget-button" onClick={this.handleForgotPassword}>{"忘记密码?"}</Button>
      </Modal>
    );
  }
}

const mapStateToProps = (state, ownProps) => ({
  user: state.account.user,
  loading: state.ui.loading,
  visible: (!state.account.user || !state.account.user.email) && !state.ui.isShowResetPassword
});

const mapDispatchToProps = (dispatch, ownProps) => ({
  forgotPassword: () => {
    dispatch(showResetPassword());
  }
})

export default connect(mapStateToProps, mapDispatchToProps)(Login)