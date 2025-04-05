<template>
  <div>
    <div class="favorites-page">
      <!-- 返回按钮 -->
      <el-button type="default" icon="ArrowLeft" @click="goBack" plain>
        返回上一页
      </el-button>

      <h2>📂 我的收藏</h2>

      <div v-if="favorites.length === 0" class="empty">
        暂无收藏内容
      </div>

      <div class="movie-grid">
        <MovieCard
          v-for="movie in favorites"
          :key="movie.id"
          :movie="movie"
        />
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted } from 'vue'
import MovieCard from '../components/MovieCard.vue'
import { useRouter } from 'vue-router'
const router = useRouter()

const goBack = () => {
  router.back()
}

const favorites = ref([])

onMounted(() => {
  const stored = localStorage.getItem('favorites')
  favorites.value = stored ? JSON.parse(stored) : []
})
</script>

<style scoped>
.favorites-page {
  padding: 2rem;
}

.movie-grid {
  margin-top: 1.5rem;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 20px;
}

.empty {
  margin-top: 1rem;
  color: #999;
}
</style>
