<template>
  <a-card>
    <div>
      <a-form-model layout="horizontal" ref="searchKey" :model="pagination.searchKey" @submit="handleSubmit">
        <div class="fold">
          <a-row >
          <a-col :md="8" :sm="24" >
            <a-button type="primary" @click="createRecord">新建指标集</a-button>
          </a-col>
					<a-col :md="8" :sm="24" >
            <a-form-model-item
              label="指标集ID"
              :labelCol="{span: 5}"
              :wrapperCol="{span: 18, offset: 1}"
            >
              <a-input placeholder="请输入" v-model="pagination.searchKey.viewSetId" />
            </a-form-model-item>
          </a-col>
					<a-col :md="8" :sm="24" >
					  <a-form-model-item
					    label="指标集名称"
					    :labelCol="{span: 5}"
					    :wrapperCol="{span: 18, offset: 1}"
					  >
					    <a-input placeholder="请输入" v-model="pagination.searchKey.viewSetName" />
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
							<a @click="showRecord(record)">
								<a-button>查看指标</a-button>
							</a>
							<a @click="updateRecord(record)">
								<a-button type="primary" >编辑</a-button>
							</a>
							<a-popconfirm
								title="此指标集的指标不再关联,确定删除？" 
								ok-text="是" 
								cancel-text="否"
								@confirm="deleteRecord(record)">
								<a-button type="danger" >删除</a-button>
							</a-popconfirm>
						</a-button-group>
			    </div>
			  </a-table>
    </div>
		<!-- begin my modal-->
		<a-modal :visible="visibleRecord" :title="modalTitle"
			width='60%'
			@ok="handleModalOk">
			<a-form style="max-width: 500px; margin: 40px auto 0;">
				<a-form-item
					label="指标集Id"
					:labelCol="{span: 7}"
					:wrapperCol="{span: 17}"
					:required="true"
				>
					<a-input placeholder="请输入" v-model="viewSetForm.viewSetId" />
				</a-form-item>
				<a-form-item
					label="指标集名称"
					:labelCol="{span: 7}"
					:wrapperCol="{span: 17}"
					:required="true"
				>
					<a-input placeholder="请输入" v-model="viewSetForm.viewSetName" />
				</a-form-item>
				<a-form-item
					label="描述"
					:labelCol="{span: 7}"
					:wrapperCol="{span: 17}"
					:required="true"
				>
					<a-input placeholder="请输入" v-model="viewSetForm.description" />
				</a-form-item>
				<a-form-item v-if="modalTitle === '编辑指标集'" :wrapperCol="{span: 17, offset: 7}">
					<a @click="updateSaveRecord">
						<a-button type="danger">保存更新</a-button>
					</a>
				</a-form-item>
				<a-form-item v-if="modalTitle === '新建指标集'" :wrapperCol="{span: 17, offset: 7}">
					<a @click="createSaveRecord">
						<a-button type="danger">保存新建</a-button>
					</a>
				</a-form-item>
			</a-form>
		</a-modal>
		<!-- end my modal-->
  </a-card>
</template>

<script>
import {dataSeries} from '@/utils/dataSeries'
import {getViewSetList, createViewSet, deleteViewSet, updateViewSet} from '@/services/metric'

export default {
  name: 'ViewSetList',
	activated() {
		this.fetch(this.pagination)
	},
  data () {
    return {
			modalTitle: '',
			visibleRecord: false,
			viewSetForm: {
				id: 0,
				viewSetId: '',
				viewSetName: '',
				description: '' 
			},
			pagination: {
				'total': 0,
				'pageSize': 10,
				'currentPage': 1,
				'ordering': '-id',
				'searchKey': {
					'viewSetId': '',
					'viewSetName': ''
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
					title: '指标集Id',
					dataIndex: 'viewSetId'
				},
				{
					title: '指标集名称',
					dataIndex: 'viewSetName'
				},
				{
					title: '描述',
					dataIndex: 'description'
				},
				{
					title: '指标数量',
					dataIndex: 'attrCount'
				},
				{
					title: '修改时间',
					dataIndex: 'updateDate',
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
			getViewSetList(params).then(resp => {
				let retData = resp.data
				if (retData.code == 0) {
					this.dataSource = []
					const results = retData.data.results
					for (let i = 0; i < results.length; i++) {
						const updateDate = `${this.$options.filters.secFormat(results[i].update_date)}`
						this.dataSource.push({
							key: i,
							id: results[i].id,
							viewSetId: results[i].view_set_id,
							viewSetName: results[i].view_set_name,
							description: results[i].description,
							attrCount: results[i].attr_count,
							updateDate: updateDate,
							createUser: results[i].username
						})
					}
					const pager = { ...this.pagination }
					pager.total = retData.data.count;
					this.pagination = pager;
					this.loading = false
				} else {
					this.loading = false
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
			pager.searchKey.viewSetId = ''
			pager.searchKey.viewSetName = []
			this.pagination = pager;
			this.fetch(this.pagination)
		},
		createRecord() {
			this.modalTitle = '新建指标集'
			this.visibleRecord = true
		},
		createSaveRecord() {
			createViewSet(this.viewSetForm).then(resp => {
				let retData = resp.data
				if (retData.code == 0) {
					this.fetch(this.pagination)
					this.loading = false
					this.$message.success('新建成功！', 3)
				} else {
					this.loading = false
					this.$message.error('新建失败！' + retData.message, 3)
				}
			})
		},
		updateRecord(params) {
			this.modalTitle = '编辑指标集',
			this.viewSetForm.id = params.id
			this.viewSetForm.viewSetId = params.viewSetId
			this.viewSetForm.viewSetName = params.viewSetName
			this.viewSetForm.description = params.description
			this.visibleRecord = true
		},
		updateSaveRecord() {
			updateViewSet(this.viewSetForm).then(resp => {
				let retData = resp.data
				if (retData.code == 0) {
					this.fetch(this.pagination)
					this.loading = false
					this.$message.success('更新成功！', 3)
				} else {
					this.loading = false
					this.$message.error('更新失败！' + retData.message, 3)
				}
			})
		},
    deleteRecord(record) {
			this.loading = true;
			deleteViewSet(record.id).then(resp => {
				let retData = resp.data
				if (retData.code == 0) {
					this.fetch(this.pagination)
					this.loading = false
					this.$message.success(record.id + '删除成功！', 3)
				} else {
					this.loading = false
					this.$message.error('删除失败！' + retData.message, 3)
				}
			})
    },
		handleModalOk(e) {
			this.viewSetForm.id = 0
			this.viewSetForm.viewSetId = ''
			this.viewSetForm.viewSetName = ''
			this.viewSetForm.description = ''
			this.fetch(this.pagination)
			this.visibleRecord = false
		}
  }
}
</script>

<style lang="less" scoped>
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
