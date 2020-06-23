const { request } = require('interceptor.js');

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

const verifyCode = (obj, successCallback, failCallback) => {
    return request({
        url: "smscode",
        data: obj,
        method: 'POST',
        success: successCallback,
        fail: failCallback,
    })
}

const register = (obj, successCallback, failCallback) => {
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

const getActivityTypes = (successCallback, failCallback) => {
    return request({
        url: 'tags',
        success: successCallback,
        fail: failCallback,
        method: "GET",
    })
}

const getActivityList = (successCallback, failCallback) => {
    return request({
        url: 'activities',
        success: successCallback,
        fail: failCallback,
        method: "GET"
    });
}

const getFilteredActivities = (filteredParams, successCallback, failCallback) => {
    return request({
        url: "activities?" + filteredParams,
        success: successCallback,
        fail: failCallback,
        method: "GET"
    });
}

const getActivity = (activityId, successCallback, failCallback) => {
    return request({
        url: 'activity/' + activityId,
        success: successCallback,
        fail: failCallback,
        method: "GET"
    });
}

const getRegisteredActivityList = (idList, successCallback, failCallback) => {
    return request({
        url: arrToUrl("registeredActivities", idList, "activityId"),
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

const removeRegisteredActivityList = (idList, successCallback, failCallback) => {
    return request({
        url: arrToUrl("registeredActivities", idList, "activityId"),
        success: successCallback,
        fail: failCallback,
        method: "DELETE"
    });
}

const arrToUrl = (baseUrl, arr, key) => {
    if (!arr || arr.length < 1) {
        return baseUrl;
    }
    let paramUrl = "";
    for (let i = 0; i < arr.length; i++) {
        if (i === arr.length - 1) {
            paramUrl += `${arr[i]}`;
            break;
        }
        paramUrl += `${arr[i]},`;
    }
    return `${baseUrl}?${key}=${paramUrl}`;
}

const getCarousel = (successCallback, failCallback) => {
    return request({
        url: 'carousel',
        success: successCallback,
        fail: failCallback,
        method: "GET"
    });
}

const getActivityDetail = (activityId, successCallback, failCallback) => {
    return request({
        url: `activity_detail?activityId=${activityId}`,
        success: successCallback,
        fail: failCallback,
        method: "GET"
    });
}

const toggleInterest = (activityId, isInterest, successCallback, failCallback) => {
    return request({
        url: `activity_detail/interest?activityId=${activityId}&interest=${isInterest ? 1 : 0}`,
        success: successCallback,
        fail: failCallback,
        method: "POST"
    });
}

const toggleThumbsUp = (activityId, isThumbsUp, successCallback, failCallback) => {
    return request({
        url: `activity_detail/thumbs_up?activityId=${activityId}&thumbs_up=${isThumbsUp ? 1 : 0}`,
        success: successCallback,
        fail: failCallback,
        method: "POST"
    });
}

const toggleRegister = (activityId, isSignUp, successCallback, failCallback) => {
    if(isSignUp){
        return postRegisteredActivityList({activityId}, successCallback, failCallback);

    }
    return removeRegisteredActivityList([activityId], successCallback, failCallback);
}

const shareActivity = (activityId) => {
    return request({
        url: `activity_detail/share?activityId=${activityId}`,
        method: "POST"
    });
}

const getMyActivities = (type, successCallback, failCallback) => {
    return request({
        url: 'myActivities?filter=' + type,
        method: 'GET',
        success: successCallback,
        fail: failCallback,
    })
}

const getPhoneNumber = (obj, successCallback, failCallback) => {
  return request({
    url: 'getPhoneNumber',
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
    register,
    getRegisterStatus,
    getActivityTypes,
    getActivityList,
    getFilteredActivities,
    getActivity,
    getRegisteredActivityList,
    postRegisteredActivityList,
    removeRegisteredActivityList,
    getCarousel,
    getActivityDetail,
    toggleInterest,
    toggleThumbsUp,
    toggleRegister,
    shareActivity,
    getMyActivities,
    getPhoneNumber
}
