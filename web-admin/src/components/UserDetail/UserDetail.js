import { Form } from 'antd';
import React from 'react';
import { connect } from 'react-redux';
import { AUDIT_STATUS } from '../../constants';
import './UserDetail.less'

class UserDetail extends React.Component {
  render() {
    const formItemLayout = {
        labelCol: {
          xs: { span: 24 },
          sm: { span: 6 },
        },
        wrapperCol: {
          xs: { span: 24 },
          sm: { span: 18 },
        },
      };

    return (
        <Form className="user-detail" {...formItemLayout}>
            <Form.Item label="状态">{AUDIT_STATUS[this.props.user.audit_status] || "未知状态"}</Form.Item>
            <Form.Item label="身份证">{this.props.user.idcard}</Form.Item>
            {this.props.user.role === "志愿者"?null:<Form.Item label="残疾人证">{this.props.user.disabledID}</Form.Item>}
            <Form.Item label="注册手机">{this.props.user.tel}</Form.Item>
            <Form.Item label="联系电话">{this.props.user.linktel}</Form.Item>
            <Form.Item label="联系地址">{this.props.user.linkaddress}</Form.Item>
            <Form.Item label="性别">{this.props.user.gender}</Form.Item>
            <Form.Item label="生日">{this.props.user.birthdate}</Form.Item>
            <Form.Item label="注册时间">{this.props.user.registrationDate}</Form.Item>
            <Form.Item label="紧急联系人">{this.props.user.emergencyPerson}</Form.Item>
            <Form.Item label="紧急联系电话">{this.props.user.emergencyTel}</Form.Item>
            <Form.Item label="备注">{this.props.user.comment}</Form.Item>
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

