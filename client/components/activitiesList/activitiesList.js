// components/activitiesList/activitiesList.js
const {
  getActivityList,
  getFilteredActivities
} = require('../../utils/requestUtil.js');

const apiUrl = require('../../config.js').apiUrl;

Component({
  /**
   * 组件的属性列表
   */
  properties: {
    activitiesProp: {
      type: Array,
      value: [],
    }
  },

  /**
   * 组件的初始数据
   */
  data: {},

  pageLifetimes: {
    show: function () {
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
        activity.fee = this.getActivityFee(activity);
        if (activity.activity_them_pic_name) {
          activity.themeUrl = apiUrl + 'activity/themePic?activity_them_pic_name=' + activity.activity_them_pic_name;
        } else {
          activity.themeUrl = '../../images/banner_outer.jpeg';
        }
        formattedActivities.push(activity);
      }
      this.setData({
        activitiesProp: formattedActivities
      });
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
        activity_id = item.id;
      if (activity_id == null) {
        return;
      }
      // Fix wiki bug: Register/View activities (4. Pop up wrong warning...)
      let activityStartTime = event.currentTarget.dataset.item['start_time']
      let activityEndTime = event.currentTarget.dataset.item['end_time']
      let currentTime = new Date()
      if (currentTime > new Date(activityEndTime)) {
        wx.showModal({
          showCancel: false,
          title: '活动已结束',
          content: "您想操作的活动已结束，请选择还未开始的活动，谢谢!"
        })
        return
      } else if (currentTime >= new Date(activityStartTime) && currentTime <= new Date(activityEndTime)) {
        wx.showModal({
          showCancel: false,
          title: '活动已开始',
          content: "您想操作的活动已开始，请选择还未开始的活动，谢谢!"
        })
        return
      }
      wx.navigateTo({
        url: '/pages/activityDetail/activityDetail?activity_id=' + activity_id,
      })
    },

    onFilterParamChange: function (event) {
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

    onPulling: function () {

    },

    getActivityTimeStr: function (activity) {
      let startTime = activity.start_time.replace('T', ' ').replace(/-/g, ".");
      let endTime = activity.end_time.replace('T', ' ').replace(/-/g, ".");
      let timeStr = "";
      if (activity.duration.day != 0) {
        timeStr = startTime.substr(0, 10) + " - " + endTime.substr(0, 10)
      } else {
        timeStr = startTime.substr(0, 16) + "-" + endTime.substr(11, 5)
      }
      return timeStr;
    },

    getActivityFee: function (activity) {
      let fee = "";
      if (activity.is_fee_needed) {
        fee = "¥" + activity.activity_fee;
      } else {
        fee = "免费";
      }
      return fee;
    },
   
  }
})