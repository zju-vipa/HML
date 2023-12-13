<template>
    <div>
      <!-- <h2>人在回路的电网系统</h2> -->
      <h1>大电网复杂系统人机协同双向学习引擎</h1>
      <el-card>
        <h2>当前特征工程</h2>
        <query-human-feature :isHFeaDialog="true"></query-human-feature>
        <!-- 当前任务 -->
        <!-- <el-table style="width: 100%" stripe  >
          <el-table-column label="序号" type="index" > </el-table-column>
          <el-table-column label="任务名称" > </el-table-column>
          <el-table-column label="数据集名" > </el-table-column>
          <el-table-column label="特征工程" > </el-table-column>
          <el-table-column label="是否公开" > </el-table-column>
        </el-table> -->
      </el-card>
      <el-card>
        <!-- 当前任务 -->
        <h2>当前学习器模型</h2>
        <query-learner :isLearnDialog="true"></query-learner>
        <!-- <el-table style="width: 100%">
          <el-table-column label="序号" type="index"> </el-table-column>
          <el-table-column label="任务名称" > </el-table-column>
          <el-table-column label="数据集名"> </el-table-column>
          <el-table-column label="特征工程"> </el-table-column>
          <el-table-column label="是否公开"> </el-table-column>
        </el-table> -->
      </el-card>
    </div>
</template>

<script>
import QueryHumanFeature from './feature/QueryHumanFeature'
import QueryLearner from './learn/QueryLearner'
export default {
  name: 'Home',
  components: {
    QueryHumanFeature,
    QueryLearner
  },
  data () {
    return {
      userInfo: {
        name: ['letian', 'letian2'],
        password: '123'
      }
    }
  }
}
</script>

<style scoped>
  h1{
    text-align: center;
    font-size: 30px
  }
  h2{
    text-align: center;
    padding-bottom: 10px;
    border-bottom: 3px solid rgb(102, 102, 102);
    font-size: 26px
  }
  .el-table{
    margin: 0px auto;
  }

</style>
