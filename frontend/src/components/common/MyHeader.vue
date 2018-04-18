<template>
  <div id="header">
    <span class="brand">彭一的博客管理后台</span>
    <span class="use-user">欢迎您，
      <span>{{username}}</span> |
      <span class="signout" @click="signout">注销</span>
    </span>
  </div>
</template>

<script>
  import { mapGetters } from 'vuex'

  export default {
    computed: {
      username() {
        return '彭一'
      }
    },
    methods: {
      signout() {
        window.location.href = "/#/signin"
      }
    }
  }
</script>

<style scoped>
  span.signout { cursor: pointer;}
</style>
