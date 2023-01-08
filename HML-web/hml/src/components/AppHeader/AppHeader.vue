<template>
  <div>
    <div class="header">
      <!-- <span class="logo-title">HML</span> -->
      <a href="#" class="logo">
        <img class="logo-img" src="./../../assets/img/logo.png" alt="图标">
        <span class="logo-title">大电网人机协同双向学习系统</span>
      </a>
      <!-- <div class="header-list">
        <span>模型列表</span>
        <span>使用手册</span>
      </div> -->
      <el-dropdown class="dropdown" @command="handleCommand">
        <span class="el-dropdown-link">
          {{user.username}}<i class="el-icon-arrow-down el-icon--right"></i>
        </span>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item command="update">修改密码</el-dropdown-item>
          <el-dropdown-item command="exit">退出系统</el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
    </div>
  </div>
</template>
<script>
export default {
  data () {
    return {
      // 用户名
      user: JSON.parse(localStorage.getItem('user'))
    }
  },
  methods: {
    // 点击下拉菜单触发事件
    handleCommand (command) {
      // console.log(this.user)
      // 这里也可以使用switch
      if (command === 'exit') {
        // 退出系统
        this.handleExit()
      } else {
        // this.handleUpdatePass()
      }
    },
    // // 退出系统
    handleExit () {
      // 1, 获取系统的token
      // const token = JSON.parse(localStorage.getItem('token'))
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      this.$router.push('/login')
    }
  }
}
</script>
<style scoped>
  .logo{
    text-decoration: none
  }
  .logo-img{
    width: 25px;
    height: 25px;
    vertical-align:middle;
    padding: 0 10px 0 40px
  }
  .logo-title{
    color: white;
    cursor: pointer;
    padding-left: 10px;
    font-size: 18px;
  }
  .dropdown{
    cursor: pointer;
    float: right;
    margin-right: 20px;
    color: white
  }
  /* .header-list{
    display: inline-block;
    margin-left: 100px;
    color: #B8C7CE;
  }
  .header-list span {
    margin-left: 40px;
    cursor: pointer;
  }
  .header-list span:hover{
    color: #ffffff;
  }
  .header-list span:active{
    color: #ffffff;
  } */
</style>
