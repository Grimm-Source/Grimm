const {getProfile, postRegisteredActivityList} = require('../../utils/requestUtil.js');
const {userInfoMessage} = require('../../utils/messageHelper.js');

Page({
  data: {
    apply: {},
    activityId: null,
    role: null,
    message: userInfoMessage
  },
  //事件处理函数
  onLoad: function (option) {
    if(!option.activityId){
      return;
    }
    this.setData({
        activityId: option.activityId
    });
    this.getContactInfo();
  }, 
  getContactInfo: function (){
    getProfile((res)=>{
        this.setData({
          apply: {
              tel: res.linktel,
              address: res.linkaddress,
              needPickUp: false,
              toPickUp: false
          },
          role: res.role
        })
    }); 
  },
  bindInputChange: function(e){
    let apply = this.data.apply,
    key = e.currentTarget.dataset['infoKey'];
    apply[key] = e.detail && e.detail.value || "";
    this.setData({
      apply
    });
  },
  checkboxChange: function (e) {
    let apply = this.data.apply;
    if(this.data.role === "视障人士"){
        apply["needPickUp"] = !apply["needPickUp"]   
    }else{
        apply["toPickUp"] = !apply["toPickUp"]
    }
    this.setData({apply})
  },
  onTapSubmit: function(){
    if(!this.__validate("linktel", this.data.apply && this.data.apply.tel)){
      wx.showToast({
        title: userInfoMessage["linktel"]["message"],
        icon: 'none',
        duration: 2000
      });
      return;
    }else if(!this.__validate("linkaddress", this.data.apply && this.data.apply.address)){
      wx.showToast({
        title: userInfoMessage["linkaddress"]["message"],
        icon: 'none', //error
        duration: 2000
      });
      return;
    }
    let obj = {
        activityId: + this.data.activityId,
        ...this.data.apply
    };
    if(this.data.role === "视障人士"){
        delete obj["toPickUp"];
        obj["needPickUp"] = obj["needPickUp"]?1:0;
    }else{
        delete obj["needPickUp"];
        obj["toPickUp"] = obj["toPickUp"]?1:0;
    }

    postRegisteredActivityList([obj],()=>{
      wx.navigateTo({
          url: '/pages/activityDetail/activityDetail?activity_id='+ this.data.activityId
      })
    },(message)=>{
      wx.showToast({
        title: message || '报名失败',
        icon: 'none', //error
        duration: 2000
      });
    });
  },
  __validate: function(key, value){
    let mobile = /^(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\d{8}$/,
    phone = /^((\d{7,8})|(\d{4}|\d{3})-(\d{7,8})|(\d{4}|\d{3})-(\d{7,8})-(\d{4}|\d{3}|\d{2}|\d{1})|(\d{7,8})-(\d{4}|\d{3}|\d{2}|\d{1}))$/;
    switch(key) {
      case "linktel":
        return !!value && (mobile.test(value) || phone.test(value));
      default:
        return !!value
    }
  },
})
