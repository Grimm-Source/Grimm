var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
import { SuperComponent, wxComponent } from '../common/src/index';
import config from '../common/config';
import props from './props';
const { prefix } = config;
const name = `${prefix}-tree-select`;
let TreeSelect = class TreeSelect extends SuperComponent {
    constructor() {
        super(...arguments);
        this.externalClasses = [
            `${prefix}-class`,
            `${prefix}-class-left-column`,
            `${prefix}-class-left-item`,
            `${prefix}-class-middle-item`,
            `${prefix}-class-right-column`,
            `${prefix}-class-right-item`,
            `${prefix}-class-right-item-label`,
        ];
        this.options = {
            multipleSlots: true,
        };
        this.data = {
            prefix,
            classPrefix: name,
            scrollIntoView: null,
        };
        this.properties = props;
        this.controlledProps = [
            {
                key: 'value',
                event: 'change',
            },
        ];
        this.observers = {
            'value, options, keys, multiple'() {
                this.buildTreeOptions();
            },
        };
        this.lifetimes = {
            ready() {
                this.getScrollIntoView('init');
            },
        };
        this.methods = {
            buildTreeOptions() {
                const { options, value, multiple, keys } = this.data;
                const treeOptions = [];
                const innerValue = [];
                let level = -1;
                let node = { children: options };
                if (options.length === 0)
                    return;
                while (node && node.children) {
                    level += 1;
                    const list = node.children.map((item) => ({
                        label: item[(keys === null || keys === void 0 ? void 0 : keys.label) || 'label'],
                        value: item[(keys === null || keys === void 0 ? void 0 : keys.value) || 'value'],
                        children: item.children,
                    }));
                    const thisValue = value === null || value === void 0 ? void 0 : value[level];
                    treeOptions.push([...list]);
                    if (thisValue == null) {
                        const [firstChild] = list;
                        node = firstChild;
                    }
                    else {
                        const child = list.find((child) => child.value === thisValue);
                        node = child !== null && child !== void 0 ? child : list[0];
                    }
                }
                const leafLevel = Math.max(0, level);
                treeOptions === null || treeOptions === void 0 ? void 0 : treeOptions.forEach((ele, idx) => {
                    const v = idx === treeOptions.length - 1 && multiple ? [ele[0].value] : ele[0].value;
                    innerValue.push((value === null || value === void 0 ? void 0 : value[idx]) || v);
                });
                if (multiple) {
                    const finalValue = this.data.value || this.data.defaultValue;
                    if (finalValue[leafLevel] != null && !Array.isArray(finalValue[leafLevel])) {
                        throw TypeError('应传入数组类型的 value');
                    }
                }
                this.setData({
                    innerValue,
                    leafLevel,
                    treeOptions,
                });
            },
            getScrollIntoView(status) {
                const { value, scrollIntoView } = this.data;
                if (status === 'init') {
                    const scrollIntoView = Array.isArray(value)
                        ? value.map((item) => {
                            return Array.isArray(item) ? item[0] : item;
                        })
                        : [value];
                    this.setData({
                        scrollIntoView,
                    });
                }
                else {
                    if (scrollIntoView === null)
                        return;
                    this.setData({
                        scrollIntoView: null,
                    });
                }
            },
            onRootChange(e) {
                const { innerValue } = this.data;
                const { value: itemValue } = e.detail;
                this.getScrollIntoView('none');
                innerValue[0] = itemValue;
                this._trigger('change', { value: innerValue, level: 0 });
            },
            handleTreeClick(e) {
                const { level, value: itemValue } = e.currentTarget.dataset;
                const { innerValue } = this.data;
                innerValue[level] = itemValue;
                this.getScrollIntoView('none');
                this._trigger('change', { value: innerValue, level: 1 });
            },
            handleRadioChange(e) {
                const { innerValue } = this.data;
                const { value: itemValue } = e.detail;
                const { level } = e.target.dataset;
                innerValue[level] = itemValue;
                this.getScrollIntoView('none');
                this._trigger('change', { value: innerValue, level });
            },
        };
    }
};
TreeSelect = __decorate([
    wxComponent()
], TreeSelect);
export default TreeSelect;
