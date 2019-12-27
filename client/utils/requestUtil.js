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

const getRegisterStatus = (code, successCallback, failCallback) => {
    return request({
        url: 'jscode2session?js_code=' + code,
        success: successCallback,
        fail: failCallback,
        method: "GET"
    }); 
}

const getActivityList = (successCallback, failCallback) => {
    return request({
        url: 'activities',
        success: successCallback,
        fail: failCallback,
        method: "GET"
    }); 
}

const getRegisteredActivityList = (idList, successCallback, failCallback) => {
    let url = 'registeredActivities';
    if(idList){
        let idString = "";
        for(let i = 0; i < idList.length;i++){
            if(i === idList.length - 1){
                idString += `${idList[i]}`;
                break;
            }
            idString += `${idList[i]},`;
        }
        url += "?activityId=" + idString
    }
    return request({
        url,
        success: successCallback,
        fail: failCallback,
        method: "GET"
    }); 
}

const postRegisteredActivityList = (obj, successCallback, failCallback) => {
    return request({
        url: 'registeredActivities',
        success: successCallback,
        fail: failCallback,
        method: "POST",
        data: obj
    }); 
}

const removeRegisteredActivityList = (obj, successCallback, failCallback) => {
    return request({
        url: 'registeredActivities',
        success: successCallback,
        fail: failCallback,
        method: "DELETE",
        data: obj
    }); 
}

module.exports = {
    getProfile,
    updateProfile,
    getVerifyCode,
    verifyCode,
    register,
    getRegisterStatus,
    getActivityList,
    getRegisteredActivityList,
    postRegisteredActivityList,
    removeRegisteredActivityList
}
  