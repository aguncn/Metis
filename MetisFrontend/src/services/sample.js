import {SAMPLE_LIST, SAMPLE_UPDATE, SAMPLE_DELETE, SAMPLE_COUNT} from '@/services/api'
import {SAMPLE_UPLOAD_FILE, SAMPLE_UPLOAD_LIST, SAMPLE_UPLOAD_DELETE} from '@/services/api'
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
export async function updateSample(data) {
	console.log(data)
	const id = data.id
	const trainTest = data['trainTest']
	const source = data['source']
	const positiveNegative = data['positiveNegative']
	// 传给DjangoRestFramework的edit的URL需要带pk(id)参数，在这里组合一下
	const SAMPLE_UPDATE_PATH = SAMPLE_UPDATE + id + '/'
  return request(SAMPLE_UPDATE_PATH, METHOD.PATCH, {
		  id,
			trainTest, 
			source,
			positiveNegative
	})
}

/**
 * 获取所有样本集
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

/**
 * 上传样本集
 */

export async function uploadSampleFile(formData) {
	const fileName = formData['name']
	const SAMPLE_UPLOAD_FILE_PATH = SAMPLE_UPLOAD_FILE + fileName + '/'
  return request(SAMPLE_UPLOAD_FILE_PATH, METHOD.POST, {
		formData
		})
}

/**
 * 获取上传样本集任务
 */
export async function getSampleUploadList(data) {
	const pageSize = data['pageSize']
	const currentPage = data['currentPage']
	const ordering = data['ordering']
	const sampleSetUploadId = data['searchKey']['sampleSetUploadId']
  return request(SAMPLE_UPLOAD_LIST, METHOD.GET, {
		pageSize,
		currentPage,
		ordering, 
		'sample_set_upload_id': sampleSetUploadId
	})
}

/**
 * 删除上传样本集任务
 */
export async function deleteUploadSample(data) {
	// 传给DjangoRestFramework的delete的URL需要带pk(id)参数，在这里组合一下
	const SAMPLE_UPLOAD_DELETE_PATH = SAMPLE_UPLOAD_DELETE + data + '/'
  return request(SAMPLE_UPLOAD_DELETE_PATH, METHOD.DELETE)
}

export default {
  sampleCount,
	deleteSample,
	getSampleList,
	updateSample,
	uploadSampleFile,
	getSampleUploadList,
	deleteUploadSample
}
