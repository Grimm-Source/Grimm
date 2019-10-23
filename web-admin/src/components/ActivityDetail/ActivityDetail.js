import { Form, DatePicker, Input, Button, Spin } from 'antd';
import moment from 'moment';
import React from 'react';
import { hideActivityModal, getActivity, publishActivity} from '../../actions';
import { connect } from 'react-redux';

import './ActivityDetail.less';

const { RangePicker } = DatePicker;


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
      const rangeTimeValue = fieldsValue['date'];
      const values = {
        ...fieldsValue,
        // date: fieldsValue['date'].format('YYYY-MM-DD HH:mm:ss'),
        id: this.props.activity.id,
        adminId: this.props.userId,
        start_time: rangeTimeValue[0].format('YYYY-MM-DD HH:mm:ss'),
        end_time: rangeTimeValue[1].format('YYYY-MM-DD HH:mm:ss'),
      };
      this.props.publishActivity(values);
      this.props.hideActivityModal();
    });
  };

  changeDate = (date, dateString) => {
    if(date && date.length === 2){
      const startTime = new Date(dateString[0]).getTime();
      const endTime = new Date(dateString[1]).getTime();
      let delta = Math.abs(endTime - startTime) / 1000;                    
      let diffObj = {};  
      let result = '';                                                            
      let structure = {                                                                  
          '年': 31536000,
          '月': 2592000,
          '周': 604800, // uncomment row to ignore
          '天': 86400,   // feel free to add your own row
          '小时': 3600,
          '分钟': 60,
          '秒': 1
      };

      Object.keys(structure).forEach(function(key){
        diffObj[key] = Math.floor(delta / structure[key]);
        delta -= diffObj[key] * structure[key];
        if(diffObj[key] !== 0){
          result += `${diffObj[key]}${key}`
        }
      });

      this.props.form.setFieldsValue({
        duration: result
      });
    }
  }

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

    const disabledDate = (current) => {
      // Can not select days before today
      return current < moment().startOf('day');
    }
    
    return (
      
       this.props.loading? <Spin size="large" />: <Form {...formItemLayout} onSubmit={this.handleSubmit}>
       <Form.Item label="活动时间">
         {getFieldDecorator('date', {
            rules: [
                { 
                    type: 'array', 
                    required: true, 
                    message: '请选择时间' 
                }],
            })(<RangePicker disabledDate={disabledDate} onChange={this.changeDate} showTime format="YYYY-MM-DD HH:mm:ss" />)}
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
            //  initialValue: '0',
             rules: [
               {
                 required: true,
                 message: '活动持续时间不能为0，请重新选择开始和结束时间',
               },
             ],
           })(<Input disabled={true} placeholder="0" />)}
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
          value: (props.activity.duration && `${props.activity.duration.day}天${props.activity.duration.hour}小时${props.activity.duration.min}分钟${props.activity.duration.sec}秒`) || ""
        }),
        date: Form.createFormField({
          value: (props.activity.start_time &&  props.activity.end_time && [moment(props.activity.start_time, 'YYYY-MM-DD HH:mm:ss'), moment(props.activity.end_time, 'YYYY-MM-DD HH:mm:ss')]) || null
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