import React from 'react';
import { Descriptions} from 'antd';
import { connect } from 'react-redux';
import './AdminDetail.css'

const Item = Descriptions.Item;

function AdminDetail(props) {      
        return (
            <div>
                <Descriptions title="管理员信息">
                    {props.loading?<span>正在加载...</span>:<Item label="邮箱">{props.admin && props.admin.email}</Item>}
                </Descriptions>
            </div>
        );
  }

const mapStateToProps = (state, ownProps) => ({
    admin: state.ui.admin,
    loading: state.ui.loading
  });
  
  export default connect(mapStateToProps)(AdminDetail)