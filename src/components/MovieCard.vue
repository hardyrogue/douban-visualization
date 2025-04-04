<template>
  <el-card class="movie-card clickable" shadow="hover" @click="goDetail">
    <img
      :src="`/api/image-proxy/?url=${encodeURIComponent(movie.cover)}`"
      @error="e => e.target.src = defaultCover"
      class="cover"
      alt="movie cover"
    />
    <div class="info">
      <h3 class="title">{{ movie.title }}</h3>
      <p>年份：{{ movie.year }}</p>
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

const defaultCover = 'https://via.placeholder.com/200x300?text=No+Image'  // ✅ 兜底图
</script>


<style scoped>
.movie-card {
  width: 200px;
  padding: 10px;
}
.cover {
  width: 100%;
  height: 280px;
  object-fit: cover;
  border-radius: 6px;
  margin-bottom: 10px;
}
.info {
  text-align: left;
}
.title {
  margin: 0 0 6px;
  font-size: 16px;
  font-weight: bold;
}
.clickable {
  cursor: pointer;
  transition: transform 0.2s;
}
.clickable:hover {
  transform: translateY(-2px);
}
.cover {
  width: 100%;
  height: 280px;
  object-fit: cover;
  border-radius: 6px;
  margin-bottom: 10px;
}
.subtitle {
  font-size: 13px;
  color: #999;
  margin-top: 4px;
}

</style>
