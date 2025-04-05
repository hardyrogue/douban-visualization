<template>
  <div class="header-actions">
    <el-button type="primary" @click="openCreateDialog">➕ 新增用户</el-button>
  </div>

  <div class="user-list">
    <h2>👥 用户管理</h2>
    <el-table :data="users" style="width: 100%" stripe border>
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="username" label="用户名" />
      <el-table-column prop="userprofile__role" label="角色" />
      <el-table-column label="操作" width="180">
        <template #default="{ row }">
          <el-button size="small" @click="openEditDialog(row)">编辑</el-button>
          <el-popconfirm title="确定删除此用户？" @confirm="deleteUser(row.id)">
            <template #reference>
              <el-button type="danger" size="small">删除</el-button>
            </template>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>
  </div>

  <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑用户' : '新增用户'" width="400px">
    <el-form :model="form" label-width="80px">
      <el-form-item label="用户名">
        <el-input v-model="form.username" />
      </el-form-item>
      <el-form-item label="角色">
        <el-select v-model="form.role" placeholder="请选择角色">
          <el-option label="普通用户" value="user" />
          <el-option label="管理员" value="admin" />
        </el-select>
      </el-form-item>
      <el-form-item :label="isEdit ? '新密码' : '密码'">
        <el-input v-model="form.password" type="password" :placeholder="isEdit ? '如需修改请填写' : '请输入密码'" />
      </el-form-item>
    </el-form>

    <template #footer>
      <el-button @click="dialogVisible = false">取消</el-button>
      <el-button type="primary" @click="handleSubmit">保存</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from '@/services/axios'
import { ElMessage } from 'element-plus'

const users = ref([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const editingUserId = ref(null)

const form = ref({
  username: '',
  password: '',
  role: 'user',
})

// 获取用户列表
const fetchUsers = async () => {
  const res = await axios.get('http://localhost:8000/api/users/')
  users.value = res.data.users
}

// 新增用户弹窗
const openCreateDialog = () => {
  isEdit.value = false
  form.value = {
    username: '',
    password: '',
    role: 'user'
  }
  dialogVisible.value = true
}

// 编辑用户弹窗
const openEditDialog = (user) => {
  isEdit.value = true
  editingUserId.value = user.id
  form.value = {
    username: user.username,
    email: user.email || '',
    password: '', // 不预填密码
    role: user.userprofile__role || 'user'
  }
  dialogVisible.value = true
}

// 保存（新增或编辑）
const handleSubmit = async () => {
  if (!form.value.username || (!isEdit.value && !form.value.password)) {
    ElMessage.error('用户名和密码不能为空')
    return
  }

  try {
    if (isEdit.value) {
      await axios.put(`http://localhost:8000/api/users/${editingUserId.value}/`, form.value)
      ElMessage.success('更新成功')
    } else {
      await axios.post('http://localhost:8000/api/users/', form.value)
      ElMessage.success('创建成功')
    }

    dialogVisible.value = false
    fetchUsers()
  } catch (err) {
    console.error(err)
    ElMessage.error(err.response?.data?.error || '操作失败')
  }
}

// 删除用户
const deleteUser = async (id) => {
  try {
    await axios.delete(`http://localhost:8000/api/users/${id}/`)
    ElMessage.success('用户已删除')
    fetchUsers()
  } catch (err) {
    ElMessage.error('删除失败')
  }
}

onMounted(fetchUsers)
</script>

<style scoped>
.user-list {
  padding: 1rem;
}
.header-actions {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 1rem;
}
</style>
