//跨域代理前缀
// const API_PROXY_PREFIX='/api'
// const BASE_URL = process.env.NODE_ENV === 'production' ? process.env.VUE_APP_API_BASE_URL : API_PROXY_PREFIX
const BASE_URL = process.env.VUE_APP_API_BASE_URL
const REAL_URL = process.env.VUE_APP_API_REAL_URL
module.exports = {
	REGISTER: `${REAL_URL}/account/register/`,
	UPDATE_PASSWORD: `${REAL_URL}/account/update_password/`,
	UPDATE_EMAIL: `${REAL_URL}/account/update_email/`,
	FORGET_PASSWORD: `${REAL_URL}/account/forget_password/`,
	RESET_PASSWORD: `${REAL_URL}/account/reset_password/`,
  LOGIN: `${REAL_URL}/jwt_auth/`,
	TASK_CREATE: `${REAL_URL}/task/create/`,
	TASK_LIST: `${REAL_URL}/task/list/`,
	TASK_DELETE: `${REAL_URL}/task/delete/`,
	MODEL_LIST: `${REAL_URL}/task/model_list/`,
	SAMPLE_COUNT: `${REAL_URL}/sample/count`,
	SAMPLE_LIST: `${REAL_URL}/sample/list/`,
	SAMPLE_UPDATE: `${REAL_URL}/sample/update/`,
	SAMPLE_DELETE: `${REAL_URL}/sample/delete/`,
	SAMPLE_UPLOAD_FILE: `${REAL_URL}/sample/upload_file/`,
	SAMPLE_UPLOAD_LIST: `${REAL_URL}/sample/upload_list/`,
	SAMPLE_UPLOAD_DELETE: `${REAL_URL}/sample/upload_delete/`,
	ANOMALY_LIST: `${REAL_URL}/anomaly/list/`,
	ANOMALY_UPDATE: `${REAL_URL}/anomaly/update/`,
	VIEW_SET_LIST: `${REAL_URL}/metric/view_set_list/`,
	VIEW_SET_CREATE: `${REAL_URL}/metric/view_set_create/`,
	VIEW_SET_UPDATE: `${REAL_URL}/metric/view_set_update/`,
	VIEW_SET_DELETE: `${REAL_URL}/metric/view_set_delete/`,
	ATTR_LIST: `${REAL_URL}/metric/attr_list/`,
	ATTR_CREATE: `${REAL_URL}/metric/attr_create/`,
	ATTR_UPDATE: `${REAL_URL}/metric/attr_update/`,
	ATTR_DELETE: `${REAL_URL}/metric/attr_delete/`,
  ROUTES: `${BASE_URL}/routes`
}
