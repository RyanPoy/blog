<template>

  <div id="signin">
    <el-dialog title="博客后台管理" :visible="true" width="30%" :center="true" :show-close="false">
      <el-form label-width="80px">
        <el-form-item label="登录名">
          <el-input type="text" v-model="user.signinname" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="密码">
          <el-input type="password" v-model="user.password" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button size="large" rows="2" type="primary" @click="signin">登录</el-button>
          <span style="margin-left: 30px; color: red;">{{loginErr}}</span>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
  export default {

    data() {
      return {
        user: {signinname: '', password: ''},
        loginErr: ''
      }
    },
    methods: {
      signin() {
        this.axios.post('/api/signin/', this.user).then(response => {
          let r = response.data
          if (r.code == 0) {
            window.location.href="/#/admin/articles"
          } else {
            this.loginErr = r.err_str
          }
        })
      }
    }
  }

</script>

<style scoped>
   #signin {background-color: #000; position: absolute; top:0; bottom:0; width:100%;}
</style>
