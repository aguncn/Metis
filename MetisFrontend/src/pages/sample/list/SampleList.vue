<template>
  <a-card>
		<div>
		  
		</div>
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
			  >
			    <div slot="action" slot-scope="record">
						<a-button-group>
							<a @click="showSample(record)">
								<a-button>查看</a-button>
							</a>
							<a @click="editSample(record)">
								<a-button type="primary" >编辑</a-button>
							</a>
							<a-popconfirm
								title="确定删除？" 
								ok-text="是" 
								cancel-text="否"
								@confirm="deleteRecord(record)">
								<a-button type="danger" >删除</a-button>
							</a-popconfirm>
							<a @click="exportSample(record)">
								<a-button>导出</a-button>
							</a>
						</a-button-group>
			    </div>
			    <template slot="trainTest" slot-scope="text">
			    		<a-tag color='red' v-if="text==='train'">训练集</a-tag> 
			    		<a-tag color='blue' v-if="text==='test'">测试集</a-tag>
			    </template>
					<template slot="positiveNegative" slot-scope="text">
							<a-icon type="plus-circle" theme="outlined" :style="{ fontSize: '20px', color: '#0f0' }" v-if="text==='positive'" /> 
							<a-icon type="minus-circle" theme="outlined" :style="{ fontSize: '20px', color: '#f00' }" v-if="text==='negative'"/>
					</template>
			    <div slot='source' slot-scope="record">
			    	<a-tag >{{record}}</a-tag>
			    </div>
			  </a-table>
    </div>
		
		<a-modal v-model="visibleShowSample" :title="titleSample" 
			width='80%'
			@ok="handleShowSampleOk">
				<ve-line :data="dataSingleAbc"></ve-line>
		</a-modal>
		
		<a-modal v-model="visibleEditSample" title="编辑"
			width='40%'
			@ok="handleEditSampleOk">
			<a-form style="max-width: 500px; margin: 40px auto 0;">
				<a-form-item
					label="样本来源"
					:labelCol="{span: 7}"
					:wrapperCol="{span: 17}"
					:required="true"
				>
					<a-select v-model='taskForm.source'>
						<a-select-option value="metis">Metis</a-select-option>
						<a-select-option value="api">API</a-select-option>
						<a-select-option value="unknown">Unknown</a-select-option>
					</a-select>
				</a-form-item>
				<a-form-item
					label="正/负样本"
					:labelCol="{span: 7}"
					:wrapperCol="{span: 17}"
					:required="true"
				>
					<a-select v-model='taskForm.positiveNegative'>
						<a-select-option value="negative">负样本</a-select-option>
						<a-select-option value="positive">正样本</a-select-option>
					</a-select>
				</a-form-item>
				<a-form-item
					label="测试/训练集"
					:labelCol="{span: 7}"
					:wrapperCol="{span: 17}"
					:required="true"
				>
					<a-select v-model='taskForm.trainTest'>
						<a-select-option value="train">训练集</a-select-option>
						<a-select-option value="test">测试集</a-select-option>
					</a-select>
				</a-form-item>
				<a-form-item :wrapperCol="{span: 17, offset: 7}">
					<a @click="updateSample">
						<a-button type="danger">提交修改</a-button>
					</a>
				</a-form-item>
			</a-form>
		</a-modal>
  </a-card>
</template>

<script>
import Papa from 'papaparse'
import {dataSeries} from '@/utils/dataSeries'
import {getSampleList, updateSample, deleteSample} from '@/services/sample'

export default {
  name: 'SampleList',
	activated() {
		this.fetch(this.pagination)
	},
  data () {
    return {
			dataAbc: [],
			dataSingleAbc: {},
			visibleEditSample: false,
			visibleShowSample: false,
			titleSample: '',
			titleSamples: [],
      advanced: false,
			headers: {
				authorization: 'authorization-text',
			},
			taskForm: {
				id: 0,
				source: '',
				trainTest: '',
				positiveNegative: '' 
			},
			pagination: {
				'total': 0,
				'pageSize': 10,
				'currentPage': 1,
				'ordering': '-id',
				'searchKey': {
					'taskId': '',
					'source': '',
					'taskStaus': '',
					'modelName': '',
					'trainDate': ''
				},
				onChange: page => {
					const pager = { ...this.pagination };
					pager.currentPage = page;
					this.pagination = pager;
					this.fetch(this.pagination);
				},
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
					dataIndex: 'anomalyTime',
					//customRender: (record, index) => {
					//	return `${this.$options.filters.secFormat(record.anomalyTime)}`
					//}
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
					this.dataAbc = []
					const results = retData.data.results
					for (let i = 0; i < results.length; i++) {
						const anomalyTime = `${this.$options.filters.secFormat(results[i].anomaly_time)}`
						const attrName = results[i].attr_name
						const view_set_name = results[i].view_set_name
						this.dataSource.push({
							key: i,
							id: results[i].id,
							attrName: attrName,
							viewSetName: view_set_name,
							anomalyTime: anomalyTime,
							source: results[i].source,
							trainTest: results[i].train_or_test,
							positiveNegative: results[i].positive_or_negative,
							dataA: results[i].data_a,
							dataB: results[i].data_b,
							dataC: results[i].data_c,
							createDate: results[i].create_date,
							createUser: results[i].username
						})
						this.dataAbc.push(dataSeries(anomalyTime, 
																	results[i].data_a, 
																	results[i].data_b, 
																	results[i].data_c))
						this.titleSamples.push(`[${view_set_name}-${attrName}]:${anomalyTime}`)
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
					this.loading = false;
					this.$message.error('删除失败！' + retData.message, 3)
				}
			})
    },
    toggleAdvanced () {
      this.advanced = !this.advanced
    },
		showSample(params) {
			this.titleSample = this.titleSamples[params.key]
			this.dataSingleAbc = this.dataAbc[params.key]
			this.visibleShowSample = true;
		},
		editSample(params) {
			this.taskForm.id = params.id
			this.taskForm.trainTest = params.trainTest
			this.taskForm.source = params.source
			this.taskForm.positiveNegative = params.positiveNegative
			this.visibleEditSample = true;
		},
		handleEditSampleOk(e) {
			this.fetch(this.pagination)
			this.visibleEditSample = false;
		},
		updateSample() {
			updateSample(this.taskForm).then(resp => {
				let retData = resp.data
				if (retData.code == 0) {
					this.fetch(this.pagination)
					this.loading = false;
					this.$message.success('更新成功！', 3)
				} else {
					this.loading = false;
					this.$message.error('更新失败！' + retData.message, 3)
				}
			})
		},
		exportSample(params) {
			const itemObj =  this.dataSource[params.key]
			const itemList = [
				itemObj
			]
			console.log(itemList)

			let csv = Papa.unparse(itemList)
			// 定义文件内容，类型必须为Blob 否则createObjectURL会报错
			const content = new Blob([`\ufeff${csv}`], {type: 'text/plain;charset=utf-8'})
			// 生成url对象
			const urlObject = window.URL || window.webkitURL || window
			const url = urlObject.createObjectURL(content)
			// 生成<a></a>DOM元素
			const el = document.createElement('a')
			// 链接赋值
			el.href = url
			el.download = `指标${itemObj.attrName}-${itemObj.anomalyTime}导出.csv`
			// 必须点击否则不会下载
			el.click()
			// 移除链接释放资源
			urlObject.revokeObjectURL(url)

		},
		handleShowSampleOk(e) {
			this.visibleShowSample = false;
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
