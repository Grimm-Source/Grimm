import { Button } from 'antd';
import React from 'react';

import './ButtonGroup.less';

const ADButtonGroup = Button.Group;

export default class ButtonGroup extends React.Component {
  constructor(props){
      super(props);
      let preValue = this._getValue();
      let value = preValue.value;
      let map = {};
      
      value.forEach((item)=>{
        map[item]= true;
      });

      this.state={
        buttons: this.props.buttons || [],
        value,
        map,
        isSourceList: preValue.isSourceList, 
      }
  }

  _getValue = ()=>{
    if(Array.isArray(this.props.value)){
      return {
        value: this.props.value,
        isSourceList: true
      };
    }

    return {
      value: this.props.value && this.props.value.split? this.props.value.split(","): [],
      isSourceList: false
    };
  }

  onClickButton=(key)=>{
    let map = this.state.map;
    map[key] = !map[key];
    let result = [];
    for(let key in map){
        if(map[key]){
            result.push(key);
        }
    }
    this.setState({
        map
    });
    
    this.props.onChange(this.state.isSourceList?result: result.join(","));
  }

  getButtons=()=>{
    return this.props.buttons.map((item)=>{
        return <Button key={item} className={this.state.map[item]?'active-button':'inactive-button'} onClick={this.onClickButton.bind(this, item)}>{item}</Button>  
    })
  }

  render() {
    const buttons = this.getButtons();
    return (
        <ADButtonGroup className="button-group">
            {buttons}
        </ADButtonGroup>
    );
  }
}