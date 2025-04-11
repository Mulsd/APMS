<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import { watch } from 'vue'
import { ElMessage } from 'element-plus'
import type { UploadProps, UploadUserFile } from 'element-plus'
import axios from '~/utils/axios'
import { useRouter } from 'vue-router'
import { UploadFilled } from '@element-plus/icons-vue'
const router = useRouter()

onMounted(() => {
  const token = localStorage.getItem('token')
  if (!token) {
    router.push('/login')
    return
  }
  //fetchData()
})

// 复用Project接口
interface Project {
  proj: string
  company: string
  order: string
  assign: string
  shot: string
  perpay: number
  count: number
  inpay: number
  outpay: number
  allpay: number
  inpayya: string
  outpayya: string
  inpayfor: string
  outpayfor: string
  note: string
  tag: string
  start: string
  end: string | undefined;  // 修改这里，使用 undefined 代替 null
}

// 上传文件列表
const fileList = ref<UploadUserFile[]>([])
// 表单数据
const formData = ref<Project>({
  proj: '',
  company: '',
  order: '',
  assign: '',
  shot: '',
  perpay: 0,
  count: 0,
  inpay: 0,
  outpay: 0,
  allpay: 0,
  inpayfor: '',
  outpayfor: '',
  note: '',
  tag: '未完成',
  inpayya: '未付款',
  outpayya: '未付款',
  start: new Date().toISOString().split('T')[0],
  end: undefined,  // 修改这里，使用 undefined 代替 null
})

// 设置axios基础URL
axios.defaults.baseURL = 'http://localhost:8000'

// 处理文件上传
const handleUpload: UploadProps['onChange'] = (uploadFile) => {
  fileList.value.push(uploadFile)
  // 从文件名中提取信息
  const fileName = uploadFile.name
  // 这里可以添加文件名解析逻辑，将提取的信息填充到formData中
  parseFileName(fileName)
}

// 解析文件名
const parseFileName = (fileName: string) => {
  // 示例：假设文件名格式为 "项目名_公司名_业务类型.xxx"
  const parts = fileName.split('_')
  if (parts.length >= 3) {
    formData.value.proj = parts[0]
    formData.value.company = parts[1]
    formData.value.order = parts[2].split('.')[0]
  }
}

// 提交表单
const submitForm = async () => {
  try {
    await axios.post('/api/projects/', formData.value)
    ElMessage.success('添加成功')
    // 只重置表单数据，保留文件列表
    resetFormOnly()
  } catch (error: any) {
    const errorMessage = error.response?.data?.message || error.response?.data || '添加失败'
    console.error('添加失败:', errorMessage)
    ElMessage.error(errorMessage)
  }
}

// 只重置表单数据
const resetFormOnly = () => {
  formData.value = {
    proj: '',
    company: '',
    order: '',
    assign: '',
    shot: '',
    perpay: 0,
    count: 0,
    inpay: 0,
    outpay: 0,
    allpay: 0,
    inpayfor: '',
    outpayfor: '',
    note: '',
    tag: '未完成',
    inpayya: '未付款',
    outpayya: '未付款',
    start: new Date().toISOString().split('T')[0],
    end: undefined,
  }
}

// 完全重置（表单数据和文件列表）
const resetForm = () => {
  resetFormOnly()
  fileList.value = []
}

// 移除文件
const handleRemove = (uploadFile: UploadUserFile) => {
  const index = fileList.value.indexOf(uploadFile)
  if (index !== -1) {
    fileList.value.splice(index, 1)
  }
}

// 添加处理表格行点击的函数
const handleRowClick = (row: UploadUserFile) => {
  parseFileName(row.name)
  ElMessage.success('已加载文件信息')
}


// 监听单价和数量的变化，自动计算收入
watch([() => formData.value.perpay, () => formData.value.count], ([newPerpay, newCount]) => {
  formData.value.inpay = Number(newPerpay) * Number(newCount)
})

// 监听收入和支出的变化，自动计算总计（收入-支出）
watch([() => formData.value.inpay, () => formData.value.outpay], ([newInpay, newOutpay]) => {
  formData.value.allpay = Number(newInpay) - Number(newOutpay)
})
</script>

<template>
  <div class="container">
    <el-upload
      class="upload-demo"
      drag
      action="#"
      :auto-upload="false"
      :on-change="handleUpload"
      :on-remove="handleRemove"
      multiple
    >
      <el-icon class="el-icon--upload"><upload-filled /></el-icon>
      <div class="el-upload__text">
        将文件拖到此处，或<em>点击上传</em>
      </div>
    </el-upload>

    <!-- 文件列表预览 -->
    <div class="file-list" v-if="fileList.length > 0">
      <h3>已选择的文件：</h3>
      <el-table :data="fileList" style="width: 100%"
        @row-click="handleRowClick"
        :row-style="{ cursor: 'pointer' }"
      >
        <el-table-column prop="name" label="文件名" />
        <el-table-column prop="size" label="大小" width="180">
          <template #default="{ row }">
            {{ (row.size / 1024).toFixed(2) }} KB
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 表单部分 -->
    <el-form :model="formData" label-width="120px" class="form-container">
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
        <el-input v-model="formData.shot" />
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

      <el-form-item>
        <el-button type="primary" @click="submitForm">提交</el-button>
        <el-button @click="resetForm">重置</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<style scoped>
.container {
  padding: 20px;
}

.upload-demo {
  margin-bottom: 20px;
}

.file-list {
  margin: 20px 0;
}

.form-container {
  max-width: 800px;
  margin: 0 auto;
}
</style>