// components/activeSignIn/activeSignIn.js
const {
  getCertificatectivity,
  getFilteredActivities
} = require('../../utils/requestUtil.js');

Component({
  /**
   * Component properties
   */
  properties: {},

  /**
   * Component initial data
   */
  data: {
    activities: [],
    

  },

  pageLifetimes: {
    show: function () {
      console.log("1111getCertificatectivity:")
      getCertificatectivity((res) => {
        console.log("getCertificatectivity:", res)

        this._setActivities(res.activities);

      })
    }
  },
  /**
   * Component methods
   */
  methods: {
    _setActivities: function (activities) {
      let needActivities = [];
      for (let index = 0; index < activities.length; index++) {
        let activity = activities[index];
        activity.schedule = this.getActivityTimeStr(activity);
        // activity.fee = this.getActivityFee(activity);
        const startTime = new Date(activity.start_time).getTime()
        const nowTime = new Date().getTime()
        const lastMinutes = Math.floor((startTime - nowTime) / (1000 * 60))
        // if (lastMinutes < 17200) { //后续上线需要为30，表示30分钟内
          needActivities.push(activity);
        // }
      }
      this.setData({
        activities: needActivities
      });
    },
    getActivityTimeStr: function (activity) {
      let startTime = activity.start_time.replace('T', ' ').replace(/-/g, ".");
      let endTime = activity.end_time.replace('T', ' ').replace(/-/g, ".");
      let timeStr = "";
      timeStr = startTime.substr(5, 11) + " - " + endTime.substr(5, 11)
      // if (activity.duration.day != 0) {
      // } else {
      //   timeStr = startTime.substr(0, 16) + "-" + endTime.substr(11, 5)
      // }
      return timeStr;
    },
    onTapSignIn: function (event) {
      let item = event.currentTarget.dataset && event.currentTarget.dataset.item,
        activity_id = item.id;
      if (activity_id == null) {
        return;
      }
      wx.navigateTo({
        url: '/pages/signIn/signIn?id=' + activity_id,
      })
    },
  }
})