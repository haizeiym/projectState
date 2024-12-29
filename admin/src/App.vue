<template>
  <el-container>
    <el-header>
      <h1>项目状态系统</h1>
      <h6>项目状态为所有子节点统一状态</h6>
    </el-header>
    <el-main>
      <router-view></router-view>
    </el-main>
  </el-container>
</template>

<script setup>
import { ElContainer, ElHeader, ElMain } from 'element-plus'
</script>

<style>
.el-header {
  background-color: #409EFF;
  color: white;
  display: flex;
  flex-direction: column;
  justify-content: center;
  height: 100px;
}

.el-header h1 {
  margin: 0;
  padding: 5px 0;
}

.el-header h6 {
  margin: 0;
  padding: 5px 0;
}
</style>