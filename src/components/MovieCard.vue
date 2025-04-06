<template>
  <el-card class="movie-card" shadow="hover" @click="goDetail">
    <!-- 显示电影封面，若没有则显示默认封面 -->
    <img
      :src="movie.cover ? `http://localhost:8000/api/image-proxy/?url=${encodeURIComponent(movie.cover)}` : defaultCover"
      @error="e => e.target.src = defaultCover" 
      class="cover"
    />

    <!-- 显示电影的基本信息 -->
    <div class="info">
      <!-- 电影标题，若有溢出则显示完整信息 -->
      <h3 class="title" :title="movie.title">{{ movie.title }}</h3>
      <p class="year">📅 {{ movie.year || '年份未知' }}</p> <!-- 显示电影的年份 -->
      <p class="subtitle">{{ movie.sub_title || '暂无英文标题' }}</p> <!-- 显示副标题 -->
    </div>
  </el-card>
</template>

<script setup>
import { useRouter } from 'vue-router'

// 接收父组件传递的电影对象
const props = defineProps({
  movie: Object
})

const router = useRouter()  // Vue Router 实例，用于页面跳转

// 点击卡片时跳转到电影详情页面
const goDetail = () => {
  router.push(`/movie/${props.movie.id}`)  // 导航到电影的详情页面
}

// 默认封面图片
const defaultCover = 'https://via.placeholder.com/200x300?text=No+Image'
</script>

<style scoped>
/* 卡片外观 */
.movie-card {
  width: 220px;
  padding: 0;
  border-radius: 10px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.25s ease-in-out;
}

/* 鼠标悬停效果：上移并显示阴影 */
.movie-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

/* 封面图片样式：填充满卡片，处理图片的宽高比例 */
.cover {
  width: 100%;
  height: 300px;
  object-fit: cover;
  border-bottom: 1px solid #f0f0f0;
  transition: transform 0.3s ease;
}

/* 鼠标悬停时，封面图微微放大 */
.movie-card:hover .cover {
  transform: scale(1.03);
}

/* 电影信息区域 */
.info {
  padding: 12px;
  background: #fff;
}

/* 电影标题样式 */
.title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  line-height: 1.4;
  margin-bottom: 4px;
}

/* 电影年份样式 */
.year {
  font-size: 13px;
  color: #666;
  margin-bottom: 4px;
}

/* 电影副标题样式 */
.subtitle {
  font-size: 12px;
  color: #999;
}
</style>
