<template>
  <div class="profile-page">
    <div class="card">
      <div class="card-header">
        <h2>个人中心</h2>
        <el-button size="small" @click="router.back()">返回</el-button>
      </div>

      <el-form label-width="80px">
        <el-form-item label="头像">
          <el-upload
            class="avatar-uploader"
            :show-file-list="false"
            :before-upload="handleAvatarChange"
          >
            <img v-if="avatarPreview" :src="avatarPreview" class="avatar" />
            <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
          </el-upload>
        </el-form-item>

        <el-form-item label="个人简介">
          <el-input v-model="form.bio" placeholder="输入个人简介" />
        </el-form-item>
        <el-form-item label="个人邮箱">
          <el-input v-model="form.email" placeholder="输入邮箱" />
        </el-form-item>

        <el-form-item label="原密码">
          <el-input v-model="form.old_password" type="password" placeholder="请输入原密码(留空不修改)" />
        </el-form-item>

        <el-form-item label="新密码">
          <el-input v-model="form.new_password" type="password" placeholder="请输入新密码" />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="handleSave">保存</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from '@/services/axios'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { eventBus } from '@/eventBus'

const router = useRouter()

const avatarFile = ref(null)
const avatarPreview = ref('')
const form = ref({
  bio: '',
  email: '',
  old_password: '',
  new_password: ''
})

const getProfileInfo = async () => {
  try {
    const res = await axios.get('/auth/user/')
    form.value.bio = res.data.bio || ''
    form.value.email = res.data.email || ''
    avatarPreview.value = res.data.avatar || ''
  } catch (err) {
    ElMessage.error('获取用户信息失败')
    router.push('/login')
  }
}

onMounted(() => {
  getProfileInfo()
})

const handleAvatarChange = (file) => {
  avatarFile.value = file
  const reader = new FileReader()
  reader.onload = () => {
    avatarPreview.value = reader.result
  }
  reader.readAsDataURL(file)
  return false  // 阻止默认上传行为
}

const handleSave = async () => {
  // ⚠️ 新旧密码不能相同
  if (form.value.old_password && form.value.new_password && form.value.old_password === form.value.new_password) {
    ElMessage.warning('新密码不能与原密码相同')
    return
  }

  try {
    // ✅ 基本信息 + 头像
    const formData = new FormData()
    formData.append('bio', form.value.bio)
    formData.append('email', form.value.email)
    if (avatarFile.value) {
      formData.append('avatar', avatarFile.value)
    }

    await axios.post('/auth/profile/update/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })

    // ✅ 修改密码（前提是填写了）
    if (form.value.old_password && form.value.new_password) {
      await axios.post('/auth/change-password/', {
        old_password: form.value.old_password,
        new_password: form.value.new_password
      })
    }

    ElMessage.success('保存成功')
    eventBus.emit('user-updated')

    form.value.old_password = ''
    form.value.new_password = ''
  } catch (err) {
    ElMessage.error(err.response?.data?.error || '保存失败')
  }
}

</script>

<style scoped>
.profile-page {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 4rem 0;
}
.card {
  background: #fff;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0,0,0,0.05);
  width: 480px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}
.avatar-uploader {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 88px;
  height: 88px;
  border: 1px dashed #dcdfe6;
  border-radius: 50%;
  overflow: hidden;
}
.avatar {
  width: 88px;
  height: 88px;
  border-radius: 50%;
}
.avatar-uploader-icon {
  font-size: 24px;
  color: #999;
}
</style>
