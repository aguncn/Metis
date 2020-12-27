<template>
  <a-card>
    <div>
      <a-form-model layout="horizontal" ref="searchKey" :model="pagination.searchKey" @submit="handleSubmit">
        <div class="fold">
          <a-row>
          <a-col :md="12" :sm="24" >
            <a-form-model-item
              label="上传文件名"
              :labelCol="{span: 5}"
              :wrapperCol="{span: 18, offset: 1}"
            >
              <a-input placeholder="请输入" v-model="pagination.searchKey.attr" />
            </a-form-model-item>
          </a-col>
          <a-col :md="12" :sm="24" >
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
          <a-button style="margin-left: 8px" html-type="reset">重置</a-button>
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
					<a-popconfirm 
						title="确定删除？" 
						ok-text="是" 
						cancel-text="否"
						@confirm="deleteRecord(record)">
						<a-button type="danger" >删除</a-button>
					</a-popconfirm>
				</div>
				<div slot='fileName' slot-scope="record">
					<a :href="record.filePath" target="_blank">
					  {{record.fileName}}
					</a>
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
	
			<a-row class="upload" style="margin-top: 16px">
				<a-col :md="24" :sm="24" >
					<div class="clearfix">
						<a-upload :file-list="fileList" :remove="handleRemove" :before-upload="beforeUpload">
							<a-button> <a-icon type="upload" /> 选择样本 </a-button>
						</a-upload>
						<a-button
							type="primary"
							accept=".csv,.xls,.xlsx"
							:disabled="fileList.length === 0"
							:loading="uploading"
							style="margin-top: 16px"
							@click="handleUpload"
						>
							{{ uploading ? '上传导入中' : '导入' }}
						</a-button>
					</div>
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
import moment from 'moment'
import axios from 'axios';
import {uploadSampleFile, getSampleUploadList, deleteUploadSample} from '@/services/sample'


export default {
  name: 'ImportSample',
	activated() {
		this.fetch(this.pagination)
	},
  data () {
    return {
			fileList: [],
			uploading: false,
			visibleShowImport: false,
			viewSetForm: {
				id: 0,
				sampleSetUploadId: '',
				viewSetName: '',
				description: '' 
			},
			timeRange:
			{
				今天: [moment().startOf('day'), moment()],
				昨天: [moment().startOf('day').subtract(1,'days'), moment().endOf('day').subtract(1, 'days')],
				最近三天: [moment().startOf('day').subtract(2, 'days'), moment().endOf('day')],
				最近一周: [moment().startOf('day').subtract(1, 'weeks'), moment()],
				本月: [moment().startOf('month'), moment()],
				本年: [moment().startOf('year'), moment()]
			},
			// 分页里可以加上排序，过滤搜索关键字，这就是前后端分享，双向绑定的好处
			// 后端使用django rest framework结合django_filters插件，一条龙完成
			pagination: {
				'total': 0,
				'pageSize': 10,
				'currentPage': 1,
				'ordering': '-id',
				'searchKey': {
					'sampleSetUploadId': '',
					'description': ''
				},
				//这种onChange切换分页，才是官网推荐方式
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
					title: '上传样本任务Id',
					dataIndex: 'sampleSetUploadId'
				},
				{
					title: '文件名',
					scopedSlots: {customRender: 'fileName'} 
				},
				{
					title: '描述',
					dataIndex: 'description'
				},
				{
					title: '指标数量',
					dataIndex: 'sampleCount'
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
			getSampleUploadList(params).then(resp => {
				let retData = resp.data
				if (retData.code == 0) {
					this.dataSource = []
					const results = retData.data.results
					console.log(results)
					for (let i = 0; i < results.length; i++) {
						const updateDate = `${this.$options.filters.secFormat(results[i].update_date)}`
						this.dataSource.push({
							key: i,
							id: results[i].id,
							sampleSetUploadId: results[i].sample_set_upload_id,
							fileName: results[i].file_name,
							filePath: results[i].file_path,
							description: results[i].description,
							sampleCount: results[i].sample_count,
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
		createChange(dates, dateStrings) {
		  this.taskForm.dateRange.beginTime = dateStrings[0]
			this.taskForm.dateRange.endTime = dateStrings[1]
		},
		handleSubmit(e) {
			e.preventDefault();
			this.fetch(this.pagination)
		},
		resetForm() {
			const pager = { ...this.pagination };
			pager.currentPage = 1;
			pager.searchKey.sampleSetUploadId = ''
			this.pagination = pager;
			this.fetch(this.pagination)
		},
		handleRemove(file) {
			const index = this.fileList.indexOf(file);
			const newFileList = this.fileList.slice();
			newFileList.splice(index, 1);
			//这里配合beforeUpload里的非注释部分，实现单文件上传
			this.fileList = [];
		},
		beforeUpload(file) {
			//this.fileList = [...this.fileList, file];
			//单 文件上传
			this.fileList = [file];
			return false;
		},
		handleUpload() {
			const { fileList } = this;
			// FormData，确实好用
			const formData = new FormData();
			//不用for循环，直接拿第一个文件
			formData.append('file', this.fileList[0]);
			const fileName = formData.get('file')['name'];
			this.uploading = true;
			// 用纯的axios可以搞定，但使用二次封装过的，暂时有问题。
			const instance = axios.create({
			　　withCredentials: true  //表示跨域请求时是否需要使用凭证，默认为false
			})
			const url = `http://127.0.0.1:8000/sample/upload_file/${fileName}/`
			console.log(url)
			instance.post(url,formData).then(resp => {
				let retData = resp.data
				if (retData.code == 0) {
					this.fileList = [];
					this.uploading = false;
					this.$message.success('成功导入.');
				} else {
					this.uploading = false;
					this.fileList = [];
					this.$message.error('导入失败.');
				}
				this.fetch(this.pagination)
			})
		},
		onModalImport(e) {
			this.visibleShowImport = true
		},
		handleModalImportOk(e) {
			this.visibleShowImport = false
		},
		deleteRecord(record) {
			this.loading = true;
			deleteUploadSample(record.id).then(resp => {
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
  }
}
</script>
<style lang="less" scoped>
  .search{
    margin-bottom: 54px;
  }
	.upload{
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

