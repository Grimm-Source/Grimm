import React from 'react';
import { connect } from 'react-redux';
import {} from 'antd';
import ActivityNameList from '../../components/ActivityNameList/ActivityNameList.js';


import './Report.less';

class Report extends React.Component { 

  render() { 
    return <ActivityNameList className="report-table"/>;
  }
}

const mapStateToProps = (state, ownProps) => ({
  loading: state.ui.loading,
});

const mapDispatchToProps = (dispatch, ownProps) => ({
 
})

export default connect(mapStateToProps, mapDispatchToProps)(Report)