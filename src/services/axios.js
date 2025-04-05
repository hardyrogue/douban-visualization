// src/services/axios.js
import axios from 'axios'

const instance = axios.create({
  baseURL: 'http://localhost:8000/api',  // ✅ Django 后端地址
  timeout: 10000,
  withCredentials: true                  // ✅ 允许带 cookie（关键）
})

export default instance
axios.defaults.withCredentials = true
