import { Form, DatePicker, Input, Button, Spin } from 'antd';
import moment from 'moment';
import React from 'react';
import { hideActivityModal, getActivity, publishActivity} from '../../actions';
import { connect } from 'react-redux';

import './ActivityDetail.less';

class ActivityDetail extends React.Component {

  componentDidMount(){
    if(!this.props.activityId){
      return;
    }
    this.props.getActivity(this.props.activityId);
  }

  handleSubmit = e => {
    e.preventDefault();
    this.props.form.validateFields((err, fieldsValue) => {
      if (err) {
        return;
      }
      
      const values = {
        ...fieldsValue,
        date: fieldsValue['date'].format('YYYY-MM-DD HH:mm:ss'),
        id: this.props.activity.id,
        adminId: this.props.userId
      };
      this.props.publishActivity(values);
      this.props.hideActivityModal();
    });
  };

  render() {
    const { getFieldDecorator } = this.props.form;
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
      
       this.props.loading? <Spin size="large" />: <Form {...formItemLayout} onSubmit={this.handleSubmit}>
       <Form.Item label="活动时间">
         {getFieldDecorator('date', {
               rules: [
                   { 
                       type: 'object', 
                       required: true, 
                       message: '请选择时间' 
                   }],
               })(<DatePicker showTime format="YYYY-MM-DD HH:mm:ss" placeholder="请选择活动时间"/>,
         )}
       </Form.Item>
       <Form.Item label="活动主题">
           {getFieldDecorator('title', {
             initialValue: this.props.activity.title,
             rules: [
               {
                 required: true,
                 message: '请输入活动主题',
               },
             ],
           })(<Input placeholder="请输入活动主题" />)}
       </Form.Item>
       <Form.Item label="活动地点">
           {getFieldDecorator('location', {
             rules: [
               {
                 required: true,
                 message: '请输入活动地点',
               },
             ],
           })(<Input placeholder="请输入活动地点" />)}
       </Form.Item>
       <Form.Item label="活动持续时间">
           {getFieldDecorator('duration', {
             rules: [
               {
                 required: true,
                 message: '请输入活动持续时间',
               },
             ],
           })(<Input placeholder="请输入活动持续时间" />)}
       </Form.Item>
       <Form.Item label="活动内容">
           {getFieldDecorator('content', {
             rules: [
               {
                 required: true,
                 message: '请输入活动内容',
               },
             ],
           })(<Input.TextArea placeholder="请输入活动内容" />)}
       </Form.Item>
       <Form.Item label="活动注意事项">
           {getFieldDecorator('notice', )(<Input placeholder="请输入活动注意事项" />)}
       </Form.Item>
       <Form.Item label="其它">
           {getFieldDecorator('others', )(<Input placeholder="请输入其它事项" />)}
       </Form.Item>
       <Form.Item
         wrapperCol={{
           xs: { span: 24, offset: 0 },
           sm: { span: 16, offset: 8 },
         }}
       >
         <Button type="primary" htmlType="submit">
           发布
         </Button>
       </Form.Item>
     </Form>
    );
  }
}

const WrappedActivityDetail = Form.create({ 
    mapPropsToFields(props) {
      if(!props.activity){
        return {};
      }
      return {
        title: Form.createFormField({
          value: props.activity.title || ""
        }),
        content: Form.createFormField({
          value: props.activity.content || ""
        }),
        location: Form.createFormField({
          value: props.activity.location || ""
        }),
        notice: Form.createFormField({
          value: props.activity.notice || ""
        }),
        others: Form.createFormField({
          value: props.activity.others || ""
        }),
        duration: Form.createFormField({
          value: props.activity.duration || ""
        }),
        date: Form.createFormField({
          value: (props.activity.date && moment(props.activity.date, 'YYYY-MM-DD HH:mm:ss')) || null
        })
      }
    },
    })(ActivityDetail);

const mapStateToProps = (state) => ({
  activityId: state.ui.activityId,
  activity: state.ui.activity,
  loading: state.ui.loading,
  userId: state.account.user && state.account.user.id
})

const mapDispatchToProps = (dispatch) => ({
  hideActivityModal : () => {
    dispatch(hideActivityModal());
  },
  getActivity : (activityId) => {
    dispatch(getActivity(activityId));
  },
  publishActivity : (activity) => {
    dispatch(publishActivity(activity));
    dispatch(hideActivityModal());
  }
})

export default connect(mapStateToProps, mapDispatchToProps)(WrappedActivityDetail)