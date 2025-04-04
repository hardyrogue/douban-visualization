<template>
  <DefaultLayout>
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
          <img src="https://img.icons8.com/clouds/100/movie.png" />
        </div>
      </div>
    </div>
  </DefaultLayout>
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
  '肖申克的救赎', '黑客帝国', '泰坦尼克号', '星际穿越', '大话西游'
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
  padding: 2rem;
  background: #f9f9f9;
}

.search-row {
  display: flex;
  align-items: center;
  gap: 1rem;
  max-width: 1200px;
  margin: 0 auto 1.5rem;
}

.search-area {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-left: 2rem;
}

.logo {
  width: 32px;
  height: 32px;
}

.hot-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-left: auto;
  margin-right: 2rem;
}

.hot-tag {
  cursor: pointer;
  font-size: 14px;
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
  width: 200px;
  background: white;
  padding: 1rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.sidebar h4 {
  font-size: 16px;
  margin-bottom: 0.5rem;
}

.sidebar ul {
  list-style: none;
  padding-left: 0;
  margin-bottom: 1rem;
}

.sidebar li {
  font-size: 15px;
  color: #333;
  margin-bottom: 0.3rem;
  cursor: pointer;
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
</style>
