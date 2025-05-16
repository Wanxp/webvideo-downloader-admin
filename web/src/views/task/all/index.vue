<script setup>
import { h, onMounted, ref, resolveDirective, withDirectives } from 'vue'
import {
  NButton,
  NForm,
  NFormItem,
  NInput,
  NInputNumber,
  NPopconfirm,
  NSwitch,
  NTreeSelect,
  NRadio,
  NRadioGroup,
  NTag,
} from 'naive-ui'

import CommonPage from '@/components/page/CommonPage.vue'
import CrudModal from '@/components/table/CrudModal.vue'
import CrudTable from '@/components/table/CrudTable.vue'
import IconPicker from '@/components/icon/IconPicker.vue'
import TheIcon from '@/components/icon/TheIcon.vue'

import { formatDate, renderIcon } from '@/utils'
import { useCRUD } from '@/composables'
import api from '@/api'
import {toMB, toMBSpeed} from "@/utils/common/netUtil";

defineOptions({ name: '下载管理' })

const $table = ref(null)
const queryItems = ref({})
const vPermission = resolveDirective('permission')
const timeout = ref(2000)
const errorTimes = ref(2)

// 表单初始化内容
const initForm = {
  linksurl: '',
  fileName: '',
}

const {
  modalVisible,
  modalTitle,
  modalLoading,
  handleAdd,
  handleDelete,
  handleEdit,
  handleSave,
  modalForm,
  modalFormRef,
} = useCRUD({
  name: '下载',
  initForm,
  doCreate: api.createTask,
  doDelete: api.deleteTask,
  doUpdate: api.updateTask,
  refresh: () => $table.value?.handleSearch(),
})

onMounted(() => {
  $table.value?.handleSearch()
  getTreeSelect()
  //每秒刷新一次
  setInterval(() => {
    $table.value?.handleSearch()
  }, timeout.value)
})

// 是否展示 "平台类型"
const showPlatformType = ref(false)
const taskOptions = ref([])

const columns = [
  { title: 'ID', key: 'id', width: 20, ellipsis: { tooltip: true }, align: 'center',hide: true },
  { title: '名称', key: 'fileName', width: 100, ellipsis: { tooltip: true }, align: 'center' },
  {
    title: '平台',
    key: 'platform',
    width: 40,
    align: 'center',
    ellipsis: { tooltip: true },
    render(row) {
      let round = false
      let bordered = false
      return h(
        NTag,
        { type: 'primary', round: round, bordered: bordered },
        { default: () => {
            const platform = row.platform
            return platform
          }}
      )
    },
  },
  { title: '分P', key: 'pRange', width: 30, ellipsis: { tooltip: true }, align: 'center' },
  { title: '画质', key: 'quality', width: 40, ellipsis: { tooltip: true }, align: 'center' },
  { title: '大小', key: 'totalSize', width: 40, ellipsis: { tooltip: true }, align: 'center',
  render(row) {
    return toMB(row.totalSize)
  }},
  { title: '速度', key: 'speed', width: 40, ellipsis: { tooltip: true }, align: 'center',render(row) {
    const currentTime = new Date().getTime();
    const updatedTime = new Date(row.updated_at).getTime();
    if (currentTime - updatedTime > errorTimes.value * timeout.value) {
      return '0 MB/s';
    }
    return toMBSpeed(row.speed);    }
  },
  { title: '进度', key: 'rate', width: 40, ellipsis: { tooltip: true }, align: 'center',
  render(row) {
    return row.rate >= 0.99 ? '100%' : (row.rate * 100).toFixed(2) + '%' ;
  }},
  {
    title: '状态',
    key: 'status',
    width: 40,
    align: 'center',
    render(row) {
      const currentTime = new Date().getTime();
      const updatedTime = new Date(row.updated_at).getTime();
      let type = 'primary'
      let statusName = ''
      if (row.rate > 0.9999) {
        type = 'success'
        statusName = '下载完成'
      }else if (currentTime - updatedTime > errorTimes.value * timeout.value) {
          type = 'error'
          statusName = '异常'
      }else {
        const status = row.status
        switch (status) {
          case 10:
            type = 'info'
            statusName = '等待下载'
            break
          case 20:
            type = 'success'
            statusName = '下载中'
            break
          case 30:
            type = 'warning'
            statusName = '合并中'
            break
          case 40:
            type = 'success'
            statusName = '下载完成'
            break
          case 99:
            type = 'error'
            statusName = '停止'
            break
          case 199:
            type = 'error'
            statusName = '暂停'
            break
          default:
            statusName = ''
            break
        }
      }
      let round = false
      let bordered = false
      return h(
        NTag,
        { type: type, round: round, bordered: bordered },
        { default: () => {
           return statusName

          }}
      )
    },
  },
  // { title: '排序', key: 'order', width: 80, ellipsis: { tooltip: true }, align: 'center' },
  { title: '本地路径', key: 'filePath', width: 80, ellipsis: { tooltip: true }, align: 'center' },
  // { title: '下载URL', key: 'url', width: 80, ellipsis: { tooltip: true }, align: 'center', hide: true },
  {
    title: '操作',
    key: 'actions',
    width: 120,
    align: 'center',
    fixed: 'right',
    render(row) {
      return [
        withDirectives(
        h(
              NPopconfirm,
          {
            onPositiveClick: () => handleRedownload({ id: row.id }),
          },
          {
            trigger: () =>
              withDirectives(
                h(
                  NButton,
                  {
                    size: 'tiny',
                    quaternary: true,
                    type: 'info',
                    style: `display: ${row.children && row.children.length > 0 ? 'none' : ''};`, //有子菜单不允许删除
                  },
                  {
                    default: () => '重新下载',
                    icon: renderIcon('material-symbols:replay', { size: 16 }),
                  }
                ),
                [[vPermission, 'delete/api/v1/task/activate/redownload']]
              ),
            default: () => h('div', {}, '确定重新下载该任务吗?'),
          }
        ),
          [[vPermission, 'post/api/v1/task/create']]
        ),
        withDirectives(
          h(
              NPopconfirm,
          {
            onPositiveClick: () => handleRedownload({ id: row.id }),
          },
          {
            trigger: () =>
              withDirectives(
                h(
                  NButton,
                  {
                    size: 'tiny',
                    quaternary: true,
                    type: 'info',
                    style: `display: ${row.children && row.children.length > 0 ? 'none' : ''};`, //有子菜单不允许删除
                  },
                  {
                    default: () => '停止',
                    icon: renderIcon('material-symbols:stop', { size: 16 }),
                  }
                ),
                [[vPermission, 'delete/api/v1/task/stop']]
              ),
            default: () => h('div', {}, '确定停止该任务吗?停止后将无法继续下载,需要重新下载!'),
          }
        ),
          [[vPermission, 'post/api/v1/task/update']]
        ),
        h(
          NPopconfirm,
          {
            onPositiveClick: () => handleDelete({ id: row.id }, false),
          },
          {
            trigger: () =>
              withDirectives(
                h(
                  NButton,
                  {
                    size: 'tiny',
                    quaternary: true,
                    type: 'error',
                  },
                  {
                    default: () => '删除',
                    icon: renderIcon('material-symbols:delete-outline', { size: 16 }),
                  }
                ),
                [[vPermission, 'delete/api/v1/task/delete']]
              ),
            default: () => h('div', {}, '确定删除该任务吗?'),
          }
        ),
      ]
    },
  },
]
// 修改是否keepalive
async function handleStart(row) {
  if (!row.id) return
  row.publishing = true
  row.keepalive = row.keepalive === false ? true : false
  await api.updateMenu(row)
  row.publishing = false
  $message?.success(row.keepalive ? '已开启' : '已关闭')
}

// 修改是否隐藏
async function handleRedownload(params) {
    try {
      modalLoading.value = true
      const data = await api.activateRedownload(params)
      $message.success('开始成功')
      modalLoading.value = false
      refresh(data)
    } catch (error) {
      modalLoading.value = false
    }
}





// 新增菜单(可选目录)
async function handleClickAdd() {
    initForm.parent_id = 0
  initForm.platform_type = 'bili'
  initForm.order = new Date().getTime() * 1000
  showPlatformType.value = true
  handleAdd()
}



async function getTreeSelect() {
  const { data } = await api.getTaskList()
  const task = { id: 0, name: '根目录', children: [] }
  task.children = data
  taskOptions.value = [task]
}

</script>

<template>
  <!-- 业务页面 -->
  <CommonPage show-footer title="下载列表">
    <template #action>
      <NButton v-permission="'post/api/v1/task/create'" type="primary" @click="handleClickAdd">
        <TheIcon icon="material-symbols:add" :size="18" class="mr-5" />新建下载
      </NButton>
    </template>


    <!-- 表格 -->
    <CrudTable
      ref="$table"
      v-model:query-items="queryItems"
      :is-pagination="false"
      :columns="columns"
      :get-data="api.getTaskList"
      :single-line="true"
      :show-loading-when-query="false"
    >
    </CrudTable>



    <!-- 新增/编辑/查看 弹窗 -->
    <CrudModal
      v-model:visible="modalVisible"
      :title="modalTitle"
      :loading="modalLoading"
      @save="handleSave"
    >
      <!-- 表单 -->
      <NForm
        ref="modalFormRef"
        label-placement="left"
        label-align="left"
        :label-width="80"
        :model="modalForm"
      >
        <NFormItem
          label="视频地址"
          path="linksurl"
          :rule="{
            required: true,
            message: '请输入视频油猴或暴力猴链接或本地m3u8路径',
            trigger: ['blur'],
          }"
        >
          <NInput v-model="modalForm.linksurl"  placeholder="请输入视频油猴或暴力猴链接或本地m3u8路径"/>
        </NFormItem>
        <NFormItem
          label="文件名"
          path="fileName"
          :rule="{
            required: true,
            message: '请输入文件名',
            trigger: ['blur'],
          }"
        >
          <NInput v-model="modalForm.fileName"  placeholder="请输入文件名"/>
        </NFormItem>
      </NForm>
    </CrudModal>
  </CommonPage>
</template>
