<template>
  <div class="user-management-container">
    <!-- 返回按钮 -->
    <el-button class="back-btn" link type="primary" icon="ArrowLeft" @click="goBack">
      返回
    </el-button>

    <!-- 控制栏：搜索 + 新增用户 -->
    <div class="controls">
      <!-- 搜索框 -->
      <el-input
        v-model="searchKeyword"
        placeholder="搜索用户名"
        clearable
        @input="handleSearch"
      />
      <!-- 新增用户按钮 -->
      <el-button type="primary" @click="openCreateDialog">➕ 新增用户</el-button>
    </div>

    <!-- 用户表格 -->
    <el-table :data="users" style="width: 100%" stripe border>
      <!-- 用户ID -->
      <el-table-column prop="id" label="ID" width="60" />
      <!-- 用户名 -->
      <el-table-column prop="username" label="用户名" />
      <!-- 用户邮箱 -->
      <el-table-column prop="userprofile__email" label="邮箱" />
      <!-- 用户角色 -->
      <el-table-column prop="userprofile__role" label="角色" />
      <!-- 操作列：编辑 + 删除 -->
      <el-table-column label="操作" width="180">
        <template #default="{ row }">
          <!-- 编辑按钮 -->
          <el-button size="small" @click="openEditDialog(row)">编辑</el-button>
          <!-- 删除按钮 -->
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
        <!-- 用户名 -->
        <el-form-item label="用户名">
          <el-input v-model="form.username" />
        </el-form-item>
        <!-- 邮箱 -->
        <el-form-item label="邮箱">
          <el-input v-model="form.email" />
        </el-form-item>
        <!-- 角色选择 -->
        <el-form-item label="角色">
          <el-select v-model="form.role" placeholder="请选择角色">
            <el-option label="普通用户" value="user" />
            <el-option label="管理员" value="admin" />
          </el-select>
        </el-form-item>
        <!-- 密码 -->
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
// 引入所需模块
import { ref, onMounted } from 'vue'
import axios from '@/services/axios'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'

const router = useRouter()
const users = ref([])  // 用户列表
const dialogVisible = ref(false)  // 弹窗显示状态
const isEdit = ref(false)  // 是否为编辑模式
const editingUserId = ref(null)  // 编辑用户的ID
const searchKeyword = ref('')  // 搜索关键词
const pagination = ref({
  page: 1,  // 当前页
  pageSize: 5,  // 每页显示的记录数
  total: 0,  // 总记录数
})

const form = ref({
  username: '',
  email: '',
  password: '',
  role: 'user',
})

// 返回上一页
const goBack = () => {
  router.back()
}

// 获取用户列表
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

// 搜索处理
const handleSearch = () => {
  pagination.value.page = 1
  fetchUsers()
}

// 分页变化处理
const handlePageChange = (page) => {
  pagination.value.page = page
  fetchUsers()
}

// 打开新增用户弹窗
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

// 打开编辑用户弹窗
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

// 提交表单：新增或编辑用户
const handleSubmit = async () => {
  if (!form.value.username || (!isEdit.value && !form.value.password)) {
    ElMessage.error('用户名和密码不能为空')
    return
  }

  try {
    if (isEdit.value) {
      // 更新用户信息
      await axios.put(`http://localhost:8000/api/users/${editingUserId.value}/`, form.value)
      ElMessage.success('更新成功')
    } else {
      // 创建新用户
      await axios.post('http://localhost:8000/api/users/', form.value)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    fetchUsers()
  } catch (err) {
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

// 页面加载时获取用户列表
onMounted(fetchUsers)
</script>

<style scoped>
/* 容器样式 */
.user-management-container {
  position: relative;
  max-width: 960px;
  margin: 2rem auto;
  background: #fff;
  padding: 2.5rem 2rem 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
}

/* 返回按钮样式 */
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
