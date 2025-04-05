<template>
  <div>
    <!-- 🔍 搜索栏 + ➕ 新增按钮 -->
    <div class="controls">
      <el-input
        v-model="searchKeyword"
        placeholder="搜索用户名"
        style="width: 200px"
        clearable
        @input="handleSearch"
      />
      <el-button type="primary" @click="openCreateDialog">➕ 新增用户</el-button>
    </div>

    <!-- 👥 用户表格 -->
    <el-table :data="users" style="width: 100%" stripe border>
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="username" label="用户名" />
      <el-table-column prop="email" label="邮箱" />
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

    <!-- 📄 分页 -->
    <el-pagination
      style="margin-top: 1rem"
      layout="prev, pager, next, jumper, ->, total"
      :current-page="pagination.page"
      :page-size="pagination.pageSize"
      :total="pagination.total"
      @current-change="handlePageChange"
    />

    <!-- ✏️ 弹窗 -->
    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑用户' : '新增用户'" width="400px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="用户名">
          <el-input v-model="form.username" />
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="form.email" />
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
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from '@/services/axios'
import { ElMessage } from 'element-plus'

const users = ref([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const editingUserId = ref(null)
const searchKeyword = ref('')

const pagination = ref({
  page: 1,
  pageSize: 10,
  total: 0,
})

const form = ref({
  username: '',
  email: '',
  password: '',
  role: 'user',
})

const fetchUsers = async () => {
  const res = await axios.get('http://localhost:8000/api/users/', {
    params: {
      q: searchKeyword.value,
      page: pagination.value.page,
      page_size: pagination.value.pageSize,
    },
  })
  users.value = res.data.users
  pagination.value.total = res.data.total
}

const handleSearch = () => {
  pagination.value.page = 1
  fetchUsers()
}

const handlePageChange = (newPage) => {
  pagination.value.page = newPage
  fetchUsers()
}

const openCreateDialog = () => {
  isEdit.value = false
  form.value = {
    username: '',
    email: '',
    password: '',
    role: 'user'
  }
  dialogVisible.value = true
}

const openEditDialog = (user) => {
  isEdit.value = true
  editingUserId.value = user.id
  form.value = {
    username: user.username,
    email: user.email || '',
    password: '',
    role: user.userprofile__role || 'user'
  }
  dialogVisible.value = true
}

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

.controls {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
  gap: 1rem;
}
</style>
