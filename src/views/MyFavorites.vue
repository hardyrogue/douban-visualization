<template>
  <div>
    <div class="favorites-page">
      <!-- 返回按钮 -->
      <el-button type="default" icon="ArrowLeft" @click="goBack" plain>
        返回上一页
      </el-button>

      <h2 class="title">📂 我的收藏</h2>

      <div v-if="favorites.length === 0" class="empty">
        暂无收藏内容
      </div>

      <div class="movie-grid">
        <div v-for="movie in favorites" :key="movie.douban_id" class="movie-card">
          <!-- 电影标题 -->
          <h3 class="movie-title">{{ movie.title }}</h3>
          <!-- 电影 ID -->
          <p class="movie-id">ID: {{ movie.douban_id }}</p>
          <!-- 显示评分 -->
          <p class="rating">评分：{{ movie.rating || '暂无评分' }}</p>
        </div>
      </div>

      <div v-if="favorites.length === 0" class="empty">
        暂无收藏内容
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const favorites = ref([])

const goBack = () => {
  router.back()
}

// 请求获取收藏列表
onMounted(async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/movies/favorites/list/')
    console.log('获取收藏列表成功', response.data)  // 👈 看看返回的数据
    favorites.value = response.data.favorites || []  // 处理返回的数据
  } catch (error) {
    console.error('获取收藏列表失败：', error)
  }
})
</script>

<style scoped>
.favorites-page {
  padding: 2rem;
}

.title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 1rem;
  color: #333;
}

.movie-grid {
  margin-top: 1.5rem;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 20px;
}

.movie-card {
  background-color: #fff;
  border-radius: 8px;
  padding: 1rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.movie-card:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
}

.movie-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 0.5rem;
  color: #333;
}

.movie-id {
  font-size: 14px;
  color: #777;
  margin-bottom: 0.5rem;
}

.rating {
  font-size: 14px;
  color: #555;
}

.empty {
  margin-top: 1rem;
  color: #999;
}
</style>
