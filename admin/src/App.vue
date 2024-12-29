<template>
  <el-container>
    <el-header>
      <h1>项目状态系统</h1>
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
  line-height: 60px;
}
</style>