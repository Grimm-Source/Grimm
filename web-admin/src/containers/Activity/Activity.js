import React from 'react';
import { Modal } from 'antd';
import ActivityDetail from '../../components/ActivityDetail/ActivityDetail.js';
import { hideActivityModal} from '../../actions';
import { connect } from 'react-redux';

import './Activity.css';

class Activity extends React.Component {
  render() {
    return (
        <Modal
          className="activity-modal"
          title="编辑活动"
          visible={this.props.visible}
          destroyOnClose={true}
          maskClosable={false}
          onCancel = {this.props.onCancel}
          cancelButtonProps={{ disabled: true }}
          okButtonProps={{ disabled: true }}
        >
          <ActivityDetail activity={this.props.activity}/>
        </Modal>
    );
  }
}

const mapStateToProps = (state, ownProps) => ({
  visible: state.ui.isShowActivityModal
})

const mapDispatchToProps = (dispatch, ownProps) => ({
  onCancel : () => {
    dispatch(hideActivityModal());
  }
})

export default connect(mapStateToProps, mapDispatchToProps)(Activity)