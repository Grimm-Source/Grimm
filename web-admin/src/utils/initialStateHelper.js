import {HOME_TAG_TYPE,
        ADMIN_PANEL_TYPE,
        ADMIN_FORM_TYPE,
        USER_LIST_TYPE} from "../constants";

import { storage } from "../utils/localStorageHelper";

let user = storage.getItem("user");
let newUsers = storage.getItem("notice-new-users");

const initialState = {
    ui: {
        isCopy: false,
        isShowActivityModal: false,
        isShowDrawer: false,
        isShowUserDetail: false,
        isShowLogin: true,
        isShowResetPassword: false,
        activityId: null,
        activityStatics: {
            targetVolunteer: 50,
            targetDisabled: 50,
            signUpVolunteer: 10,
            signUpDisabled: 40,
            checkInVolunteer: 8,
            checkInDisabled: 35
        },
        activityNameList:[
            {
              id: '1',
              name: '张三',
              type: 'volunteer',
              activity: '爱心牵手活动',
              status: '已报名',
              pickUp: false,
              pickUpName: ''
            },
            {
              id: '2',
              name: '李四',
              type: 'volunteer',
              activity: '爱心牵手',
              status: '已签到',
              pickUp: false,
              pickUpName: ''
            },
            {
              id: '3',
              name: '王二五',
              type: 'disabled',
              activity: '爱心牵手',
              status: '已报名',
              pickUp: false,
              pickUpName: ''
            },
            {
              id: '4',
              name: '张刘',
              type: 'disabled',
              activity: '爱心牵手',
              status: '已签到',
              pickUp: false,
              pickUpName: ''
            },
            {
                id: '5',
                name: '张三一',
                type: 'disabled',
                activity: '爱心牵手活动',
                status: '已报名',
                pickUp: false,
                pickUpName: ''
              },
              {
                id: '6',
                name: '李四二',
                type: 'volunteer',
                activity: '爱心牵手',
                status: '已签到',
                pickUp: true,
                pickUpName: '王二六'
              },
              {
                id: '7',
                name: '王二六',
                type: 'disabled',
                activity: '爱心牵手',
                status: '已报名',
                pickUp: true,
                pickUpName: '李四二'
              },
              {
                id: '8',
                name: '张刘八',
                type: 'disabled',
                activity: '爱心牵手',
                status: '已签到',
                pickUp: false,
                pickUpName: ''
              },
              {
                id: '9',
                name: '王十八',
                type: 'disabled',
                activity: '爱心牵手',
                status: '已签到',
                pickUp: false,
                pickUpName: ''
              },
              {
                id: '10',
                name: '张四八',
                type: 'disabled',
                activity: '爱心牵手',
                status: '已签到',
                pickUp: false,
                pickUpName: ''
              },
              {
                id: '11',
                name: '李里',
                type: 'volunteer',
                activity: '爱心牵手',
                status: '已签到',
                pickUp: false,
                pickUpName: ''
              }
        ],
        activityDetailType: "EDIT",
        user: {},
        selectedUsers: [],
        activity: {},
        admin: {},
        loading: false,
        homeTagType: HOME_TAG_TYPE.ACTIVITY,
        adminPanelType: ADMIN_PANEL_TYPE.DETAIL,
        adminFormType: ADMIN_FORM_TYPE.LOGIN,
        userListType: USER_LIST_TYPE.VOLUNTEER,
        isShowEmailVerify: false,
        emailAddrWaitForVerified: null,
    },
    account: {
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
        newUsers: newUsers || []
    }
}

export default initialState;