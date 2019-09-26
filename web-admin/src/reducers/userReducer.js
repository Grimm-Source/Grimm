import {ACTION_TYPES} from '../actions/actionTypes.js';

const user = (state = [], action) => {
    switch (action.type) {
      case ACTION_TYPES.USER_LIST_SET:
          return {
            ...state,
            users: action.users || []
          };

      default:
        return state;
    }
  }
  
  export default user;