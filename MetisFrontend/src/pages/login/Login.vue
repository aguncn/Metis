<template>
  <common-layout>
    <div class="top">
      <div class="header">
        <img alt="logo" class="logo" src="@/assets/img/logo.png" />
        <span class="title">{{systemName}}</span>
      </div>
      <div class="desc">Metis 用于时序异常检测的AIOPS平台</div>
    </div>
    <div class="login">
			<a-tabs :active-key="activeKey" @change="tabChange"  size="large" :tabBarStyle="{textAlign: 'center'}" style="padding: 0 2px;">
				<a-tab-pane tab="登录" key="1">
					<a-form @submit="onSubmitLogin" :form="formLogin">
            <a-alert type="error" :closable="true" v-show="error" :message="error" showIcon style="margin-bottom: 24px;" />
            <a-form-item>
              <a-input
                autocomplete="autocomplete"
                size="large"
                placeholder="admin"
                v-decorator="['name', {rules: [{ required: true, message: '请输入账户名', whitespace: true}]}]"
              >
                <a-icon slot="prefix" type="user" />
              </a-input>
            </a-form-item>
            <a-form-item>
              <a-input
                size="large"
                placeholder="888888"
                autocomplete="autocomplete"
                type="password"
                v-decorator="['password', {rules: [{ required: true, message: '请输入密码', whitespace: true}]}]"
              >
                <a-icon slot="prefix" type="lock" />
              </a-input>
            </a-form-item>
						<div>
						  <a-checkbox :checked="true" >自动登录</a-checkbox>
						  <a style="float: right">忘记密码</a>
						</div>
						<a-form-item>
						  <a-button :loading="logging" style="width: 100%;margin-top: 24px" size="large" htmlType="submit" type="primary">用户登录</a-button>
						</a-form-item>
					</a-form>
				</a-tab-pane>
				<a-tab-pane tab="注册" key="2">
					<a-form @submit="onSubmitRegister" :form="formRegister">
					  <a-alert type="error" :closable="true" v-show="error" :message="error" showIcon style="margin-bottom: 24px;" />
					  <a-form-item>
					    <a-input
					      autocomplete="autocomplete"
					      size="large"
					      placeholder="username"
					      v-decorator="['username', {rules: [{ required: true, message: '请输入账户名', whitespace: true}]}]"
					    >
					      <a-icon slot="prefix" type="user" />
					    </a-input>
					  </a-form-item>
					  <a-form-item>
					    <a-input
					      size="large"
					      placeholder="password"
					      autocomplete="autocomplete"
					      type="password"
					      v-decorator="['password', {rules: [{ required: true, message: '请输入密码', whitespace: true}]}]"
					    >
					      <a-icon slot="prefix" type="lock" />
					    </a-input>
					  </a-form-item>
						<a-form-item>
						  <a-input
						    size="large"
						    placeholder="password"
						    autocomplete="autocomplete"
						    type="password"
						    v-decorator="['passwordConfirm', {rules: [{ required: true, message: '请确认密码', whitespace: true}]}]"
						  >
						    <a-icon slot="prefix" type="lock" />
						  </a-input>
						</a-form-item>
						<a-form-item>
						  <a-button :loading="logging" style="width: 100%;margin-top: 24px" size="large" htmlType="submit" type="danger">用户注册</a-button>
						</a-form-item>
					</a-form>
				</a-tab-pane>
			</a-tabs>
    </div>
  </common-layout>
</template>

<script>
import CommonLayout from '@/layouts/CommonLayout'
import {register, login, getRoutesConfig} from '@/services/user'
import {setAuthorization} from '@/utils/request'
import {loadRoutes} from '@/utils/routerUtil'
import {mapMutations} from 'vuex'

export default {
  name: 'Login',
  components: {CommonLayout},
  data () {
    return {
      logging: false,
			activeKey: '1',
      error: '',
      formLogin: this.$form.createForm(this),
			formRegister: this.$form.createForm(this)
    }
  },
  computed: {
    systemName () {
      return this.$store.state.setting.systemName
    }
  },
  methods: {
    ...mapMutations('account', ['setUser', 'setPermissions', 'setRoles']),
		tabChange (key) {
			this.activeKey = key
		},
		onSubmitRegister (e) {
		  e.preventDefault()
		  this.formRegister.validateFields((err) => {
		    if (!err) {
		      this.logging = true
		      const username = this.formRegister.getFieldValue('username')
		      const password = this.formRegister.getFieldValue('password')
					const passwordConfirm = this.formRegister.getFieldValue('passwordConfirm')
		      if (password !== passwordConfirm) {
						this.logging = false
						this.$message.error("两次密码不一致", 3)
						return
					}
					register({username, password, passwordConfirm}).then((res) => {
						const registerRes = res.data
						if (registerRes.code === 0) {
							this.logging = false
							this.activeKey = '1'
							this.$message.success('用户注册成功', 3)

						} else {
							this.logging = false
							this.$message.error(registerRes.data, 3)
						}
						
					})
		    }
		  })
		},
    onSubmitLogin (e) {
      e.preventDefault()
      this.formLogin.validateFields((err) => {
        if (!err) {
          this.logging = true
          const name = this.formLogin.getFieldValue('name')
          const password = this.formLogin.getFieldValue('password')
          login(name, password).then(this.afterLogin)
        }
      })
    },
    afterLogin(res) {
      this.logging = false
      const loginRes = res.data
      if (loginRes.code === 0) {
        const {user, permissions, roles} = loginRes.data
        this.setUser(user)
        this.setPermissions(permissions)
        this.setRoles(roles)
        setAuthorization({token: loginRes.data.token, expireAt: new Date(loginRes.data.expireAt)})
        // 获取路由配置
        getRoutesConfig().then(result => {
          const routesConfig = result.data.data
          loadRoutes(routesConfig)
          this.$router.push('/anomaly/all_list')
          this.$message.success(loginRes.message, 3)
        })
      } else {
    		// 原来的代码已注释，新加了logging状态终止，跳出弹窗3秒提示错误。
    		// this.error = loginRes.message
    		this.logging = false
    		this.$message.error(loginRes.data.message, 3)
      }
    }
  }
}
</script>

<style lang="less" scoped>
  .common-layout{
    .top {
      text-align: center;
      .header {
        height: 44px;
        line-height: 44px;
        a {
          text-decoration: none;
        }
        .logo {
          height: 44px;
          vertical-align: top;
          margin-right: 16px;
        }
        .title {
          font-size: 33px;
          color: @title-color;
          font-family: 'Myriad Pro', 'Helvetica Neue', Arial, Helvetica, sans-serif;
          font-weight: 600;
          position: relative;
          top: 2px;
        }
      }
      .desc {
        font-size: 14px;
        color: @text-color-second;
        margin-top: 12px;
        margin-bottom: 40px;
      }
    }
    .login{
      width: 368px;
      margin: 0 auto;
      @media screen and (max-width: 576px) {
        width: 95%;
      }
      @media screen and (max-width: 320px) {
        .captcha-button{
          font-size: 14px;
        }
      }
      .icon {
        font-size: 24px;
        color: @text-color-second;
        margin-left: 16px;
        vertical-align: middle;
        cursor: pointer;
        transition: color 0.3s;

        &:hover {
          color: @primary-color;
        }
      }
    }
  }
</style>
