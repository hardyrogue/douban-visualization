// src/services/movieService.js
import axios from './axios'  // ✅ 用我们自定义的 axios 实例

export function searchMovies(keyword) {
  return axios
    .get('/movies/search/', {
      params: { q: keyword }
    })
    .then(res => {
      console.log('后端返回内容：', res.data)
      return res.data.results
    })
    .catch(error => {
      console.error('请求出错：', error)
      return []
    })
}
