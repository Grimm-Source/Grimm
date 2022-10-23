const {
  getPickupDetailInfo,
  setPickupDetailInfo
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
    pickupRequirementItems: [{
        value: '0',
        name: '接视障人士参加活动',
        items: [{
            value: '0_1',
            name: '私家车'
          },
          {
            value: '0_2',
            name: '步行地铁'
          }
        ]
      },
      {
        value: '1',
        name: '送视障人士回家',
        items: [{
            value: '1_0',
            name: '私家车'
          },
          {
            value: '1_1',
            name: '步行地铁'
          }
        ]
      },
      {
        value: '2',
        name: '接送视障人士参加活动',
        items: [{
            value: '2_0',
            name: '私家车'
          },
          {
            value: '2_1',
            name: '步行地铁'
          }
        ]
      },
    ],
    title: '',
    date: '',
    address: '',
    activity_id: '',
    cardInfo: {
      avatarUrl: '',
      name: '',
      address: '',
      provideService: '',
    },
    itemChecked: false

  },

  onLoad: function (options) {
    this.setData({
      avatarUrl: app.globalData.userInfo.avatarUrl,
      activity_id: options.activity_id == 'undefined' ? '' : options.activity_id,
      title: options.title == 'undefined' ? '' : options.title,
      date: options.date == 'undefined' ? '' : options.date,
      address: options.address == 'undefined' ? '' : options.address,
    })
  },

  onShow: function () {
    console.log("detail page...")
    getPickupDetailInfo(this.data.activity_id, (res) => {
      console.log('Get impired pickup info.', res);
      let pickupList = [];
      if (res && res.length > 0) {
        for (let i = 0; i < res.length; i++) {
          pickupList.push({
            'name': res[i]['name'],
            'address': res[i]['pickup_addr'],
            'avatarUrl': res[i]['avatar_url'] ? res[i]['avatar_url'] : '../../images/avatar.jpeg',
            'openid': res[i]['openid'],
            'pickup_method': res[i]['pickup_method'] ? res[i]['pickup_method'] : []
          })
        }
      } else {
        wx.showModal({
          title: '提示',
          content: '当前没有视障人士需要帮助',
          showCancel: false,
        })
      }
      this.setData({
        pickupList: pickupList
      })
    });
  },

  checkboxChange(e) {
    console.log('checkbox发生change事件，携带value值为：', e.detail.value)
    this.setData({
      provideService: e.detail.value
    })
    const items = this.data.pickupRequirementItems
    const values = e.detail.value
    this.setData({
      itemChecked: false
    })
    for (let i = 0, lenI = items.length; i < lenI; ++i) {
      items[i].checked = false
      for (let x = 0, lenX = items[i].items.length; x < lenX; ++x) {
        items[i].items[x].checked = false
        for (let j = 0, lenJ = values.length; j < lenJ; ++j) {
          if (items[i].items[x].value === values[j]) {
            items[i].items[x].checked = true
            this.setData({
              itemChecked: true
            })
            break
          }
        }
      }
      for (let j = 0, lenJ = values.length; j < lenJ; ++j) {
        if (items[i].value === values[j]) {
          items[i].checked = true
          this.setData({
            itemChecked: true
          })
          break
        }
      }
    }

    this.setData({
      pickupRequirementItems: items
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

  clickCardDetail: function (event) {
    console.log('click card detail button')
    var item = event.currentTarget.dataset.item
    debugger
    var pickDetail = [
      {value: '0', name: '接视障人士参加活动', checked: false, items:[
        {value: '0_1', name: '私家车', checked: false},
        {value: '0_2', name: '步行地铁', checked: false}
      ]},
      {value: '1', name: '送视障人士回家', checked: false, items:[
        {value: '1_0', name: '私家车', checked: false},
        {value: '1_1', name: '步行地铁', checked: false}
      ]},
      {value: '2', name: '接送视障人士参加活动', checked: false, items:[
        {value: '2_0', name: '私家车', checked: false},
        {value: '2_1', name: '步行地铁', checked: false}
      ]},
    ]
    let method = item.pickup_method.split(",")
    if (method.indexOf("0") > -1){
      pickDetail[0]['checked'] = true
      if (method.indexOf("0_1") > -1){
        pickDetail[0]['items'][0]['checked'] = true
      }
      if (method.indexOf("0_2") > -1){
        pickDetail[0]['items'][1]['checked'] = true
      }
    }
    if (method.indexOf("1") > -1){
      pickDetail[1]['checked'] = true
      if (method.indexOf("1_0") > -1){
        pickDetail[1]['items'][0]['checked'] = true
      }
      if (method.indexOf("1_1") > -1){
        pickDetail[1]['items'][1]['checked'] = true
      }
    }
    if (method.indexOf("2") > -1){
      pickDetail[2]['checked'] = true
      if (method.indexOf("2_0") > -1){
        pickDetail[2]['items'][0]['checked'] = true
      }
      if (method.indexOf("2_1") > -1){
        pickDetail[2]['items'][1]['checked'] = true
      }
    }
    this.setData({
      impairedOpenid: item['openid'],
      cardDetailVisible: true,
      cardInfo: {
        avatarUrl: item.avatarUrl,
        name: item.name,
        address: item.address,
        pickupItemDetail: '',
      },
      pickupRequirementItems: pickDetail
    })
  },

  onTapCardDetailConfirm: function () {
    if (!this.data.itemChecked || !this.data.provideService || this.data.provideService.length == 0) {
      wx.showModal({
        title: '提示',
        content: '请填写您可以提供的志愿者服务',
        showCancel: false,
      })
      return;
    }
    setPickupDetailInfo({
      "activity_id": this.data.activity_id,
      "impairedOpenid": this.data.impairedOpenid,
      "pickupMethod": this.data.provideService.join(','),
    }, (res) => {
      let that = this
      wx.showToast({
        title: '提交成功',
        icon: 'success',
        duration: 2000
      });
      that.onLoad(that.data);
      this.setData({
        cardDetailVisible: false
      })
    }, (err) => {
      wx.showModal({
        showCancel: false,
        title: '提交失败',
        content: err || "网络失败，请稍候再试"
      });
    });
  },

  onTapCardDetailCancel: function () {
    this.setData({
      cardDetailVisible: false
    })
  },

  tabMapArea: function () {
    wx.showToast({
      title: '暂不支持',
      icon: 'none',
      duration: 2000
    });
  }
})
