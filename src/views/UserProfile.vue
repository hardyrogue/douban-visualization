<template>
  <div class="profile-container">
    <!-- 返回按钮 -->
    <el-button @click="goBack" type="primary" icon="el-icon-arrow-left" class="back-button">返回</el-button>

    <div class="form-container">
      <h2>个人中心</h2>
      <el-form :model="form" ref="formRef">
        <!-- 用户头像 -->
        <el-form-item label="头像" class="avatar-form-item">
          <el-upload
            class="avatar-uploader"
            action=""
            :show-file-list="false"
            :before-upload="beforeAvatarUpload"
            :on-change="handleAvatarChange"
            :on-remove="handleAvatarRemove"
            accept="image/*"
          >
            <img
              v-if="form.avatar"
              :src="form.avatar"
              class="avatar-preview"
              alt="头像预览"
            />
            <i v-else class="el-icon-plus avatar-icon"></i>
          </el-upload>
        </el-form-item>

        <!-- 用户简介 -->
        <el-form-item label="个人简介" class="bio-form-item">
          <el-input v-model="form.bio" placeholder="输入个人简介" />
        </el-form-item>

        <el-button type="primary" @click="saveProfile" class="save-button">保存</el-button>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from '@/services/axios'

const router = useRouter()

const form = ref({
  avatar: '',
  bio: ''
})

const fetchUserInfo = async () => {
  try {
    const response = await axios.get('/auth/user/')
    form.value.avatar = response.data.avatar || ''
    form.value.bio = response.data.bio || ''
  } catch (error) {
    console.error('无法获取用户信息', error)
  }
}

const saveProfile = async () => {
  try {
    const response = await axios.put('/auth/user/', form.value)
    console.log('个人资料已保存', response.data)
  } catch (error) {
    console.error('保存失败', error)
  }
}

const goBack = () => {
  router.go(-1)
}

// 限制上传头像文件类型和大小
const beforeAvatarUpload = (file) => {
  const isImage = file.type.startsWith('image/')
  if (!isImage) {
    this.$message.error('只能上传图片文件')
  }
  const isLt2M = file.size / 1024 / 1024 < 2  // 限制文件大小 2MB
  if (!isLt2M) {
    this.$message.error('上传头像图片大小不能超过 2MB')
  }
  return isImage && isLt2M
}

const handleAvatarChange = (file) => {
  const reader = new FileReader()
  reader.onload = (e) => {
    form.value.avatar = e.target.result  // 这里设置为文件的 Base64 数据
  }
  reader.readAsDataURL(file.raw)
}

const handleAvatarRemove = () => {
  form.value.avatar = ''
}

fetchUserInfo()
</script>

<style scoped>
.profile-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  flex-direction: column;
  padding-top: 50px; /* 增加顶部间隙 */
}

.back-button {
  align-self: flex-start;
  margin-left: 20px;
  margin-bottom: 20px;
}

.form-container {
  width: 400px;
  padding: 20px;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
}

h2 {
  margin-bottom: 20px;
  font-size: 24px;
  font-weight: bold;
}

.avatar-preview {
  width: 100px;
  height: 100px;
  margin-top: 10px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 20px;
}

.avatar-uploader {
  display: inline-block;
}

.avatar-icon {
  font-size: 28px;
  color: #409EFF;
}

.el-form-item {
  margin-bottom: 15px;
}

.el-button {
  margin-top: 20px;
}

.save-button {
  width: 100%;
}

.bio-form-item {
  margin-top: 20px;
}

</style>
