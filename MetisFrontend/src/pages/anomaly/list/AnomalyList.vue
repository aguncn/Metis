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
        </div>
        <span style="float: right; margin-top: 3px;">
          <a-button type="primary" html-type="submit">查询</a-button>
          <a-button style="margin-left: 8px" html-type="reset" @click="resetForm">重置</a-button>
        </span>
      </a-form-model>
    </div>
    <div>
			<a-list
			  :grid="{gutter: 24, lg: 3, md: 2, sm: 1, xs: 1}"
			  :dataSource="dataSource"
				:pagination="pagination"
			>
			  <a-list-item slot="renderItem" slot-scope="item">
			    <template>
			      <a-card :hoverable="true">
			        <a-card-meta >
			          <div style="margin-bottom: 2px" slot="title">
									{{item.titleSample}} 
									<a @click="showSample(item)">
										O
									</a>
								</div>
			          <div class="meta-content" slot="description">
									<ve-line :data="item.dataGraphAbc"></ve-line>
								</div>
			        </a-card-meta>
			        <a slot="actions">
								<a-button type="dashed">标记为正样本</a-button>
							</a>
			        <a slot="actions">
								<a-button type="dashed">标记为负样本</a-button>
							</a>
			      </a-card>
			    </template>
			  </a-list-item>
			</a-list>
    </div>
		
		<a-modal v-model="visibleShowSample" :title="titleSample" 
			width='80%'
			@ok="handleShowSampleOk">
				<ve-line :data="dataSingleAbc"></ve-line>
		</a-modal>
  </a-card>
</template>

<script>
import {dataSeries} from '@/utils/dataSeries'
import {getAnomalyList} from '@/services/anomaly'

export default {
  name: 'AnomalyList',
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
			taskForm: {
				id: 0,
				source: '',
				trainTest: '',
				positiveNegative: '' 
			},
			pagination: {
				'total': 0,
				'pageSize': 6,
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
				},
				{
					title: '用户',
					dataIndex: 'createUser',
				},
				{
					title: '图表',
					scopedSlots: { customRender: 'graph' }
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
			getAnomalyList(params).then(resp => {
				let retData = resp.data
				if (retData.code == 0) {
					this.dataSource = []
					this.dataAbc = []
					this.dataGraphAbc = {}
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
							titleSample: `[${view_set_name}-${attrName}]:${anomalyTime}`,
							dataGraphAbc: dataSeries(anomalyTime, 
																results[i].data_a, 
																results[i].data_b, 
																results[i].data_c),
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
		handleTableChange(pagination) {
			console.log('xxxxxxxxxxx')
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
		
		showSample(params) {
			this.titleSample = this.titleSamples[params.key]
			this.dataSingleAbc = this.dataAbc[params.key]
			this.visibleShowSample = true;
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
	.meta-content{
	  position: relative;
	  overflow: hidden;
	  text-overflow: ellipsis;
	  display: -webkit-box;
	  height: 350px;
	  -webkit-line-clamp: 3;
	  -webkit-box-orient: vertical;
	}
</style>
