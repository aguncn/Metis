<template>
	<div>
		<a-dropdown>
		  <div class="header-avatar" style="cursor: pointer">
		    <span class="name">{{user.name}}<a-icon type="down" /></span>
				
		  </div>
		  <a-menu  slot="overlay">
		    <a-menu-item @click="onModalUpdatePassword">
		      <a-icon type="lock" />
		      <span>更新密码</span>
		    </a-menu-item>
		    <a-menu-item @click="onModalUpdateEmail">
		      <a-icon type="mail" />
		      <span>更改邮件</span>
		    </a-menu-item>
		    <a-menu-divider />
		    <a-menu-item @click="logout">
		      <a-icon style="margin-right: 8px;" type="poweroff" />
		      <span>退出登录</span>
		    </a-menu-item>
		  </a-menu>
		</a-dropdown>
		<!-- begin my modal-->
		<a-modal :visible="visiblePassword" title="更新密码"
			width='60%'
			:closable="false"
			>
			<a-form @submit="onUpdatePassword" :form="formUpdatePassword">
				<a-form-item
					label="旧密码"
					:labelCol="{span: 7}"
					:wrapperCol="{span: 17}"
					:required="true"
				>
					<a-input
					  autocomplete="autocomplete"
					  size="large"
					  placeholder="请输入当前密码"
					  v-decorator="['currentPassword', {rules: [{ required: true, message: '请输入当前密码', whitespace: true}]}]"
					>
						<a-icon slot="prefix" type="lock" />
					</a-input>
				</a-form-item>
				<a-form-item
					label="新密码"
					:labelCol="{span: 7}"
					:wrapperCol="{span: 17}"
					:required="true"
				>
					<a-input
					  autocomplete="autocomplete"
					  size="large"
					  placeholder="输入新密码"
					  v-decorator="['newPassword', {rules: [{ required: true, message: '请输入新密码', whitespace: true}]}]"
					>
						<a-icon slot="prefix" type="lock" />
					</a-input>
				</a-form-item>
				<a-form-item
					label="新密码确认"
					:labelCol="{span: 7}"
					:wrapperCol="{span: 17}"
					:required="true"
				>
					<a-input
					  autocomplete="autocomplete"
					  size="large"
					  placeholder="再次输入新密码"
					  v-decorator="['newPasswordConfirm', {rules: [{ required: true, message: '请再输入新密码', whitespace: true}]}]"
					>
						<a-icon slot="prefix" type="lock" />
					</a-input>
				</a-form-item>
				<a-form-item :wrapperCol="{span: 17, offset: 7}">
					<a-button type="danger" size="large" htmlType="submit">更改密码</a-button>
				</a-form-item>
			</a-form>
			 <template slot="footer">
					<a-button type="primary" @click="handleModalUpdatePasswordOk">
						关闭
					</a-button>
				</template>
		</a-modal>
		<!-- end my modal-->
		<!-- begin my modal-->
		<a-modal :visible="visibleEmail" title="更改邮箱"
			width='60%'
			:closable="false"
			>
			<a-form @submit="onUpdateEmail" :form="formUpdateEmail">
				<a-form-item
					label="当前邮箱"
					:labelCol="{span: 7}"
					:wrapperCol="{span: 17}"
					:required="true"
				>
					<a-input
					  autocomplete="autocomplete"
					  size="large"
					  placeholder="请输入当前邮箱"
					  v-decorator="['currentEmail', {rules: [{ required: true, message: '请输入当前邮箱', whitespace: true}]}]"
					>
						<a-icon slot="prefix" type="mail" />
					</a-input>
				</a-form-item>
				<a-form-item
					label="新邮箱"
					:labelCol="{span: 7}"
					:wrapperCol="{span: 17}"
					:required="true"
				>
					<a-input
					  autocomplete="autocomplete"
					  size="large"
					  placeholder="输入新邮箱"
					  v-decorator="['newEmail', {rules: [{ required: true, message: '请输入新邮箱', whitespace: true}]}]"
					>
						<a-icon slot="prefix" type="mail" />
					</a-input>
				</a-form-item>
				<a-form-item
					label="新邮箱确认"
					:labelCol="{span: 7}"
					:wrapperCol="{span: 17}"
					:required="true"
				>
					<a-input
					  autocomplete="autocomplete"
					  size="large"
					  placeholder="再次输入新邮箱"
					  v-decorator="['newEmailConfirm', {rules: [{ required: true, message: '请再输入新邮箱', whitespace: true}]}]"
					>
						<a-icon slot="prefix" type="mail" />
					</a-input>
				</a-form-item>
				<a-form-item :wrapperCol="{span: 17, offset: 7}">
					<a-button type="danger" size="large" htmlType="submit">更改邮箱</a-button>
				</a-form-item>
			</a-form>
			 <template slot="footer">
					<a-button type="primary" @click="handleModalUpdateEmailOk">
						关闭
					</a-button>
				</template>
		</a-modal>
		<!-- end my modal-->
	</div>
  
</template>

<script>
import {mapGetters} from 'vuex'
import {logout} from '@/services/user'
import {register, forgetPassword, resetPassword, login, getRoutesConfig} from '@/services/user'

export default {
  name: 'HeaderAvatar',
  computed: {
    ...mapGetters('account', ['user']),
  },
	data () {
	  return {
	    logging: false,
			visiblePassword: false,
			visibleEmail: false,
			formUpdatePassword: this.$form.createForm(this),
			formUpdateEmail: this.$form.createForm(this),
	  }
	},
  methods: {
    logout() {
      logout()
      this.$router.push('/login')
    },
		onModalUpdatePassword(e) {
			this.visiblePassword = true
		},
		onUpdatePassword (e) {
		  e.preventDefault()
		  this.formEmail.validateFields((err) => {
		    if (!err) {
		      this.logging = true
					const email = this.formEmail.getFieldValue('email')
					this.email = email
					forgetPassword(email).then((res) => {
						const forgetPasswordRes = res.data
						if (forgetPasswordRes.code === 0) {
							this.logging = false
							this.$message.success('验证码已发出，请检查邮件', 3)
							this.visibleCode = true
		
						} else {
							this.logging = false
							this.$message.error(forgetPasswordRes.data, 3)
						}
						
					})
		    }
		  })
		},
		handleModalUpdatePasswordOk(e) {
			this.visiblePassword = false
		},
		onModalUpdateEmail(e) {
			this.visibleEmail = true
		},
		onUpdateEmail (e) {
		  e.preventDefault()
		  this.formEmail.validateFields((err) => {
		    if (!err) {
		      this.logging = true
					const email = this.formEmail.getFieldValue('email')
					this.email = email
					forgetPassword(email).then((res) => {
						const forgetPasswordRes = res.data
						if (forgetPasswordRes.code === 0) {
							this.logging = false
							this.$message.success('验证码已发出，请检查邮件', 3)
							this.visibleCode = true
		
						} else {
							this.logging = false
							this.$message.error(forgetPasswordRes.data, 3)
						}
						
					})
		    }
		  })
		},
		handleModalUpdateEmailOk(e) {
			this.visibleEmail = false
		}
  }
}
</script>

<style lang="less">
  .header-avatar{
    display: inline-flex;
    .avatar, .name{
      align-self: center;
    }
    .avatar{
      margin-right: 8px;
    }
    .name{
			font-size: 16px;
      font-weight: 400;
    }
  }
  .avatar-menu{
    width: 150px;
  }

</style>
