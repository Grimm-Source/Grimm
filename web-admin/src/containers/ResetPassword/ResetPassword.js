import React from 'react';
import { connect } from 'react-redux';
import {Modal, Form, Input, Icon, Button } from 'antd';
import {resetPassword, hideResetPassword} from '../../actions/index'

import './ResetPassword.less';


class ForgotPassword extends React.Component {
    handleResetPassword = e => {
        e.preventDefault();
        this.props.form.validateFields((error, values) => {
            if (!error) {
                this.props.resetPassword(values.email);
            } 
        })
    };

    handleCancel = e => {
        e.preventDefault();
        this.props.cancelRestPassword();
    }

    validateEmail = (rule, email) => {
        let reg = /^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/;
        return reg.test(email);
    }

    render() {
        const { getFieldDecorator } = this.props.form;
        return (
            <Modal
            className="reset-modal"
            title= "找回密码"
            visible= {this.props.visible}
            destroyOnClose={true}
            closable={true}
            maskClosable={true}
            cancelButtonProps={{ disabled: true }}
            okButtonProps={{ disabled: true}}
            onCancel = {this.handleCancel}
          >
            <Form className='reset-form'>
                <Form.Item>
                    <h2 className="reset-description">新的密码将会发送至您的注册邮箱</h2>
                </Form.Item>
                <Form.Item>
                    {getFieldDecorator('email', {
                        rules: [{ required: true, message: "请输入邮箱" },
                        { validator: this.validateEmail, message: "请输入正确的邮箱！" }],
                    })(
                        <Input
                            type="email"
                            prefix={<Icon type="user" style={{ color: 'rgba(0,0,0,.25)' }} />}
                            placeholder="请输入邮箱"
                        />,
                    )}
                </Form.Item>
                <Form.Item >
                    <Button type="primary" htmlType="submit" className="forgot-password-button" onClick={this.handleResetPassword}>下一步</Button>
                </Form.Item>
            </Form>
          </Modal>
        )
    }
}

const mapStateToProps = (state, ownProps) => ({
    visible: state.ui.isShowResetPassword,
});

const mapDispatchToProps = (dispatch, ownProps) => ({
    resetPassword: (accountId) => {
       dispatch(resetPassword(accountId));
    },
    cancelRestPassword: () => {
        dispatch(hideResetPassword());
    }
})

const forgotPasswordForm = Form.create()(ForgotPassword);

export default connect(mapStateToProps, mapDispatchToProps)(forgotPasswordForm)
