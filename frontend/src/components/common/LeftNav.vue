<template>
  <div>
    <el-menu :default-openeds="['1']">
      <el-submenu index="1">
        <template slot="title">博客管理</template>
        <el-menu-item-group>
          <el-menu-item index="1-1">
            <router-link :to="{'name': 'AdminArticle'}">文章</router-link>
          </el-menu-item>
          <el-menu-item index="1-2">
            <router-link :to="{'name': 'AdminTag'}">标签</router-link>
          </el-menu-item>
          <el-menu-item index="1-3">
            <router-link :to="{'name': 'AdminSeries'}">系列</router-link>
          </el-menu-item>
          <el-menu-item index="1-4">
            <router-link :to="{'name': 'AdminImage'}">图片</router-link>
          </el-menu-item>
          <el-menu-item index="1-5">
            <router-link :to="{'name': 'AdminPage'}">单页面</router-link>
          </el-menu-item>
          <el-menu-item index="1-6">
            <router-link :to="{'name': 'AdminLink'}">友链</router-link>
          </el-menu-item>
        </el-menu-item-group>
      </el-submenu>
    </el-menu>
  </div>
</template>

<script>
</script>

<style scoped>
  .el-menu-item a {text-decoration: none; color: #2C3E50;}
  .el-menu-item a.router-link-exact-active, .el-menu-item a.router-link-active {color: #409EFF;}
  .el-menu-item {cursor: pointer;}
  .el-menu-item a { width:100%; display: inline-block;}
</style>