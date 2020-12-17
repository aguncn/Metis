import {ANOMALY_LIST, ANOMALY_UPDATE} from '@/services/api'
import {request, METHOD} from '@/utils/request'

/**
 * 获取所有异常时序
 */
export async function getAnomalyList(data) {
	const pageSize = data['pageSize']
	const currentPage = data['currentPage']
	const ordering = data['ordering']
	const markFlag = data['searchKey']['markFlag']
	const beginTime = data['searchKey']['beginTime']
	const endTime = data['searchKey']['endTime']
	const viewSet = data['searchKey']['viewSet']
	const attr = data['searchKey']['attr']
  return request(ANOMALY_LIST, METHOD.GET, {
		pageSize,
		currentPage,
		ordering, 
		'mark_flag': markFlag,
		'begin_time': beginTime,
		'end_time': endTime,
		'attr': attr,
		'view_set': viewSet,
		
	})
}

/**
 * 标注异常时序，更新到样本库
 */
export async function updateAnomaly(data) {
	const anomalyId = data['anomalyId']
	const markFlag = data['markFlag']
  return request(ANOMALY_UPDATE, METHOD.POST, {
		anomalyId,
		markFlag
	})
}

export default {
	getAnomalyList,
	updateAnomaly
	
}
