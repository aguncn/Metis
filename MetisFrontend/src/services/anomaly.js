import {ANOMALY_LIST} from '@/services/api'
import {request, METHOD} from '@/utils/request'

/**
 * 获取所有异常时序
 */
export async function getAnomalyList(data) {
	const pageSize = data['pageSize']
	const currentPage = data['currentPage']
	const ordering = data['ordering']
	const taskId = data['searchKey']['taskId']
	const source = data['searchKey']['source']
	const taskStaus = data['searchKey']['taskStaus']
	const modelName = data['searchKey']['modelName']
	const trainDate = data['searchKey']['trainDate']
  return request(ANOMALY_LIST, METHOD.GET, {
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
	getAnomalyList
	
}
