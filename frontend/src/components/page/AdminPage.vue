<template>
  <div>
    <el-tabs type="card">
      <el-tab-pane label="页面列表">
        <page-list></page-list>
      </el-tab-pane>
      <el-tab-pane label="创建单页面">创建单页面</el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
  import PageList from '@/components/page/PageList'

  export default({
    components: {
      PageList
    }
  })

</script>

<style>
</style>
