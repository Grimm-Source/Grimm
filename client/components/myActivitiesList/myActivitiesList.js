// components/myActivities/myActivitiesList.js
const { getMyActivities } = require('../../utils/requestUtil.js');

const myActivitiesType = {
  MYALL: 0,
  REGISTERED: 1,
  INTERESTED: 2
};

const timeTitle = {
  TIME: '时间'
};

Component({
  /**
   * 组件的属性列表
   */
  properties: {
    selectedIdx: {
      type: Number,
      observer: function(filterType) {
        // console.log(newIdx);
        this.onFilterParamChange(filterType);
      },
    }
  },

  /**
   * 组件的初始数据
   */

  data: {
    selectedActivities: myActivitiesType.MYALL,
    myActivities: [],
  },

  pageLifetimes: {
    show: function () {
      this.onFilterParamChange(this.data.selectedIdx);
    }
  },

  /**
   * 组件的方法列表
   */
  methods: {
    _setMyActivities: function (filterType, activities) {
      let formattedActivities = [];
      for (let index = 0; index < activities.length; index++) {
        let activity = activities[index];
        let isOneDay = activities[index].duration.day == 0;
        console.log(activity);
        // remove seconds
        const startFullTime = (activity.start_time).replace("T", " ");
        const endFullTime = (activity.end_time).replace("T", " ");
        let startTime = startFullTime.substring(0, startFullTime.lastIndexOf(':'));
        let endTime = endFullTime.substring(0, endFullTime.lastIndexOf(':'));
        let startTimeStrs = startTime.split(' ');
        let endTimeStrs = endTime.split(' ');
        activity.timeTitle = timeTitle.TIME;
        
        // set time -> start time - end time
        if (startTimeStrs.length < 2 || endTimeStrs.length < 2) {
          activity.schedule = startTime + " - " + endTime;
        }
        else if(isOneDay){
          activity.schedule = startTime + " - " + endTimeStrs[1];
        }
        else {
          activity.schedule = startTimeStrs[0] + " - " + endTimeStrs[0];
        }

        // set activity fee
        if(activity.is_fee_needed){
          activity.fee = "¥" + activity_fee;
        } else{
          activity.fee = "免费";
        }
        
        // set default preview img
        activity.imgSrc = "../../images/banner_icon.jpeg";

        formattedActivities.push(activity);
      }

      // if (filterType == myActivitiesType.MYALL) {
      //   selectedActivities = this.data.myAllActivities;
      // }
      // else if (filterType == myActivitiesType.REGISTERED) {
      //   selectedActivities = this.data.myRegisteredActivities;
      // }
      // else if (filterType == myActivitiesType.INTERESTED) {
      //   selectedActivities = this.data.myInterestedActivites;
      // }

      // if(selectedActivities == null) {
      //   console.log("Wrong selected index : " + filterType);
      // }

      this.setData({
        myActivities: formattedActivities,
        selectedActivities: filterType
      });
    },

    _getFilterTypeStr: function(type) {
      if (type == myActivitiesType.MYALL) {
        return "all";
      }

      if (type == myActivitiesType.INTERESTED) {
        return "favorite";
      }

      if (type == myActivitiesType.REGISTERED) {
        return "registered";
      }
    },
    
    onTapActivity: function (event) {
      let activityId = event.currentTarget.id;
      if(activityId ==  null){
        return;
      }
      wx.navigateTo({
          url: '/pages/activityDetail/activityDetail?id='+ activityId,
      })
    },

    onFilterParamChange: function (type) {
      const filterStr = this._getFilterTypeStr(type);
      // getActivityList((res)=>{
      //   this._setMyActivities(type, res);
      // }); 
      getMyActivities(filterStr, (res) => {
        this._setMyActivities(type, res);
      });
    }
  }
})
