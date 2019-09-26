import {ACTION_TYPES} from '../actions/actionTypes.js'

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
          isShowActivityModal: true,
          activityId: action.activityId || null
        };
      case ACTION_TYPES.UI_ACTIVITY_HIDE:
        return {
          ...state,
          isShowActivityModal: false,
          activityId: null,
          activity: {}
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
      case ACTION_TYPES.UI_ACTIVITY_SET:
        return {
          ...state,
          activity: action.activity || {}
        };
      default:
        return state;
    }
  }
  
  export default ui;
  