import {ACTION_TYPES} from './actionTypes';
import request from '../utils/request';
import { ADMIN_PANEL_TYPE, ADMIN_FORM_TYPE } from "../constants";
import { message } from 'antd';

//ui section
export const loading = () =>({ 
    type: ACTION_TYPES.UI_LOADING
});

export const hideLoading = () =>({ 
    type: ACTION_TYPES.UI_LOADING_HIDE
});

export const switchHomeTag = (activeKey) =>({ 
    type: ACTION_TYPES.UI_HOME_TAG_SWITCH,
    activeKey
});

export const switchAdminPanel = (activeKey) =>({ 
    type: ACTION_TYPES.UI_ADMIN_PANEL_SWITCH,
    activeKey
});

export const switchAdminFormType = (activeKey) =>({ 
    type: ACTION_TYPES.UI_ADMIN_FORM_TYPE_SWITCH,
    activeKey
});

export const showActivityModal = (activityId) =>({ 
    type: ACTION_TYPES.UI_ACTIVITY_SHOW,
    activityId
});

export const hideActivityModal = () =>({ 
    type: ACTION_TYPES.UI_ACTIVITY_HIDE
});

//account section
export const loginAccount = (user) => (dispatch, getState) => {
    dispatch(loading());
    return dispatch(verifyAccount(user));
};

const verifyAccount = user => dispatch => {
    return request({
        path: "login",
        method: "POST",
        data: user
    }).then((userInfo) => {
        sessionStorage.setItem("user", JSON.stringify(userInfo));
        dispatch(login(userInfo));    
        dispatch(switchAdminFormType(ADMIN_FORM_TYPE.CREATE));
        message.success('登录成功');
    }, (errorMessage)=>{
        message.error(`登录失败，${errorMessage}`);
    }).finally(()=>{
        dispatch(hideLoading());
    });
}

export const login = (user) => ({
    type: ACTION_TYPES.ACCOUNT_LOGIN,
    user
});

export const logout = ()=>({
    type: ACTION_TYPES.ACCOUNT_LOGOUT
});

//activity section
export const publishActivity = (activity) => (dispatch, getState) => {
    dispatch(loading());
    if(!activity["id"]){
        return dispatch(postActivity(activity));
    }
    return dispatch(updateActivity(activity));
};

const postActivity = activity => dispatch => {
    return request({
        path: `activity`,
        method: "POST",
        data: activity
    }).then(() => {
        dispatch(setActivity({})); 
        dispatch(fetchActivityList());
        message.success('活动发布成功');   
    }, (errorMessage)=>{
        message.error(`活动发布失败，${errorMessage}`);
        dispatch(hideLoading());
    }).finally(()=>{

    });
}

const updateActivity = activity => dispatch => {
    return request({
        path: `activity/${activity.id}`,
        method: "POST",
        data: activity
    }).then(() => {
        dispatch(setActivity({})); 
        dispatch(fetchActivityList());
        message.success('活动发布成功');   
    }, (errorMessage)=>{
        message.error(`活动发布失败，${errorMessage}`);
        dispatch(hideLoading());
    }).finally(()=>{

    });
}

export const getActivity = (id) => (dispatch, getState) => {
    dispatch(loading());
    return dispatch(fetchActivity(id))
};

const fetchActivity = id => dispatch => {
    return request({
        path: `activity/${id}`
    }).then(activity => {
        dispatch(setActivity(activity));    
    }).finally(()=>{
        dispatch(hideLoading());
    });
}

export const setActivity = activity =>({
    type: ACTION_TYPES.UI_ACTIVITY_SET,
    activity
});

export const removeActivity = (activityId) => (dispatch, getState) => {
    dispatch(loading());
    return dispatch(deleteActivity(activityId));
};

const deleteActivity = activityId => dispatch => {
    return request({
        path: `activity/${activityId}`,
        method: "DELETE"
    }).then(() => {
        dispatch(getActivityList());
        message.success('活动删除成功');
    }, (errorMessage)=>{
        message.error(`活动删除失败，${errorMessage}`);
        dispatch(hideLoading());
    });
}

export const getActivityList = () => (dispatch, getState) => {
    dispatch(loading());
    return dispatch(fetchActivityList())
};

const fetchActivityList = id => dispatch => {
    return request({
        path: "activities"
    }).then(activities => {
        dispatch(setActivities(activities));
    }).finally(()=>{
        dispatch(hideLoading());
    });
}

export const setActivities = activities =>({
    type: ACTION_TYPES.ACTIVITY_LIST_SET,
    activities
});

//admin section
export const publishAdmin = (admin) => (dispatch, getState) => {
    dispatch(loading());
    return dispatch(postAdmin(admin));
};

const postAdmin = admin => dispatch => {
    return request({
        path: `admin`,
        method: "POST",
        data: admin
    }).then(() => {    
        dispatch(getAdminList());
        dispatch(switchAdminPanel(ADMIN_PANEL_TYPE.DETAIL));
        message.success('管理员创建成功');
    }, (errorMessage)=>{
        message.error(`管理员创建失败，${errorMessage}`);
        dispatch(hideLoading());
    });
}

export const setAdmin = (admin) => ({
    type: ACTION_TYPES.UI_ADMIN_SET,
    admin
});


export const removeAdmin = (adminId) => (dispatch, getState) => {
    dispatch(loading());
    return dispatch(deleteAdmin(adminId));
};

const deleteAdmin = adminId => dispatch => {
    return request({
        path: `admin/${adminId}`,
        method: "DELETE"
    }).then(() => {
        dispatch(getAdminList());
        message.success('管理员删除成功');
    },(errorMessage)=>{
        message.error(`管理员删除失败，${errorMessage}`);
        dispatch(hideLoading());
    });
}

export const getAdmin = (id) => (dispatch, getState) => {
    dispatch(loading());
    return dispatch(fetchAdmin(id))
};

const fetchAdmin = id => dispatch => {
    return request({
        path: `admin/${id}`
    }).then(admin => {
        dispatch(setAdmin(admin));    
    }).finally(()=>{
        dispatch(hideLoading());
    });
}

export const getAdminList = () => (dispatch, getState) => {
    dispatch(loading());
    return dispatch(fetchAdminList())
};

const fetchAdminList = () => dispatch => {
    return request({
        path: "admins"
    }).then(admins => {
        dispatch(setAdmins(admins));
        
        if( admins.length > 0){
            dispatch(setAdmin(admins[0]));
            dispatch(getAdmin(admins[0]["id"]));
            return true;
        }
        
        setAdmin({});
        return false;
    }).finally((needHideLoading)=>{
        if( !needHideLoading){
            return
        }
        dispatch(hideLoading());
    });;
}

export const setAdmins = admins =>({
    type: ACTION_TYPES.ADMIN_LIST_SET,
    admins
});

