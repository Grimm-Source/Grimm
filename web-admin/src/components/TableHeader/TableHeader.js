import React from 'react';
import { connect } from 'react-redux';

import './TableHeader.less'

class TableHeader extends React.Component {
  render() {
    return (
        <div className="table-header">
            <span className="left">{this.props.left}</span>
            <span className="right">{this.props.right}</span>
        </div>
    );
  }
}

const mapStateToProps = (state, ownProps) => ({
  loading: state.ui.loading
});

const mapDispatchToProps = (dispatch, ownProps) => ({

})

export default connect(mapStateToProps, mapDispatchToProps)(TableHeader)