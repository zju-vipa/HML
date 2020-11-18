<template>
   <div class="login-container">
     <h2 class="login-title">人在回路机器学习系统</h2>
     <el-form class="login-form" :model="loginForm" :rules="loginFormRules" ref="loginFormRef">
       <el-form-item  prop="email">
         <el-input v-model="loginForm.email" style="width:350px" placeholder="请输入邮箱"></el-input>
       </el-form-item>
       <el-form-item  prop="password">
         <el-input type="password" style="width:350px" v-model="loginForm.password" placeholder="请输入密码"></el-input>
       </el-form-item>
        <el-form-item>
         <el-row>
           <el-col :span="12">
              <el-button type="primary" @click="submitLogin" style="width:160px">登录</el-button>
           </el-col>
           <el-col :span="12">
              <el-button type="primary" @click="gotoRegister" style="width:170px">注册</el-button>
           </el-col>
         </el-row>
       </el-form-item>
     </el-form>
   </div>
</template>

<script>
import loginApi from './../../api/user'
export default {
  name: 'Login',
  data () {
    return {
      loginForm: {
        email: 'wang@123',
        password: '123456'
      },
      // 登录表单验证规则
      loginFormRules: {
        email: [
          { required: true, message: '请输入邮箱', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    // 登录功能实现
    submitLogin () {
      this.$refs.loginFormRef.validate(valid => {
        if (valid) {
          console.log(this.loginForm)
          loginApi.login(this.loginForm).then(response => {
            const resp = response.data
            if (resp.meta.code === 200) {
              // 将用户信息保存到浏览器缓存
              localStorage.setItem('user', JSON.stringify(resp.data))
              localStorage.setItem('token', JSON.stringify(resp.data.token))
              // this.$message.success('登录成功')
              this.$router.push('/layout')
            } else {
              this.$message.error('登录失败')
            }
          })
        } else {
          return false
        }
      })
    },
    // 去注册
    gotoRegister () {
      this.$router.push('/register')
    }
  }
}
</script>

<style scoped>
  .login-container{
    position: absolute;
    width: 100%;
    height: 100%;
    background: url("./../../assets/img/time.jpg");
    /* background-position: 500px 400px; */
    background-size: cover;
    background-position: absolute;
    overflow: hidden;
  }
  .login-form{
    width: 350px;
    margin: 40px auto;
    padding: 30px;
    border-radius: 20px;
  }
  .login-title{
    text-align: center;
    color: white;
    margin-top: 100px;
    letter-spacing: 0.5em;
    font-weight: 600;
    font-size: 30px;
  }
  .el-form-item__label{
    text-align: center !important;
  }
  .el-button{
    background: rgb(36, 46, 73);
    border: 1px solid rgb(36, 46, 73);
  }

</style>
