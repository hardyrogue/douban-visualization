<template>
  <div class="user-management-container">
    <!-- 返回按钮 -->
    <el-button class="back-btn" link type="primary" icon="ArrowLeft" @click="goBack">
      返回
    </el-button>

    <!-- 控制栏：搜索 + 新增 -->
    <div class="controls">
      <el-input
        v-model="searchKeyword"
        placeholder="搜索用户名"
        clearable
        @input="handleSearch"
      />
      <el-button type="primary" @click="openCreateDialog">➕ 新增用户</el-button>
    </div>

    <!-- 表格 -->
    <el-table :data="users" style="width: 100%" stripe border>
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="username" label="用户名" />
      <el-table-column prop="userprofile__email" label="邮箱" />
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

    <!-- 分页 -->
    <el-pagination
      layout="prev, pager, next, jumper, ->, total"
      :current-page="pagination.page"
      :page-size="pagination.pageSize"
      :total="pagination.total"
      @current-change="handlePageChange"
    />

    <!-- 弹窗表单 -->
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
          <el-input
            v-model="form.password"
            type="password"
            :placeholder="isEdit ? '如需修改请填写' : '请输入密码'"
          />
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
import { useRouter } from 'vue-router'

const router = useRouter()
const users = ref([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const editingUserId = ref(null)
const searchKeyword = ref('')
const pagination = ref({
  page: 1,
  pageSize: 5,
  total: 0,
})

const form = ref({
  username: '',
  email: '',
  password: '',
  role: 'user',
})

const goBack = () => {
  router.back()
}

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

const handlePageChange = (page) => {
  pagination.value.page = page
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
    email : user.userprofile__email || '',
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
.user-management-container {
  position: relative;
  max-width: 960px;
  margin: 2rem auto;
  background: #fff;
  padding: 2.5rem 2rem 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
}

/* 返回按钮（容器左上角） */
.back-btn {
  position: absolute;
  top: 16px;
  left: 16px;
  font-size: 14px;
  padding: 4px 8px;
  z-index: 10;
}

/* 控制区域：搜索框 + 新增按钮 */
.controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  margin-top: 1rem; /* 避开返回按钮 */
}

.controls .el-input {
  width: 240px;
}

/* 表格样式 */
.el-table {
  border-radius: 8px;
  overflow: hidden;
  font-size: 14px;
}

.el-table .el-button + .el-button {
  margin-left: 0.5rem;
}

/* 分页居中 */
.el-pagination {
  justify-content: center;
  margin-top: 1.5rem;
}
</style>
