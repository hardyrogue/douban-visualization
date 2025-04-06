<template>
  <div>
    <div class="home-container">
      <!-- 顶部搜索栏 -->
      <div class="search-row">
        <div class="search-area">
          <img src="/src/assets/logo.png" class="logo" />
          <SearchBar v-model:keyword="keyword" @search="handleSearch" />
        </div>
        <div class="hot-tags">
          <el-tag
            v-for="(tag, idx) in hotList"
            :key="idx"
            type="info"
            class="hot-tag"
            @click="applyHotKeyword(tag)"
          >
            {{ tag }}
          </el-tag>
        </div>
      </div>

      <!-- 内容区域 -->
      <div class="content-wrapper">
        <!-- 加载动画 -->
        <div v-if="loading" class="loading-box">
          <img
            src="https://media.tenor.com/On7kvXhzml4AAAAj/loading-gif.gif"
            class="loading-gif"
          />
          <p class="loading-text">正在获取电影列表，请稍候...</p>
        </div>

        <!-- 搜索结果 -->
        <div v-else class="movie-area">
          <transition-group name="fade-move" tag="div" class="movie-grid">
            <MovieCard
              v-for="(movie, index) in movies"
              :key="movie.id"
              :movie="movie"
              class="card-wrapper"
              :style="{ transitionDelay: `${index * 80}ms` }"
            />
          </transition-group>
          <div v-if="!movies.length" class="empty">暂无搜索结果</div>
        </div>

        <!-- 右侧推荐 -->
        <div class="sidebar">
          <h4>🔥 热门搜索</h4>
          <ul>
            <li v-for="tag in hotList" :key="tag" @click="applyHotKeyword(tag)">
              {{ tag }}
            </li>
          </ul>
          <img src="/src/assets/2024.png" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import DefaultLayout from '../layout/DefaultLayout.vue'
import SearchBar from '../components/SearchBar.vue'
import MovieCard from '../components/MovieCard.vue'
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { searchMovies } from '../services/movieService'

const route = useRoute()
const router = useRouter()
const keyword = ref(route.query.q || '')
const movies = ref([])
const loading = ref(false)

const hotList = [
  '流浪地球', '教父', '复仇者联盟', '盗梦空间', '功夫熊猫',
  '肖申克的救赎', '黑客帝国', '泰坦尼克号', '星际穿越', 
  '毒液', '速度与激情', '无间道', '战狼2', '美丽人生',
  '千与千寻', '这个杀手不太冷', '阿甘正传', '蝙蝠侠：黑暗骑士', '海上钢琴师',
  '摩托骑士','Mobland','疯狂的麦克斯','传奇','失控的布朗森',
  '小猪佩奇','小王子','小妇人','小丑','我的世界',
  '疯狂动物城','The Drop','伦敦路','Taboo','怪奇物语'
]

// 点击热门关键词
const applyHotKeyword = (kw) => {
  keyword.value = kw
  router.push({ path: '/home', query: { q: kw } })
}

// 搜索按钮点击或回车触发
const handleSearch = () => {
  if (keyword.value) {
    router.push({ path: '/home', query: { q: keyword.value } })
  }
}

watch(
  () => route.query.q,
  async (newQ) => {
    console.log('[watch触发]', newQ) // ✅ 添加这行
    if (!newQ) return (movies.value = [])
    keyword.value = newQ
    loading.value = true
    movies.value = await searchMovies(newQ)
    loading.value = false
  },
  { immediate: true }
)

</script>

<style scoped>
.home-container {
  padding: 2rem 3rem;
  background: #f5f6fa;
}

.search-row {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
}

.search-area {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 1rem;
}

.logo {
  width: 40px;
  height: 40px;
}

.hot-tags {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 0.5rem;
}

.hot-tag {
  cursor: pointer;
  font-size: 13px;
  border-radius: 20px;
  padding: 3px 12px;
  transition: all 0.2s;
}
.hot-tag:hover {
  background-color: #409eff;
  color: white;
}

.content-wrapper {
  display: flex;
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.movie-area {
  flex: 1;
}

.movie-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 20px;
}

.sidebar {
  width: 220px;
  background: white;
  padding: 1.2rem;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
}

.sidebar h4 {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 0.75rem;
}

.sidebar ul {
  list-style: none;
  padding-left: 0;
  margin-bottom: 1rem;
}

.sidebar li {
  font-size: 14px;
  color: #333;
  margin-bottom: 0.4rem;
  cursor: pointer;
  transition: color 0.2s;
}
.sidebar li:hover {
  color: #409eff;
}

.loading-box {
  padding: 4rem;
  text-align: center;
  background: white;
  border-radius: 12px;
  width: 100%;
}
.loading-gif {
  width: 80px;
  height: 80px;
  margin-bottom: 1rem;
}
.loading-text {
  font-size: 18px;
  color: #409EFF;
  font-weight: bold;
  text-shadow: 0 0 6px #409EFF;
}

.empty {
  text-align: center;
  color: #999;
  font-size: 16px;
  padding: 3rem;
}
</style>