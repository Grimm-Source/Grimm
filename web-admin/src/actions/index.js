import {ACTION_TYPES} from './actionTypes';
import request from '../utils/request';
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
        dispatch(login(user));    
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
    return dispatch(postActivity(activity));
};

const postActivity = activity => dispatch => {
    return request({
        path: `activity`,
        method: "POST",
        data: activity
    }).then(() => {
        dispatch(setActivity({})); 
        message.success('活动发布成功');   
    }).finally(()=>{
        dispatch(hideLoading());
    });;
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
        path: `activity/delete`,
        method: "POST",
        data: activityId
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
        dispatch(switchAdminPanel("detail"));
        message.success('管理员创建成功');
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
        path: `admin/delete`,
        method: "POST",
        data: {id : adminId}
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
    dispatch(setAdmin({}));
    return dispatch(fetchAdminList())
};

const fetchAdminList = () => dispatch => {
    return request({
        path: "admins"
    }).then(admins => {
        dispatch(setAdmins(admins));
        if( admins.length > 0){
            dispatch(getAdmin(admins[0]["id"]));
            return true;
        }
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

