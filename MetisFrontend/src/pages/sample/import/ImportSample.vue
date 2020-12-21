<template>
  <a-card>
    <div>
      <a-form-model layout="horizontal" ref="searchKey" :model="pagination.searchKey" @submit="handleSubmit">
        <div class="fold">
          <a-row>
						<a-col :md="8" :sm="24" >
							<a-form-model-item
								label="文件名"
								:labelCol="{span: 5}"
								:wrapperCol="{span: 18, offset: 1}"
							>
								<a-input placeholder="请输入" v-model="pagination.searchKey.taskId" />
							</a-form-model-item>
						</a-col>
						<a-col :md="8" :sm="24" >
							<a-form-model-item
								label="备注"
								:labelCol="{span: 5}"
								:wrapperCol="{span: 18, offset: 1}"
							>
								<a-input placeholder="请输入" />
							</a-form-model-item>
						</a-col>
						<a-col :md="8" :sm="24" >
							<a-form-model-item
								label="时间范围"
								:labelCol="{span: 5}"
								:wrapperCol="{span: 18, offset: 1}"
							>

							</a-form-model-item>
						</a-col>
          </a-row>
        </div>
        <span style="float: right; margin-top: 3px;">
          <a-button type="primary" html-type="submit">查询</a-button>
          <a-button style="margin-left: 8px" html-type="reset" @click="resetForm">重置</a-button>
					<a-button style="margin-left: 8px" type="primary" icon="import" ghost @click="onModalImport">
						导入
					</a-button>
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
		<!-- begin my modal-->
		<a-modal :visible="visibleShowImport" title="导入样本"
			width='60%'
			:closable="false"
			>
			<a-alert type="info">
				<span slot="description">
					<a-row>
						<a-col :md="6" :sm="6" >
							<a href="http://127.0.0.1:8000/media/样本导入模板.csv" target="_blank">
								样本导入模板
							</a>
						</a-col>
						<a-col :md="6" :sm="6" >
							<a href="http://127.0.0.1:8000/media/样本导入规则.xls" target="_blank">
								样本导入规则
							</a>
						</a-col>
					</a-row>
				</span>
			</a-alert>
			<a-row class="upload">
				<a-col :md="12" :sm="24" >
					<input type="file" id="sampleFile" />
				</a-col>
				<a-col :md="12" :sm="24" >
					<a-button type="danger" @click="uploadFile">导入</a-button>
				</a-col>
			</a-row>
		 <template slot="footer">
				<a-button type="primary" @click="handleModalImportOk">
					关闭
				</a-button>
			</template>
		</a-modal>
		<!-- end my modal-->
  </a-card>
</template>

<script>

export default {
  name: 'ImportSample',
  data () {
    return {
			dataAbc: [],
			dataSingleAbc: {},
			visibleEditSample: false,
			visibleShowSample: false,
			visibleShowImport: false,
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
			]
    }
  },
  methods: {
		uploadFile:function () {
				var data = new FormData();
				data.append('name',this.name);
				data.append('price',this.price);
				var image =document.getElementById('sampleFile').files[0];
				data.append('file',image);
				this.axios({
						url:'/api/sadmin/addcate/',
						data:data,
						method:'post'
				}).then((res)=>{
						if (res.data.code==200){
								this.$router.push({'path':'show'})
						}
						alert(res.data.message)
				}).catch((err)=>{
						console.log(err)
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
		onModalImport(e) {
			this.visibleShowImport = true
		},
		handleModalImportOk(e) {
			this.visibleShowImport = false
		}
  }
}
</script>
<style lang="less" scoped>
  .search{
    margin-bottom: 54px;
  }
  .fold{
    width: calc(100% - 250px);
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

