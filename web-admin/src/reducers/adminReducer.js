import {ACTION_TYPES} from '../actions/actionTypes.js'

const admin = (state = [], action) => {
    switch (action.type) {
      case ACTION_TYPES.ADMIN_LIST_SET:
        return {
          ...state,
          admins: action.admins || []
        };
      default:
        return state;
    }
  }
  
  export default admin;