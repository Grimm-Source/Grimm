const {
  getNeedPickupImpaired,
} = require('../../utils/requestUtil.js');

const app = getApp();

Page({
  data: {
    selectShow: false, //控制下拉列表的显示隐藏，false隐藏、true显示
    selectData: ['区域', '上海'], //下拉列表的数据
    index: 0, //选择的下拉列表下标
    pickupList: [],
    avatarUrl: '../../images/avatar.jpeg',
    cardDetailVisible: false,
    pickupRequirementItems: [
      {value: '0', name: '接视障人士参加活动',checked:false,items:[
        {value: '0_1', name: '私家车'},
        {value: '0_1', name: '步行地铁'}
      ]},
      {value: '1', name: '送视障人士回家',checked:false,items:[
        {value: '1_0', name: '私家车'},
        {value: '1_1', name: '步行地铁'}
      ]},
      {value: '2', name: '接送视障人士参加活动',checked:false,items:[
        {value: '2_0', name: '私家车'},
        {value: '2_1', name: '步行地铁'}
      ]},
    ],
    title: '',
    date: '',
    address: '',
    activityId: '',
    cardInfo: {
      avatarUrl: '',
      name: '',
      address: '',
      provideService: '',
    }
  },

  onLoad: function (options) {
    this.setData({
      avatarUrl: app.globalData.userInfo.avatarUrl,
      activityId: options.activityId == 'undefined' ? '': options.activityId, 
      title: options.title == 'undefined' ? '': options.title, 
      date: options.date == 'undefined' ? '': options.date, 
      address: options.address == 'undefined' ? '': options.address,
    })
  },

  onShow: function () {
    getNeedPickupImpaired(this.data.activityId, (res) => {
      console.log('Get impired pickup info.')
      this.setData({
        pickupList: [
          {'name': '张思锐', 'address': '上海市静安区曹家渡街道', 'avatarUrl': '../../images/avatar.jpeg', 'openid': 'aaaaaa', 'provideService': []},
          {'name': '李小佛', 'address': '上海市静安区曹家渡街道', 'avatarUrl': '../../images/avatar.jpeg', 'openid': 'bbbbbb', 'provideService': []},
          {'name': '王飞舞', 'address': '上海市静安区曹家渡街道', 'avatarUrl': '../../images/avatar.jpeg', 'openid': 'cccccc', 'provideService': []}
        ]
      })
    });
  },

  checkboxChange(e) {
    console.log('checkbox发生change事件，携带value值为：', e.detail.value)
    this.setData({ provideService: e.detail.value })
    const items = this.data.pickupRequirementItems
    const values = e.detail.value
    for (let i = 0, lenI = items.length; i < lenI; ++i) {
      items[i].checked = false
      for (let x = 0, lenX = items[i].items.length; x < lenX; ++x) {
        items[i].items[x].checked = false
        for (let j = 0, lenJ = values.length; j < lenJ; ++j) {
          if(items[i].items[x].value === values[j]){
            items[i].items[x].checked = true
            break
          }
        } 
       } 
      for (let j = 0, lenJ = values.length; j < lenJ; ++j) {
        if (items[i].value === values[j]) {
          items[i].checked = true
          break
        }
      }
    }

    this.setData({
      items
    })
  },

  // 点击下拉显示框
  selectTap() {
    this.setData({
      selectShow: !this.data.selectShow
    });
  },
  // 点击下拉列表
  optionTap(e) {
    let Index = e.currentTarget.dataset.index; //获取点击的下拉列表的下标
    this.setData({
      index: Index,
      selectShow: !this.data.selectShow
    });
  },

  clickCardDetail: function(event) {
    console.log('click card detail button')
    var item = event.currentTarget.dataset.item
    this.setData({
      cardDetailVisible: true,
      cardInfo: {
        avatarUrl: item.avatarUrl,
        name: item.name,
        address: item.address,
        pickupItemDetail: '',
      }
    })
  },

  onTapCardDetailConfirm: function() {
    wx.showToast({
      title: '提交成功',
      icon: 'success', 
      duration: 2000
    });
    this.setData({ cardDetailVisible: false })
  },

  onTapCardDetailCancel: function() {
    this.setData({ cardDetailVisible: false })
  },

  tabMapArea: function() {
    wx.showToast({
      title: '暂不支持',
      icon: 'none', 
      duration: 2000
    });
  }
})