import React from 'react';
import { connect } from 'react-redux';
import { Form, Input, Button } from 'antd';
import { changePassword } from '../../actions';

class ChangePassword extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            confirmDirty: false
        }
    }

    handleConfirmBlur = e => {
        const { value } = e.target;
        this.setState({ confirmDirty: this.state.confirmDirty || !!value });
    };

    validatePasswordFormat = (rule, value, callback) => {
        const { form } = this.props;
        let reg = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{8,21}/;
        if (value && !reg.test(value)) {
            callback('密码为8~21位，至少包含一个大小字母，一个小写字母及一个特殊字符!');
        }else if (value && this.state.confirmDirty) {
            form.validateFields(['confirmPassword'], { force: true });
        }
        callback();
    };

    compareToFirstPassword = (rule, value, callback) => {
        const { form } = this.props;
        if (value && value !== form.getFieldValue('newPassword')) {
          callback('两次密码输入不一致!');
        } else {
          callback();
        }
    };

    handleChangePassword = e => {
        e.preventDefault();
        const { user } = this.props
        this.props.form.validateFieldsAndScroll((err, values) => {
            if (!err) {
                this.props.changePassword(user.id, values.oldPassword, values.newPassword);
                console.log('Received values of form: ', values);
            }
        });
    }

    render(){
        const { getFieldDecorator } = this.props.form;
        const formItemLayout = {
            labelCol: {
                xs: { span: 24 },
                sm: { span: 6 },
            },
            wrapperCol: {
                xs: { span: 24 },
                sm: { 
                    span: 14,
                    offset: 4
                 },
            },
        };
        const tailFormItemLayout = {
            wrapperCol: {
              xs: {
                span: 24,
                offset: 0,
              },
              sm: {
                span: 16,
                offset: 10,
              },
            },
        };
        return(
            <div className="change-password">
                <Form {...formItemLayout} onSubmit={this.handleChangePassword}>
                    <Form.Item label="旧密码">
                        {getFieldDecorator('oldPassword', {
                            rules: [
                                {
                                  required: true,
                                  message: '请输入旧密码!',
                                }
                              ],
                            })(<Input.Password />)}
                    </Form.Item>
                    <Form.Item label="新密码" hasFeedback>
                        {getFieldDecorator('newPassword', {
                            rules: [
                            {
                                required: true,
                                message: '请输入新密码!',
                            },
                            {
                                validator: this.validatePasswordFormat,
                            },
                            ],
                        })(<Input.Password />)}
                    </Form.Item>
                    <Form.Item label="确认密码" hasFeedback>
                        {getFieldDecorator('confirmPassword', {
                            rules: [
                            {
                                required: true,
                                message: '请再次输入新密码!',
                            },
                            {
                                validator: this.compareToFirstPassword,
                            },
                            ],
                        })(<Input.Password onBlur={this.handleConfirmBlur} />)}
                    </Form.Item>
                    <Form.Item {...tailFormItemLayout}>
                        <Button type="primary" htmlType="submit">
                            修改
                        </Button>
                    </Form.Item>
                </Form>
            </div>
        )
    }
}

const mapStateToProps = (state, ownProps) => ({
    user: state.account.user
})

const mapDispatchToProps = (dispatch, ownProps) => ({
    changePassword: (adminId, oldVal, newVal) => {
        dispatch(changePassword(adminId, oldVal, newVal))
    }
})

const changePasswordForm = Form.create()(ChangePassword);

export default connect(mapStateToProps, mapDispatchToProps)(changePasswordForm)