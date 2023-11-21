import {ACTION_TYPES} from '../actions/actionTypes.js'

const activity = (state = [], action) => {
    switch (action.type) {
      case ACTION_TYPES.ACTIVITY_LIST_SET:
          return {
            ...state,
            activities: action.activities || []
          };
      case ACTION_TYPES.ACTIVITY_REGISTERED_VOLUNTEERS_SET:
          return {
            ...state,
            volunteers: action.volunteers || []
          }
      default:
        return state;
    }
  }
  
  export default activity;