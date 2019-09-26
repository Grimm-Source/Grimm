import { Form } from 'antd';
import React from 'react';
import { } from '../../actions';
import { connect } from 'react-redux';
import './UserDetail.css'

class UserDetail extends React.Component {
  render() {
    const formItemLayout = {
        labelCol: {
          xs: { span: 24 },
          sm: { span: 4 },
        },
        wrapperCol: {
          xs: { span: 24 },
          sm: { span: 20 },
        },
      };

    return (
        <Form className="user-detail" {...formItemLayout}>
            <Form.Item label="身份证">{this.props.user.idCard}</Form.Item>
            <Form.Item label="手机号">{this.props.user.tel}</Form.Item>
            <Form.Item label="联系电话">{this.props.user.linkTel}</Form.Item>
            <Form.Item label="联系地址">{this.props.user.linkAddress}</Form.Item>
            <Form.Item label="性别">{this.props.user.gender}</Form.Item>
            <Form.Item label="生日">{this.props.user.birthday}</Form.Item>
            <Form.Item label="注册时间">{this.props.user.registerDate}</Form.Item>
            <Form.Item label="状态">{this.props.user.state}</Form.Item>
            <Form.Item label="审批时间">{this.props.user.operationDate}</Form.Item>
            <Form.Item label="审批人">{this.props.user.operationAdmin}</Form.Item>
        </Form>
    );
  }
}

const mapStateToProps = (state, ownProps) => ({
    loading: state.ui.loading,
    user: state.ui.user
});

const mapDispatchToProps = (dispatch, ownProps) => ({

})

export default connect(mapStateToProps, mapDispatchToProps)(UserDetail)

