// components/myActivities/myActivitiesList.js
Component({
  /**
   * 组件的属性列表
   */
  properties: {
    selectedIdx: {
      type: Number,
      observer: function(newIdx) {
        // console.log(newIdx);
        let selectedActivities = this.data.myAllActivities;
        if(newIdx == 1) {
          selectedActivities = this.data.myJoinedActivities;
        }
        else if(newIdx == 2) {
          selectedActivities = this.data.myInterestedActivites;
        }
        else if (newIdx == 3) {
          selectedActivities = this.data.myClosedActivities;
        }

        this.setData({
          myActivities : selectedActivities
        });
      },
    }
  },

  /**
   * 组件的初始数据
   */

  data: {
    selectedActivities: 'myAllActivities',

    myActivities: [
      { 'id': '0', 'time': '2020-01-01 13:30-14:30', 'location': '世纪公园', 'title': '世纪公园新年暴走dfsafdsafdsa', state: 'joined', statestring: '报名成功' },
      { 'id': '1', 'time': '2020-01-01 13:30-14:30', 'location': '世纪公园', 'title': '世纪公园新年暴走', state: 'interested', statestring: '感兴趣' },
      { 'id': '2', 'time': '2020-01-01 13:30-14:30', 'location': '世纪公园', 'title': '世纪公园新年暴走dfsafdsafdsa', state: 'closed', statestring: '已结束' },
    ],

    myAllActivities: [
      { 'id': '0', 'time': '2020-01-01 13:30-14:30', 'location': '世纪公园', 'title': '世纪公园新年暴走dfsafdsafdsa', state: 'joined', statestring: '报名成功' },
      { 'id': '1', 'time': '2020-01-01 13:30-14:30', 'location': '世纪公园', 'title': '世纪公园新年暴走', state: 'interested', statestring: '感兴趣' },
      { 'id': '2', 'time': '2020-01-01 13:30-14:30', 'location': '世纪公园', 'title': '世纪公园新年暴走dfsafdsafdsa', state: 'closed', statestring: '已结束' },
    ],

    myJoinedActivities: [
      { 'id': '0', 'time': '2020-01-01 13:30-14:30', 'location': '世纪公园', 'title': '世纪公园新年暴走dfsafdsafdsa', state: 'joined', statestring: '报名成功' },
    ],
    myInterestedActivites: [
      { 'id': '1', 'time': '2020-01-01 13:30-14:30', 'location': '世纪公园', 'title': '世纪公园新年暴走', state: 'interested', statestring: '感兴趣' },
    ],
    myClosedActivities: [
      { 'id': '2', 'time': '2020-01-01 13:30-14:30', 'location': '世纪公园', 'title': '世纪公园新年暴走dfsafdsafdsa', state: 'closed', statestring: '已结束' }
    ],
  },

  /**
   * 组件的方法列表
   */
  methods: {
    
  }
})
