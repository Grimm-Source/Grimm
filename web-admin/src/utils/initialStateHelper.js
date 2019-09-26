import {HOME_TAG_TYPE,
        ADMIN_PANEL_TYPE,
        ADMIN_FORM_TYPE} from "../constants";

let user = sessionStorage.getItem("user") && JSON.parse(sessionStorage.getItem("user"));

const initialState = {
    ui: {
        isShowActivityModal: false,
        isShowDrawer: false,
        isShowUserDetail: false,
        activityId: null,
        user: {},
        activity: {},
        admin: {},
        loading: false,
        homeTagType: HOME_TAG_TYPE.ACTIVITY,
        adminPanelType: ADMIN_PANEL_TYPE.DETAIL,
        adminFormType: ADMIN_FORM_TYPE.LOGIN
    },
    account:{
        user: user || {}
    },
    admin: {
        admins: []
    },
    activity: {
        activities: []
    },
    user: {
        users: []
    },
    notice: {
        newUsers: []
    }
}

export default initialState;