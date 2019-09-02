let user = sessionStorage.getItem("user") && JSON.parse(sessionStorage.getItem("user"));

const initialState = {
    ui: {
        activeHomeTagKey: "activity",
        isShowActivityModal: false,
        activityId: null,
        activity: {},
        admin: {},
        loading: false,
        activeAdminKey: "detail",
        adminFormType: "login"
    },
    account:{
        user: user || {},
    },
    admin: {
        list: []
    },
    activity: {
        list: []
    }
}

export default initialState;