<template>
  <div>
    <div class="navbar" >
      <div class="toggle-button" @click="controlCollapse">|||</div>
      <el-menu :router="true"
              :default-active="activePath"
               class="el-menu-vertical-demo" background-color="#333744"
               text-color="#fff" active-text-color="#409EFF"
               :collapse="isCollapse"
         :collapse-transition="false">
        <el-menu-item index="/home">
          <i class="el-icon-s-home"></i>
          <span slot="title">首页</span>
        </el-menu-item>
        <el-menu-item index="/data">
          <i class="el-icon-s-data"></i>
         <!-- <el-tooltip class="item" effect="dark" content="数据" placement="left" :disabled="this.isCollapse ? false: true">
            <i class="el-icon-s-data"></i>
         </el-tooltip> -->
          <span slot="title">数据</span>
        </el-menu-item>
        <el-menu-item index="/feature">
          <i class="el-icon-s-management"></i>
          <span slot="title">特征</span>
        </el-menu-item>
        <el-menu-item index="/learn">
          <i class="el-icon-s-platform"></i>
          <span slot="title">学习</span>
        </el-menu-item>
        <el-menu-item index="/decision">
          <i class="el-icon-s-tools"></i>
          <span slot="title">决策</span>
        </el-menu-item>
      </el-menu>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AppNavBar',
  data () {
    return {
      isCollapse: false
    }
  },
  computed: {
    activePath () {
      // console.log(this.$route.path)
      if (this.$route.path === '/data/originDataset') {
        return '/data'
      } else if (this.$route.path === '/data/humanDataset') {
        return '/data'
      } else if (this.$route.path === '/data/powerNet') {
        return '/data'
      } else if (this.$route.path === '/data/powerNetDatasetCreate') {
        return '/data'
      } else if (this.$route.path === '/data/powerNetTransientStabilityDatasetCreate') {
        return '/data'
      } else if (this.$route.path === '/data/queryPowerNetResult') {
        return '/data'
      } else if (this.$route.path === '/feature/humanfea') {
        return '/feature'
      } else if (this.$route.path === '/feature/queryFea') {
        return '/feature'
      } else if (this.$route.path === '/learn/queryLearner') {
        return '/learn'
      } else if (this.$route.path === '/decision/decHumanFea') {
        return '/decision'
      } else if (this.$route.path === '/decision/decLearner') {
        return '/decision'
      } else if (this.$route.path === '/decision/queryDecision') {
        return '/decision'
      }
      return this.$route.path
    }
  },
  methods: {
    controlCollapse () {
      this.isCollapse = !this.isCollapse
      this.$emit('isCollapse', this.isCollapse)
    },
    showPath () {
      console.log(this.$route.path)
    }
    // goActivePath () {
    //   this.activePath = this.$route.path
    //   console.log(this.$route.path)
    // }
  }
}
</script>

<style scoped>

.toggle-button{
  background: #4A5064;
  font-size: 10px;
  text-align: center;
  /* color: #B8C7CE; */
  color:#ffffff;
  cursor: pointer;
  line-height: 24px;
  letter-spacing: 0.2em;
  /* border-bottom: 1px solid #ffffff; */
}
.el-menu{
  border-right: none;
}
.el-menu-item i{
  margin-right: 26px;
}
/* .el-menu-item .el-tooltip i{
  margin-right: 20px;
} */
</style>
