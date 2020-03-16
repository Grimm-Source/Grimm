// components/myActivities/myActivitiesList.js
const { getActivityList, getFilteredActivities, getActivityTypes } = require('../../utils/requestUtil.js');

const myActivitiesType = {
  MYALL: 0,
  REGISTERED: 1,
  INTERESTED: 2,
  JOINED: 3
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

    myAllActivities: [
      { 'id': '0', 'time': '2020-01-01 13:30-14:30', 'location': '世纪公园', 'title': '世纪公园新年暴走dfsafdsafdsa', state: 'joined', statestring: '报名成功' },
      { 'id': '1', 'time': '2020-01-01 13:30-14:30', 'location': '世纪公园', 'title': '世纪公园新年暴走', state: 'interested', statestring: '感兴趣' },
      { 'id': '2', 'time': '2020-01-01 13:30-14:30', 'location': '世纪公园', 'title': '世纪公园新年暴走dfsafdsafdsa', state: 'closed', statestring: '已结束' },
    ],

    myRegisteredActivities: [
      { 'id': '0', 'time': '2020-01-01 13:30-14:30', 'location': '世纪公园', 'title': '世纪公园新年暴走dfsafdsafdsa', state: 'joined', statestring: '报名成功' },
    ],
    myInterestedActivites: [
      { 'id': '1', 'time': '2020-01-01 13:30-14:30', 'location': '世纪公园', 'title': '世纪公园新年暴走', state: 'interested', statestring: '感兴趣' },
    ],
    myJoinedActivities: [
      { 'id': '2', 'time': '2020-01-01 13:30-14:30', 'location': '世纪公园', 'title': '世纪公园新年暴走dfsafdsafdsa', state: 'closed', statestring: '已结束' }
    ],
  },

  /**
   * 组件的方法列表
   */
  methods: {
    _setMyActivities: function (filterType, res) {
      console.log(res);
      let selectedActivities = null;

      if (filterType == myActivitiesType.MYALL) {
        selectedActivities = this.data.myAllActivities;
      }
      else if (filterType == myActivitiesType.REGISTERED) {
        selectedActivities = this.data.myRegisteredActivities;
      }
      else if (filterType == myActivitiesType.INTERESTED) {
        selectedActivities = this.data.myInterestedActivites;
      }
      else if (filterType == myActivitiesType.JOINED) {
        selectedActivities = this.data.myJoinedActivities;
      }

      if(selectedActivities == null) {
        console.log("Wrong selected index : " + filterType);
      }

      this.setData({
        myActivities: selectedActivities,
        selectedActivities: filterType
      });
    },
    
    onTapActivity: function (event) {
      wx.navigateTo({
        url: '/pages/activityDetail/activityDetail?id=1',
      })
    },

    onFilterParamChange: function (type) {
      console.log("sxx: " + type);
      
      if (type == myActivitiesType.MYALL) {
        let myAllActivities = this.data.myRegisteredActivities.concat(this.data.myInterestedActivites, this.data.myJoinedActivities);
      }

      this._setMyActivities(type, null);
      // getFilteredActivities(params, (res) => {
      //   this._setMyActivities(res);
      // });
    }
  }
})
