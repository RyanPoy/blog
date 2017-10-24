<template>
  <div id="app">
    <el-container>
      <el-aside height="100%" style="width:150px">
        <left-nav></left-nav>
      </el-aside>
      <el-container>
        <el-header>头</el-header>
        <el-main>
          <router-view/>
        </el-main>
        <el-footer>尾</el-footer>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import LeftNav from '@/components/common/LeftNav'

export default {
  name: 'app',
  components: {
    LeftNav
  }
}
</script>

<style>
#app {
  font-family: 'Microsoft YaHei', 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2C3E50;
}
</style>
