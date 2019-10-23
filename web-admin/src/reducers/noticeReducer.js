import {ACTION_TYPES} from '../actions/actionTypes.js';

const notice = (state = [], action) => {
    switch (action.type) {
      case ACTION_TYPES.NOTICE_NEW_USERS_SET:
          return {
            ...state,
            newUsers: action.users || []
          };

      default:
        return state;
    }
  }
  
  export default notice;