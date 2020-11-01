import {ACTION_TYPES} from './actionTypes';
import request from '../utils/request';
import { ADMIN_PANEL_TYPE, ADMIN_FORM_TYPE } from "../constants";
import { storage } from "../utils/localStorageHelper";
import { message } from 'antd';

//ui section
export const loading = () => ({
    type: ACTION_TYPES.UI_LOADING
});

export const hideLoading = () => ({
    type: ACTION_TYPES.UI_LOADING_HIDE
});

export const switchHomeTag = (activeKey) => ({
    type: ACTION_TYPES.UI_HOME_TAG_SWITCH,
    activeKey
});

export const switchUserList = () => ({
    type: ACTION_TYPES.UI_USER_LIST_SWITCH
});

export const switchAdminPanel = (activeKey) => ({
    type: ACTION_TYPES.UI_ADMIN_PANEL_SWITCH,
    activeKey
});

export const switchAdminFormType = (activeKey) => ({
    type: ACTION_TYPES.UI_ADMIN_FORM_TYPE_SWITCH,
    activeKey
});

export const showActivityModal = (activityId, activityDetailType) => ({
    type: ACTION_TYPES.UI_ACTIVITY_SHOW,
    activityId,
    activityDetailType
});

export const hideActivityModal = () => ({
    type: ACTION_TYPES.UI_ACTIVITY_HIDE
});

export const switchActivityDetail = (activeKey) => ({
    type: ACTION_TYPES.UI_ACTIVITY_DETAIL_SWITCH,
    activeKey
});

export const showDrawer = () => ({
    type: ACTION_TYPES.UI_DRAWER_SHOW
});

export const hideDrawer = () => ({
    type: ACTION_TYPES.UI_DRAWER_HIDE
});

export const showUserDetail = (user) => ({
    type: ACTION_TYPES.UI_USER_DETAIL_SHOW,
    user
});

export const hideUserDetail = () => ({
    type: ACTION_TYPES.UI_USER_DETAIL_HIDE
});

export const setSelectedUsers = (users) => ({
    type: ACTION_TYPES.UI_SELECTED_USER_LIST,
    users
})

export const showLogin = () => ({
    type: ACTION_TYPES.UI_SHOW_LOGIN
})

export const showResetPassword = () => ({
    type: ACTION_TYPES.UI_SHOW_RESET_PASSWORD
})

export const hideResetPassword = () => ({
    type: ACTION_TYPES.UI_HIDE_RESET_PASSWORD
})

export const showEmailVerify = (emailAddr) => ({
    type: ACTION_TYPES.UI_SHOW_EMAIL_VERIFY,
    emailAddr
});

export const hideEmailVerify = () => ({
    type: ACTION_TYPES.UI_HIDE_EMAIL_VERIFY
});



//account section
export const loginAccount = (user) => (dispatch, getState) => {
    dispatch(loading());
    return dispatch(verifyAccount(user));
};

const verifyAccount = user => dispatch => {
    var emailAddr = user.email;
    return request({
        path: "login",
        method: "POST",
        data: user
    }).then((userInfo) => {
        storage.setItem("user", userInfo);
        dispatch(login(userInfo));  
        dispatch(fetchActivityList());
        dispatch(switchAdminFormType(ADMIN_FORM_TYPE.CREATE));
        message.success('登录成功');
    }, (errorMessage) => {
        message.error(`登录失败，${errorMessage}`);
        const EMAIL_NOT_VERIFIED_ERROR_STRING = "请先认证邮箱";

        if (errorMessage === EMAIL_NOT_VERIFIED_ERROR_STRING) {
            dispatch(showEmailVerify(emailAddr));
        }
    }).finally(() => {
        dispatch(hideLoading());
    });
}

export const login = (user) => ({
    type: ACTION_TYPES.ACCOUNT_LOGIN,
    user
});

export const logout = () => ({
    type: ACTION_TYPES.ACCOUNT_LOGOUT
});

export const resetPassword = (accountId) => (dispatch, getState) => {
    dispatch(loading());
    return request({
        path: "admin/forget-password?email=" + accountId,
        method: "GET"
    }).then((accountID) => {
        message.success('新的密码已成功发送到注册邮箱');
        dispatch(hideResetPassword());
    }, (errorMessage) => {
        message.error(`新得密码发送失败，${errorMessage}`);
    }).finally(()=>{
        dispatch(hideLoading());
    });
}

export const verifyAdminEmail = (emailAddr) => (dispatch, getState) => {
    if (emailAddr == null) {
        return;
    }
    return request({
        path: "email?email=" + emailAddr,
        method: "GET"
    }).then((userInfo) => {
        message.success('邮箱验证码已发送');
    }, (errorMessage) => {
        message.error(`邮箱验证码发送失败${errorMessage}`);
    }).finally(() => {});
};

//activity section
export const publishActivity = (activity) => (dispatch, getState) => {
    dispatch(loading());
    if (!activity["id"]) {
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
    }, (errorMessage) => {
        message.error(`活动发布失败，${errorMessage}`);
        dispatch(hideLoading());
    }).finally(() => {

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
    }, (errorMessage) => {
        message.error(`活动发布失败，${errorMessage}`);
        dispatch(hideLoading());
    }).finally(() => {

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
    }).finally(() => {
        dispatch(hideLoading());
    });
}

export const setActivity = activity => ({
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
    }, (errorMessage) => {
        message.error(`活动删除失败，${errorMessage}`);
        dispatch(hideLoading());
    });
}

export const getActivityStatics = (id) => (dispatch, getState) => {
    dispatch(loading());
    return dispatch(fetchActivityStatics(id))
};

const fetchActivityStatics = id => dispatch => {
    // return request({
    //     path: `activityStatics?id=${id}`
    // }).then(activity => {
    //     dispatch(setActivityStatics(activity));    
    // }).finally(() => {
        dispatch(hideLoading());
    // });
}

export const setActivityStatics = activityStatics => ({
    type: ACTION_TYPES.UI_ACTIVITY_STATICS_SET,
    activityStatics
});

export const getActivityNameList = (id) => (dispatch, getState) => {
    dispatch(loading());
    return dispatch(fetchActivityNameList(id))
};

const fetchActivityNameList = id => dispatch => {
    // if(!id){
    //     return request({
    //         path: `activityNameList`
    //     }).then(namelist => {
    //         dispatch(setActivityNameList(namelist));    
    //     }).finally(() => {
    //         dispatch(hideLoading());
    //     });
    // }
    // return request({
    //     path: `activityNameList?id=${id}`
    // }).then(namelist => {
    //     dispatch(setActivityNameList(namelist));    
    // }).finally(() => {
        dispatch(hideLoading());
    // });
}

export const setActivityNameList = activityNameList => ({
    type: ACTION_TYPES.UI_ACTIVITY_NAME_LIST_SET,
    activityNameList
});

export const getActivityList = () => (dispatch, getState) => {
    dispatch(loading());
    return dispatch(fetchActivityList())
};

const fetchActivityList = id => dispatch => {
    return request({
        path: "activities"
    }).then(activities => {
        dispatch(setActivities(activities));
    }).finally(() => {
        dispatch(hideLoading());
    });
}

export const setActivities = activities => ({
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
    }, (errorMessage) => {
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
    }, (errorMessage) => {
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
    }).finally(() => {
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
        
        if (admins.length > 0) {
            dispatch(setAdmin(admins[0]));
            dispatch(getAdmin(admins[0]["id"]));
            return true;
        }
        
        setAdmin({});
        return false;
    }).finally((needHideLoading) => {
        if (!needHideLoading) {
            return
        }
        dispatch(hideLoading());
    });;
}

export const setAdmins = admins => ({
    type: ACTION_TYPES.ADMIN_LIST_SET,
    admins
});

export const getVolunteerList = () => (dispatch, getState) => {
    dispatch(loading());
    return dispatch(fetchVolunteerList())
};

const fetchVolunteerList = () => dispatch => {
    return request({
        path: "users?role=volunteer"
    }).then(users => {
        dispatch(setUsers(users));
    }).finally(() => {
        dispatch(hideLoading());
    });
}

export const getDisabledList = () => (dispatch, getState) => {
    dispatch(loading());
    return dispatch(fetchDisabledList());
}

const fetchDisabledList = () => dispatch => {
    return request({
        path: "users?role=disabled"
    }).then(users => {
        dispatch(setUsers(users));
    }).finally(() => {
        dispatch(hideLoading());
    });
}

export const getRegisteredVolunteers = (activityId) => (dispatch, getState) => {
    dispatch(loading());
    return dispatch(fetchRegisteredVolunteers(activityId));
}

const fetchRegisteredVolunteers = (activityId) => dispatch => {
    return request({
        path: "activityRegistration/" + activityId
    }).then(result => {
        dispatch(setRegisteredVolunteers(result.users))
    }).finally(() => {
        dispatch(hideLoading())
    })
}

export const setUsers = users => ({
    type: ACTION_TYPES.USER_LIST_SET,
    users
});

export const setNoticeUsers = users => {
    storage.setItem("notice-new-users", users);
    return ({
        type: ACTION_TYPES.NOTICE_NEW_USERS_SET,
        users
    })
};

export const setRegisteredVolunteers = volunteers => {
    return ({
        type: ACTION_TYPES.ACTIVITY_REGISTERED_VOLUNTEERS_SET,
        volunteers
    })
}

export const updateUsers = (users, isVolunteer) => (dispatch, getState) => {
    dispatch(loading());
    return dispatch(patchUserList(users, isVolunteer))
}

const patchUserList = (users, isVolunteer) => dispatch => {
    return request({
        path: "users",
        method: "PATCH",
        data: users
    }).then(() => {
        if (isVolunteer) {
            dispatch(fetchVolunteerList());
        } else {
            dispatch(fetchDisabledList());
        }
    }, (errorMessage) => {
        message.error(`操作失败，${errorMessage}`);
        dispatch(hideLoading());
    });
}

//profile section
export const changePassword = (adminId, oldVal, newVal) => async (dispatch, getState) => {
    dispatch(loading());
    try {
        await request({
            path: `admin/${adminId}/update-password`,
            method: 'POST',
            data: {
                adminId,
                old_password: oldVal,
                new_password: newVal
            }
        });
        message.success('密码修改成功！');
        dispatch(hideLoading());
    } catch (errorMessage) {
        message.error(`密码修改失败，${errorMessage}`);
        dispatch(hideLoading());
    }
}
