<template>
  <div>
    <el-form :inline="true">
      <el-form-item label="名称">
        <el-input v-model="newTagName" placeholder="请填入名称"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="create">添加</el-button>
      </el-form-item>
    </el-form>

    <el-table :data="tags" stripe style="width: 100%">
      <el-table-column prop="id" label="ID" align="left"></el-table-column>
      <el-table-column prop="" label="名称" align="left">
        <template slot-scope="scope">
          <el-input v-model="scope.row.name" placeholder="请输入内容">111</el-input>
        </template>
      </el-table-column>
      <el-table-column prop="article_number" label="文章数量" align="left"></el-table-column>
      <el-table-column prop="created_at" label="创建时间" align="left"></el-table-column>
      <el-table-column prop="updated_at" label="修改时间" align="left"></el-table-column>
      <el-table-column prop="" label="操作" align="left">
        <template slot-scope="scope">
          <el-button size="small" @click="update(scope.$index, scope.row)">更新</el-button>
          <el-button size="small" type="danger" @click="_delete(scope.$index, scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>

export default {
  data() {
    return {
      tags: [],
      newTagName: ''
    }
  },
  mounted() {
    this.axios.get('/api/tags').then(response => {
      let r = response.data
      console.log(r)
      if (r.code == 0) {
        this.tags = r.data.tags
      }
    })
  },
  methods: {
    create() {
      if (this.newTagName && this.newTagName.length > 0) {
        this.axios.post('/api/tags/', {'name': this.newTagName }).then(response => {
          let r = response.data
          if (r.code == 0) {
            this.newTagName = ''
            this.tags.push(r.data.tag)
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
      } 
    },

    _delete(index, tag) {
      if (tag.id && tag.id > 0) {
        this.axios.delete('/api/tags/', {data: tag}).then(response => {
          let r = response.data
          if (r.code == 0) {
            this.tags.splice(index, 1)
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
    },
    update(index, tag) {
      if (tag.name && tag.name.length > 0) {
        this.axios.put('/api/tags/', tag).then(response => {
          let r = response.data
          if (r.code == 0) {
            this.$set(this.tags, index, tag)
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
      }
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
