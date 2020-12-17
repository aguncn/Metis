<template>
  <a-card>
    <div>
			<a-table 
				:columns="outerColumns" 
				:data-source="outerData" 
				class="components-table-demo-nested"
				:pagination="pagination">
			    <a slot="operation" slot-scope="text">
						<a-button type="primary" >编辑</a-button>
					</a>
			    <a-table
			      slot="expandedRowRender"
			      slot-scope="record"
			      :columns="innerColumns"
						:data-source="record.innerData"			
			      :pagination="false"
			    >
			      <span slot="operation" slot-scope="record" class="table-operation">
			        <a-dropdown>
			          <a-menu slot="overlay">
			            <a-menu-item>
			              编辑
			            </a-menu-item>
			            <a-menu-item>
			              删除
			            </a-menu-item>
			          </a-menu>
			          <a> 操作 <a-icon type="down" /> </a>
			        </a-dropdown>
			      </span>
			    </a-table>
			  </a-table>
    </div>
  </a-card>
</template>

<script>
import {getViewSetList, getAttrList} from '@/services/metric'

export default {
  name: 'MetricList',
	activated() {
		this.fetch(this.pagination)
	},
  data () {
    return {
			outerColumns: [
				{ title: '指标集ID', dataIndex: 'id', key: 'id' },
				{ title: '指标集', dataIndex: 'viewName', key: 'viewName' },
				{ title: '指标数', dataIndex: 'attrCount'},
				{ title: '更新时间', dataIndex: 'updateDate', key: 'updateDate' },
				{ title: 'Action', key: 'operation', scopedSlots: { customRender: 'operation' } }
			],
			innerColumns: [
				{ title: '指标ID', dataIndex: 'id', key: 'id' },
				{ title: '指标', dataIndex: 'attrName', key: 'attrName' },
				{ title: '更新时间', dataIndex: 'updateDate', key: 'updateDate' },
				{
				  title: '',
				  dataIndex: 'operation',
				  key: 'operation',
				  scopedSlots: { customRender: 'operation' },
				},
			],
			outerData: [],
			pagination: {
				'total': 0,
				'pageSize': 10,
				'currentPage': 1,
				onChange: page => {
					const pager = { ...this.pagination };
					pager.currentPage = page;
					this.pagination = pager;
					this.fetch(this.pagination);
				},
			},
			loading: false,
    }
  },
	methods: {
		fetch(params={}) {
			this.loading = true;
			getViewSetList(params).then(resp => {
				let retData = resp.data
				if (retData.code == 0) {
					this.outerData = []
					const results = retData.data.results
					console.log(results)
					for (let i = 0; i < results.length; i++) {
						this.outerData.push({
							key: i,
							id: results[i].id,
							viewId: results[i].view_id,
							viewName: results[i].view_name,
							attrCount: results[i].attr_count,
							innerData: [],
							updateDate: results[i].update_date
						})
					}
					const pager = { ...this.pagination };
					pager.total = retData.data.count;
					this.pagination = pager;
					this.loading = false;
				} else {
					this.loading = false;
					this.$message.error(createRes.message, 3)
				}
			}).then(() => {
				for (let i = 0; i < this.outerData.length; i++) {
					const viewSetId = this.outerData[i].id
					let innerData = []
					getAttrList(viewSetId).then(resp => {
						let retData = resp.data
						if (retData.code == 0) {
							const results = retData.data
							for (let i = 0; i < results.length; i++) {
								innerData.push({
									key: viewSetId*10 + i,
									id: results[i].id,
									attrId: results[i].attr_id,
									attrName: results[i].attr_name,
									updateDate: results[i].update_date
								})
							}
							this.outerData[i].innerData = innerData
						} else {
							this.loading = false;
							this.$message.error(createRes.message, 3)
						}
					})
				}
			})
		},
		fetchAttr(viewSetId) {
			
		},
		
		expandedRowRender(record) {
			console.log(record)
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
