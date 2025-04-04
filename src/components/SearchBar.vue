<template>
  <el-input
    v-model="input"
    placeholder="请输入电影名称"
    clearable
    @keyup.enter="emitSearch"
    class="search-input"
  >
    <template #append>
      <el-button @click="emitSearch">搜索</el-button>
    </template>
  </el-input>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  keyword: String,
})

const emit = defineEmits(['update:keyword', 'search'])

const input = ref(props.keyword || '')

// ✅ 外部 keyword 改变时，内部同步
watch(
  () => props.keyword,
  (newVal) => {
    input.value = newVal || ''
  }
)

// ✅ 内部 input 改变时，emit update:keyword
watch(
  input,
  (val) => {
    emit('update:keyword', val)
  }
)

const emitSearch = () => {
  emit('search')
}
</script>

<style scoped>
.search-input {
  width: 320px;
}
</style>
