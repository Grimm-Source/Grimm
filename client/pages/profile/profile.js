const {userInfoMessage} = require('../../utils/messageHelper.js');
const {getVerifyCode, verifyCode, getProfile, updateProfile} = require('../../utils/requestUtil.js');

Page({
  
  data: {
    meta:{
      genderArray: ["男","女"],
      birthdayStartDate: "1910-01-01",
      birthdayEndDate: (new Date).toJSON().split("T")[0],
    },
    message: userInfoMessage
  },

  onShow: function (options) {
    this.__initData();
    this.__getProfile();
  },

  updateProfile: function(e){
    if(!this.data.ui.isFormValid){
      return;
    }
    if(!this.__isUserInfoUpdated()){
      wx.showToast({
        title: '请更新后提交',
        duration: 1000
      });
      return;
    }
    this.__updateProfile();
  },

  getCode: function(e){
    getVerifyCode(this.data.userInfo.tel);
    this.__setUis({
      "isCodeSent": true,
      "telNeedValidate": this.data.userInfo.tel 
    });
    this.__updateTimer();
  },

  validateCode: function(){
    if(!this.data.code || this.data.code.length !== 6){
      return;
    }
    if(this.data.ui.telNeedValidate !== this.data.userInfo.tel){ //incase the user change the number after get a code
      wx.showToast({
        title: '验证失败',
        icon: 'none', //error
        duration: 2000
      });
      return;
    }
    verifyCode({ 
      tel: this.data.userInfo.tel, 
      verification_code: this.data.code
    },()=>{
        wx.showToast({
          title: '验证成功',
          icon: 'success', //error
          duration: 2000
        });
        clearInterval(this.timer);
        this.setData({"code": ""});
        this.__setError("tel",false);
        this.__setUis({
          "isCodeSent": false,
          "leftTimeLabel": `获取验证码`,
          "isTelValid": true,
          "tel": false
        });
        this.__validateAll();
    },()=>{
      wx.showToast({
        title: '验证码错误',
        icon: 'none', //error
        duration: 2000
      });
    });
  },

  bindInputChange: function(e){
    switch( e.currentTarget.dataset['infoKey']) {
      case "tel": 
        this.__bindTelChange(e);
        break;
      case "code": 
        this.setData({"code": e.detail && e.detail.value});
        break;
      case "gender":
        this.__updateUserInfo("gender", this.data.meta.genderArray[e.detail && Number(e.detail.value)]);
        break;
      default:
        this.__updateUserInfo(e.currentTarget.dataset['infoKey'], e.detail && e.detail.value);
    }
  },

  tapError: function(e){
    let key = e.currentTarget.dataset['infoKey'];
    wx.showToast({
      title: userInfoMessage[key]["message"],
      icon: 'none',
      duration: 2000
    });
  },

  __initData: function(){
    this.setData({
      code:"",
      ui:{
          isTelChanged: false,
          leftTimeLabel: "获取验证码",
          isCodeSent: false,
          isTelValid: true,
          telNeedValidate: null,
          isFormValid: false,
          isLoadingValid: false,
          isLoadingUpdate: false,
          auditStatus: wx.getStorageSync('auditStatus')
      },
      error: {
        tel: false,
        linkaddress: false,
        linktel: false,
        emergencyPerson: false,
        emergencyTel: false
      }
    });
  },

  __bindTelChange: function(e){
    if((e.detail && e.detail.value) === this.data.userInfo.tel){
      return;
    }
    this.__setUis({
      "isTelChanged": true,
      "isTelValid": false
    });
    this.setData({"code": ""});
    this.__updateUserInfo("tel", e.detail && e.detail.value);
  },

  __updateUserInfo: function(key, value = null, isIgnoreValid){
    let userInfo = this.data && this.data.userInfo;
    userInfo[key] = value.trim();
    this.setData({
        userInfo
    });
    if(!isIgnoreValid && !this.__validate(key, value)){
      this.__setUi("isFormValid", false);
      this.__setError(key, true);
    }else{
      this.__validateAll();
    }
  },

  __isUserInfoUpdated: function(){
    let userInfo = this.data && this.data.userInfo;
    let userInfoSource = this.data && this.data.userInfoSource;
    for(var key in userInfo){
      if( userInfo[key] !== userInfoSource[key]){
        return true;
      }
    }
    return false;
  },

  __setUi: function(key, value){
    let ui = this.data && this.data.ui;
      ui[key] = value;
      this.setData({
        ui
      });
  },

  __setError: function(key, value){
    let error = this.data && this.data.error;
      error[key] = value;
      this.setData({
        error
      });
  },

  __setUis: function(obj){
    for(let key in obj){
      this.__setUi(key, obj[key]);
    }
  },

  __validate: function(key, value){
    if(key==="usercomment"){
      return true;
    }
    let name = /^[\u4E00-\u9FA5A-Za-z\s]+(·[\u4E00-\u9FA5A-Za-z]+)*$/, //中英文名包括点或者空格
    mobile = /^(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\d{8}$/,
    phone = /^((\d{7,8})|(\d{4}|\d{3})-(\d{7,8})|(\d{4}|\d{3})-(\d{7,8})-(\d{4}|\d{3}|\d{2}|\d{1})|(\d{7,8})-(\d{4}|\d{3}|\d{2}|\d{1}))$/;
    switch(key) {
      case "emergencyPerson":
          if(this.data.userInfo.role !== "视障人士"){
            return true;
          }
          return !!value && name.test(value);
      case "tel":
        return !!value && mobile.test(value) && this.data.ui.isTelValid;
      case "emergencyTel":
        if(this.data.userInfo.role !== "视障人士"){
          return true;
        }
      case "linktel":
        return !!value && (mobile.test(value) || phone.test(value));
      case "disabledID":
        if(this.data.userInfo.role !== "视障人士"){
          return true;
        }
      default:
        return !!value
    }
  },

  __validateAll: function(){
    let isValidate = true;
    for(let key in this.data.userInfo){
      if(!this.__validate(key, this.data.userInfo[key])){
        console.error(`key%%%%%%${key}%%%%%%%value%%%%%%%${this.data.userInfo[key]}`)
        isValidate = false;
        this.__setError(key, true);
      }else{
        console.log(`key%%%%%%${key}%%%%%%%value%%%%%%%${this.data.userInfo[key]}`)
        this.__setError(key, false);
      }
    }
    this.__setUi("isFormValid", isValidate);
  },

  __updateTimer: function(){
    let time = 60;
    this.timer = setInterval(() => {
      this.__setUi("leftTimeLabel", `${time--}秒后再试`);
      if(time < 0){
        time = 60;
        clearInterval(this.timer);
        this.__setUi("isCodeSent", false);
        this.__setUi("leftTimeLabel", `获取验证码`);
      }
    }, 1000);
  },

  __getProfile: function(){
    return getProfile((data) => {
      this.setData({
        userInfo: data,
        userInfoSource: Object.assign({}, data)
      });
    },(err) => {
      wx.showModal({
        title: '提示',
        content: err,
        showCancel: false,
        success () {
          wx.switchTab({
            url: '../home/home',
          });
        }
      });     
    });
  },

  __updateProfile: function(){
    return updateProfile(this.data.userInfo, (res)=>{
      wx.showToast({
        title: '已更新',
        icon: 'success',
        duration: 300
      });
      wx.switchTab({
        url: '../personal/personal',
      });
    },(err)=>{
      wx.showModal({
        showCancel: false,
        title: '更新失败',
        content: err || "网络失败，请稍候再试"
      });  
    });
  }
})