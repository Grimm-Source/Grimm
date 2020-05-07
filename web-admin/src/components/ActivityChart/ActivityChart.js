import { Radio, Progress, Alert, Statistic } from 'antd';
import React from 'react';
import { connect } from 'react-redux';
import SignUpChart from '../SignUpChart/SignUpChart.js';
import { getActivityStatics, switchActivityDetail } from '../../actions';
import {ACTIVITY_DETAIL_TYPE} from '../../constants/index.js';
import { StarOutlined, ShareAltOutlined } from '@ant-design/icons';
import TextLoop from 'react-text-loop';


import './ActivityChart.less';


const CHART_TYPE = {
  SIGN_UP: "SIGN_UP",
  CHECK_IN: "CHECK_IN"
}

class ActivityChart extends React.Component {
    constructor(props){
      super(props);
      this.state={
        chartType: CHART_TYPE.SIGN_UP
      }
    }

    componentDidMount(){
      if(!this.props.activityId){
        return;
      }
      this.props.getActivityStatics(this.props.activityId);
    }

    onChangeChart = e => {
      this.setState({ chartType: e.target.value });
    };

    render() {
        const {
          targetVolunteer,
          targetDisabled,
          signUpVolunteer,
          signUpDisabled,
          checkInVolunteer,
          checkInDisabled
        } = this.props.data;
      
        const signUp = signUpVolunteer + signUpDisabled;
        const targetTotal = targetVolunteer + targetDisabled;
        const restSignUp = targetTotal - signUp;
        const restSignUpVolunteer = targetVolunteer - signUpVolunteer;
        const restSignUpDisabled = targetDisabled - signUpDisabled;


        const checkIn = checkInVolunteer + checkInDisabled;
        const restCheckIn = signUp - checkIn;
        const restCheckInVolunteer = signUpVolunteer - checkInVolunteer;
        const restCheckInDisabled = signUpDisabled - checkInDisabled;

        const signUpRateDisabledPer = Number((signUpDisabled/targetDisabled*100).toFixed(2));
        const signUpRateVolunteerPer = Number((signUpVolunteer/targetVolunteer*100).toFixed(2));
        const signUpRateDisabledStr =  `${signUpDisabled}/${targetDisabled}`;
        const signUpRateVolunteerStr =  `${signUpVolunteer}/${targetVolunteer}`;

        const checkInRateDisabledPer = Number((checkInDisabled/signUpDisabled*100).toFixed(2));
        const checkInRateVolunteerPer = Number((checkInVolunteer/signUpVolunteer*100).toFixed(2));
        const checkInRateDisabledStr =  `${checkInDisabled}/${signUpDisabled}`;
        const checkInRateVolunteerStr =  `${checkInVolunteer}/${signUpVolunteer}`;   
        
        const data = {
          signUpVolunteer,
          signUpDisabled,
          signUp,
          restSignUp,
          targetTotal,
          restSignUpVolunteer,
          restSignUpDisabled,
          checkInVolunteer,
          checkInDisabled,
          checkIn,
          restCheckIn,
          restCheckInVolunteer,
          restCheckInDisabled
        };

        return (
        <div className="activity-chart">
          
          <div className="activity-chart-header">
            <div className="left-group">
              <Radio.Group className="chart-type" value={this.state.chartType} onChange={this.onChangeChart}>
                  <Radio.Button value={CHART_TYPE.SIGN_UP}>报名</Radio.Button>
                  <Radio.Button value={CHART_TYPE.CHECK_IN}>签到</Radio.Button>
              </Radio.Group>
              <div className="activity-progress">
                {this.state.chartType === CHART_TYPE.SIGN_UP?(<div>
                  <span>志愿者报名情况: <span className="count-label" onClick={this.props.onClickName} >{signUpRateVolunteerStr}</span></span><span><Progress percent={signUpRateVolunteerPer} status="active" /></span>
                  <span>视障人士报名情况: <span className="count-label" onClick={this.props.onClickName}>{signUpRateDisabledStr}</span></span><span><Progress percent={signUpRateDisabledPer} status="active" /></span>
                </div>):(<div>
                  <span>志愿者签到情况: <span className="count-label" onClick={this.props.onClickName}> {checkInRateVolunteerStr}</span></span><span><Progress percent={checkInRateVolunteerPer} status="active" /></span>
                  <span>视障人士签到情况: <span className="count-label" onClick={this.props.onClickName}> {checkInRateDisabledStr}</span></span><span><Progress percent={checkInRateDisabledPer} status="active" /></span>
                </div>)
                }
                
                <Alert
                    className="alert-loop"
                    banner
                    message={
                      this.state.chartType === CHART_TYPE.SIGN_UP?<TextLoop mask>
                        <div>{restSignUpVolunteer > 0? `志愿者还有${restSignUpVolunteer}个名额!`: "正在加载..."}</div>
                        <div>{restSignUpDisabled > 0? `视障人士还有${restSignUpDisabled}个名额!`: "正在加载..."}</div>
                      </TextLoop>:<TextLoop mask>
                        <div>{restCheckInVolunteer > 0? `志愿者未签到${restCheckInVolunteer}人!`: "正在加载..."}</div>
                        <div>{restCheckInDisabled > 0? `视障人士未签到${restCheckInDisabled}人!`: "正在加载..."}</div>
                      </TextLoop>
                    }
                  />
              </div>
            </div>
            <div className="right-group">
              {/* <Statistic title="收藏次数" style={{fontSize: "22px", margin:"20px"}} value={128} prefix={<StarOutlined />} />
              <Statistic title="转发次数" style={{fontSize: "22px", margin:"20px"}} value={10} prefix={<ShareAltOutlined />} /> */}
            </div>
          </div>
          
          <SignUpChart data={data} isSignUp={this.state.chartType === CHART_TYPE.SIGN_UP}/>
        </div>
        );
    }
  
}

const mapStateToProps = (state) => ({
  activityId: state.ui.activityId,
  data: state.ui.activityStatics
})

const mapDispatchToProps = (dispatch) => ({
  getActivityStatics : (activityId) => {
    dispatch(getActivityStatics(activityId));
  },
  onClickName: ()=>{
    dispatch(switchActivityDetail(ACTIVITY_DETAIL_TYPE.NAME_LIST));
  }
})

export default connect(
    mapStateToProps,
    mapDispatchToProps
  )(ActivityChart);