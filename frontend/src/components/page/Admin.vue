<template>
  <div>
    <my-header />
    <div id="content">
      <div id="left">
        <left-nav/>
      </div>
      <div id="main">
        <router-view></router-view>
      </div>
    </div>
    <div id="footer"></div>
  </div>
</template>

<script>
import LeftNav from '@/components/common/LeftNav'
import MyHeader from '@/components/common/MyHeader'

export default {
  name: 'app',
  components: {
    LeftNav, MyHeader
  }
}

</script>

<style scoped>
</style>
