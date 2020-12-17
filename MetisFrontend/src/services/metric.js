import {VIEW_SET_LIST, VIEW_SET_CREATE, VIEW_SET_UPDATE, VIEW_SET_DELETE} from '@/services/api'
import {ATTR_LIST, ATTR_CREATE, ATTR_UPDATE, ATTR_DELETE} from '@/services/api'
import {request, METHOD} from '@/utils/request'
import {isEmpty} from '@/utils/util'

/**
 * 新建指标集
 */
export async function createViewSet(data) {
	const viewSetId = data['viewSetId']
	const viewSetName = data['viewSetName']
	const description = data['description']
  return request(VIEW_SET_CREATE, METHOD.POST, {
    viewSetId,
    viewSetName,
    description
  })
}

/**
 * 获取所有指标集
 */
export async function getViewSetList(data) {
	let pageSize, currentPage, ordering, viewSetId, viewSetName
	if (isEmpty(data)) {
		pageSize = 1000
		currentPage = 1
	} else {
		pageSize = data['pageSize']
		currentPage = data['currentPage']
		ordering = data['ordering']
		viewSetId = data['searchKey']['viewSetId']
		viewSetName = data['searchKey']['viewSetName']
	}
	
  return request(VIEW_SET_LIST, METHOD.GET, {
		pageSize,
		currentPage,
		ordering, 
		'view_set_id': viewSetId,
		'view_set_name': viewSetName
	})
}

/**
 * 删除指标集
 */
export async function deleteViewSet(data) {
	// 传给DjangoRestFramework的delete的URL需要带pk(id)参数，在这里组合一下
	const VIEW_SET_DELETE_PATH = VIEW_SET_DELETE + data + '/'
  return request(VIEW_SET_DELETE_PATH, METHOD.DELETE)
}

/**
 * 编辑指标集
 */
export async function updateViewSet(data) {
	console.log(data)
	const id = data.id
	const viewSetId = data['viewSetId']
	const viewSetName = data['viewSetName']
	const description = data['description']
	// 传给DjangoRestFramework的edit的URL需要带pk(id)参数，在这里组合一下
	const VIEW_SET_UPDATE_PATH = VIEW_SET_UPDATE + id + '/'
  return request(VIEW_SET_UPDATE_PATH, METHOD.PATCH, {
		  id,
			viewSetId,
			viewSetName,
			description
	})
}


/**
 * 新建指标
 */
export async function createAttr(data) {
	console.log(data)
	const attrId = data['attrId']
	const attrName = data['attrName']
	const description = data['description']
	const viewSetId = data['viewSetId']
	const modelId = data['modelId']
	const securityToken = data['securityToken']
	const checkSecurity = data['checkSecurity']
	const url = data['url']
  return request(ATTR_CREATE, METHOD.POST, {
    attrId,
    attrName,
    description,
		viewSetId,
		modelId,
		securityToken,
		checkSecurity,
		url
  })
}

/**
 * 获取所有指标
 */
export async function getAttrList(data) {
	const pageSize = data['pageSize']
	const currentPage = data['currentPage']
	const ordering = data['ordering']
	const attrId = data['searchKey']['attrId']
	const attrName = data['searchKey']['attrName']
	const viewSetId = data['searchKey']['viewSetId']
  return request(ATTR_LIST, METHOD.GET, {
		pageSize,
		currentPage,
		ordering, 
		'attr_id': attrId,
		'attr_name': attrName,
		'view_set_id': viewSetId
	})
}

/**
 * 删除指标
 */
export async function deleteAttr(data) {
	// 传给DjangoRestFramework的delete的URL需要带pk(id)参数，在这里组合一下
	const ATTR_DELETE_PATH = ATTR_DELETE + data + '/'
  return request(ATTR_DELETE_PATH, METHOD.DELETE)
}

/**
 * 编辑指标
 */
export async function updateAttr(data) {
	console.log(data)
	const id = data.id
	const attrId = data['attrId']
	const attrName = data['attrName']
	const description = data['description']
	const viewSetId = data['viewSetId']
	const modelId = data['modelId']
	const securityToken = data['securityToken']
	const checkSecurity = data['checkSecurity']
	const url = data['url']
	// 传给DjangoRestFramework的edit的URL需要带pk(id)参数，在这里组合一下
	const ATTR_UPDATE_PATH = ATTR_UPDATE + id + '/'
  return request(ATTR_UPDATE_PATH, METHOD.PATCH, {
		  id,
			attrId,
			attrName,
			description,
			viewSetId,
			modelId,
			securityToken,
			checkSecurity,
			url
	})
}

export default {
	createViewSet,
  getViewSetList,
	updateViewSet,
	deleteViewSet,
	createAttr,
	getAttrList,
	updateAttr,
	deleteAttr,
}