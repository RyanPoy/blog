<template>
  <div>
    <el-table :data="pages" stripe style="width: 100%">
      <el-table-column prop="id" label="ID" align="left"></el-table-column>
      <el-table-column prop="title" label="标题" align="left"></el-table-column>
      <el-table-column prop="series.name" label="连接地址" align="left"></el-table-column>
      <el-table-column prop="view_number" label="浏览次数" align="left"></el-table-column>
      <el-table-column prop="pretty_tags" label="标签" align="left"></el-table-column>

      <el-table-column prop="created_at" label="创建时间" align="left"></el-table-column>
      <el-table-column prop="updated_at" label="修改时间" align="left"></el-table-column>
      <el-table-column prop="" label="操作" align="left">
        <template slot-scope="scope">
          <el-button size="small" type="danger" @click="_delete(scope.$index, scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
  import { utils } from '@/utils'

  export default({
    data() {
      return {
        pages: [],
      }
    },
    methods: {
      create(newLink) {
        this.axios.post(utils.apiDomain + '/pages/', this.newLink).then(response => {
          let r = response.data
          if (r.code == 0) {
            this.newLink = {name: '', url: '', seq: 0}
            this.pages.push(r.data.link)
            this.$message({
              message: '添加成功',
              type: 'success'
            });
          } else {
            this.$message({
              message: r.err_str,
              type: 'error'
            });
          }
        })
      },
      update(link) {
        this.axios.put(utils.apiDomain + '/pages/', link).then(response => {
          let r = response.data
          if (r.code == 0) {

            link.name = r.data.link.name
            link.url = r.data.link.url
            link.seq = r.data.link.seq
            link.created_at = r.data.link.created_at
            link.updated_at = r.data.link.updated_at

            this.$message({
              message: '更新成功',
              type: 'success'
            });
          } else {
            this.$message({
              message: r.err_str,
              type: 'error'
            });
          }
        })
      },
      _delete(index, link) {
        if (link.id && link.id > 0) {
          this.axios.delete(utils.apiDomain + '/pages/', {data: link}).then(response => {
            let r = response.data
            if (r.code == 0) {
              this.pages.splice(index, 1)
              this.$message({
                message: '删除成功',
                type: 'success'
              });
            } else {
              this.$message({
                message: r.err_str,
                type: 'error'
              });
            }
          })
        }
      }
    },
    mounted() {
      this.axios.get(utils.apiDomain + '/pages').then(response => {
        let r = response.data
        if (r.code == 0) {
          this.pages = r.data.pages
        }
      })
    }
  })
</script>

<style>
</style>