<template>
  <div>
    <!-- 我的收藏页面 -->
    <div class="favorites-page">
      <!-- 返回按钮 -->
      <el-button type="default" icon="ArrowLeft" @click="goBack" plain>
        返回上一页
      </el-button>

      <!-- 页面标题 -->
      <h2 class="title">📂 我的收藏</h2>

      <!-- 如果没有收藏的电影，显示提示信息 -->
      <div v-if="favorites.length === 0" class="empty">
        暂无收藏内容
      </div>

      <!-- 电影网格展示 -->
      <div class="movie-grid">
        <!-- 遍历显示收藏的每一部电影 -->
        <div v-for="movie in favorites" :key="movie.douban_id" class="movie-card">
          <!-- 电影标题 -->
          <h3 class="movie-title">{{ movie.title }}</h3>
          <!-- 显示电影 ID -->
          <p class="movie-id">ID: {{ movie.douban_id }}</p>
          <!-- 显示电影评分 -->
          <p class="rating">评分：{{ movie.rating || '暂无评分' }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// 引入 Vue 和相关库
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

// 路由实例
const router = useRouter()

// 定义收藏列表
const favorites = ref([])

// 返回上一页
const goBack = () => {
  router.back()
}

// 获取收藏列表数据
onMounted(async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/movies/favorites/list/')
    console.log('获取收藏列表成功', response.data)  // 查看返回的数据结构
    favorites.value = response.data.favorites || []  // 处理返回的数据
  } catch (error) {
    console.error('获取收藏列表失败：', error)
  }
})
</script>

<style scoped>
/* 页面容器样式 */
.favorites-page {
  padding: 2rem;
}

/* 页面标题样式 */
.title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 1rem;
  color: #333;
}

/* 电影网格布局 */
.movie-grid {
  margin-top: 1.5rem;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 20px;
}

/* 单个电影卡片样式 */
.movie-card {
  background-color: #fff;
  border-radius: 8px;
  padding: 1rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

/* 鼠标悬停效果 */
.movie-card:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
}

/* 电影标题样式 */
.movie-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 0.5rem;
  color: #333;
}

/* 电影 ID 样式 */
.movie-id {
  font-size: 14px;
  color: #777;
  margin-bottom: 0.5rem;
}

/* 电影评分样式 */
.rating {
  font-size: 14px;
  color: #555;
}

/* 无收藏内容时的提示样式 */
.empty {
  margin-top: 1rem;
  color: #999;
}
</style>
