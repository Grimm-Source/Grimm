import React from 'react';
import { connect } from 'react-redux';
import { Table, Input, Button, Icon } from 'antd';
import Highlighter from 'react-highlight-words';

import './Report.less';

const data = [
  {
    key: '1',
    name: '张三',
    activity: '爱心牵手活动',
    status: '已报名',
  },
  {
    key: '2',
    name: '李四',
    activity: '爱心牵手',
    status: '已签到',
  },
  {
    key: '3',
    name: '王二五',
    activity: '爱心牵手',
    status: '报名未签到',
  },
  {
    key: '4',
    name: '张刘',
    activity: '爱心牵手',
    status: '已签到',
  },
];

class Report extends React.Component { 
  
  state = {
    searchText: '',
    sortedInfo: null,
  };

  getColumnSearchProps = (dataIndex, title) => ({
    filterDropdown: ({ setSelectedKeys, selectedKeys, confirm, clearFilters }) => (
      <div style={{ padding: 8 }}>
        <Input
          ref={node => {
            this.searchInput = node;
          }}
          placeholder={`搜索${title}`}
          value={selectedKeys[0]}
          onChange={e => setSelectedKeys(e.target.value ? [e.target.value] : [])}
          onPressEnter={() => this.handleSearch(selectedKeys, confirm)}
          style={{ width: 188, marginBottom: 8, display: 'block' }}
        />
        <Button
          type="primary"
          onClick={() => this.handleSearch(selectedKeys, confirm)}
          icon="search"
          size="small"
          style={{ width: 90, marginRight: 8 }}
        >
          搜索
        </Button>
        <Button onClick={() => this.handleReset(clearFilters)} size="small" style={{ width: 90 }}>
          重置
        </Button>
      </div>
    ),
    filterIcon: filtered => (
      <Icon type="search" style={{ color: filtered ? '#1890ff' : undefined }} />
    ),
    onFilter: (value, record) =>
      record[dataIndex]
        .toString()
        .toLowerCase()
        .includes(value.toLowerCase()),
    onFilterDropdownVisibleChange: visible => {
      if (visible) {
        setTimeout(() => this.searchInput.select());
      }
    },
    render: text => (
      <Highlighter
        highlightStyle={{ backgroundColor: '#ffc069', padding: 0 }}
        searchWords={[this.state.searchText]}
        autoEscape
        textToHighlight={text.toString()}
      />
    ),
  });

  handleSearch = (selectedKeys, confirm) => {
    confirm();
    this.setState({ searchText: selectedKeys[0] });
  };

  handleReset = clearFilters => {
    clearFilters();
    this.setState({ searchText: '' });
  };

  handleChange = (sorter) => {
    this.setState({
      sortedInfo: sorter
    });
  };


  render() { 
    let { sortedInfo } = this.state;
    sortedInfo = sortedInfo || {}; 
    const columns = [
      {
        title: '用户',
        dataIndex: 'name',
        key: 'name',
        width: '30%',
        sorter: (a, b) => a.name.length - b.name.length,
        sortDirections: ['descend', 'ascend'],
        ...this.getColumnSearchProps('name', '用户'),
      },
      {
        title: '活动',
        dataIndex: 'activity',
        key: 'activity',
        width: '30%',
        sorter: (a, b) => a.activity.length - b.activity.length,
        sortDirections: ['descend', 'ascend'],
        ...this.getColumnSearchProps('activity', '活动'),
      },
      {
        title: '状态',
        dataIndex: 'status',
        key: 'status'
      },
    ];
    return <Table columns={columns} dataSource={data} onChange={this.handleChange}/>;
  }
}

const mapStateToProps = (state, ownProps) => ({
  loading: state.ui.loading,
});

const mapDispatchToProps = (dispatch, ownProps) => ({
 
})

export default connect(mapStateToProps, mapDispatchToProps)(Report)