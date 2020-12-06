import {TASK_CREATE, TASK_LIST, TASK_DELETE} from '@/services/api'
import {request, METHOD, removeAuthorization} from '@/utils/request'

/**
 * 新建训练任务
 */
export async function createTask(data) {
	const beginTime = data['dateRange']['beginTime']
	const endTime = data['dateRange']['endTime']
	const source = data['source']
	const trainTest = data['trainTest']
	const negativeCount = data['negativeCount']
	const positiveCount = data['positiveCount']
	const totalCount = data['totalCount']
  return request(TASK_CREATE, METHOD.POST, {
    trainTest,
    source,
    beginTime,
    endTime,
		totalCount,
		positiveCount,
		negativeCount
  })
}

/**
 * 删除训练任务
 */
export async function deleteTask(data) {
	// 传给DjangoRestFramework的delete的URL需要带pk(id)参数，在这里组合一下
	const TASK_DELETE_PATH = TASK_DELETE + data + '/'
  return request(TASK_DELETE_PATH, METHOD.DELETE)
}

/**
 * 获取所有训练任务
 */
export async function getTaskList(data) {
	const pageSize = data['pageSize']
	const currentPage = data['currentPage']
	const ordering = data['ordering']
	const taskId = data['searchKey']['taskId']
	const source = data['searchKey']['source']
	const taskStaus = data['searchKey']['taskStaus']
	const modelName = data['searchKey']['modelName']
	const trainDate = data['searchKey']['trainDate']
  return request(TASK_LIST, METHOD.GET, {
		pageSize,
		currentPage,
		ordering, 
		'task_id': taskId,
		source,
		taskStaus,
		modelName,
		trainDate
	})
}


export default {
  createTask,
	getTaskList,
	deleteTask
}
