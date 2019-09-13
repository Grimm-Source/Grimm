import {ACTION_TYPES} from '../actions/actionTypes.js'

const activity = (state = [], action) => {
    switch (action.type) {
      case ACTION_TYPES.ACTIVITY_LIST_SET:
          return {
            ...state,
            activities: action.activities || []
          };

      default:
        return state;
    }
  }
  
  export default activity;