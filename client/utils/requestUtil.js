const {request} = require('interceptor.js');

function getProfile(id, successCallback, failCallback){
    return request({
        url: `profile/${id}`, 
        success: successCallback,
        fail: failCallback
    });
}

function updateProfile(userInfo, successCallback, failCallback){
    return request({
        url: `profile`, 
        method: "POST",
        data: userInfo,
        success: successCallback,
        fail: failCallback
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
  