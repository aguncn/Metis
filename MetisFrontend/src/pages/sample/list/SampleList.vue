<template>
  <a-card>
    <div :class="advanced ? 'search' : null">
      <a-form-model layout="horizontal" ref="searchKey" :model="pagination.searchKey" @submit="handleSubmit">
        <div :class="advanced ? null: 'fold'">
          <a-row >
          <a-col :md="8" :sm="24" >
            <a-form-model-item
              label="指标"
              :labelCol="{span: 5}"
              :wrapperCol="{span: 18, offset: 1}"
            >
              <a-input placeholder="请输入" v-model="pagination.searchKey.taskId" />
            </a-form-model-item>
          </a-col>
          <a-col :md="8" :sm="24" >
            <a-form-model-item
              label="来源"
              :labelCol="{span: 5}"
              :wrapperCol="{span: 18, offset: 1}"
            >
              <a-select placeholder="请选择">
                <a-select-option value="metis">methis</a-select-option>
                <a-select-option value="api">api</a-select-option>
              </a-select>
            </a-form-model-item>
          </a-col>
          <a-col :md="8" :sm="24" >
            <a-form-model-item
              label="集合"
              :labelCol="{span: 5}"
              :wrapperCol="{span: 18, offset: 1}"
            >
              <a-input-number style="width: 100%" placeholder="请输入" />
            </a-form-model-item>
          </a-col>
        </a-row>
          <a-row v-if="advanced">
          <a-col :md="8" :sm="24" >
            <a-form-model-item
              label="训练日期"
              :labelCol="{span: 5}"
              :wrapperCol="{span: 18, offset: 1}"
            >
              <a-date-picker style="width: 100%" placeholder="请输入更新日期" />
            </a-form-model-item>
          </a-col>
          <a-col :md="8" :sm="24" >
            <a-form-model-item
              label="任务id"
              :labelCol="{span: 5}"
              :wrapperCol="{span: 18, offset: 1}"
            >
              <a-input placeholder="请输入" />
            </a-form-model-item>
          </a-col>
        </a-row>
        </div>
        <span style="float: right; margin-top: 3px;">
          <a-button type="primary" html-type="submit">查询</a-button>
          <a-button style="margin-left: 8px" html-type="reset" @click="resetForm">重置</a-button>
          <a @click="toggleAdvanced" style="margin-left: 8px">
            {{advanced ? '收起' : '展开'}}
            <a-icon :type="advanced ? 'up' : 'down'" />
          </a>
        </span>
      </a-form-model>
    </div>
    <div>
			<!-- myself -->
			<a-table
			    :columns="columns"
			    :row-key="record => record.id"
			    :data-source="dataSource"
			    :pagination="pagination"
			    :loading="loading"
			    @change="handleTableChange"
			  >
			    <div slot="action" slot-scope="record">
						<a-button-group>
							<a @click="showSample(record)">
								<a-button>查看</a-button>
							</a>
							<a @click="deleteRecord(record)">
								<a-button type="primary" >编辑</a-button>
							</a>
							<a @click="deleteRecord(record)">
								<a-button type="danger" >删除</a-button>
							</a>
						</a-button-group>
			    </div>
			    <template slot="trainTest" slot-scope="text">
			    		<a-tag color='red' v-if="text==='train'">训练集</a-tag> 
			    		<a-tag color='blue' v-if="text==='test'">测试集</a-tag>
			    </template>
					<template slot="positiveNegative" slot-scope="text">
							<a-icon type="plus-circle" theme="outlined" :style="{ fontSize: '22px', color: '#ccc' }" v-if="text==='positive'" /> 
							<a-icon type="minus-circle" theme="outlined" :style="{ fontSize: '22px', color: '#ccc' }" v-if="text==='negative'"/>
					</template>
			    <div slot='source' slot-scope="record">
			    	<a-tag >{{record}}</a-tag>
			    </div>
			  </a-table>
    </div>
		
		<a-modal v-model="visibleSample" title="样本集合" 
			width='80%'
			@ok="handleOk">
			<div v-if="data.length">
				<v-chart
					:forceFit="true"
					height="400"
					:data="data"
					:padding="padding"
				>
					<v-tooltip
						:x="x"
						:y="100"
						:follow="false"
						crosshairs='y'
						:htmlContent="htmlContent"
					></v-tooltip>
					<v-line 
						position="date*value"
						color='type'
					>
					</v-line>
					<v-axis
						dataKey="date"
						:label="label"
					>
					</v-axis>
					<v-axis
						dataKey="value"
						:label="labelFormat"
					>
					</v-axis>
				</v-chart>
			</div>
		</a-modal>
  </a-card>
</template>

<script>
import {getSampleList, deleteSample} from '@/services/sample'
import jquery from 'jquery'
const DataSet = require('@antv/data-set')

const label = {
  textStyle: {
    fill: '#aaaaaa'
  }
}

const labelFormat = {
  textStyle: {
    fill: '#aaaaaa'
  },
  formatter: function formatter(text) {
    return text.replace(/(\d)(?=(?:\d{3})+$)/g, '$1,');
  }
}

const data = [{
  date: '2018/8/1',
  type: 'download',
  value: 4623
}, {
  date: '2018/8/1',
  type: 'register',
  value: 2208
}, {
  date: '2018/8/1',
  type: 'bill',
  value: 182
}, {
  date: '2018/8/2',
  type: 'download',
  value: 6145
}, {
  date: '2018/8/2',
  type: 'register',
  value: 2016
}, {
  date: '2018/8/2',
  type: 'bill',
  value: 257
}, {
  date: '2018/8/3',
  type: 'download',
  value: 508
}, {
  date: '2018/8/3',
  type: 'register',
  value: 2916
}, {
  date: '2018/8/3',
  type: 'bill',
  value: 289
}, {
  date: '2018/8/4',
  type: 'download',
  value: 6268
}, {
  date: '2018/8/4',
  type: 'register',
  value: 4512
}, {
  date: '2018/8/4',
  type: 'bill',
  value: 428
}, {
  date: '2018/8/5',
  type: 'download',
  value: 6411
}, {
  date: '2018/8/5',
  type: 'register',
  value: 8281
}, {
  date: '2018/8/5',
  type: 'bill',
  value: 619
}, {
  date: '2018/8/6',
  type: 'download',
  value: 1890
}, {
  date: '2018/8/6',
  type: 'register',
  value: 2008
}, {
  date: '2018/8/6',
  type: 'bill',
  value: 87
}, {
  date: '2018/8/7',
  type: 'download',
  value: 4251
}, {
  date: '2018/8/7',
  type: 'register',
  value: 1963
}, {
  date: '2018/8/7',
  type: 'bill',
  value: 706
}, {
  date: '2018/8/8',
  type: 'download',
  value: 2978
}, {
  date: '2018/8/8',
  type: 'register',
  value: 2367
}, {
  date: '2018/8/8',
  type: 'bill',
  value: 387
}, {
  date: '2018/8/9',
  type: 'download',
  value: 3880
}, {
  date: '2018/8/9',
  type: 'register',
  value: 2956
}, {
  date: '2018/8/9',
  type: 'bill',
  value: 488
}, {
  date: '2018/8/10',
  type: 'download',
  value: 3606
}, {
  date: '2018/8/10',
  type: 'register',
  value: 678
}, {
  date: '2018/8/10',
  type: 'bill',
  value: 507
}, {
  date: '2018/8/11',
  type: 'download',
  value: 4311
}, {
  date: '2018/8/11',
  type: 'register',
  value: 3188
}, {
  date: '2018/8/11',
  type: 'bill',
  value: 548
}, {
  date: '2018/8/12',
  type: 'download',
  value: 4116
}, {
  date: '2018/8/12',
  type: 'register',
  value: 3491
}, {
  date: '2018/8/12',
  type: 'bill',
  value: 456
}, {
  date: '2018/8/13',
  type: 'download',
  value: 6419
}, {
  date: '2018/8/13',
  type: 'register',
  value: 2852
}, {
  date: '2018/8/13',
  type: 'bill',
  value: 689
}, {
  date: '2018/8/14',
  type: 'download',
  value: 1643
}, {
  date: '2018/8/14',
  type: 'register',
  value: 4788
}, {
  date: '2018/8/14',
  type: 'bill',
  value: 280
}, {
  date: '2018/8/15',
  type: 'download',
  value: 445
}, {
  date: '2018/8/15',
  type: 'register',
  value: 4319
}, {
  date: '2018/8/15',
  type: 'bill',
  value: 176
}];
const x = jquery("#mountNode").width() - 20;
export default {
  name: 'SampleList',
	activated() {
		this.fetch(this.pagination)
	},
	mounted() {
		this.setStyle();
	},
  data () {
    return {
			data: data,
			padding: [100, 20, 30, 45],
			x,
			label,
			labelFormat,
			htmlContent: (title, items) => {
				var alias = {
					download: '当日累计下载量',
					register: '当日累计注册量',
					bill: '当日累计成交量'
				};
				var html = '<div class="custom-tooltip">';
				for (var i = 0; i < items.length; i++) {
					var item = items[i];
					var color = item.color;
					var name = alias[item.name];
					var value = item.value;
					var domHead = '<div class="custom-tooltip-item" style="border-left-color:' + color + '">';
					var domName = '<div class="custom-tooltip-item-name">' + name + '</div>';
					var domValue = '<div class="custom-tooltip-item-value">' + value + '</div>';
					var domTail = '</div>';
					html += domHead + domName + domValue + domTail;
				}
				return html + '</div>';
			},
			visibleSample: false,
      advanced: false,
			pagination: {
				'total': 0,
				'pageSize': 20,
				'currentPage': 1,
				'ordering': '-id',
				'searchKey': {
					'taskId': '',
					'source': [],
					'taskStaus': '',
					'modelName': '',
					'trainDate': ''
					
				}
			},
			loading: false,
      dataSource: [],
			columns: [
				{
					title: '指标',
					dataIndex: 'attrName',
					customRender: (text, record) => {
						return (
							<a-tooltip>
								<template slot="title">
									{record.viewSetName}
								</template>
								{text}
							</a-tooltip>
						)
					}
				},
				{
					title: '异常时间',
					customRender: (record, index) => {
						return `${this.$options.filters.minFormat(record.anomalyTime)}`
					}
				},
				{
					title: '来源',
					dataIndex: 'source',
					scopedSlots: {customRender: 'source'} 
				},
				{
					title: '集合',
					dataIndex: 'trainTest',
					scopedSlots: {customRender: 'trainTest'} 
				},
				{
					title: '正负样本',
					scopedSlots: {customRender: 'positiveNegative'},
					dataIndex: 'positiveNegative',
				},
				{
					title: '用户',
					dataIndex: 'createUser',
				},
				{
					title: '操作',
					scopedSlots: { customRender: 'action' }
				}
			]
    }
  },
  methods: {
		fetch(params={}) {
			this.loading = true;
			getSampleList(params).then(resp => {
				let retData = resp.data
				if (retData.code == 0) {
					this.dataSource = []
					const results = retData.data.results
					console.log(results)
					for (let i = 0; i < results.length; i++) {
						this.dataSource.push({
							key: i,
							id: results[i].id,
							attrName: results[i].attr_name,
							viewSetName: results[i].view_set_name,
							anomalyTime: results[i].anomaly_time,
							trainTest: results[i].train_or_test,
							positiveNegative: results[i].positive_or_negative,
							modelName: results[i].model_name,
							taskStatus: results[i].task_status,
							source: results[i].source,
							startDate: results[i].start_date,
							endDate: results[i].end_date,
							createDate: results[i].create_date,
							createUser: results[i].username
						})
					}
					const pager = { ...this.pagination };
					// Read total count from server
					pager.total = retData.data.count;
					this.pagination = pager;
					this.loading = false;
				} else {
					this.loading = false;
					this.$message.error(createRes.message, 3)
				}
			})
		},
		handleTableChange(pagination) {
      const pager = { ...this.pagination };
      pager.currentPage = pagination.current;
      this.pagination = pager;
      this.fetch(this.pagination);
    },
		handleSubmit(e) {
			e.preventDefault();
			this.fetch(this.pagination)
		},
		resetForm() {
			const pager = { ...this.pagination };
			pager.currentPage = 1;
			pager.searchKey.taskId = ''
			pager.searchKey.source = []
			this.pagination = pager;
			this.fetch(this.pagination);
		},
    deleteRecord(record) {
			this.loading = true;
			deleteSample(record.id).then(resp => {
				let retData = resp.data
				if (retData.code == 0) {
					this.fetch(this.pagination)
					this.loading = false;
					this.$message.success(record.id + '删除成功！', 3)
				} else {
					console.log(retData, "@@@@@@@@@")
					this.loading = false;
					this.$message.error('删除失败！' + retData.message, 3)
				}
			})
    },
    toggleAdvanced () {
      this.advanced = !this.advanced
    },
		
		showSample() {
			this.visibleSample = true;
		},
		handleOk(e) {
			console.log(e);
			this.visibleSample = false;
		},
		setStyle(){
			const id = 'legend-html';
			if (document.getElementById(id)) {
					return;
			}
			const styleTxt = `
				.custom-tooltip {
						width: 100% !important;
						height: 10% !important;
						position: absolute;
						top: 0px;
						left: 0px
				}

				.custom-tooltip-item {
						width: 150px;
						height: 50px;
						position: relative;
						float: left;
						margin-left: 20px;
						border-left-style: solid;
						border-left-width: 5px
				}

				.custom-tooltip-item:first-child {
						margin-left: 0
				}

				.custom-tooltip-item-name {
						width: 80%;
						height: 20px;
						position: absolute;
						top: 0px;
						left: 10px;
						color: rgba(0, 0, 0, 0.45);
						font-size: 14px
				}

				.custom-tooltip-item-value {
						width: 80%;
						height: 30px;
						position: absolute;
						bottom: 0px;
						left: 10px;
						color: #262626;
						font-size: 22px;
				}
			`;
			const style = document.createElement('style');
			style.setAttribute('id', id);
			style.innerHTML = styleTxt;
			document.getElementsByTagName('head')[0].appendChild(style);
		}
  }
}
</script>

<style lang="less" scoped>
  .search{
    margin-bottom: 54px;
  }
  .fold{
    width: calc(100% - 216px);
    display: inline-block
  }
  .operator{
    margin-bottom: 18px;
  }
  @media screen and (max-width: 900px) {
    .fold {
      width: 100%;
    }
  }
</style>
