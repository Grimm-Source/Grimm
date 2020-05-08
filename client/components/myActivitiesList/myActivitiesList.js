// components/myActivities/myActivitiesList.js
const { getMyActivities } = require('../../utils/requestUtil.js');
const app = getApp()

const myActivitiesType = {
  MYALL: 0,
  REGISTERED: 1,
  INTERESTED: 2
};

const timeTitle = {
  TIME: '时间',
  DATE: '地点' 
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
      this.onFilterParamChange(this.data.selectedActivities);
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
        // remove seconds
        const startFullTime = activity.start_time;
        const endFullTime = activity.end_time;
        let startTime = startFullTime.substring(0, startFullTime.lastIndexOf(':'));
        let endTime = endFullTime.substring(0, endFullTime.lastIndexOf(':'));

        let startTimeStrs = startTime.split(' ');
        let endTimeStrs = endTime.split(' ');

        activity.timeTitle = timeTitle.DATE;

        if (startTimeStrs.length < 2 || endTimeStrs.length < 2) {
          activity.schedule = startTime + " - " + endTime;
        }
        else if(isOneDay){
          // start date time - end time
          activity.schedule = startTime + " - " + endTimeStrs[1];
          activity.timeTitle = timeTitle.TIME;
        }
        else {
          // start date - end date
          activity.schedule = startTimeStrs[0] + " - " + endTimeStrs[0];
        }

        // set default preview img
        activity.imgSrc = "../../images/banner.jpg";

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
        return "attended";
      }

      if (type == myActivitiesType.INTERESTED) {
        return "isInterested";
      }

      if (type == myActivitiesType.REGISTERED) {
        return "registered";
      }
    },
    
    onTapActivity: function (event) {
      console.log(event)
      wx.navigateTo({
        url: `/pages/activityDetail/activityDetail?id=${event.currentTarget.dataset.id}`,
      })
    },

    onFilterParamChange: function (type) {
      const filterStr = this._getFilterTypeStr(type);
      // getMyActivities(filterStr, (res) => {
      //   this._setMyActivities(type, res);
      // });
      const activities = []
      app.globalData.activityList.forEach(item => {
        if(item[filterStr]){
          activities.push(item)
        }
      })
      this._setMyActivities(type, activities);
    }
  }
})
