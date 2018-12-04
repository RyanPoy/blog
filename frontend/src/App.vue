<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
export default {}
</script>

<style>
body,div,dl,dt,dd,ul,ol,li,h1,h2,h3,h4,h5,h6,pre,form,fieldset,input,textarea,p,blockquote,th,td,img {padding:0;margin:0;}

a {text-decoration:none;}

#app {
  font-family:"Microsoft YaHei",Arial,Helvetica,sans-serif,"宋体";
  font-size:12px;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

@font-face {font-family: "iconfont";
  src: url('assets/images/iconfont.eot'); /* IE9*/
  src: url('assets/images/iconfont.eot#iefix') format('embedded-opentype'), /* IE6-IE8 */
  url('assets/images/iconfont.woff') format('woff'), /* chrome, firefox */
  url('assets/images/iconfont.ttf') format('truetype'), /* chrome, firefox, opera, Safari, Android, iOS 4.2+*/
  url('assets/images/iconfont.svg#iconfont') format('svg'); /* iOS 4.1- */
}

.iconfont {
  font-family: "iconfont" !important;
  font-size: 16px;
  font-style: normal;
  -webkit-font-smoothing: antialiased;
  -webkit-text-stroke-width: 0.2px;
  -moz-osx-font-smoothing: grayscale;
}

#header {
  height: 50px;
  line-height: 50px;
  background-color: #131313;
  color:#FFF;
  font-size: 16px;
  padding-left:20px;
}

#header .use-user {font-size: 12px; float:right; padding-right:40px;}

#content {
  overflow: hidden;
}

#main {
  font-size: 12px;
  float:left;
  width:88%;
  margin-left:10%;
  margin-top:1em;
}

#left {
  float:left;
  width:8%;
  background-color: #131313;
  border-top:1px solid #262626;
  border-right:1px solid #262626;
  position: absolute;
  top:50px;
  bottom:0px;
}

.search-form { padding-top:1em;}
/*.el-form-item__label {font-size:12px;}*/
.search-form {border-bottom: 1px solid #EEE; padding-bottom: 1em; margin-bottom: 1em;}
.buttons {padding-bottom: 1em; }
.search-form .el-form-item{ margin-bottom: 0;}
td.compact, th.compact {padding-top:5px 2px;}
th.compact {background: #EEE; border-top:1px solid #E9E9E9;}


.el-tree--highlight-current .el-tree-node.is-current>.el-tree-node__content { background-color: #CCCCCC; }

.conditions-table {
  border:none;
  width:100%;
}
.conditions-table tr .el-form-item {
  width:300px;
  height:40px;
  line-height:45px;
}
.conditions-table tr .el-form-item .el-form-item__label {
  width:100px;
  text-align: right;
  margin:0;
}

</style>
