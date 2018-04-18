<template>
  <div id="left-nav">
    <dl :class="{ open: menu.isOpen }" v-for="menu in menus">
      <dt @click="menu.isOpen = !menu.isOpen">
        {{menu.name}}
        <i class="el-icon-arrow-down"></i>
        <i class="el-icon-arrow-up"></i>
      </dt>
      <dd v-for="submenu in menu.submenus" :class="{ active: currentUri.indexOf('#'+menu.uri+submenu.uri)==0}">
        <a :href="'/#'+menu.uri+submenu.uri">{{submenu.name}}</a>
      </dd>
    </dl>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        menus: [],
        currentUri: window.location.hash
      }
    },
    watch: {
      '$route'(to, from) {
        this.currentUri = window.location.hash
      }
    },
    mounted() {
      // 这里定义的menus应该从后端获取（后端返回的是做了权限过滤的了）
      this.axios.get('/api/left-nav').then(response => {
        let r = response.data
        if (r.code == 0) {
          let menus = r.data.menus
          for (var i = 0; i < menus.length; i++) {
            menus[i].isOpen = this.currentUri.indexOf(menus[i].uri) == 1; // 前面有一个 #
          }
          this.menus = menus;
        } else {
          this.$message({
            message: r.msg,
            type: 'error'
          });
        }
      });
    }
  }

</script>

<style scoped>
  /*#left-nav {min-height:598px;}*/
  dl {border-bottom:1px solid #393939; margin-bottom:10px;}

  dl i.el-icon-arrow-up {display:none;}
  dl i.el-icon-arrow-down {display:inline;}

  dl.open i.el-icon-arrow-up {display:inline;}
  dl.open i.el-icon-arrow-down {display:none;}
  dl>dd{display:none;}
  dl.open>dd{display:block;}

  dt {font-size:12px; color:#999; padding:5px 0 5px 20px; cursor: pointer;}
  dd {margin:1px 0;}
  dd>a {font-size:13px;color:#FFF; display: block; width:100%; padding:5px 0 5px 20px;}
  dd:hover, dd.active {background:#393939;}

</style>
