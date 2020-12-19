import {REGISTER, FORGET_PASSWORD, RESET_PASSWORD, LOGIN, ROUTES} from '@/services/api'
import {UPDATE_PASSWORD, UPDATE_EMAIL} from '@/services/api'
import {request, METHOD, removeAuthorization} from '@/utils/request'

/**
 * 注册服务
 * @param name 账户名
 * @param password 账户密码
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function register({username, password, passwordConfirm, email}) {
  return request(REGISTER, METHOD.POST, {
    username,
    password,
		passwordConfirm,
		email
  })
}

/**
 * 更新密码
 * @param name 账户名
 * @param password 账户密码
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function updatePassword({username, currentPassword, newPassword, newPasswordConfirm}) {
  return request(UPDATE_PASSWORD, METHOD.POST, {
		username,
    currentPassword,
    newPassword,
		newPasswordConfirm
  })
}

/**
 * 更新邮箱
 * @param name 账户名
 * @param password 账户密码
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function updateEmail({username, newEmail, newEmailConfirm}) {
  return request(UPDATE_EMAIL, METHOD.POST, {
		username,
    newEmail,
    newEmailConfirm
  })
}

/**
 * 忘记密码
 * @param name 账户名
 * @param password 账户密码
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function forgetPassword(email) {
	console.log(email)
  return request(FORGET_PASSWORD, METHOD.POST, {
		email
  })
}

/**
 * 重置密码
 * @param name 账户名
 * @param password 账户密码
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function resetPassword(email, verificationCode) {
	console.log(email, verificationCode)
  return request(RESET_PASSWORD, METHOD.POST, {
		email,
		verificationCode
  })
}

/**
 * 登录服务
 * @param name 账户名
 * @param password 账户密码
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function login(name, password) {
  return request(LOGIN, METHOD.POST, {
    username: name,
    password: password
  })
}

export async function getRoutesConfig() {
  return request(ROUTES, METHOD.GET)
}

/**
 * 退出登录
 */
export function logout() {
  localStorage.removeItem(process.env.VUE_APP_ROUTES_KEY)
  localStorage.removeItem(process.env.VUE_APP_PERMISSIONS_KEY)
  localStorage.removeItem(process.env.VUE_APP_ROLES_KEY)
  removeAuthorization()
}
export default {
  login,
  logout,
  getRoutesConfig
}
