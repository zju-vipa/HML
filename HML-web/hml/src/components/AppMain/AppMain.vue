<template>
    <div>
      <div class="main">
      <!-- <el-breadcrumb v-show="this.$route.path !== '/home'" separator-class="el-icon-arrow-right">
        <el-breadcrumb-item class="line" :to="{ path: this.$route.path }">{{this.$route.meta.title}}</el-breadcrumb-item>
      </el-breadcrumb> -->
        <router-view></router-view>
      </div>
    </div>
</template>

<script>
export default {
  name: 'AppMain'
}
</script>

<style scoped>
.line{
  border-left: 3px solid rgb(49, 197, 198);
  padding-left: 10px
}
</style>
