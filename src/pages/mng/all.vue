<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { TableInstance } from 'element-plus'
import axios from '~/utils/axios'
import { useRouter } from 'vue-router'
const router = useRouter()

onMounted(() => {
  const token = localStorage.getItem('token')
  if (!token) {
    router.push('/login')
    return
  }
  fetchData()
})

// 添加项目数据类型接口
interface Project {
  //id: number;
  proj: string;
  company: string;
  order: string;
  assign: string;
  shot: string;
  perpay: number;
  count: number;
  inpay: number;
  outpay: number;
  allpay: number;
  inpayya: string;
  outpayya: string;
  inpayfor: string;
  outpayfor: string;
  note: string;
  tag: string;
  start: string;
  end: string | '';  // 修改这里，允许为 null
}

const tableData = ref<Project[]>([])
const multipleSelection = ref<Project[]>([])
const dialogVisible = ref(false)
const defaultFormData: Project = {
  //id: 0,
  proj: '',
  company: '',
  order: '',
  assign: '',
  shot: '',      // 初始化为数字
  perpay: 0,    // 初始化为数字
  count: 0,     // 初始化为数字
  inpay: 0,     // 初始化为数字
  outpay: 0,    // 初始化为数字
  allpay: 0,    // 初始化为数字
  inpayfor: '',
  outpayfor: '',
  note: '',
  tag: '未完成',
  inpayya: '未付款',
  outpayya: '未付款',
  start: new Date().toISOString().split('T')[0],
  end: null as unknown as string  // 修改这里，允许为 null
}

const formData = ref<Project>({ ...defaultFormData })

// 重置表单时使用
// 重命名函数以避免重复声明
const initFormData = () => {
  formData.value = { ...defaultFormData }
}

// 设置 axios 基础 URL
axios.defaults.baseURL = 'http://localhost:8000'

// 获取数据
const fetchData = async () => {
  try {
    const response = await axios.get('/api/projects/')
    // 对数据进行倒序排列
    tableData.value = response.data.reverse()
  } catch (error) {
    ElMessage.error('获取数据失败')
  }
}

// 添加数据
const handleApiError = (error: any, defaultMessage: string) => {
  const errorMessage = error.response?.data?.message || error.response?.data || defaultMessage
  console.error(`${defaultMessage}:`, errorMessage, error)
  ElMessage.error(errorMessage)
}

// 然后在各个函数中使用：
const addProject = async (project: Project) => {
  try {
    await axios.post('/api/projects/', project)
    await fetchData()
    ElMessage.success('添加成功')
  } catch (error: any) {
    handleApiError(error, '添加失败')
  }
}

// 更新数据
const updateProject = async (project: Project) => {
  try {
    await axios.put(`/api/projects/${(project as any).id}`, project)
    await fetchData()
    ElMessage.success('更新成功')
  } catch (error: any) {
    const errorMessage = error.response?.data?.message || error.response?.data || '更新失败'
    console.error('更新数据失败:', errorMessage, error)
    ElMessage.error(errorMessage)
  }
}

// 删除数据
const deleteProject = async (id: number) => {
  try {
    await axios.delete(`/api/projects/${id}/`)
    await fetchData()
    ElMessage.success('删除成功')
  } catch (error: any) {
    const errorMessage = error.response?.data?.message || error.response?.data || '删除失败'
    console.error('删除数据失败:', errorMessage, error)
    ElMessage.error(errorMessage)
  }
}

onMounted(() => {
  fetchData()
})

// 处理表格选择
const handleSelectionChange = (val: Project[]) => {
  multipleSelection.value = val
}

// 添加数据
// 删除这个重复的声明
// const handleAdd = () => {
//   dialogVisible.value = true
// }

// 保留这个新的声明
const handleAdd = () => {
  isEdit.value = false
  editingProject.value = null
  resetFormData()
  dialogVisible.value = true
}

// formData 的重置逻辑重复了两次，可以提取为一个函数
const resetFormData = () => {
  formData.value = { ...defaultFormData,
    //id: 0,
    proj: '',
    company: '',
    order: '',
    assign: '',
    shot: '',
    perpay: 0,
    count: 0,
    inpay: 0,
    inpayfor: '',
    outpay: 0,
    outpayfor: '',
    allpay: 0,
    note: '',
    tag: '未完成',
    inpayya: '未付款',
    outpayya: '未付款',
    start: new Date().toISOString().split('T')[0],
    end: ''
  }
}

// 添加编辑相关的状态
const isEdit = ref(false)
const editingProject = ref<Project | null>(null)

// 添加编辑按钮的处理函数
const handleEdit = (row: Project) => {
  isEdit.value = true
  editingProject.value = row
  formData.value = { ...row }
  dialogVisible.value = true
}

// 修改 submitForm 函数
const submitForm = async () => {
  try {
    if (isEdit.value) {
      // 使用类型断言来处理id属性
      await updateProject({ ...(formData.value as any), id: (editingProject.value as any).id })
    } else {
      await addProject(formData.value)
    }
    dialogVisible.value = false
    resetFormData()
    isEdit.value = false
    editingProject.value = null
  } catch (error) {
    // 错误已在相应函数中处理
  }
}


// 删除选中数据
const handleDelete = async () => {
  if (multipleSelection.value.length === 0) {
    ElMessage.warning('请选择要删除的数据')
    return
  }

  try {
    await ElMessageBox.confirm('确认删除选中的数据吗？', '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    for (const item of multipleSelection.value) {
      await deleteProject((item as any).id)
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}
const formatDateTime = (dateTime: string | null) => {
        return dateTime ? dateTime.replace('T', ' ').replace('Z', '') : ''
      }
// 在 script setup 中添加
import { watch } from 'vue'

// 监听单价和数量的变化，自动计算收入
watch([() => formData.value.perpay, () => formData.value.count], ([newPerpay, newCount]) => {
  formData.value.inpay = Number(newPerpay) * Number(newCount)
})

// 监听收入和支出的变化，自动计算总计（收入-支出）
watch([() => formData.value.inpay, () => formData.value.outpay], ([newInpay, newOutpay]) => {
  formData.value.allpay = Number(newInpay) - Number(newOutpay)
})
const currentPage = ref(1)
const pageSize = ref(10)

const handleSizeChange = (val: number) => {
  pageSize.value = val
  currentPage.value = 1
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
}
</script>

<template>
  <h1>展现所有数据，内容由新到旧</h1>
  <div class="container">
    <div class="button-group" mb="4">
      <el-button type="primary" @click="handleAdd">添加数据</el-button>
      <el-button type="danger" @click="handleDelete">删除数据</el-button>
    </div>
    <el-table
      :data="tableData.slice((currentPage - 1) * pageSize, currentPage * pageSize)"
      border
      style="width: 100%"
      @selection-change="handleSelectionChange"
    >
      <el-table-column type="selection" width="43" />
      <!-- <el-table-column prop="ID" label="ID"/> -->
      <el-table-column type="index" label="序号" width="60" />
      <el-table-column prop="start" label="下发时间" sortable width="150">
        <template #default="scope">
          {{ formatDateTime(scope.row.start) }}
        </template>
      </el-table-column>
      <el-table-column prop="proj" label="项目" width="100" />
      <el-table-column
      prop="tag"
      label="状态"
      width="80"
      :filters="[
        { text: '已完成', value: '已完成' },
        { text: '未完成', value: '未完成' },
      ]"
      :filter-method="(value, row) => row.tag === value"
      filter-placement="bottom-end"
      >
      <template #default="scope">
        <el-tag
          :type="scope.row.tag === '未完成' ? 'warning' : 'success'"
          disable-transitions
          >{{ scope.row.tag }}</el-tag
        >
      </template>
    </el-table-column>
    <el-table-column prop="company" label="委托公司" width="120" />
    <el-table-column prop="order" label="业务"/>
    <el-table-column prop="assign" label="负责人"/>
    <el-table-column prop="shot" label="镜头" width="60" />
    <el-table-column prop="perpay" label="单价"/>
    <el-table-column prop="count" label="数量" width="60" />
    <el-table-column prop="inpay" label="收入"/>
    <el-table-column prop="inpayya" label="甲方付款状态" width="90">
      <template #default="scope">
        <el-tag
          :type="scope.row.inpayya === '已支付' ? 'success' : 'warning'"
          disable-transitions
        >{{ scope.row.inpayya }}</el-tag>
      </template>
    </el-table-column>
    <el-table-column prop="inpayfor" label="入账方式" width="90" />
    <el-table-column prop="outpay" label="支出" width="60" />
    <el-table-column prop="outpayya" label="外包工资状态" width="90">
      <template #default="scope">
        <el-tag
          :type="scope.row.outpayya === '已支付' ? 'success' : 'warning'"
          disable-transitions
        >{{ scope.row.outpayya }}</el-tag>
      </template>
    </el-table-column>
    <el-table-column prop="outpayfor" label="出账方式" width="90" />
    <el-table-column prop="allpay" label="总计" width="60" />
    <el-table-column prop="end" label="收稿时间" width="150">
      <template #default="scope">
        {{ scope.row.end ? scope.row.end.replace('T', ' ').replace('Z', '') : '' }}
      </template>
    </el-table-column>
    <el-table-column prop="note" label="备注" width="200" />
    <el-table-column label="操作" width="80" fixed="right">
      <template #default="scope">
        <el-button
          size="small"
          type="primary"
          @click="handleEdit(scope.row)"
        >
          编辑
        </el-button>
      </template>
    </el-table-column>
    </el-table>

    <!-- 在表格下方添加分页器 -->
    <div class="pagination-container" style="margin-top: 20px;">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 30, 50]"
        :total="tableData.length"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>

    <!-- 添加数据的对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑数据' : '添加数据'"
      width="50%"
    >
      <el-form :model="formData" label-width="120px">
        <el-form-item label="下发时间">
          <el-date-picker
            v-model="formData.start"
            type="datetime"
            placeholder="选择下发时间"
            format="YYYY-MM-DD HH:mm:ss"
            value-format="YYYY-MM-DD HH:mm:ss"
          />
        </el-form-item>
        <el-form-item label="项目">
          <el-input v-model="formData.proj" />
        </el-form-item>
        <el-form-item label="委托公司">
          <el-input v-model="formData.company" />
        </el-form-item>
        <el-form-item label="业务">
          <el-input v-model="formData.order" />
        </el-form-item>
        <el-form-item label="负责人">
          <el-input v-model="formData.assign" />
        </el-form-item>
        <el-form-item label="镜头">
          <el-input
            v-model="formData.shot" />
        </el-form-item>
        <el-form-item label="数量">
          <el-input
            v-model="formData.count"
            type="number"
            :min="0"
            @input="(val: string) => formData.count = Number(val.replace(/[^\d]/g, ''))"
          />
        </el-form-item>
        <el-form-item label="单价">
          <el-input v-model="formData.perpay" />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="formData.tag" placeholder="请选择状态">
            <el-option label="已完成" value="已完成" />
            <el-option label="未完成" value="未完成" />
          </el-select>
        </el-form-item>
        <el-form-item label="收入">
          <el-input v-model="formData.inpay" />
        </el-form-item>
        <el-form-item label="甲方付款状态">
          <el-select v-model="formData.inpayya" placeholder="请选择付款状态">
          <el-option label="已支付" value="已支付" />
          <el-option label="未支付" value="未支付" />
          </el-select>
        </el-form-item>
        <el-form-item label="入账方式">
          <el-input v-model="formData.inpayfor" />
        </el-form-item>
        <el-form-item label="支出">
          <el-input v-model="formData.outpay" />
        </el-form-item>
        <el-form-item label="工资状态">
          <el-select v-model="formData.outpayya" placeholder="请选择外包支付状态">
            <el-option label="已支付" value="已支付" />
            <el-option label="未支付" value="未支付" />
          </el-select>
        </el-form-item>
        <el-form-item label="出账方式">
          <el-input v-model="formData.outpayfor" />
        </el-form-item>
        <el-form-item label="总计">
          <el-input v-model="formData.allpay" />
        </el-form-item>
        <el-form-item label="收稿时间">
          <el-date-picker
            v-model="formData.end"
            type="datetime"
            clearable
            placeholder="选择收稿时间"
            format="YYYY-MM-DD HH:mm:ss"
            value-format="YYYY-MM-DD HH:mm:ss"
          />
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="formData.note" type="textarea" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.container {
  padding: 9px;
  text-align: left;
}

.button-group {
  display: flex;
  gap: 10px;
}
</style>
