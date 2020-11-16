<template>
    <div>
      <!-- 头部区域 -->
      <app-header class="header"></app-header>
<!--      左侧导航栏区域-->
      <app-navBar  :class="this.isCollapse ? 'navbar2' : 'navbar'"  @isCollapse="chooseCollapse"></app-navBar>
<!--      右侧主区域-->
      <app-main :class="this.isCollapse ? 'main2' : 'main'"></app-main>
    </div>
</template>

<script>
import AppMain from './AppMain/AppMain'
import AppNavBar from './AppNavBar/AppNavBar'
import AppHeader from './AppHeader/AppHeader'
export default {
  name: 'Layout',
  components: {
    AppMain,
    AppNavBar,
    AppHeader
  },
  data () {
    return {
      isCollapse: false
    }
  },
  methods: {
    chooseCollapse (params) {
      console.log(params)
      this.isCollapse = params
    }
  }
}
</script>

<style scoped>
.header {
    background-color:#367FA9;
    height: 50px;
    line-height: 50px;
    position: absolute;
    top: 0px;
    left: 0px;
    right: 0px;
  }
  .navbar{
    position: absolute;
    left: 0px;
    top:  50px;
    bottom: 0px;
    width: 180px;
    overflow-y: auto;
    background:#222d32;
  }
    .navbar2{
    position: absolute;
    left: 0px;
    top:  50px;
    bottom: 0px;
    width: 60px;
    overflow-y: auto;
    background: #222d32;
  }
  .main{
    position: absolute;
    top: 50px;
    left: 180px;
    right: 0px;
    bottom: 0px;
    overflow-y: auto;
    background: #eaedf1;
  }
  .main2{
    position: absolute;
    top: 50px;
    left: 60px;
    right: 0px;
    bottom: 0px;
    overflow-y: auto;
    background: #eaedf1;
  }
.toggle-button{
  background: #222d32;
  font-size: 10px;
  text-align: center;
  color: #B8C7CE;
  cursor: pointer;
  line-height: 24px;
  /* 这个是控制这三个竖线之间的间距的，注意，这里不是用margin和padding */
  letter-spacing: 0.2em;
}
</style>
