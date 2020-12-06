import {SAMPLE_COUNT, SAMPLE_LIST, SAMPLE_EDIT, SAMPLE_DELETE} from '@/services/api'
import {request, METHOD, removeAuthorization} from '@/utils/request'

/**
 * 获取指定小范围的正负样本数量
 */
export async function sampleCount(data) {
	const beginTime = data['dateRange']['beginTime']
	const endTime = data['dateRange']['endTime']
	const source = data['source']
	const trainTest = data['trainTest']
  return request(SAMPLE_COUNT, METHOD.GET, {
    trainTest,
    source,
		beginTime,
		endTime
  })
}

/**
 * 删除样本
 */
export async function deleteSample(data) {
	// 传给DjangoRestFramework的delete的URL需要带pk(id)参数，在这里组合一下
	const SAMPLE_DELETE_PATH = SAMPLE_DELETE + data + '/'
  return request(SAMPLE_DELETE_PATH, METHOD.DELETE)
}

/**
 * 编辑样本
 */
export async function editSample(data) {
	// 传给DjangoRestFramework的edit的URL需要带pk(id)参数，在这里组合一下
	const SAMPLE_EDIT_PATH = SAMPLE_EDIT + data + '/'
  return request(SAMPLE_EDIT_PATH, METHOD.POST)
}

/**
 * 获取所有样本务
 */
export async function getSampleList(data) {
	const pageSize = data['pageSize']
	const currentPage = data['currentPage']
	const ordering = data['ordering']
	const taskId = data['searchKey']['taskId']
	const source = data['searchKey']['source']
	const taskStaus = data['searchKey']['taskStaus']
	const modelName = data['searchKey']['modelName']
	const trainDate = data['searchKey']['trainDate']
  return request(SAMPLE_LIST, METHOD.GET, {
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
  sampleCount,
	deleteSample,
	getSampleList,
	editSample
	
}
