import {ACTION_TYPES} from '../actions/actionTypes.js';
import {USER_LIST_TYPE, ACTIVITY_DETAIL_TYPE} from '../constants/index.js';

const ui = (state = [], action) => {
    switch (action.type) {
      case ACTION_TYPES.UI_LOADING:
        return {
          ...state,
          loading: true
        };
      case ACTION_TYPES.UI_LOADING_HIDE:
        return {
          ...state,
          loading: false
        };
      case ACTION_TYPES.UI_HOME_TAG_SWITCH:
        return {
          ...state,
          homeTagType: action.activeKey 
        };
      case ACTION_TYPES.UI_DRAWER_SHOW:
        return {
          ...state,
          isShowDrawer: true
        };
      case ACTION_TYPES.UI_DRAWER_HIDE:
        return {
          ...state,
          isShowDrawer: false
      };
      case ACTION_TYPES.UI_USER_DETAIL_SHOW:
        return {
          ...state,
          isShowUserDetail: true,
          user: action.user
        };
      case ACTION_TYPES.UI_USER_DETAIL_HIDE:
        return {
          ...state,
          isShowUserDetail: false,
          user: {}
        };
      case ACTION_TYPES.UI_ACTIVITY_SHOW:
        return {
          ...state,
          isCopy: action.isCopy,
          isShowActivityModal: true,
          activityId: action.activityId || null,
          activityDetailType: action.activityDetailType || ACTIVITY_DETAIL_TYPE.EDIT || ACTIVITY_DETAIL_TYPE.COPY
        };
      case ACTION_TYPES.UI_ACTIVITY_HIDE:
        return {
          ...state,
          isShowActivityModal: false,
          activityId: null,
          activity: {}
      };
      case ACTION_TYPES.UI_ACTIVITY_DETAIL_SWITCH:
        return {
          ...state,
          activityDetailType: action.activeKey,
      };
      case ACTION_TYPES.UI_ADMIN_SET:
        return {
          ...state,
          admin: action.admin || {}
        };
      case ACTION_TYPES.UI_ADMIN_PANEL_SWITCH:
          return {
            ...state,
            adminPanelType: action.activeKey
          };
      case ACTION_TYPES.UI_ADMIN_FORM_TYPE_SWITCH:
          return {
            ...state,
            adminFormType: action.activeKey
          };
      case ACTION_TYPES.UI_USER_LIST_SWITCH:
          return {
            ...state,
            userListType: state.userListType === USER_LIST_TYPE.VOLUNTEER? USER_LIST_TYPE.DISABLED:USER_LIST_TYPE.VOLUNTEER
          };
      case ACTION_TYPES.UI_ACTIVITY_SET:
        return {
          ...state,
          activity: action.activity || {}
        };
      case ACTION_TYPES.UI_ACTIVITY_STATICS_SET:
        return {
          ...state,
          activityStatics: action.activityStatics || {}
        };
        case ACTION_TYPES.UI_ACTIVITY_NAME_LIST_SET:
          return {
            ...state,
            activityNameList: action.activityNameList || {}
          };
      case ACTION_TYPES.UI_SELECTED_USER_LIST:
        return {
          ...state,
          selectedUsers: action.users || []
        };
      case ACTION_TYPES.UI_SHOW_LOGIN:
        return {
          ...state,
          isShowLogin: true,
        };

      case ACTION_TYPES.UI_SHOW_LOGIN:
          return {
            ...state,
            isShowLogin: true,
          };
      case ACTION_TYPES.UI_SHOW_RESET_PASSWORD:
        return {
          ...state,
          isShowResetPassword: true
          };
      case ACTION_TYPES.UI_HIDE_RESET_PASSWORD:
        return {
          ...state,
          isShowResetPassword: false
        };
      case ACTION_TYPES.UI_SHOW_EMAIL_VERIFY:
        return {
          ...state,
          isShowEmailVerify: true,
          emailAddrWaitForVerified: action.emailAddr
        };
      case ACTION_TYPES.UI_HIDE_EMAIL_VERIFY:
        return {
          ...state,
          isShowEmailVerify: false,
          emailAddrWaitForVerified: null
        };

      default:
        return state;
    }
  }
  
  export default ui;