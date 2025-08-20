<template>
  <div id="app">
    <a-config-provider :locale="zhCN">
      <MainView />
    </a-config-provider>
  </div>
</template>

<script setup>
import zhCN from 'ant-design-vue/es/locale/zh_CN'
import MainView from './views/MainView.vue'
import 'ant-design-vue/dist/reset.css'
import './styles/global.css'
</script>

<style>
#app {
  height: 100vh;
  width: 100vw;
  overflow: hidden;
}
</style>
