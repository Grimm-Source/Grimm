import { List, Skeleton, Modal, Tag } from 'antd';
import React from 'react';
import {
  showActivityModal,
  getActivityList,
  removeActivity,
} from '../../actions';
import { ACTIVITY_TAGS } from '../../constants';
import {ACTIVITY_DETAIL_TYPE} from '../../constants/index.js';
import { connect } from 'react-redux';

import './ActivityList.less';
const { confirm } = Modal;

class ActivityList extends React.Component {
  componentDidMount() {
    this.props.getActivityList();
  }

  render() {
    return (
        <List
          className="activity-list"
          loading={this.props.loading}
          itemLayout="horizontal"
          dataSource={this.props.activities}
          pagination={{  
            pageSize: 10
          }}
          renderItem={item => (
            <List.Item
              actions={[
                <span>{item.tag && item.tag.split(",").map((value, index)=>{
                  return <Tag className="tag" key={index} color={ACTIVITY_TAGS[value]}>{value}</Tag>
                })}</span>,
                <span
                  key="edit"
                  className="list-item-button"
                  onClick={this.props.onClickActivity.bind(this, item, ACTIVITY_DETAIL_TYPE.EDIT)}
                >
                  编辑
                </span>,
                <span
                  key="copy"
                  className="list-item-button"
                  onClick={this.props.onClickActivity.bind(this, item, ACTIVITY_DETAIL_TYPE.COPY)}
                >
                  复制
                </span>,
                <span
                    key="register"
                  className="list-item-button"
                    onClick={this.props.onClickActivity.bind(this, item, ACTIVITY_DETAIL_TYPE.VOLUNTEER_LIST)}
                >
                  报名管理
              </span>,
                <span
                  key="delete"
                  className="list-item-button"
                  onClick={this.props.onClickRemoveActivity.bind(this, item)}
                >
                  删除
                </span>
              ]}
            >
              <Skeleton avatar title={false} loading={this.props.loading} active>
                <List.Item.Meta
                  title={<span><span>{(item.start_time.split("T"))[0]===(item.end_time.split("T"))[0] ? (item.start_time.split("T"))[0] : `${(item.start_time.split("T"))[0]} ~ ${(item.end_time.split("T"))[0]}`}</span> | <span>{item.title}</span> | <span>{item.location}</span></span>}
                  description={item.content}
                  className="activity-content"
                  onClick={this.props.onClickActivity.bind(this, item, ACTIVITY_DETAIL_TYPE.EDIT)}
                />
              </Skeleton>
            </List.Item>
            
          )}
        />
    );
  }
}

const mapStateToProps = (state, ownProps) => ({
  activities: state.activity.activities,
  loading: state.ui.loading
});

const mapDispatchToProps = (dispatch, ownProps) => ({
  onClickActivity: (activityInfo, type) => {
    dispatch(showActivityModal(activityInfo.id, type));
  },
  onClickRemoveActivity: activityInfo => {
    confirm({
      title: '确定删除该活动吗?',
      okText: '确定',
      okType: 'danger',
      cancelText: '取消',
      onOk() {
        dispatch(removeActivity(activityInfo.id));
      },
      onCancel() {
        console.log('Cancel');
      }
    });
  },
  getActivityList: () => {
    dispatch(getActivityList());
  }
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(ActivityList);
