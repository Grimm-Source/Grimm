import React from 'react';
import { connect } from 'react-redux';

class BaseInfo extends React.Component {
    render(){
        return(
            <div>BaseInfo</div>
        )
    }
}

const mapStateToProps = (state, ownProps) => ({

})

const mapDispatchToProps = (dispatch, ownProps) => ({
})

export default connect(mapStateToProps, mapDispatchToProps)(BaseInfo)