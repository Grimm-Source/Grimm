import { Button, Radio, Select } from 'antd';
// import TableHeader from '../../components/TableHeader/TableHeader';
import ActivityList from '../../components/ActivityLIst/ActivityList';
import Report from '../../containers/Report/Report';
import React from 'react';
import { connect } from 'react-redux';
import './ActivityPanel.less';

const { Option } = Select;

class ActivityPanel extends React.Component {
    constructor(props){
        super(props);
        this.state={
          isReport: false,
        }
    }

    onChange=(value)=>{
        this.setState({
            isReport: value !== "activities"
        });
    }

    render() {
        return (
        <div className="activity-container" >
            <Select defaultValue="activities" style={{ width: 120 }}  onChange={this.onChange}>
              <Option value="activities">活动列表</Option>
              <Option value="activityNames">报名情况</Option>
            </Select>
            {this.state.isReport? <Report/>: <ActivityList/>}
        </div>
        );
    }
}

const mapStateToProps = (state, ownProps) => ({
  loading: state.ui.loading
});

const mapDispatchToProps = (dispatch, ownProps) => ({
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(ActivityPanel);
