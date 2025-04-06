<template>
  <el-card class="movie-card" shadow="hover" @click="goDetail">
    <img
      :src="movie.cover ? `http://localhost:8000/api/image-proxy/?url=${encodeURIComponent(movie.cover)}` : defaultCover"
      @error="e => e.target.src = defaultCover"
      class="cover"
    />

    <div class="info">
      <h3 class="title" :title="movie.title">{{ movie.title }}</h3>
      <p class="year">📅 {{ movie.year || '年份未知' }}</p>
      <p class="subtitle">{{ movie.sub_title || '暂无英文标题' }}</p>
    </div>
  </el-card>
</template>

<script setup>
import { useRouter } from 'vue-router'

const props = defineProps({
  movie: Object
})

const router = useRouter()

const goDetail = () => {
  router.push(`/movie/${props.movie.id}`)
}

const defaultCover = 'https://via.placeholder.com/200x300?text=No+Image'
</script>

<style scoped>
.movie-card {
  width: 220px;
  padding: 0;
  border-radius: 10px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.25s ease-in-out;
}
.movie-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

.cover {
  width: 100%;
  height: 300px;
  object-fit: cover;
  border-bottom: 1px solid #f0f0f0;
  transition: transform 0.3s ease;
}
.movie-card:hover .cover {
  transform: scale(1.03);
}

.info {
  padding: 12px;
  background: #fff;
}

.title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  line-height: 1.4;
  margin-bottom: 4px;
}

.year {
  font-size: 13px;
  color: #666;
  margin-bottom: 4px;
}

.subtitle {
  font-size: 12px;
  color: #999;
}
</style>
