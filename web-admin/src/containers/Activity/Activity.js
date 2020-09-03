import React from 'react';
import { Modal, Tabs } from 'antd';
import ActivityDetail from '../../components/ActivityDetail/ActivityDetail.js';
import ActivityChart from '../../components/ActivityChart/ActivityChart.js';
// import ActivityNameList from '../../components/ActivityNameList/ActivityNameList.js';
import ActivityVolunteerList from '../../components/ActivityVolunteerList/ActivityVolunteerList.js'
import { hideActivityModal, switchActivityDetail} from '../../actions';
import {ACTIVITY_DETAIL_TYPE} from '../../constants/index.js';
import { connect } from 'react-redux';

import './Activity.less';

const { TabPane } = Tabs;

class Activity extends React.Component {

  onChangeTab = value => {
    this.props.onChangeActivityDetail(value);
  };

  render() {
    return (
        <Modal
          className="activity-modal"
          title={this.props.activityId?"":"活动编辑"}
          visible={this.props.isActivityVisible}
          destroyOnClose={true}
          maskClosable={false}
          onCancel = {this.props.onCancel}
          cancelButtonProps={{ disabled: true }}
          okButtonProps={{ disabled: true }}
        >

          {
            !this.props.activityId?<ActivityDetail />:
            <Tabs activeKey={this.props.activityDetailType} tabPosition="top" onChange={this.onChangeTab}>
              <TabPane tab="内容" key={ACTIVITY_DETAIL_TYPE.EDIT}>
                <ActivityDetail />
              </TabPane>
              {/* <TabPane tab="名单" key={ACTIVITY_DETAIL_TYPE.NAME_LIST}>
                <ActivityNameList />
              </TabPane> */}
              <TabPane tab="报名管理" key={ACTIVITY_DETAIL_TYPE.VOLUNTEER_LIST}>
                <ActivityVolunteerList />
              </TabPane>
              <TabPane tab="统计" key={ACTIVITY_DETAIL_TYPE.CHART}>
                <ActivityChart />
              </TabPane>
            </Tabs>
          }
        </Modal>
    );
  }
}

const mapStateToProps = (state, ownProps) => ({
  isActivityVisible: state.ui.isShowActivityModal,
  activityId: state.ui.activityId,
  activityDetailType: state.ui.activityDetailType
})

const mapDispatchToProps = (dispatch, ownProps) => ({
  onCancel : () => {
    dispatch(hideActivityModal());
  },
  onChangeActivityDetail: (type)=>{
    dispatch(switchActivityDetail(type));
  }
})

export default connect(mapStateToProps, mapDispatchToProps)(Activity)