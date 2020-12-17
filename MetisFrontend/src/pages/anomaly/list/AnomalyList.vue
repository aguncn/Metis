<template>
  <a-card>
    <div>
      <a-form-model layout="horizontal" ref="searchKey" :model="pagination.searchKey" @submit="handleSubmit">
        <div class="fold">
          <a-row >
          <a-col :md="8" :sm="24" >
            <a-form-model-item
              label="指标集"
              :labelCol="{span: 5}"
              :wrapperCol="{span: 18, offset: 1}"
            >
              <a-input placeholder="请输入" v-model="pagination.searchKey.viewSet" />
            </a-form-model-item>
          </a-col>
          <a-col :md="8" :sm="24" >
            <a-form-model-item
              label="指标"
              :labelCol="{span: 5}"
              :wrapperCol="{span: 18, offset: 1}"
            >
              <a-input placeholder="请输入" v-model="pagination.searchKey.attr" />
            </a-form-model-item>
          </a-col>
          <a-col :md="8" :sm="24" >
            <a-form-model-item
              label="时间范围"
              :labelCol="{span: 5}"
              :wrapperCol="{span: 18, offset: 1}"
            >
              <a-range-picker
              	:ranges='timeRange'
              	:placeholder="['开始时间', '结束时间']"
              	@change="createChange"
              	style="width: 100%" 
              />
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
			          <div class="meta-title" style="margin-bottom: 2px" slot="title">
									<a @click="showSample(item)">
										{{item.titleSample}} 
										<a-icon type="arrows-alt" theme="outlined"  />
									</a>
								</div>
			          <div class="meta-content" slot="description">
									<ve-line :data="item.dataGraphAbc"></ve-line>
								</div>
			        </a-card-meta>
							<div class="meta-title" v-if="item.markFlag == 'negative' || item.markFlag == 'positive'">
								<a-button type="dashed" v-if="item.markFlag == 'negative'">
									<a-icon type="minus-circle" theme="outlined" :style="{ fontSize: '16px', color: '#f00' }"/>
									已标记为负样本
								</a-button>
								<a-button type="dashed" v-else>
									<a-icon type="plus-circle" theme="outlined" :style="{ fontSize: '16px', color: '#0f0' }"/>
									已标记为正样本
								</a-button>
								<a slot="actions"  @click="updateAnomaly(item.id, 'cancel')">
										<a-button type="primary">取消标记</a-button>
								</a>
							</div>
							<div class="meta-title" v-else >
								<a slot="actions" @click="updateAnomaly(item.id, 'positive')">
									<a-button type="dashed">标记为正样本</a-button>
								</a>
								<a slot="actions"  @click="updateAnomaly(item.id, 'negative')">
										<a-button type="dashed">标记为负样本</a-button>
								</a>
							</div>
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
import moment from 'moment'
import {dataSeries} from '@/utils/dataSeries'
import {getAnomalyList, updateAnomaly} from '@/services/anomaly'

export default {
  name: 'AnomalyList',
	activated() {
		this.fetch(this.pagination)
	},
  data () {
    return {
			loading: false,
			dataSource: [],
			dataAbc: [],
			dataSingleAbc: {},
			visibleEditSample: false,
			visibleShowSample: false,
			titleSample: '',
			titleSamples: [],
			timeRange:
			{
				今天: [moment().startOf('day'), moment()],
				昨天: [moment().startOf('day').subtract(1,'days'), moment().endOf('day').subtract(1, 'days')],
				最近三天: [moment().startOf('day').subtract(2, 'days'), moment().endOf('day')],
				最近一周: [moment().startOf('day').subtract(1, 'weeks'), moment()],
				本月: [moment().startOf('month'), moment()],
				本年: [moment().startOf('year'), moment()]
			},
			pagination: {
				'total': 0,
				'pageSize': 6,
				'currentPage': 1,
				'ordering': '-id',
				'searchKey': {
					'markFlag': this.$route.meta.label,
					'viewSet': '',
					'attr': '',
					'beginTime': '',
					'endTime': ''
				},
				onChange: page => {
					const pager = { ...this.pagination };
					pager.currentPage = page;
					this.pagination = pager;
					this.fetch(this.pagination);
				},
			},
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
							markFlag: results[i].mark_flag,
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
		moment,
		createChange(dates, dateStrings) {
		  this.pagination.searchKey.beginTime = dateStrings[0]
			this.pagination.searchKey.endTime = dateStrings[1]
		},
		
		handleSubmit(e) {
			e.preventDefault();
			this.fetch(this.pagination)
		},
		resetForm() {
			const pager = { ...this.pagination };
			pager.currentPage = 1;
			pager.searchKey.viewSet = ''
			pager.searchKey.attr = ''
			pager.searchKey.beginTime = ''
			pager.searchKey.endTime = ''
			this.pagination = pager;
			this.fetch(this.pagination);
		},
		updateAnomaly(anomalyId, markFlag) {
			updateAnomaly({anomalyId, markFlag}).then(resp => {
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
	.meta-title{
	  font-size: 10px;
		text-align: center;
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
