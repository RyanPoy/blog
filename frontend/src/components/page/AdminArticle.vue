<template>
  <div>
    <el-tabs type="card">
      <el-tab-pane label="列表">
        <el-table :data="articles" stripe style="width: 100%">
          <el-table-column type="expand">
            <template slot-scope="props">
              <el-form label-position="left" inline class="table-expand">
                <el-form-item label="标题">
                  <el-input v-model="props.row.title"></el-input>
                </el-form-item>
                <el-form-item label="关键词">
                  <el-input v-model="props.row.keywords"></el-input>
                </el-form-item>
                <el-form-item label="系列">
                  <el-select v-model="props.row.series">
                    <el-option v-for="item in seriesList" :key="item.name" :label="item.name" :value="item.id"></el-option>
                  </el-select>
                </el-form-item>
                <el-form-item label="浏览次数">
                  <el-input v-model="props.row.view_number"></el-input></span>
                </el-form-item>
                <el-form-item label="标签">
                  <el-select multiple v-model="props.row.pretty_tags">
                    <el-option v-for="item in tags" :key="item.name" :label="item.name" :value="item.id"></el-option>
                  </el-select>
                </el-form-item>
                <el-form-item label=" ">
                  <el-button size="small" type="primary" @click="update(props.$index, props.row)">更新</el-button>
                </el-form-item>
              </el-form>
            </template>
          </el-table-column>

          <el-table-column prop="id" label="ID" align="left"></el-table-column>
          <el-table-column prop="title" label="标题" align="left"></el-table-column>
          <el-table-column prop="keywords" label="关键词" align="left"></el-table-column>
          <el-table-column prop="series.name" label="系列" align="left"></el-table-column>
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
      </el-tab-pane>


      <el-tab-pane label="新建">
        <el-form :model="newArticle" label-position="left" inline class="table-expand">
          <el-form-item label="标题">
            <el-input v-model="newArticle.title"></el-input></span>
          </el-form-item>
          <el-form-item label="关键词">
            <el-input v-model="newArticle.keywords"></el-input></span>
          </el-form-item>
          <el-form-item label="系列">
            <el-select v-model="newArticle.series">
              <el-option v-for="item in seriesList" :key="item.name" :label="item.name" :value="item.id"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="浏览次数">
            <el-input v-model="newArticle.view_number"></el-input></span>
          </el-form-item>
          <el-form-item label="标签">
            <el-select multiple v-model="newArticle.pretty_tags">
              <el-option v-for="item in tags" :key="item.name" :label="item.name" :value="item.id"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="正文">
            <el-input type="textarea" v-model="newArticle.content" :rows="15"></el-input>
          </el-form-item>
          <el-form-item label="">
            <el-button size="small" type="primary" @click="create(newArticle)">创建</el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>

  export default({
    data() {
      return {
        articles: [],
        seriesList: [],
        tags: [],
        newArticle: {},
      }
    },
    methods: {
      create(newarticle) {
        this.axios.post('/api/articles/', newarticle).then(response => {
          let r = response.data
          if (r.code == 0) {
            this.articles.unshift(r.data.article)
            this.newArticle = {}
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
      update(index, article) {
        this.axios.put('/api/articles/', article).then(response => {
          let r = response.data
          if (r.code == 0) {
            this.$set(this.articles, index, r.data.article)
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
      _delete(index, article) {
        if (article.id && article.id > 0) {
          this.axios.delete('/api/articles/', {data: article}).then(response => {
            let r = response.data
            if (r.code == 0) {
              this.articles.splice(index, 1)
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
      this.axios.get('/api/articles').then(response => {
        let r = response.data
        if (r.code == 0) {
          this.articles = r.data.articles
        }
      })
      this.axios.get('/api/series').then(response => {
        let r = response.data
        if (r.code == 0) {
          this.seriesList = r.data.series
        }
      })
      this.axios.get('/api/tags').then(response => {
        let r = response.data
        if (r.code == 0) {
          this.tags = r.data.tags
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
