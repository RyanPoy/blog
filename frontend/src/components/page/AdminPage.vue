<template>
  <div>
    <el-tabs type="card">
      <el-tab-pane label="页面列表">
        <el-table :data="pages" stripe style="width: 100%">
          <el-table-column type="expand">
            <template slot-scope="props">
              <el-form label-position="left" inline class="table-expand">
                <el-form-item label="标题">
                  <el-input v-model="props.row.title"></el-input></span>
                </el-form-item>
                <el-form-item label="链接地址">
                  <el-input v-model="props.row.uri"></el-input></span>
                </el-form-item>
                <el-form-item label="排序">
                  <el-input v-model="props.row.seq"></el-input></span>
                </el-form-item>
                <el-form-item label="正文">
                  <el-input type="textarea" v-model="props.row.content" :rows="15"></el-input>
                </el-form-item>
                <el-form-item label=" ">
                  <el-button size="small" type="primary" @click="update(props.$index, props.row)">更新</el-button>
                </el-form-item>
              </el-form>
            </template>
          </el-table-column>

          <el-table-column prop="id" label="ID" align="left"></el-table-column>
          <el-table-column prop="title" label="标题" align="left"></el-table-column>
          <el-table-column prop="uri" label="链接地址" align="left"></el-table-column>
          <el-table-column prop="seq" label="排序" align="left"></el-table-column>

          <el-table-column prop="created_at" label="创建时间" align="left"></el-table-column>
          <el-table-column prop="updated_at" label="修改时间" align="left"></el-table-column>
          <el-table-column prop="" label="操作" align="left">
            <template slot-scope="scope">
              <el-button size="small" type="danger" @click="_delete(scope.$index, scope.row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>


      <el-tab-pane label="创建单页面">
        <el-form :model="newPage" label-position="left" inline class="table-expand">
          <el-form-item label="标题">
            <el-input v-model="newPage.title"></el-input></span>
          </el-form-item>
          <el-form-item label="链接地址">
            <el-input v-model="newPage.uri"></el-input></span>
          </el-form-item>
          <el-form-item label="排序">
            <el-input v-model="newPage.seq"></el-input></span>
          </el-form-item>
          <el-form-item label="正文">
            <el-input type="textarea" v-model="newPage.content" :rows="15"></el-input>
          </el-form-item>
          <el-form-item label=" ">
            <el-button size="small" type="primary" @click="create(newPage)">创建</el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
  import { utils } from '@/utils'

  export default({
    data() {
      return {
        pages: [],
        newPage: {id: null, uri: '', seq: 0, content: ''},
      }
    },
    methods: {
      create(newpage) {
        this.axios.post(utils.apiDomain + '/pages/', newpage).then(response => {
          let r = response.data
          if (r.code == 0) {
            this.pages.unshift(r.data.page)
            this.newPage = {id: null, uri: '', seq: 0, content: ''}
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
      update(index, page) {
        this.axios.put(utils.apiDomain + '/pages/', page).then(response => {
          let r = response.data
          if (r.code == 0) {
            this.$set(this.pages, index, r.data.page)
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
      _delete(index, page) {
        if (page.id && page.id > 0) {
          this.axios.delete(utils.apiDomain + '/pages/', {data: page}).then(response => {
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
  .table-expand {
    font-size: 0;
  }
  .table-expand label {
    width: 90px;
    color: #99a9bf;
  }
  .table-expand .el-form-item {
    margin-right: 0;
    margin-bottom: 10px;
    text-align: left;
    width: 100%;
  }
  .table-expand .el-form-item input[type=text],
  .table-expand .el-form-item .el-textarea__inner {
    width:680px;
  }
</style>
