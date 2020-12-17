<template>
  <a-card>
    <div>
      <a-form-model layout="horizontal" ref="searchKey" :model="pagination.searchKey" @submit="handleSubmit">
        <div class="fold">
          <a-row >
          <a-col :md="8" :sm="24" >
            <a-button type="primary" @click="createRecord">新建指标</a-button>
          </a-col>
					<a-col :md="8" :sm="24" >
            <a-form-model-item
              label="指标ID"
              :labelCol="{span: 5}"
              :wrapperCol="{span: 18, offset: 1}"
            >
              <a-input placeholder="请输入" v-model="pagination.searchKey.attrId" />
            </a-form-model-item>
          </a-col>
					<a-col :md="8" :sm="24" >
					  <a-form-model-item
					    label="指标名称"
					    :labelCol="{span: 5}"
					    :wrapperCol="{span: 18, offset: 1}"
					  >
					    <a-input placeholder="请输入" v-model="pagination.searchKey.attrName" />
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
								<a-button>详细</a-button>
							</a>
							<a @click="updateRecord(record)">
								<a-button type="primary" >编辑</a-button>
							</a>
							<a-popconfirm
								title="此指指标不再关联样本,确定删除？" 
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
			:closable="false"
			>
			<a-form style="max-width: 500px; margin: 40px auto 0;">
				<a-form-item
					label="指标Id"
					:labelCol="{span: 7}"
					:wrapperCol="{span: 17}"
					:required="true"
				>
					<a-input type="number"  placeholder="请输入" v-model="attrForm.attrId" :disabled="modalTitle == '查看指标'"/>
				</a-form-item>
				<a-form-item
					label="指标名称"
					:labelCol="{span: 7}"
					:wrapperCol="{span: 17}"
					:required="true"
				>
					<a-input placeholder="请输入" v-model="attrForm.attrName" :disabled="modalTitle == '查看指标'"/>
				</a-form-item>
				<a-form-item
					label="描述"
					:labelCol="{span: 7}"
					:wrapperCol="{span: 17}"
					:required="true"
				>
					<a-input placeholder="请输入" v-model="attrForm.description" :disabled="modalTitle == '查看指标'"/>
				</a-form-item>
				<a-form-item
					label="所属指标集"
					:labelCol="{span: 7}"
					:wrapperCol="{span: 17}"
					:required="true"
				>
					<a-select v-model='attrForm.viewSetId' :disabled="modalTitle == '查看指标'">
						<a-select-option 
							v-for="item in dataSourceViewSet"
							:key="item.id"
							:value="item.id">{{item.viewSetName}}
						</a-select-option>
					</a-select>
				</a-form-item>
				<a-form-item
					label="模型文件名称"
					:labelCol="{span: 7}"
					:wrapperCol="{span: 17}"
					:required="true"
				>
					<a-select v-model='attrForm.modelId' :disabled="modalTitle == '查看指标'">
						<a-select-option 
							v-for="item in dataSourceModel"
							:key="item.id"
							:value="item.id">{{item.modelName}}
						</a-select-option>
					</a-select>
				</a-form-item>
				<a-form-item
					label="保护token"
					:labelCol="{span: 7}"
					:wrapperCol="{span: 17}"
					:required="true"
				>
					<a-input placeholder="请输入" v-model="attrForm.securityToken" :disabled="modalTitle == '查看指标'"/>
					<a-button type="primary" v-if="modalTitle !== '查看指标'" @click="generateToken">
						生成随机token
					</a-button>
				</a-form-item>
				<a-form-item
					label="启用保护token"
					:labelCol="{span: 7}"
					:wrapperCol="{span: 17}"
					:required="true"
				>
					<a-switch v-model="attrForm.checkSecurity" :disabled="modalTitle == '查看指标'"/>
				</a-form-item>
				<a-form-item
					label="监控URL"
					:labelCol="{span: 7}"
					:wrapperCol="{span: 17}"
					:required="true"
				>
					<a-input placeholder="请输入" v-model="attrForm.url" :disabled="modalTitle == '查看指标'"/>
				</a-form-item>
				<a-form-item v-if="modalTitle === '编辑指标'" :wrapperCol="{span: 17, offset: 7}">
					<a @click="updateSaveRecord">
						<a-button type="danger">保存更新</a-button>
					</a>
				</a-form-item>
				<a-form-item v-if="modalTitle === '新建指标'" :wrapperCol="{span: 17, offset: 7}">
					<a @click="createSaveRecord">
						<a-button type="danger">保存新建</a-button>
					</a>
				</a-form-item>
			</a-form>
			 <template slot="footer">
					<a-button key="submit" type="primary" @click="handleModalOk">
						关闭
					</a-button>
				</template>
		</a-modal>
		<!-- end my modal-->
  </a-card>
</template>

<script>
import {randomString} from '@/utils/util'
import {getAttrList, createAttr, deleteAttr, updateAttr} from '@/services/metric'
import {getModelList} from '@/services/task'
import {getViewSetList} from '@/services/metric'

export default {
  name: 'AttrList',
	activated() {
		//每次激活就刷新 ,这里可以接受从指标集传过来的参数，只显示某一类指标
		this.pagination.searchKey.viewSetId = this.$route.params.viewSetId
		this.fetch(this.pagination)
	},
  data () {
    return {
			modalTitle: '',
			visibleRecord: false,
			loading: false,
			dataSource: [],
			dataSourceModel: [],
			dataSourceViewSet: [],
			attrForm: {
				id: 0,
				attrId: '',
				attrName: '',
				description: '',
				viewSetId: '',
				modelId: '',
				securityToken: '',
				checkSecurity: false,
				url: ''
			},
			pagination: {
				'total': 0,
				'pageSize': 10,
				'currentPage': 1,
				'ordering': '-id',
				'searchKey': {
					'attrId': '',
					'attrName': '',
					'viewSetId': this.$route.params.viewSetId
				},
				onChange: page => {
					const pager = { ...this.pagination };
					pager.currentPage = page;
					this.pagination = pager;
					this.fetch(this.pagination);
				},
			},
			columns: [
				{
					title: '指标Id',
					dataIndex: 'attrId'
				},
				{
					title: '指标名称',
					dataIndex: 'attrName'
				},
				{
					title: '描述',
					dataIndex: 'description'
				},
				{
					title: '所属指标集',
					dataIndex: 'viewSetName'
				},
				{
					title: '关联model',
					dataIndex: 'modelName'
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
			//获取分页的指标数据
			this.loading = true;
			getAttrList(params).then(resp => {
				let retData = resp.data
				if (retData.code == 0) {
					this.dataSource = []
					const results = retData.data.results
					for (let i = 0; i < results.length; i++) {
						const updateDate = `${this.$options.filters.secFormat(results[i].update_date)}`
						this.dataSource.push({
							key: i,
							id: results[i].id,
							attrId: results[i].attr_id,
							attrName: results[i].attr_name,
							description: results[i].description,
							viewSetId: results[i].view_set_id,
							viewSetName: results[i].view_set_name,
							modelId: results[i].model_id,
							modelName: results[i].model_name,
							securityToken: results[i].security_token,
							checkSecurity: results[i].check_security,
							url: results[i].url,
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
			}).then(() => {
				//获取所有的模型文件
				this.loading = true;
				getModelList().then(resp => {
					let retData = resp.data
					if (retData.code == 0) {
						this.dataSourceModel = []
						const results = retData.data.results
						for (let i = 0; i < results.length; i++) {
							this.dataSourceModel.push({
								key: i,
								id: results[i].id,
								modelName: results[i].model_name,
							})
						}
						this.loading = false
					} else {
						this.loading = false
						this.$message.error(createRes.message, 3)
					}
				})
			}).then(() => {
				//获取所有的指标集
				this.loading = true;
				getViewSetList().then(resp => {
					let retData = resp.data
					if (retData.code == 0) {
						this.dataSourceViewSet = []
						const results = retData.data.results
						for (let i = 0; i < results.length; i++) {
							this.dataSourceViewSet.push({
								key: i,
								id: results[i].id,
								viewSetName: results[i].view_set_name,
							})
						}
						this.loading = false
					} else {
						this.loading = false
						this.$message.error(createRes.message, 3)
					}
				})
			})
		},
		generateToken() {
			this.attrForm.securityToken = randomString(true, 16, 24)
		},
		handleSubmit(e) {
			e.preventDefault();
			this.fetch(this.pagination)
		},
		resetForm() {
			const pager = { ...this.pagination };
			pager.currentPage = 1;
			pager.searchKey.attrId = ''
			pager.searchKey.attrName = ''
			pager.searchKey.viewSetId = ''
			this.pagination = pager;
			this.fetch(this.pagination)
		},
		showRecord(params) {
			this.modalTitle = '查看指标',
			this.attrForm.id = params.id
			this.attrForm.attrId = params.attrId
			this.attrForm.attrName = params.attrName
			this.attrForm.description = params.description
			this.attrForm.viewSetId = params.viewSetId
			//这里塞入selection下拉框中，value使用modelId，而label使用modelName
			this.attrForm.modelId = params.modelId
			this.attrForm.securityToken = params.securityToken
			this.attrForm.checkSecurity = params.checkSecurity
			this.attrForm.url = params.url
			this.visibleRecord = true
		},
		createRecord() {
			this.modalTitle = '新建指标'
			this.visibleRecord = true
		},
		createSaveRecord() {
			createAttr(this.attrForm).then(resp => {
				let retData = resp.data
				if (retData.code == 0) {
					this.fetch(this.pagination)
					this.loading = false
					this.$message.success('新建成功！', 3)
				} else {
					this.loading = false
					console.log(retData)
					this.$message.error('新建失败！' + retData.data, 3)
				}
			})
		},
		updateRecord(params) {
			this.modalTitle = '编辑指标',
			this.attrForm.id = params.id
			this.attrForm.attrId = params.attrId
			this.attrForm.attrName = params.attrName
			this.attrForm.description = params.description
			this.attrForm.viewSetId = params.viewSetId
			//这里塞入selection下拉框中，value使用modelId
			this.attrForm.modelId = params.modelId
			this.attrForm.securityToken = params.securityToken
			this.attrForm.checkSecurity = params.checkSecurity
			this.attrForm.url = params.url
			this.visibleRecord = true
		},
		updateSaveRecord() {
			updateAttr(this.attrForm).then(resp => {
				let retData = resp.data
				if (retData.code == 0) {
					this.fetch(this.pagination)
					this.loading = false
					this.$message.success('更新成功！', 3)
				} else {
					this.loading = false
					this.$message.error('更新失败！' + retData.data, 3)
				}
			})
		},
    deleteRecord(record) {
			this.loading = true;
			deleteAttr(record.id).then(resp => {
				let retData = resp.data
				if (retData.code == 0) {
					this.fetch(this.pagination)
					this.loading = false
					this.$message.success(record.id + '删除成功！', 3)
				} else {
					this.loading = false
					this.$message.error('删除失败！' + retData.data, 3)
				}
			})
    },
		handleModalOk(e) {
			// 关闭模态窗口时，重置form内容
			for (var key in this.attrForm ) {
			  this.attrForm[key] = null;
			}
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
