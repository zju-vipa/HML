<template>
    <div>
      <!-- 头部区域 -->
      <app-header  :class="'header'"></app-header>
      <!--      左侧导航栏区域-->
      <app-navBar  :class="this.isCollapse ? 'navbar2' : 'navbar'"  @isCollapse="chooseCollapse"></app-navBar>
      <!--      右侧主区域-->
      <app-main :class="this.isCollapse ? 'main2' : 'main'"></app-main>
    </div>
</template>

<script>
import AppHeader from './AppHeader/AppHeader'
import AppMain from './AppMain/AppMain'
import AppNavBar from './AppNavBar/AppNavBar'

export default {
  name: 'Layout',
  components: {
    AppHeader,
    AppMain,
    AppNavBar
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
    /* background-color:#367FA9; */
    background-color: #2d3a4b;
    height: 80px;
    line-height: 73px;
    position: absolute;
    top: 0px;
    left: 0px;
    right: 0px;
  }
  .navbar{
    position: absolute;
    left: 0px;
    top:  80px;
    bottom: 0px;
    width: 200px;
    overflow-y: auto;
    background:#373d41;
  }
  .navbar2{
    position: absolute;
    left: 0px;
    top:  80px;
    bottom: 0px;
    width: 64px;
    overflow-y: auto;
    background: #373d41;
  }
  .main{
    position: absolute;
    top: 80px;
    left: 200px;
    right: 0px;
    bottom: 0px;
    overflow-y: auto;
    background: #eaedf1;
  }
  .main2{
    position: absolute;
    top: 80px;
    left: 64px;
    right: 0px;
    bottom: 0px;
    overflow-y: auto;
    background: #eaedf1;
  }
  .toggle-button{
    background: #4A5064;
    font-size: 30px;
    text-align: center;
    /* color: #B8C7CE; */
    color:#ffffff;
    cursor: pointer;
    line-height: 24px;
    /* 这个是控制这三个竖线之间的间距的，注意，这里不是用margin和padding */
    letter-spacing: 0.4em;
  }
</style>
