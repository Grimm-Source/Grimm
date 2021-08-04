import {
  Form,
  DatePicker,
  Input,
  Button,
  Spin,
  Radio,
  InputNumber,
  Switch,
  message,
} from "antd";
import { SmileOutlined } from "@ant-design/icons";
import moment from "moment";
import ButtonGroup from "../ButtonGroup/ButtonGroup.js";
import { ACTIVITY_TAGS } from "../../constants";
import React from "react";
import { hideActivityModal, getActivity, publishActivity } from "../../actions";
import { connect } from "react-redux";

import "./ActivityDetail.less";

// For upload
import { Upload, Icon } from "antd";
import baseUrl from "../../config/config";

const { RangePicker } = DatePicker;

class ActivityDetail extends React.Component {
  state = {
    isInitialized: false,
    isVolLimited: undefined,
    isDisabledLimited: undefined,
    isFeeNeeded: undefined,
    displayUpload: true,
  };

  componentDidMount() {
    this.props.getActivity(this.props.activityId, this.props.isCopy);
  }

  componentWillReceiveProps(nextProps) {
    if (!nextProps.activity) {
      return;
    }

    if (
      !this.state.isInitialized &&
      Object.keys(nextProps.activity).length > 0
    ) {
      this.setState({
        isInitialized: true,
        isVolLimited: nextProps.activity.volunteer_capacity > 0,
        isDisabledLimited: nextProps.activity.vision_impaired_capacity > 0,
        isFeeNeeded: nextProps.activity.activity_fee > 0,
        displayUpload: nextProps.activity.activity_them_pic_name ? false : true,
      });
    }
  }

  componentDidUpdate() {}

  handleSubmit = (e) => {
    e.preventDefault();
    this.props.form.validateFields((err, fieldsValue) => {
      console.log(fieldsValue);
      if (err) {
        return;
      }
      if (Date.parse(new Date()) > moment(fieldsValue["date"][0]).valueOf()) {
        message.error("活动已经开始，或活动开始时间有误，无法保存");
        return;
      }
      const rangeTimeValue = fieldsValue["date"];

      const values = {
        ...fieldsValue,
        // volunteer_capacity: this.state.isVolLimited?this.props.activity.volunteer_capacity: null,
        // vision_impaired_capacity: this.state.isDisabledLimited?this.props.activity.vision_impaired_capacity: null,
        id: this.props.activity.id,
        adminId: this.props.userId,
        others: "",
        start_time: rangeTimeValue[0].format("YYYY-MM-DD HH:mm:ss"),
        end_time: rangeTimeValue[1].format("YYYY-MM-DD HH:mm:ss"),
      };
      if (values["activity_them_pic_name"].length > 0) {
        console.log(values["activity_them_pic_name"][0]);
        let url;
        if (values["activity_them_pic_name"][0].response) {
          url =
            baseUrl +
            "activity/themePic?activity_them_pic_name=" +
            values["activity_them_pic_name"][0].response.fileName;
        } else {
          url = values["activity_them_pic_name"][0].url;
        }
        values["activity_them_pic_name"][0] = {
          url,
          uid: this.props.activity.id,
        };
      }
      this.props.publishActivity(values);
      this.props.hideActivityModal();
    });
  };

  changeDate = (date, dateString) => {
    if (date && date.length === 2) {
      const startTime = new Date(dateString[0]).getTime();
      const endTime = new Date(dateString[1]).getTime();
      let delta = Math.abs(endTime - startTime) / 1000;
      let diffObj = {};
      let result = "";
      let structure = {
        年: 31536000,
        月: 2592000,
        周: 604800, // uncomment row to ignore
        天: 86400, // feel free to add your own row
        小时: 3600,
        分钟: 60,
        秒: 1,
      };

      Object.keys(structure).forEach(function (key) {
        diffObj[key] = Math.floor(delta / structure[key]);
        delta -= diffObj[key] * structure[key];
        if (diffObj[key] !== 0) {
          result += `${diffObj[key]}${key}`;
        }
      });

      this.props.form.setFieldsValue({
        duration: result,
      });
    }
  };

  onChangeVolLimited = (e) => {
    this.setState({
      isVolLimited: e.target.value,
    });
  };

  onChangeDisabledLimited = (e) => {
    this.setState({
      isDisabledLimited: e.target.value,
    });
  };

  onChangeActivityFeeNeed = (e) => {
    this.setState({
      isFeeNeeded: e.target.value,
    });
  };

  render() {
    const { getFieldDecorator } = this.props.form;
    getFieldDecorator.title = "123";
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
      return current < moment().startOf("day");
    };

    const uploadUrl = baseUrl + "activity/themePic";
    // 处理上传按钮每次触发事件
    const handleChange = (info) => {
      let changedFileList = info.fileList;
      if (changedFileList.length === 0) {
        this.setState({ displayUpload: true });
      }
      const curFile = info.file;
      if (curFile.status === "done") {
        message.success("上传成功");
        this.setState({ displayUpload: false });
        return curFile.response;
        // file.url = file.response.fileName;
      }
      if (curFile.response && curFile.response.status !== 1) {
        message.error(curFile.response.message);
        // file.url = 0;
      }
      // 向fileList中增加url字段来记录每次上传成功后服务端返回的图片名字
      // changedFileList = changedFileList.map((file) => {
      //   if (file.response && file.response.status === 1) {

      //   } else {

      //   }
      //   return file;
      // });
    };
    const uploadImgConfig = {
      action: uploadUrl,
      name: "activity_them_pic_name",
    };

    return this.props.loading ? (
      <Spin size="large" />
    ) : (
      <Form
        className="activity-form"
        {...formItemLayout}
        onSubmit={this.handleSubmit}
      >
        <Form.Item
          style={{ marginBottom: 0 }}
          htmlFor="date-item"
          label="活动时间"
        >
          <Form.Item style={{ display: "inline-block", width: "45%" }}>
            {getFieldDecorator("date", {
              rules: [
                {
                  type: "array",
                  required: true,
                  message: "请选择时间",
                },
              ],
            })(
              <RangePicker
                disabledDate={disabledDate}
                onChange={this.changeDate}
                showTime={{ format: "HH:mm" }}
                format="YYYY-MM-DD HH:mm"
              />
            )}
          </Form.Item>
          <Form.Item style={{ display: "inline-block", width: "30%" }}>
            {getFieldDecorator("duration", {
              rules: [
                {
                  required: true,
                  message: "活动持续时间不能为0，请重新选择开始和结束时间",
                },
              ],
            })(<Input disabled={true} placeholder="0" />)}
          </Form.Item>
        </Form.Item>
        <Form.Item label="活动主题">
          {getFieldDecorator("title", {
            rules: [
              {
                required: true,
                message: "请输入活动主题",
              },
            ],
          })(<Input placeholder="请输入活动主题" />)}
        </Form.Item>
        <Form.Item label="活动地点">
          {getFieldDecorator("location", {
            rules: [
              {
                required: true,
                message: "请输入活动地点",
              },
            ],
          })(<Input placeholder="请输入活动地点" />)}
        </Form.Item>
        <Form.Item label="主题图片" style={{ marginBottom: 0 }}>
          {getFieldDecorator("activity_them_pic_name", {
            valuePropName: "fileList",
            getValueFromEvent: (e) => {
              if (Array.isArray(e)) {
                return e;
              }
              return e && e.fileList;
            },
            rules: [
              {
                required: true,
                message: "请上传主题图片",
              },
            ],
          })(
            <Upload
              {...uploadImgConfig}
              listType="picture-card"
              onChange={handleChange}
              multiple={false}
              accept="image/png,image/jpg,image/jpeg"
              showUploadList={{ showPreviewIcon: false }}
            >
              {this.state.displayUpload ? (
                <div>
                  <Icon type="plus" />
                  <div className="ant-upload-text">上传</div>
                </div>
              ) : null}
            </Upload>
          )}
        </Form.Item>
        <Form.Item label="签到半径">
          {getFieldDecorator("sign_in_radius", {
            rules: [
              {
                required: true,
                message: "请输入签到半径",
              },
            ],
          })(
            <InputNumber
              min={0}
              type="number"
              id="sign_in_radius"
              placeholder=""
            />
          )}{" "}
          &emsp;公里
        </Form.Item>
        <Form.Item label="签到口令">
          {getFieldDecorator("sign_in_token", {
            rules: [
              {
                required: true,
                message: "请输入签到口令",
              },
            ],
          })(
            <Input
              disabled={!this.state.isVolLimited}
              style={{ width: "200px" }}
              placeholder="请输入签到口令"
            />
          )}
        </Form.Item>
        <Form.Item label="活动内容">
          {getFieldDecorator("content", {
            rules: [
              {
                required: true,
                message: "请输入活动内容",
              },
            ],
          })(<Input.TextArea rows={5} placeholder="请输入活动内容" />)}
        </Form.Item>
        <Form.Item htmlFor="count-item" label="招募人数">
          <div className="impaired-detail">
            <span className="inline-label">视障人士</span>
            <Radio.Group
              onChange={this.onChangeDisabledLimited}
              value={this.state.isDisabledLimited}
            >
              <Radio value={true}>有</Radio>
              <Radio value={false}>无</Radio>
            </Radio.Group>
            <Form.Item
              style={{ marginBottom: "12px", display: "inline-block" }}
            >
              {getFieldDecorator("vision_impaired_capacity", {
                rules: [
                  {
                    required: false,
                  },
                ],
              })(
                <InputNumber
                  min={0}
                  disabled={!this.state.isDisabledLimited}
                  type="number"
                  id="vision_impaired_capacity"
                  placeholder="请输入视障人士人数"
                />
              )}
            </Form.Item>
          </div>
          <div className="volunteer-detail">
            <div>
              <span className="inline-label">志愿者</span>
              <Radio.Group
                onChange={this.onChangeVolLimited}
                value={this.state.isVolLimited}
              >
                <Radio value={true}>有</Radio>
                <Radio value={false}>无</Radio>
              </Radio.Group>
              <span className="inline-label">自动审核</span>
              <Switch
                disabled={!this.state.isVolLimited}
                defaultChecked={false}
              />
            </div>
            <Form.Item
              label="岗位名称"
              style={{ display: "inline-block", width: "50%" }}
            >
              {getFieldDecorator("volunteer_job_title", {
                rules: [
                  {
                    required: false,
                    message: "请输入岗位名称",
                  },
                ],
              })(
                <Input
                  disabled={!this.state.isVolLimited}
                  placeholder="请输入岗位名称"
                />
              )}
            </Form.Item>
            <Form.Item
              label="岗位人数"
              style={{ display: "inline-block", width: "50%" }}
            >
              {getFieldDecorator("volunteer_capacity", {
                rules: [
                  {
                    required: false,
                    message: "请输入岗位人数",
                  },
                ],
              })(
                <InputNumber
                  disabled={!this.state.isVolLimited}
                  min={0}
                  type="number"
                  id="volunteer_capacity"
                  placeholder="请输入志愿者人数"
                />
              )}
            </Form.Item>
            <Form.Item label="岗位内容">
              {getFieldDecorator("volunteer_job_content", {
                rules: [
                  {
                    required: false,
                    message: "请输入岗位内容",
                  },
                ],
              })(
                <Input
                  disabled={!this.state.isVolLimited}
                  placeholder="请输入岗位内容"
                />
              )}
            </Form.Item>
          </div>
        </Form.Item>
        <Form.Item label="活动费用">
          <Radio.Group
            onChange={this.onChangeActivityFeeNeed}
            value={this.state.isFeeNeeded}
          >
            <Radio value={false}>免费</Radio>
            <Radio value={true}>收费</Radio>
          </Radio.Group>
          <Form.Item style={{ display: "inline-block", marginBottom: "0" }}>
            {getFieldDecorator("activity_fee", {
              rules: [
                {
                  required: false,
                },
              ],
            })(
              <InputNumber
                disabled={!this.state.isFeeNeeded}
                min={0}
                type="number"
                id="expense"
                placeholder="请输入活动费用"
              />
            )}
          </Form.Item>
          <span className="inline-label">元/人</span>
        </Form.Item>
        <Form.Item label="活动标签">
          {getFieldDecorator("tag", {
            rules: [
              {
                required: false,
              },
            ],
          })(<ButtonGroup buttons={Object.keys(ACTIVITY_TAGS)} />)}
        </Form.Item>
        <Form.Item label="活动注意事项">
          {getFieldDecorator("notice")(
            <Input
              placeholder="请输入活动注意事项"
              prefix={<SmileOutlined style={{ color: "#ff5722" }} />}
            />
          )}
        </Form.Item>
        {/* <Form.Item label="其它">
                       {getFieldDecorator('others', )(<Input placeholder="请输入其它事项" />)}
                    </Form.Item> */}
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
    if (!props.activity) {
      return {};
    }
    let picUrl = [];
    if (props.activity.activity_them_pic_name) {
      picUrl = [
        {
          uid: "1",
          url:
            baseUrl +
            "activity/themePic?activity_them_pic_name=" +
            props.activity.activity_them_pic_name,
        },
      ];
    }
    return {
      title: Form.createFormField({
        value: props.activity.title || "",
      }),
      content: Form.createFormField({
        value: props.activity.content || "",
      }),
      location: Form.createFormField({
        value: props.activity.location || "",
      }),
      activity_them_pic_name: Form.createFormField({
        value: picUrl,
      }),
      sign_in_radius: Form.createFormField({
        value: props.activity.sign_in_radius || "",
      }),
      sign_in_token: Form.createFormField({
        value: props.activity.sign_in_token || "",
      }),
      notice: Form.createFormField({
        value: props.activity.notice || "",
      }),
      others: Form.createFormField({
        value: props.activity.others || "",
      }),
      tag: Form.createFormField({
        value: props.activity.tag || "",
      }),
      duration: Form.createFormField({
        value:
          (props.activity.duration &&
            `${props.activity.duration.day}天${props.activity.duration.hour}小时${props.activity.duration.min}分钟`) ||
          "",
      }),
      date: Form.createFormField({
        value:
          (props.activity.start_time &&
            props.activity.end_time && [
              moment(props.activity.start_time, "YYYY-MM-DD HH:mm"),
              moment(props.activity.end_time, "YYYY-MM-DD HH:mm"),
            ]) ||
          null,
      }),
      vision_impaired_capacity: Form.createFormField({
        value: props.activity.vision_impaired_capacity,
      }),
      volunteer_capacity: Form.createFormField({
        value: props.activity.volunteer_capacity,
      }),
      volunteer_job_title: Form.createFormField({
        value: props.activity.volunteer_job_title || "",
      }),
      volunteer_job_content: Form.createFormField({
        value: props.activity.volunteer_job_content || "",
      }),
      activity_fee: Form.createFormField({
        value: props.activity.activity_fee,
      }),
    };
  },
})(ActivityDetail);

const mapStateToProps = (state) => ({
  activityId: state.ui.activityId,
  activity: state.ui.activity,
  loading: state.ui.loading,
  userId: state.account.user && state.account.user.id,
  isCopy: state.ui.isCopy,
});

const mapDispatchToProps = (dispatch) => ({
  hideActivityModal: () => {
    dispatch(hideActivityModal());
  },
  getActivity: (activityId, isCopy) => {
    dispatch(getActivity(activityId, isCopy));
  },
  publishActivity: (activity) => {
    dispatch(publishActivity(activity));
    dispatch(hideActivityModal());
  },
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(WrappedActivityDetail);
