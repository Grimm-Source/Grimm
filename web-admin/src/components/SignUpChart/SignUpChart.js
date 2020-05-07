import React from 'react';
import { connect } from 'react-redux';
import {
    Chart,
    Geom,
    Coord,
    Label,
    Legend,
    View
  } from "bizcharts";

import './SignUpChart.less';

class SignUpChart extends React.Component {

    getData=()=>{
      const {
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
      } = this.props.data;
      
      const signUpRatioOffsetAngle = signUp / targetTotal * Math.PI;
      const checkInRatioOffsetAngle = checkIn / signUp * Math.PI;

      return this.props.isSignUp?{
        pie:[
          {
            type: `剩余报名人数${restSignUp}`,
            value: restSignUp,
            key: "rest"
          },
          {
            type: `已报名人数${signUp}`,
            value: signUp,
            key: "done"
          }
        ],
        column:[
          {
            type: `已报名志愿者${signUpVolunteer}人`,
            value: signUpVolunteer
          },
          {
            type: `已报名视障人士${signUpDisabled}人`,
            value: signUpDisabled
          }
        ],
        restColumn:[
          {
            type: `剩余志愿者${restSignUpVolunteer}人`,
            value: restSignUpVolunteer
          },
          {
            type: `剩余视障人士${restSignUpDisabled}人`,
            value: restSignUpDisabled
          }
        ],
        offsetAngle: signUpRatioOffsetAngle
      }:{
        pie:[
          {
            type: `未签到${restCheckIn}人`,
            value: restCheckIn,
            key: "rest"
          },
          {
            type: `已签到${checkIn}人`,
            value: checkIn,
            key: "done"
          }
        ],
        column:[
          {
            type: `已签到志愿者${checkInVolunteer}人`,
            value: checkInVolunteer
          },
          {
            type: `已签到视障人士${checkInDisabled}人`,
            value: checkInDisabled
          }
        ],
        restColumn:[
          {
            type: `未签到志愿者${restCheckInVolunteer}人`,
            value: restCheckInVolunteer
          },
          {
            type: `未签到视障人士${restCheckInDisabled}人`,
            value: restCheckInDisabled
          }
        ],
        offsetAngle: checkInRatioOffsetAngle
      }
    }
    render() {
      const {
        pie,
        column,
        restColumn,
        offsetAngle,

      } = this.getData();
  
      class SliderChart extends React.Component {
        state = {
          isRest: false
        }

        onClickChart = e => {
          if(!e.data || !e.data.point || !e.data.point.key){
            return;
          }
          this.setState({
            isRest: e.data.point.key === "rest"
          })
        }

        render() {
          const scale = {
            value: {
              nice: false
            }
          };

          const textStyle = {
            fill: '#404040', 
            fontSize: '12',
            fontWeight: 'bold', 
            textBaseline: 'bottom' 
          };

          return (
            <Chart
              height={300}
              weight={300}
              forceFit
              padding={[20, 0, "auto", 0]}
              onClick={this.onClickChart}
            >
              <Legend />
              <View
                data={pie}
                start={{
                  x: 0,
                  y: 0
                }}
                end={{
                  x: 0.5,
                  y: 1
                }}
              >
                <Coord
                  type="theta"
                  startAngle={0 + offsetAngle}
                  endAngle={Math.PI * 2 + offsetAngle}
                />
                <Geom
                  type="intervalStack"
                  position="value"
                  color="type"
                  shape={[
                    "type",
                    "rect"
                  ]}
                >
                  <Label
                    content="type"
                    offset={-20}
                    textStyle={{
                      rotate: 0
                    }}
                    textStyle={{
                      fill: '#404040',
                      fontSize: '12', 
                      fontWeight: 'bold', 
                      textBaseline: 'bottom' 
                  }}
                  />
                </Geom>
              </View>
              {
                !this.state.isRest?<View
                data={column}
                scale={scale}
                start={{
                  x: 0.6,
                  y: 0
                }}
                end={{
                  x: 1,
                  y: 1
                }}
              >
                <Geom
                  type="intervalStack"
                  position="1*value"
                  color={["type", "#FCD7DE-#F04864"]}
                >
                  <Label content="type" offset={-20} textStyle={textStyle}/>
                </Geom>
              </View>:<View
                data={restColumn}
                scale={scale}
                start={{
                  x: 0.6,
                  y: 0
                }}
                end={{
                  x: 1,
                  y: 1
                }}
              >
                <Geom
                  type="intervalStack"
                  position="1*value"
                  color={["type", "#e4c17b-#faad14"]}
                >
                  <Label content="type" offset={-20} textStyle={textStyle}/>
                </Geom>
              </View>
              }
            </Chart>
          );
        }
      }
      return (
        <div>
          <SliderChart />
        </div>
      );
    }
  }

const mapStateToProps = (state, ownProps) => ({
  activityId: state.ui.activityId
})

const mapDispatchToProps = (dispatch, ownProps) => ({
})

export default connect(mapStateToProps, mapDispatchToProps)(SignUpChart);