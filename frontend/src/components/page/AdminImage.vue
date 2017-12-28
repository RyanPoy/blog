<template>
  <div>
    <el-upload class="upload-demo" action="/api/images/" multiple drag accept=".jpg, .png, .gif, jpeg" :show-file-list="false"
      :before-upload="checkUpload" name="images" :on-success="uploaded">
      <i class="el-icon-upload"></i>
      <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
      <div class="el-upload__tip" slot="tip">只能上传jpg/png文件，且不超过500kb</div>
    </el-upload>

    <p></p>
    <el-table :data="images" stripe style="width: 100%">
      <el-table-column prop="id" label="ID" align="left"></el-table-column>
      <el-table-column prop="" label="微缩图" align="left">
        <template slot-scope="scope">
          <img :src='scope.row.url' style='height:64px;' />
        </template>
      </el-table-column>
      <el-table-column prop="name" label="名称" align="left"></el-table-column>
      <el-table-column prop="size" label="大小" align="left"></el-table-column>
      <el-table-column prop="url" label="地址" align="left"></el-table-column>
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
        images: [],
        newImage: {name: '', url: '', seq: 0}
      }
    },
    methods: {
      checkUpload(file, fileList) {
        if (file.type.indexOf('image/') != 0) {
          return false;
        }
      },
      uploaded(response, file, fileList) {
        let r = response
        if (r.code == 0) {
          this.images.unshift(r.data.image)
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
      },
      _delete(index, image) {
        if (image.id && image.id > 0) {
          this.axios.delete(utils.apiDomain + '/images/', {data: image}).then(response => {
            let r = response.data
            if (r.code == 0) {
              this.images.splice(index, 1)
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
      this.axios.get(utils.apiDomain + '/images').then(response => {
        let r = response.data
        if (r.code == 0) {
          this.images = r.data.images
        }
      })
    }
  })
</script>

<style scoped>
.upload-demo {text-align: center;}
</style>
