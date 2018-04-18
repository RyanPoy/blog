<template>
  <div>
    <el-form :inline="true" :model="newLink">
      <el-form-item label="名称">
        <el-input v-model="newLink.name" placeholder="请填入名称"></el-input>
      </el-form-item>
      <el-form-item label="链接地址">
        <el-input v-model="newLink.url" placeholder="请填入链接地址"></el-input>
      </el-form-item>
      <el-form-item label="排序">
        <el-input v-model="newLink.seq" placeholder="请填入顺序"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="create(newLink)">添加</el-button>
      </el-form-item>
    </el-form>

    <el-table :data="links" stripe style="width: 100%">
      <el-table-column prop="id" label="ID" align="left"></el-table-column>
      
      <el-table-column prop="" label="名称" align="left">
        <template slot-scope="scope">
          <el-input v-model="scope.row.name" placeholder="请输入名称"></el-input>
        </template>
      </el-table-column>

      <el-table-column prop="url" label="连接地址" align="left">
        <template slot-scope="scope">
          <el-input v-model="scope.row.url" placeholder="请输入连接地址"></el-input>
        </template>
      </el-table-column>
      
      <el-table-column prop="排序" label="排序" align="left">
        <template slot-scope="scope">
          <el-input v-model="scope.row.seq" placeholder="请输入排列顺序"></el-input>
        </template>
      </el-table-column>

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
  export default({
    data() {
      return {
        links: [],
        newLink: {name: '', url: '', seq: 0}
      }
    },
    methods: {
      create(newLink) {
        this.axios.post('/api/links/', this.newLink).then(response => {
          let r = response.data
          if (r.code == 0) {
            this.newLink = {name: '', url: '', seq: 0}
            this.links.push(r.data.link)
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
      update(index, link) {
        this.axios.put('/api/links/', link).then(response => {
          let r = response.data
          if (r.code == 0) {
            this.$set(this.links, index, r.data.link)
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
          this.axios.delete('/api/links/', {data: link}).then(response => {
            let r = response.data
            if (r.code == 0) {
              this.links.splice(index, 1)
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
      this.axios.get('/api/links').then(response => {
        let r = response.data
        if (r.code == 0) {
          this.links = r.data.links
        }
      })
    }
  })
</script>

<style>
</style>
