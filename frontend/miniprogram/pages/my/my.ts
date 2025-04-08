// pages/my/my.ts
import Toast from '@vant/weapp/toast/toast'
const { request } = require('../../utils/request')
const app = getApp()

Page({

  /**
   * 页面的初始数据
   */
  data: {
    isRegistered: false,
    auditStatus: '', // pending
    role: '', // volunteer
    name: '',
    phone: '',
    activitiesJoined: 0,
    joindHours: 0,
    gradientColor: {
      '0%': '#ffd01e',
      '100%': '#ee0a24',
    },
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad() {
    this.init()
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady() {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow() {
    this.init()
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide() {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload() {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh() {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom() {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage() {

  },

  _isRegisteredModal() {
    wx.showModal({
      title: "请先登录或注册，然后报名活动",
      showCancel: true,
      cancelText: "再想想",
      confirmText: "立即注册",
      success: function (res) {
        if (res.confirm) {
          wx.switchTab({
            url: '/pages/my/my'
          })
        }
      }
    })
  },

  navigateToMyActivityList() {
    if (!app.globalData.isRegistered) {
      this._isRegisteredModal()
      return
    }
    wx.navigateTo({
      url: '/pages/myActivityList/myActivityList'
    })
  },

  async onLogoutTap() {
    wx.showModal({
      title: '提示',
      content: '确定要退出登录吗？',
      success: (res) => {
        if (res.confirm) {
          this.setData({
            isRegistered: false,
            auditStatus: '',
            role: '',
            name: '',
            phone: '',
            activitiesJoined: 0,
            joindHours: 0
          })
          try {
            app.globalData.isRegistered = false
            app.globalData.auditStatus = ''
            app.globalData.role = ''
            wx.removeStorageSync('openid')
            wx.showToast({
              title: "退出成功",
              icon: 'success',
              duration: 2000
            })
          } catch (e) {
            wx.showToast({
              title: "退出失败，请联系管理员",
              icon: 'none',
              duration: 2000
            })
          }
        }
      }
    })
  },

  async init() {
    if (wx.getStorageSync('openid')) {
      Toast.loading({ message: '加载中...', forbidClick: true, duration: 0 })
      wx.login({
        success: async (res) => {
          try {
            const userInfo = await request('jscode2session', 'POST', {
              js_code: res.code,
              avatar_url: ''
            })
            app.globalData.isRegistered = userInfo.isRegistered
            app.globalData.auditStatus = userInfo.auditStatus
            app.globalData.role = userInfo.role
            wx.setStorageSync('openid', userInfo.openid)
            if (userInfo.isRegistered) {
              const user = await request(`profile`, 'GET', {})
              let auditStatus = ''
              if (userInfo.auditStatus === 'pending') {
                auditStatus = '待审核'
              } else if (auditStatus === 'approved') {
                auditStatus = '已审核';
              } else {
                auditStatus = '已拒绝';
              }
              this.setData({
                isRegistered: userInfo.isRegistered,
                role: userInfo.role === 'volunteer' ? '志愿者' : '视障人士',
                auditStatus: auditStatus,
                name: user.name,
                phone: user.phone,
                activitiesJoined: user.activitiesJoined,
                joindHours: user.joindHours
              })
            }
            Toast.clear()
          } catch (error) {
            console.error('请求失败：', error)
          }
        }
      })
    }
  },

  getPhoneNumber(event) {
    const { iv, encryptedData } = event.detail
    if (iv && encryptedData) {
      Toast.loading({ message: '加载中...', forbidClick: true, duration: 0 })
      wx.login({
        success: async (res) => {
          try {
            const userInfo = await request('jscode2session', 'POST', {
              js_code: res.code,
              avatar_url: ''
            })
            app.globalData.isRegistered = userInfo.isRegistered
            app.globalData.auditStatus = userInfo.auditStatus
            app.globalData.role = userInfo.role
            wx.setStorageSync('openid', userInfo.openid)
            if (userInfo.isRegistered) {
              const user = await request(`profile`, 'GET', {})
              // console.log('user', user)
              let auditStatus = ''
              if (userInfo.auditStatus === 'pending') {
                auditStatus = '待审核'
              } else if (auditStatus === 'approved') {
                auditStatus = '已审核';
              } else {
                auditStatus = '已拒绝';
              }
              this.setData({
                isRegistered: userInfo.isRegistered,
                role: userInfo.role === 'volunteer' ? '志愿者' : '视障人士',
                auditStatus: auditStatus,
                name: user.name,
                phone: user.phone,
                activitiesJoined: user.activitiesJoined,
                joindHours: user.joindHours
              })
              Toast.clear()
              wx.showToast({
                title: "欢迎回来",
                icon: 'success',
                duration: 2000
              })
            } else {
              this._getPhoneNumber(res.code, encryptedData, iv)
              Toast.clear()
            }
          } catch (error) {
            console.error('请求失败：', error)
          }
        }
      })
    }
  },

  _getPhoneNumber(js_code, encryptedData, iv) {
    wx.login({
      success: async (res) => {
        const response = await request('getPhoneNumber', 'POST', {
          js_code: res.code,
          encryptedData,
          iv
        })
        if (response.status === 'success') {
          response.openid
          wx.navigateTo({
            url: `/pages/register/register?phone=${response.decrypt_data.purePhoneNumber}`
          })
        }
      }
    })
  },
})