// src/composables/useUserInfo.js
import { ref } from 'vue'
import axios from '@/services/axios'

export const userInfo = ref(null)

export async function fetchUserInfo() {
  try {
    const res = await axios.get('/auth/user/')
    userInfo.value = res.data
  } catch (err) {
    console.error('获取用户信息失败', err)
    userInfo.value = null
  }
}

export function clearUserInfo() {
  userInfo.value = null
}
