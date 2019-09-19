
import React from 'react';
import { Form, Icon, Input, Button } from 'antd';
import { loginAccount, publishAdmin } from '../../actions';
import { ADMIN_FORM_TYPE } from "../../constants";
import { connect } from 'react-redux';
import "./AdminForm.css";

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

    validatePassword = (rule, passward) => {
        if(this.props.type === ADMIN_FORM_TYPE.LOGIN){
            return true;
        }
        return passward.length >= 6 && passward.length <= 20;
    }

    render() {
        const { getFieldDecorator } = this.props.form;
        return (
        <Form onSubmit={this.handleSubmit} className="admin-form">
            <Form.Item>
            {getFieldDecorator('email', {
                rules: [{ required: true, message: '请输入邮箱!' }],
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
                    message: "密码为6~20位!"
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
          