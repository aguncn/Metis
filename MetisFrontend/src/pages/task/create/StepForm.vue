<template>
  <a-card :bordered="false">
    <a-steps class="steps" :current="current">
      <a-step title="样本选择" />
      <a-step title="信息确认" />
    </a-steps>
    <div class="content">
      <sample-choice v-if="current === 0" @nextStep="nextStepInfo" />
      <info-confirm v-if="current === 1" :taskForm="taskForm" @nextStep="nextStepTask" @prevStep="prevStep" />
    </div>
  </a-card>
</template>

<script>
import SampleChoice from './Step1'
import InfoConfirm from './Step2'

export default {
  name: 'StepForm',
  components: {SampleChoice, InfoConfirm},
  data () {
    return {
      current: 0,
			taskForm: {
				source: '',
				trainTest: '',
				dateRange: {
					beginTime: '',
					endTime: ''
				}
			}
    }
  },
  computed: {
    desc() {
      return "基于已有样本数据，新建一个训练任务，生成新的模型文件。"
    }
  },
  methods: {
		nextStepInfo(params) {
			this.taskForm = params
		  this.current = 1
		},
		nextStepTask(params) {
			this.taskForm = params
		},
    prevStep () {
      if (this.current > 0) {
        this.current -= 1
      }
    }
  }
}
</script>

<style lang="less" scoped>
  .steps{
    max-width: 950px;
    margin: 16px auto;
  }
</style>
