<template>
  <div>
    <a-form style="max-width: 500px; margin: 40px auto 0;">
      <a-form-item
        label="样本来源"
        :labelCol="{span: 7}"
        :wrapperCol="{span: 17}"
        class="stepFormText"
      >
				<a-tag class='primary' v-for="item in taskForm.source" :key="item.id">{{item}} </a-tag>
      </a-form-item>
      <a-form-item
        label="测试/训练集"
        :labelCol="{span: 7}"
        :wrapperCol="{span: 17}"
        class="stepFormText"
      >
				<a-tag class='alert' v-for="item in taskForm.trainTest" :key="item.id">{{item}} </a-tag>
      </a-form-item>
      <a-form-item
        label="时间范围"
        :labelCol="{span: 7}"
        :wrapperCol="{span: 17}"
        class="stepFormText"
      >
        <span > {{taskForm.dateRange.beginTime}} ~ {{taskForm.dateRange.endTime}}</span>
      </a-form-item>
      <a-form-item
        label="正样本数"
        :labelCol="{span: 7}"
        :wrapperCol="{span: 17}"
        class="stepFormText"
      >
        {{positiveCount}}
      </a-form-item>
			<a-form-item
			  label="负样本数"
			  :labelCol="{span: 7}"
			  :wrapperCol="{span: 17}"
			  class="stepFormText"
			>
			  {{negativeCount}}
			</a-form-item>
      <a-form-item :wrapperCol="{span: 17, offset: 7}">
				<a-button style="margin-left: 8px" @click="prevStep">上一步</a-button>
        <a-button :disabled=isChoice :loading="loading" type="primary" @click="nextStep">开始训练</a-button>
      </a-form-item>
			<a-alert type="info" :show-icon="true" v-if="isChoice">
			  <div class="message" slot="message">
			    *正样本或负样本数量为0，无法开始训练
			  </div>
			</a-alert>
    </a-form>
  </div>
</template>

<script>
import {sampleCount} from '@/services/sample'
import {createTask} from '@/services/task'
export default {
  name: 'InfoConfirm',
	props: {
	    taskForm: {
				required: true,
				type: Object
			}
	},
	watch: {
		taskForm: {
			deep: true,
			immediate: true,
			handler(newVal, oldVal) {
				sampleCount(newVal).then(resp => {
					let retData = resp.data
					if (retData.code == 0) {
						this.negativeCount = retData.data.negative_count
						this.positiveCount = retData.data.positive_count
					} else {
						this.$message.error(createRes.message, 3)
					}
				})
			}
		}
	},
	computed: {
		isChoice() {
			return !(this.negativeCount && this.positiveCount)
		}
	},
  data () {
    return {
      loading: false,
			negativeCount: 0,
			positiveCount: 0
    }
  },
  methods: {
    nextStep () {
      let _this = this
      _this.loading = true
			
      //setTimeout(function () {
        //_this.$emit('nextStep')
				//console.log(this.taskForm)
      //}, 1500)
			let params = this.taskForm
			params['negativeCount'] = this.negativeCount
			params['positiveCount'] = this.positiveCount
			params['totalCount'] = this.negativeCount + this.positiveCount
			createTask(params).then(resp => {
				let retData = resp.data
				if (retData.code == 0) {
					setTimeout(function () {
						_this.$closePage('/task/create', '/task/list')
					  _this.$message.success(retData.message, 3)
					}, 1500)
				} else {
					this.$message.error(retData.message + retData.data, 3)
				}
			})
    },
    prevStep () {
      this.$emit('prevStep')
    }
  }
}
</script>

<style lang="less" scoped>
  .stepFormText {
    margin-bottom: 24px;
    :global {
      .ant-form-item-label,
      .ant-form-item-control {
        line-height: 22px;
      }
    }
  }
</style>
