//app.js
const {getRegisterStatus} = require('utils/requestUtil.js');
App({
  globalData: {
    userInfo: null,
    isAuthorized: false,
    isRegistered: false
  },
  
  onLaunch: function () {

  }
})