<template>
  <div>
    <!-- 加载中提示 -->
    <div v-if="loading" class="loading-box">
      <img src="https://media.tenor.com/On7kvXhzml4AAAAj/loading-gif.gif" class="loading-gif" />
      <p class="loading-text">正在获取电影信息，请稍候...</p>
    </div>

    <div v-else class="movie-detail">
      <!-- 电影顶部操作栏：返回、收藏、豆瓣链接 -->
      <div class="sticky-header">
        <div class="header-left">
          <el-button size="small" type="warning" plain @click="goBack">⬅ 返回</el-button>
          <span class="movie-title">{{ movie.title }}</span>
        </div>
        <div class="header-right">
          <el-button
            size="small"
            :type="isFavorited ? 'danger' : 'success'"
            plain
            @click="toggleFavorite"
          >
            {{ isFavorited ? '❤️ 已收藏' : '❤️ 收藏' }}
          </el-button>
          <a :href="doubanLink" target="_blank" rel="noopener noreferrer">
            <el-button size="small" type="info" plain>🔗 豆瓣</el-button>
          </a>
        </div>
      </div>

      <!-- 电影详细信息 -->
      <div class="card movie-info">
        <img :src="`http://localhost:8000/api/image-proxy/?url=${encodeURIComponent(movie.cover)}`" class="cover" />
        <div class="info">
          <h2 class="movie-title-main">{{ movie.title }}</h2>
          <el-rate
            v-model="movie.rating"
            disabled
            show-score
            :max="10"
            score-template="{value} 分"
          />
          <div class="details">
            <p><strong>导演：</strong>{{ movie.directors || '暂无数据' }}</p>
            <p><strong>主演：</strong>{{ movie.actors || '暂无数据' }}</p>
            <p><strong>类型：</strong>{{ movie.genres || '暂无数据' }}</p>
            <p><strong>上映时间：</strong>{{ movie.year || '暂无数据' }}</p>
          </div>
          <div class="summary">
            <p><strong>简介：</strong></p>
            <p class="summary-text">{{ movie.summary || '暂无数据' }}</p>
          </div>
        </div>
      </div>

      <!-- 评分分布图 -->
      <div class="card">
        <h3>📊 评分分布</h3>
        <v-chart :option="chartOptions" autoresize style="width: 100%; height: 300px;" />
      </div>
      <!-- 评分统计分析 -->
<div class="card" v-if="movie.rating_stats">
  <h3>📈 评分统计分析</h3>
  <ul class="stats-list">
    <li><strong>平均评分：</strong>{{ movie.rating_stats.average || '暂无数据' }}</li>
    <li><strong>中位数：</strong>{{ movie.rating_stats.median || '暂无数据' }}</li>
    <li><strong>众数：</strong>{{ movie.rating_stats.mode || '暂无数据' }}</li>
    <li><strong>标准差：</strong>{{ movie.rating_stats.std_dev || '暂无数据' }}</li>
    <li>
      <strong>评分偏态：</strong>
      <span v-if="movie.rating_stats.skewness != null">
        {{
          movie.rating_stats.skewness > 0
            ? '偏向高分（正偏）'
            : movie.rating_stats.skewness < 0
            ? '偏向低分（负偏）'
            : '对称分布'
        }}
        （Skew = {{ movie.rating_stats.skewness }}）
      </span>
      <span v-else>暂无数据</span>
    </li>
    
  </ul>
</div>
<!-- 评分趋势图 -->
<div class="card" v-if="movie.rating_trend && Object.keys(movie.rating_trend).length > 0">
  <h3>📉 评分趋势图（按年份）</h3>
  <v-chart :option="trendChartOptions" autoresize style="width: 100%; height: 300px;" />
</div>
      <!-- 用户评论 -->
      <div class="card">
        <h3>🔥 热门短评</h3>
        <div v-if="comments.length === 0">暂无评论</div>
        <div v-else>
          <div v-for="(cmt, index) in comments" :key="index" class="comment-card">
            <p><strong>{{ cmt.name }}</strong> <span class="comment-time">（{{ cmt.time }}）</span></p>
            <p>{{ cmt.content }}</p>
            <div class="comment-actions">
              <span class="like">👍 {{ cmt.upvote }}</span>
              <span class="star">⭐ {{ cmt.stars }}</span>
            </div>
          </div>
          <div class="load-more">
            <el-button v-if="!noMore" @click="loadComments" :loading="loadingMore" type="primary">
              加载更多
            </el-button>
            <el-text v-else>没有更多评论啦</el-text>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// 导入 Vue 必需的库和组件
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { GridComponent, TooltipComponent, TitleComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart, LineChart } from 'echarts/charts'  // ✅ 添加 LineChart
// 注册 ECharts 图表组件
use([BarChart, LineChart, GridComponent, TooltipComponent, TitleComponent, CanvasRenderer])

// 路由相关
const route = useRoute()
const router = useRouter()

// 电影详情和状态变量
const movie = ref({})
const chartOptions = ref(null)
const trendChartOptions = ref(null)  // ✅ 加在这里
const loading = ref(true)
const loadingMore = ref(false)
const comments = ref([])
const start = ref(0)
const limit = 5
const noMore = ref(false)
const isFavorited = ref(false)

// 豆瓣链接计算属性
const doubanLink = computed(() => `https://movie.douban.com/subject/${route.params.id}/`)

// 返回上一页
const goBack = () => router.back()

// 收藏功能
const toggleFavorite = async () => {
  try {
    const requestData = {
      id: route.params.id,
      title: movie.value.title,
      cover: movie.value.cover,
      rating: movie.value.rating || 0
    }
    const res = await axios.post('http://localhost:8000/api/movies/favorite/', requestData)
    isFavorited.value = res.data.status === 'added'
  } catch (err) {
    console.error('收藏失败：', err)
  }
}

// 加载评论
const loadComments = async () => {
  if (loadingMore.value || noMore.value) return
  loadingMore.value = true
  try {
    const res = await axios.get('http://localhost:8000/api/movies/comments/', {
      params: { id: route.params.id, start: start.value, limit: limit }
    })
    const data = res.data.comments || []
    if (data.length < limit) noMore.value = true
    comments.value.push(...data)
    start.value += limit
  } catch (err) {
    console.error('评论加载失败：', err)
  } finally {
    loadingMore.value = false
  }
}

// 获取电影详情数据
onMounted(async () => {
  const movieId = route.params.id
  try {
    const res = await axios.get(`http://localhost:8000/api/movies/detail/?id=${movieId}`)
    movie.value = res.data
    const dist = res.data.rating_dist || { "1": 0, "2": 0, "3": 0, "4": 0, "5": 0 }
    chartOptions.value = {
      title: { text: '', left: 'center' },
      tooltip: {},
      xAxis: { type: 'category', data: ['1星', '2星', '3星', '4星', '5星'] },
      yAxis: { type: 'value' },
      animationDuration: 800,
      series: [{
        data: [dist['1'], dist['2'], dist['3'], dist['4'], dist['5']],
        type: 'bar',
        itemStyle: {
          borderRadius: [4, 4, 0, 0],
          color: {
            type: 'linear',
            x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: '#3b82f6' },
              { offset: 1, color: '#9333ea' }
            ]
          }
        }
      }]
    }
    // ✅ 紧接着加趋势图逻辑
const trend = res.data.rating_trend || {}
if (Object.keys(trend).length > 0) {
  trendChartOptions.value = {
    title: { text: '', left: 'center' },
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'category',
      data: Object.keys(trend),
      boundaryGap: false
    },
    yAxis: {
      type: 'value',
      min: 1,
      max: 5
    },
    series: [{
      type: 'line',
      data: Object.values(trend),
      smooth: true,
      symbol: 'circle',
      areaStyle: {
        color: 'rgba(59,130,246,0.2)'
      },
      lineStyle: {
        color: '#3b82f6',
        width: 3
      }
    }]
  }
}

    await loadComments()
  } catch (err) {
    console.error('详情加载失败：', err)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
/* 电影详情样式 */
.movie-detail {
  max-width: 960px;
  margin: 2rem auto;
  padding: 1rem;
  background: #f5f7fa;
  border-radius: 8px;
}

/* 加载动画样式 */
.loading-box {
  padding: 4rem;
  text-align: center;
  background: white;
  border-radius: 12px;
  max-width: 640px;
  margin: 4rem auto;
}
.loading-gif {
  width: 80px;
  margin-bottom: 1rem;
}
.loading-text {
  font-size: 18px;
  color: #409EFF;
  font-weight: bold;
}

/* 卡片样式 */
.card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  margin-bottom: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

/* 电影信息样式 */
.movie-info {
  display: flex;
  gap: 2rem;
  align-items: flex-start;
}
.cover {
  width: 220px;
  aspect-ratio: 2 / 3;
  object-fit: cover;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* 顶部操作栏样式 */
.sticky-header {
  position: sticky;
  top: 0;
  z-index: 999;
  background: white;
  border-bottom: 1px solid #eee;
  padding: 10px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
}

/* 评论卡片样式 */
.comment-card {
  background: #fff;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
  transition: transform 0.2s ease;
}
.comment-card:hover {
  transform: scale(1.01);
}
.comment-time {
  color: #999;
  font-size: 13px;
}
.comment-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-top: 0.5rem;
}
.comment-actions .like {
  color: #f56c6c;
}
.comment-actions .star {
  color: #f7ba2a;
}
.load-more {
  text-align: center;
  margin-top: 1rem;
}
.stats-list {
  list-style: none;
  padding: 0;
  margin: 1rem 0 0;
}
.stats-list li {
  margin-bottom: 8px;
  font-size: 15px;
  color: #333;
}
.stats-list strong {
  color: #409EFF;
}
</style>
