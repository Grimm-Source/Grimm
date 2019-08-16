const apiUrl = require('../config.js').apiUrl;

function getProfile(id, successCallback, failCallback){
    return wx.request({
        url: `${apiUrl}profile/${id}`, //仅为示例，并非真实的接口地址
        header: {
          'content-type': 'application/json' // 默认值
        },
        method: "GET",
        success (res) {
            successCallback(res);
        },
        fail(res){
            failCallback(res);        
        }
    });
}

function updateProfile(userInfo, successCallback, failCallback){
    return wx.request({
        url: `${apiUrl}profile`, //仅为示例，并非真实的接口地址
        header: {
          'content-type': 'application/json' // 默认值
        },
        data: userInfo,
        method: "POST",
        success (res) {
            successCallback(res);
        },
        fail(res){
            failCallback(res);        
        }
    });
}

function getVerifyCode(mobile){
    //get
}

function verifyCode(obj, successCallback, failCallback){
    //send
    let {mobile, code} = obj;
    successCallback();
}


module.exports = {
    getProfile,
    updateProfile,
    getVerifyCode,
    verifyCode
}
  