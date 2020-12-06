//跨域代理前缀
// const API_PROXY_PREFIX='/api'
// const BASE_URL = process.env.NODE_ENV === 'production' ? process.env.VUE_APP_API_BASE_URL : API_PROXY_PREFIX
const BASE_URL = process.env.VUE_APP_API_BASE_URL
const REAL_URL = process.env.VUE_APP_API_REAL_URL
module.exports = {
  LOGIN: `${REAL_URL}/jwt_auth/`,
	TASK_CREATE: `${REAL_URL}/task/create/`,
	TASK_LIST: `${REAL_URL}/task/list/`,
	TASK_DELETE: `${REAL_URL}/task/delete/`,
	SAMPLE_COUNT: `${REAL_URL}/sample/count`,
	SAMPLE_LIST: `${REAL_URL}/sample/list/`,
	SAMPLE_EDIT: `${REAL_URL}/sample/edit/`,
	SAMPLE_DELETE: `${REAL_URL}/sample/delete/`,
  ROUTES: `${BASE_URL}/routes`
}
