
import React from 'react';
import { Form, Icon, Input, Button } from 'antd';
import { loginAccount, publishAdmin } from '../../actions';
import { ADMIN_FORM_TYPE } from "../../constants";
import {rule as passwordReg} from '../../utils/passwordRules';
import { connect } from 'react-redux';

import "./AdminForm.less";

class AdminForm extends React.Component {

    handleSubmit = e => {
        e.preventDefault();
        this.props.form.validateFields((err, values) => {
        if (!err) {
            if(this.props.type === ADMIN_FORM_TYPE.CREATE){
                this.props.publishAdmin(values);
                return;
            }
            this.props.loginAccount(values);
        }
        });
    };

    validateEmail = (rule, email) => {
        if(this.props.type === ADMIN_FORM_TYPE.LOGIN){
            return true;
        }
        let reg = /^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/;
        return reg.test(email);
    }

    validatePassword = (rule, passward) => {
        if(this.props.type === ADMIN_FORM_TYPE.LOGIN){
            return true;
        }
        return passwordReg.test(passward);
    }

    render() {
        const { getFieldDecorator } = this.props.form;
        return (
        <Form onSubmit={this.handleSubmit} className="admin-form">
            <Form.Item>
            {getFieldDecorator('email', {
                rules: [{ required: true, message: '请输入邮箱!' },
                {validator: this.validateEmail, message: "请输入正确的邮箱！"}],
            })(
                <Input
                type="email"
                prefix={<Icon type="user" style={{ color: 'rgba(0,0,0,.25)' }} />}
                placeholder="请输入邮箱"
                />,
            )}
            </Form.Item>
            <Form.Item>
            {getFieldDecorator('password', {
                rules: [{ 
                    required: true, 
                    message: '请输入密码!'
                },
                {
                    validator: this.validatePassword,
                    message: "密码为8~21位，至少包含一个大小字母，一个小写字母及一个特殊字符！"
                }],
            })(
                <Input
                prefix={<Icon type="lock" style={{ color: 'rgba(0,0,0,.25)' }} />}
                type="password"
                placeholder="请输入密码"
                />,
            )}
            </Form.Item>
            <Button type="primary" loading={this.props.loading} htmlType="submit" className="admin-form-button">{this.props.type === ADMIN_FORM_TYPE.CREATE?"注册":"登录"}
            </Button>
        </Form>
        );
    }
}

const WrappedNormalAdminForm = Form.create({ 
    mapPropsToFields(props) {
        return {};
    },
    })(AdminForm);



const mapStateToProps = (state, ownProps) => ({
    loading: state.ui.loading,
    type: state.ui.adminFormType
  });
  
const mapDispatchToProps = (dispatch, ownProps) => ({
    loginAccount: (user) => {
        dispatch(loginAccount(user));
    },
    publishAdmin: (user) => {
        dispatch(publishAdmin(user));
    }
  })
  
export default connect(mapStateToProps, mapDispatchToProps)(WrappedNormalAdminForm)
          