// components/activitiesList/activitiesList.js
const { getActivityList, getFilteredActivities} = require('../../utils/requestUtil.js');

Component({
  /**
   * 组件的属性列表
   */
  properties: {
    activitiesProp: {
      type: Array,
      value:[],
    }
  },

  /**
   * 组件的初始数据
   */
  data: {
  },

  pageLifetimes: {
    show: function() {
      getActivityList((res) => {
        this._setActivities(res);
      })
    }
  },

  /**
   * 组件的方法列表
   */
  methods: {
    _setActivities: function (activities) {
        let formattedActivities = [];
        for (let index = 0; index < activities.length; index++) {
          let activity = activities[index];
          activity.schedule = this.getActivityTimeStr(activity);
          formattedActivities.push(activity);
        }
        this.setData({activitiesProp: formattedActivities});
    },

    _getFilteredCategoryParams(category) {
      return category != -1 ? "tags=" + category : "";
    },

    _getFilteredTimeParams(time) {
      if (time == "all" || time == "interval") {
        return "";
      } else {
        return "time=" + time;
      }

      // if (time == "0") {
      //   timeParams = "latest";
      // } else if (time == "1") {
      //   timeParams = "weekends";
      // } else if (time == "2") {
      //   let date = new Date();
      //   const currentDateStr = date.toISOString().substr(0, 10);
      //   let nextWeek = new Date(date.setDate(date.getDate() + 7));
      //   const weekDateStr = nextWeek.toISOString().substr(0, 10);
      //   timeParams = "time=" + currentDateStr + " - " + weekDateStr;
      // }
      // return timeParams;
    },

    onTapActivity: function (event) {
      let item = event.currentTarget.dataset && event.currentTarget.dataset.item,
      activityId = item.id;
      if(activityId ==  null){
        return;
      }
      wx.navigateTo({
        url: '/pages/activityDetail/activityDetail?id=' + activityId,
      })
    },

    onFilterParamChange: function(event) {
      console.log(event);
      let categoryParam = this._getFilteredCategoryParams(event.detail.category);
      let timeParam = this._getFilteredTimeParams(event.detail.time);

      if (categoryParam == "" && timeParam == "") {
        getActivityList((res) => {
          this._setActivities(res);
        });
      } else {
        var params = "";
        if (timeParam == "") {
          params = categoryParam;
        } else if (categoryParam == "") {
          params = timeParam;
        } else {
          params = timeParam + "&" + categoryParam;
        }
        getFilteredActivities(params, (res) => {
          this._setActivities(res);
        });
      }
    },

    onPulling: function() {

    },

    getActivityTimeStr: function(activity) {
      let startTime = activity.start_time.replace('T', ' ').replace(/-/g, ".");
      let endTime = activity.end_time.replace('T', ' ').replace(/-/g, ".");
      let timeStr = "";
      if (activity.duration.day != 0) {
        timeStr = startTime.substr(0, 10) + " - " + endTime.substr(0, 10)
      } else {
        timeStr = startTime.substr(0, 16) + "-" + endTime.substr(11, 5)
      }
      return timeStr;
    }
  }
})
