<template>
  <DefaultLayout>
    <div v-if="loading" class="loading-box">
      <img src="https://media.tenor.com/On7kvXhzml4AAAAj/loading-gif.gif" class="loading-gif" />
      <p class="loading-text">正在获取电影信息，请稍候...</p>
    </div>

    <div v-else class="movie-detail">
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
        <el-button size="small" type="info" plain>
          🔗 豆瓣
        </el-button>
      </a>


      </div>
    </div>

      <!-- 🎬 电影信息卡片 -->
      <div class="card movie-info">
        <img :src="`http://localhost:8000/api/image-proxy/?url=${encodeURIComponent(movie.cover)}`" class="cover" />
        <div class="info">
          <div class="title-row">
          <h2>{{ movie.title }}</h2>
          <!-- <div class="btn-group">
            <el-button size="small" type="warning" plain @click="goBack">⬅ 返回</el-button>
            <el-button size="small" type="success" plain @click="toggleCollect">❤️ 收藏</el-button>
            <el-button size="small" type="info" plain :href="doubanLink" target="_blank">🔗 豆瓣</el-button>
          </div> -->
        </div>

          <el-rate v-model="movie.rating" disabled show-score :max="10" score-template="{value} 分" />
          <div class="details">
            <p><strong>导演：</strong> {{ movie.directors || '暂无数据' }}</p>
            <p><strong>主演：</strong> {{ movie.actors || '暂无数据' }}</p>
            <p><strong>类型：</strong> {{ movie.genres || '暂无数据' }}</p>
            <p><strong>上映时间：</strong> {{ movie.year || '暂无数据' }}</p>
          </div>
          <div class="summary">
            <p><strong>简介：</strong></p>
            <p>{{ movie.summary || '暂无数据' }}</p>
          </div>
        </div>
      </div>

      <!-- 📊 评分分布图 -->
      <div class="card">
        <h3>📈 评分分布</h3>
        <v-chart :option="chartOptions" autoresize style="width: 100%; height: 300px;" />
      </div>
      <!-- 💬 评论列表 -->
      <div class="card">
        <h3>🔥 热门短评</h3>
        <div v-if="comments.length === 0">暂无评论</div>
        <div v-else>
          <div v-for="(cmt, index) in comments" :key="index" class="comment-card">
            <p><strong>{{ cmt.name }}</strong>（{{ cmt.time }}）</p>
            <p>{{ cmt.content }}</p>
            <p>👍 {{ cmt.upvote }} ｜ ⭐ {{ cmt.stars }}</p>
            <el-divider />
          </div>
          <div style="text-align: center;">
            <el-button v-if="!noMore" @click="loadComments" :loading="loadingMore" type="primary">
              加载更多
            </el-button>
            <el-text v-else>没有更多评论啦</el-text>
          </div>
        </div>
      </div>

    </div>
  </DefaultLayout>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import DefaultLayout from '../layout/DefaultLayout.vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { BarChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, TitleComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { useRouter } from 'vue-router'
use([BarChart, GridComponent, TooltipComponent, TitleComponent, CanvasRenderer])

const route = useRoute()
const movie = ref({})
const wordcloudSrc = ref('')
const chartOptions = ref(null)
const loading = ref(true)
const loadingMore = ref(false)
const comments = ref([])
const start = ref(0)
const limit = 5
const noMore = ref(false)
const router = useRouter()
const isFavorited = ref(false)

const toggleFavorite = async () => {
  try {
    const res = await axios.post('http://localhost:8000/api/movies/favorite/', { id: route.params.id })
    isFavorited.value = res.data.status === 'added'
  } catch (err) {
    console.error('收藏失败：', err)
  }
}

const doubanLink = computed(() => {
  return `https://movie.douban.com/subject/${route.params.id}/`
})

const goBack = () => {
  router.back()  // ✅ 返回上一个页面（也可替换为 router.push('/')）
}

const toggleCollect = () => {
  alert('⭐ 收藏功能可在后续实现！')
}

const loadComments = async () => {
  if (loadingMore.value || noMore.value) return
  loadingMore.value = true
  try {
    const res = await axios.get('http://localhost:8000/api/movies/comments/', {
      params: {
        id: route.params.id,
        start: start.value,
        limit: limit
      }
    })
    const data = res.data.comments || []
    if (data.length < limit) {
      noMore.value = true
    }
    comments.value.push(...data)
    start.value += limit
  } catch (err) {
    console.error('评论加载失败：', err)
  } finally {
    loadingMore.value = false
  }
}

onMounted(async () => {
  const movieId = route.params.id
  try {
    console.log('详情页加载', route.params.id)
    const res = await axios.get(`http://localhost:8000/api/movies/detail/?id=${movieId}`)

    console.log('返回数据', res.data)
    movie.value = res.data
    wordcloudSrc.value = `/static/wordclouds/${movieId}.png`
    
    const dist = res.data.rating_dist || { "1": 0, "2": 0, "3": 0, "4": 0, "5": 0 }
    chartOptions.value = {
  title: { text: '', left: 'center' },
  tooltip: {},
  xAxis: { type: 'category', data: ['1星', '2星', '3星', '4星', '5星'] },
  yAxis: { type: 'value' },
  animationDuration: 800,
  series: [
    {
      data: [dist['1'], dist['2'], dist['3'], dist['4'], dist['5']],
      type: 'bar',
      itemStyle: {
  borderRadius: [4, 4, 0, 0],
  color: {
    type: 'linear',
    x: 0, y: 0, x2: 0, y2: 1,
    colorStops: [
      { offset: 0, color: '#3b82f6' },  // 深蓝
      { offset: 1, color: '#9333ea' }   // 紫
    ]
  }
}

    }
  ]
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
.movie-detail {
  max-width: 960px;
  margin: 2rem auto;
  padding: 1rem;
  background: #f0f2f5;
  border-radius: 8px;
}

/* loading */
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
  height: 80px;
  margin-bottom: 1rem;
}
.loading-text {
  font-size: 18px;
  color: #409EFF;
  font-weight: bold;
  text-shadow: 0 0 6px #409EFF;
}

/* 卡片通用样式 */
.card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  margin-bottom: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

/* 电影信息块 */
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
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* 信息右侧 */
.info {
  flex: 1;
}
.title-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.btn-group {
  display: flex;
  gap: 0.5rem;
}

/* 文本信息 */
.details p,
.summary p {
  margin: 0.5rem 0;
  line-height: 1.6;
  color: #444;
}
.info h2 {
  margin: 0;
  font-size: 24px;
  font-weight: bold;
}

/* 词云图 */
.wordcloud {
  width: 100%;
  max-width: 600px;
  margin-top: 1rem;
}

/* 评论块 */
.comment-card {
  background: #fafafa;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
}.sticky-header {
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

.movie-title {
  font-size: 16px;
  font-weight: bold;
  margin-left: 1rem;
}

.header-left, .header-right {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.comment-card {
  background: white;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
  margin-bottom: 1rem;
  transition: transform 0.2s ease;
}
.comment-card:hover {
  transform: scale(1.01);
}
.comment-card p {
  margin: 0.3rem 0;
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

</style>