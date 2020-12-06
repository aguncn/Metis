<template>
  <div>
    <a-form style="max-width: 500px; margin: 40px auto 0;">
      <a-form-item
        label="样本来源"
        :labelCol="{span: 7}"
        :wrapperCol="{span: 17}"
				:required="true"
      >
        <a-select mode="multiple" v-model='taskForm.source'>
          <a-select-option value="metis">Metis</a-select-option>
          <a-select-option value="api">API</a-select-option>
					<a-select-option value="unknown">Unknown</a-select-option>
        </a-select>
      </a-form-item>
			<a-form-item
			  label="测试/训练集"
			  :labelCol="{span: 7}"
			  :wrapperCol="{span: 17}"
				:required="true"
			>
			  <a-select mode="multiple" v-model='taskForm.trainTest'>
			    <a-select-option value="train">训练集</a-select-option>
			    <a-select-option value="test">测试集</a-select-option>
			  </a-select>
			</a-form-item>
      <a-form-item
        label="时间范围"
        :labelCol="{span: 7}"
        :wrapperCol="{span: 17}"
				:required="true"
      >
        <a-range-picker
					:ranges='timeRange'
					:default-value="[
					   moment().startOf('month'),
					   moment().startOf('day'),
					]"
					:placeholder="['开始时间', '结束时间']"
					@change="createChange"
					style="width: 100%" 
				/>
      </a-form-item>
      <a-form-item :wrapperCol="{span: 17, offset: 7}">
        <a-button :disabled=isChoice type="primary" @click="nextStep">下一步</a-button>
      </a-form-item>
    </a-form>
  </div>
</template>

<script>
import moment from 'moment'
export default {
  name: 'SampleChoice',
	data () {
	  return {
			taskForm: {
				source: ['metis', 'api', 'unknow'],
				trainTest: ['train', 'test'],
				dateRange: {
					beginTime: moment().startOf('month').format('YYYY-MM-DD'),
					endTime: moment().startOf('day').format('YYYY-MM-DD')
				}
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
	  }
	},
	computed: {
		isChoice() {
			return !(this.taskForm.trainTest.length
				&& this.taskForm.source.length
				&& this.taskForm.dateRange.beginTime
				&& this.taskForm.dateRange.endTime)
		},
	},
  methods: {
    nextStep () {
      this.$emit('nextStep', this.taskForm)
    },
		moment,
		createChange(dates, dateStrings) {
		  this.taskForm.dateRange.beginTime = dateStrings[0]
			this.taskForm.dateRange.endTime = dateStrings[1]
		},
  }
}
</script>