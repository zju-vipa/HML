import Vue from 'vue'
import VueRouter from 'vue-router'
// 导入需要渲染的组件
import Register from '../views/user/Register'
import Login from '../views/user/Login'
import Layout from '../components/Layout'

// import Home from '../views/home/Home'
import Data from '../views/data/Data'
import OriginDataset from '../views/data/OriginDataset'
import HumanFeaDataset from '../views/data/HumanFeaDataset'

import Feature from '../views/feature/Feature'
import HumanFea from '../views/feature/HumanFea'
import QueryHumanFeature from '../views/feature/QueryHumanFeature'

import Learn from '../views/learn/Learn'
import QueryLearner from '../views/learn/QueryLearner'

import Decision from '../views/decision/Decision'
import QueryDecision from './../views/decision/QueryDecision'

import PowerNetDataset from './../views/data/powerNet/PowerNetDataset'
import QueryPowerNetResult from './../views/data/powerNet/QueryPowerNetResult'
// import Decision from '../views/decision/Decision'
// import Dataset from '../views/data/Dataset'
// import DatasetHuFea from '../views/data/DatasetHuFea'
// import HumanFea from '../views/feature/HumanFea'
// import QueryHumanFeature from './../views/feature/QueryHumanFeature'
// import QueryLearner from './../views/learn/QueryLearner'
// import DecisionHumanFea from './../views/decision/DecisionHumanFea'
// import DecisionLearn from './../views/decision/DecisionLearn'
// import QueryDecision from './../views/decision/QueryDecision'
Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: '/register'
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    // 基础页面布局
    path: '/layout',
    name: 'Layout',
    component: Layout,
    // redirect: '/home',
    children: [
      // {
      //       path: '/home',
      //       name: 'Home',
      //       component: Home
      //     },
      {
        path: '/data',
        name: 'Data',
        component: Data
      },
      {
        path: '/data/originDataset',
        name: 'OriginDataset',
        component: OriginDataset
      },
      {
        path: '/data/humanDataset',
        name: 'HumanFeaDataset',
        component: HumanFeaDataset
      },
      {
        path: '/feature',
        name: 'Feature',
        component: Feature
      },
      {
        path: '/feature/humanfea',
        name: 'HumanFea',
        component: HumanFea
      },
      {
        path: '/feature/queryFea',
        name: 'QueryHumanFeature',
        component: QueryHumanFeature
      },
      {
        path: '/learn',
        name: 'Learn',
        component: Learn
      },
      {
        path: '/learn/queryLearner',
        name: 'QueryLearner',
        component: QueryLearner
      },
      {
        path: '/decision',
        name: 'Decision',
        component: Decision
      },
      //     {
      //       path: '/decision/decHumanFea',
      //       name: 'DecisionHumanFea',
      //       component: DecisionHumanFea
      //     },
      //     {
      //       path: '/decision/decLearner',
      //       name: 'DecisionLearn',
      //       component: DecisionLearn
      //     },
      {
        path: '/decision/queryDecision',
        name: 'QueryDecision',
        component: QueryDecision
      },
      // 电网数据集
      {
        path: '/data/powerNet',
        name: 'PowerNetDataset',
        component: PowerNetDataset
      },
      {
        path: '/data/queryPowerNetResult',
        name: 'QueryPowerNetDataset',
        component: QueryPowerNetResult
      }
    ]
  }
]

const router = new VueRouter({
  routes
})

export default router
