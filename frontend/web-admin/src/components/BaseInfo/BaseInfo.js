import React from 'react';
import { Form } from 'antd';
import { connect } from 'react-redux';

class BaseInfo extends React.Component {
    render(){
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
        return(
            <div className="base-info">
                <Form {...formItemLayout}>
                    <Form.Item label="邮箱">
                        {this.props.user.email}
                    </Form.Item>
                    <Form.Item label="用户类型">
                        {this.props.user.type==="root"?"超级用户":"普通用户"}
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
})

export default connect(mapStateToProps, mapDispatchToProps)(BaseInfo)