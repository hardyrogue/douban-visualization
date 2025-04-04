<template>
  <DefaultLayout>
    <div class="dashboard-page">
      <h2 style="margin-bottom: 1rem">🎯 数据可视化看板</h2>

      <!-- 图表区域 -->
      <div class="charts">
        <v-chart class="chart-box" :option="genreOption" autoresize />
        <v-chart class="chart-box" :option="scoreOption" autoresize />
        <v-chart class="chart-box" :option="yearOption" autoresize />
      </div>
    </div>
  </DefaultLayout>
</template>

<script setup>
import DefaultLayout from '../layout/DefaultLayout.vue'
import { ref } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { PieChart, BarChart, LineChart } from 'echarts/charts'
import { TitleComponent, TooltipComponent, LegendComponent, GridComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'

use([PieChart, BarChart, LineChart, TitleComponent, TooltipComponent, LegendComponent, GridComponent, CanvasRenderer])

const genreOption = ref({
  title: { text: '类型占比', left: 'center' },
  tooltip: { trigger: 'item' },
  legend: { bottom: 0 },
  series: [
    {
      name: '类型',
      type: 'pie',
      radius: '50%',
      data: [
        { value: 40, name: '爱情' },
        { value: 30, name: '科幻' },
        { value: 20, name: '动作' },
        { value: 10, name: '悬疑' }
      ],
    }
  ]
})

const scoreOption = ref({
  title: { text: '评分分布', left: 'center' },
  tooltip: {},
  xAxis: { type: 'category', data: ['<6', '6~7', '7~8', '8~9', '9~10'] },
  yAxis: { type: 'value' },
  series: [{
    type: 'bar',
    data: [3, 12, 18, 25, 9]
  }]
})

const yearOption = ref({
  title: { text: '年度发布趋势', left: 'center' },
  tooltip: {},
  xAxis: { type: 'category', data: ['2018', '2019', '2020', '2021', '2022'] },
  yAxis: { type: 'value' },
  series: [{
    type: 'line',
    data: [10, 15, 18, 25, 22]
  }]
})
</script>

<style scoped>
.dashboard-page {
  padding: 2rem;
}
.charts {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 2rem;
}
.chart-box {
  height: 360px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  padding: 1rem;
}
</style>
