const {request} = require('interceptor.js');

const getProfile = (successCallback, failCallback) => {
    return request({
        url: "profile", 
        success: successCallback,
        fail: failCallback
    });
}

const updateProfile = (userInfo, successCallback, failCallback) => {
    return request({
        url: "profile", 
        method: "POST",
        data: userInfo,
        success: successCallback,
        fail: failCallback
    });
}

const getVerifyCode = (tel) => {
  const requestUrl = "smscode?tel=" + tel
  return request({
      url: requestUrl,
      method: "get"
  });
}

const verifyCode = (obj, successCallback, failCallback) =>{
    return request({
      url: "smscode",
      data: obj,
      method: 'POST',
      success: successCallback,
      fail: failCallback,
    })
}

const register =  (obj, successCallback, failCallback) => {
    return request({
        url: "register", 
        data: obj,
        success: successCallback,
        fail: failCallback,
        method: "POST"
    });
}

module.exports = {
    getProfile,
    updateProfile,
    getVerifyCode,
    verifyCode,
    register
}
  