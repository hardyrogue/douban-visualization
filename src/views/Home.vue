<template>
  <div>
    <!-- 首页容器 -->
    <div class="home-container">
      <!-- 搜索区域 -->
      <div class="search-row">
        <!-- 搜索框和关键词输入 -->
        <div class="search-area">
          <img src="/src/assets/logo.png" class="logo" />
          <!-- 搜索框组件，双向绑定 keyword，并监听搜索事件 -->
          <SearchBar v-model:keyword="keyword" @search="handleSearch" />
        </div>

        <!-- 热门标签列表 -->
        <div class="hot-tags">
          <!-- 遍历热门搜索标签，并绑定点击事件 -->
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
        <!-- 加载动画显示 -->
        <div v-if="loading" class="loading-box">
          <img
            src="https://media.tenor.com/On7kvXhzml4AAAAj/loading-gif.gif"
            class="loading-gif"
          />
          <p class="loading-text">正在获取电影列表，请稍候...</p>
        </div>

        <!-- 搜索结果区域 -->
        <div v-else class="movie-area">
          <transition-group name="fade-move" tag="div" class="movie-grid">
            <!-- 遍历并显示电影卡片 -->
            <MovieCard
              v-for="(movie, index) in movies"
              :key="movie.id"
              :movie="movie"
              class="card-wrapper"
              :style="{ transitionDelay: `${index * 80}ms` }"
            />
          </transition-group>
          <!-- 如果没有搜索结果，显示提示 -->
          <div v-if="!movies.length" class="empty">暂无搜索结果</div>
        </div>

        <!-- 右侧推荐栏 -->
        <div class="sidebar">
          <h4>🔥 热门搜索</h4>
          <ul>
            <!-- 遍历热门标签列表，点击标签触发搜索 -->
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
// 导入必要的组件和 Vue 方法
import SearchBar from '../components/SearchBar.vue'
import MovieCard from '../components/MovieCard.vue'
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { searchMovies } from '../services/movieService'

// 获取当前路由信息
const route = useRoute()
const router = useRouter()

// 搜索关键词和电影列表状态
const keyword = ref(route.query.q || '')  // 初始值为路由中的查询参数
const movies = ref([])  // 电影列表
const loading = ref(false)  // 加载状态

// 热门搜索词列表
const hotList = [
  '流浪地球', '教父', '复仇者联盟', '盗梦空间', '功夫熊猫',
  '肖申克的救赎', '黑客帝国', '泰坦尼克号', '星际穿越', 
  '毒液', '速度与激情', '无间道', '战狼2', '美丽人生',
  '千与千寻', '这个杀手不太冷', '阿甘正传', '蝙蝠侠：黑暗骑士', '海上钢琴师',
  '摩托骑士','Mobland','疯狂的麦克斯','传奇','失控的布朗森',
  '小猪佩奇','小王子','小妇人','小丑','我的世界',
  '疯狂动物城','The Drop','伦敦路','Taboo','怪奇物语'
]

// 处理点击热门标签
const applyHotKeyword = (kw) => {
  keyword.value = kw
  router.push({ path: '/home', query: { q: kw } })  // 更新路由查询参数，重新加载结果
}

// 搜索按钮点击或回车触发
const handleSearch = () => {
  if (keyword.value) {
    router.push({ path: '/home', query: { q: keyword.value } })  // 更新路由并查询
  }
}

// 监听路由参数变化，自动触发搜索
watch(
  () => route.query.q,  // 监听路由中的查询参数
  async (newQ) => {
    if (!newQ) return (movies.value = [])  // 如果没有关键词，清空电影列表
    keyword.value = newQ  // 更新关键词
    loading.value = true  // 显示加载动画
    movies.value = await searchMovies(newQ)  // 调用 API 获取电影列表
    loading.value = false  // 隐藏加载动画
  },
  { immediate: true }  // 初始时立即执行
)

</script>

<style scoped>
/* 页面基础布局 */
.home-container {
  padding: 2rem 3rem;
  background: #f5f6fa;
}

/* 搜索框区域 */
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

/* 热门标签区域 */
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

/* 内容区域布局 */
.content-wrapper {
  display: flex;
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

/* 电影展示区域 */
.movie-area {
  flex: 1;
}

.movie-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 20px;
}

/* 推荐栏样式 */
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

/* 加载动画样式 */
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

/* 空数据提示 */
.empty {
  text-align: center;
  color: #999;
  font-size: 16px;
  padding: 3rem;
}
</style>
