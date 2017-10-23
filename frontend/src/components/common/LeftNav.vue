<template>
  <div>
    <el-menu :default-openeds="['1']">
      <el-submenu index="1">
        <template slot="title">博客管理</template>
        <el-menu-item-group>
          <el-menu-item index="1-1">文章</el-menu-item>
          <el-menu-item index="1-2">
            <router-link :to="{'name': 'AdminTag'}">标签</router-link>
          </el-menu-item>
          <el-menu-item index="1-3">系列</el-menu-item>
          <el-menu-item index="1-4">图片</el-menu-item>
          <el-menu-item index="1-5">单页面</el-menu-item>
          <el-menu-item index="1-6">友链</el-menu-item>
        </el-menu-item-group>
      </el-submenu>
    </el-menu>
  </div>
</template>

<script>
</script>

<style scoped>
  .router-link-exact-active, .router-link-active {text-decoration: none; color: #2C3E50;}
</style>