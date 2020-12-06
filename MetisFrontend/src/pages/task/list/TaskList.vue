<template>
  <a-card>
    <div :class="advanced ? 'search' : null">
      <a-form-model layout="horizontal" ref="searchKey" :model="pagination.searchKey" @submit="handleSubmit">
        <div :class="advanced ? null: 'fold'">
          <a-row >
          <a-col :md="8" :sm="24" >
            <a-form-model-item
              label="模型名称"
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
              label="训练状态"
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
			      <a @click="deleteRecord(record)">
			        <a-button type="danger" >删除</a-button>
			      </a>
			    </div>
			    <template slot="taskStatus" slot-scope="text">
			    		<a-spin v-if="text==='running'" />
			    		<a-tag color='red' v-if="text==='error'">训练出错</a-tag> 
			    		<a-tag color='green' v-if="text==='finish'">训练完成</a-tag>
			    </template>
			    <div slot='source' slot-scope="record">
			    	<a-tag >{{record}}</a-tag>
			    </div>
			  </a-table>
    </div>
  </a-card>
</template>

<script>
import {getTaskList, deleteTask} from '@/services/task'

export default {
  name: 'TaskList',
	activated() {
		this.fetch(this.pagination)
	},
  data () {
    return {
      advanced: false,
			pagination: {
				'total': 0,
				'pageSize': 15,
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
					title: '任务id',
					dataIndex: 'taskId',
					customRender: (text, record) => {
						return (
							<a-tooltip>
								<template slot="title">
									{this.$options.filters.minFormat(record.createDate)}
								</template>
								{text}
							</a-tooltip>
						)
					}
				},
				{
					title: '样本(总-负-正)',
					customRender: (record, index) => {
						const sampleNum = `${record.sampleNum}-${record.negativeSampleNum}-${record.positiveSampleNum}`
						return sampleNum
					}
				},
				{
					title: '来源',
					dataIndex: 'source',
					scopedSlots: {customRender: 'source'} 
				},
				{
					title: '状态',
					dataIndex: 'taskStatus',
					scopedSlots: {customRender: 'taskStatus'} 
				},
				{
					title: '模型',
					dataIndex: 'modelName',
				},
				{
					title: '起止时间',
					customRender: (record) => {
						const time = `${this.$options.filters.dayFormat(record.startDate)}
													~
													${this.$options.filters.dayFormat(record.endDate)}`
						return time
					}
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
			getTaskList(params).then(resp => {
				let retData = resp.data
				if (retData.code == 0) {
					this.dataSource = []
					const results = retData.data.results
					for (let i = 0; i < results.length; i++) {
						this.dataSource.push({
							key: i,
							id: results[i].id,
							taskId: results[i].task_id,
							sampleNum: results[i].sample_num,
							negativeSampleNum: results[i].negative_sample_num,
							positiveSampleNum: results[i].positive_sample_num,
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
			deleteTask(record.id).then(resp => {
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
