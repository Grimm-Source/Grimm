import { List, Skeleton } from 'antd';
import React from 'react';
import { showActivityModal, getActivityList, removeActivity} from '../../actions';
import { connect } from 'react-redux';
import './ActivityList.css'

class ActivityList extends React.Component {
  componentDidMount () {
    this.props.getActivityList();
  }

  render() {
    return (
      <List
        className="activity-list"
        loading={this.props.loading}
        itemLayout="horizontal"
        dataSource={this.props.activities}
        renderItem={item => (
          <List.Item
            actions={[<span key="edit" className="list-item-button" onClick={this.props.onClickActivity.bind(this,item)}>编辑</span>, <span key="delete" className="list-item-button" onClick={this.props.onClickRemoveActivity.bind(this,item)}>删除</span>]}
          >
            <Skeleton avatar title={false} loading={this.props.loading} active>
              <List.Item.Meta
                title={<span><span>{(item.date.split("T"))[0]}</span> | <span>{item.title}</span> | <span>{item.location}</span></span>}
                description={item.content}
                className = "activity-content"
                onClick={this.props.onClickActivity.bind(this,item)}
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
  onClickActivity : (activityInfo) => {
    dispatch(showActivityModal(activityInfo.id));
  },
  onClickRemoveActivity: (activityInfo)=>{
    dispatch(removeActivity(activityInfo.id));
  },
  getActivityList : () => {
    dispatch(getActivityList());
  }
})

export default connect(mapStateToProps, mapDispatchToProps)(ActivityList)