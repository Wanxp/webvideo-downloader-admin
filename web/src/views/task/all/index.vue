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

defineOptions({ name: '下载管理' })

const $table = ref(null)
const queryItems = ref({})
const vPermission = resolveDirective('permission')

// 表单初始化内容
const initForm = {
  order: 1,
  keepalive: true,
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
  doCreate: api.createMenu,
  doDelete: api.deleteMenu,
  doUpdate: api.updateMenu,
  refresh: () => $table.value?.handleSearch(),
})

onMounted(() => {
  $table.value?.handleSearch()
  getTreeSelect()
})

// 是否展示 "菜单类型"
const showMenuType = ref(false)
const menuOptions = ref([])

const columns = [
  { title: 'ID', key: 'id', width: 50, ellipsis: { tooltip: true }, align: 'center' },
  { title: '名称', key: 'fileName', width: 80, ellipsis: { tooltip: true }, align: 'center' },
  {
    title: '平台',
    key: 'platform_type',
    width: 80,
    align: 'center',
    ellipsis: { tooltip: true },
    render(row) {
      let round = false
      let bordered = false
      if (row.menu_type === 'catalog') {
        bordered = true
        round = false
      } else if (row.menu_type === 'menu') {
        bordered = false
        round = true
      }
      return h(
        NTag,
        { type: 'primary', round: round, bordered: bordered },
        { default: () => (row.menu_type === 'catalog' ? '目录' : '菜单') }
      )
    },
  },
  { title: '画质', key: 'quality', width: 80, ellipsis: { tooltip: true }, align: 'center' },
  { title: '大小', key: 'totalSize', width: 80, ellipsis: { tooltip: true }, align: 'center' },
  { title: '速度', key: 'speed', width: 80, ellipsis: { tooltip: true }, align: 'center' },
  { title: '进度', key: 'rate', width: 80, ellipsis: { tooltip: true }, align: 'center' },
  {
    title: '状态',
    key: 'status',
    width: 40,
    align: 'center',
    render(row) {
      return h(TheIcon, { icon: row.icon, size: 20 })
    },
  },
  { title: '排序', key: 'order', width: 40, ellipsis: { tooltip: true }, align: 'center' },
  { title: '本地路径', key: 'path', width: 80, ellipsis: { tooltip: true }, align: 'center' },
  { title: '下载URL', key: 'url', width: 80, ellipsis: { tooltip: true }, align: 'center' },
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
            NButton,
            {
              size: 'tiny',
              quaternary: true,
              type: 'primary',
              style: `display: ${row.children && row.menu_type !== 'menu' ? '' : 'none'};`,
              onClick: () => {
                initForm.parent_id = row.id
                initForm.menu_type = 'menu'
                showMenuType.value = false
                handleStart()
              },
            },
            { default: () => '子菜单', icon: renderIcon('material-symbols:add', { size: 16 }) }
          ),
          [[vPermission, 'post/api/v1/menu/create']]
        ),
        withDirectives(
          h(
            NButton,
            {
              size: 'tiny',
              quaternary: true,
              type: 'info',
              onClick: () => {
                showMenuType.value = false
                handleStop(row)
              },
            },
            {
              default: () => '编辑',
              icon: renderIcon('material-symbols:edit-outline', { size: 16 }),
            }
          ),
          [[vPermission, 'post/api/v1/menu/update']]
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
                    style: `display: ${row.children && row.children.length > 0 ? 'none' : ''};`, //有子菜单不允许删除
                  },
                  {
                    default: () => '删除',
                    icon: renderIcon('material-symbols:delete-outline', { size: 16 }),
                  }
                ),
                [[vPermission, 'delete/api/v1/menu/delete']]
              ),
            default: () => h('div', {}, '确定删除该菜单吗?'),
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
async function handleStop(row) {
  if (!row.id) return
  row.publishing = true
  row.is_hidden = row.is_hidden === false ? true : false
  await api.updateMenu(row)
  row.publishing = false
  $message?.success(row.is_hidden ? '已隐藏' : '已取消隐藏')
}


async function getTreeSelect() {
  const { data } = await api.getMenus()
  const menu = { id: 0, name: '根目录', children: [] }
  menu.children = data
  menuOptions.value = [menu]
}
</script>

<template>
  <!-- 业务页面 -->
  <CommonPage show-footer title="下载列表">
    <!-- 表格 -->
    <CrudTable
      ref="$table"
      v-model:query-items="queryItems"
      :is-pagination="false"
      :columns="columns"
      :get-data="api.getTaskList"
      :single-line="true"
    >
    </CrudTable>

    <!-- 新增/编辑/查看 弹窗 -->
    <CrudModal
      v-model:visible="modalVisible"
      :title="modalTitle"
      :loading="modalLoading"
      @save="handleSave(getTreeSelect)"
    >
      <!-- 表单 -->
      <NForm
        ref="modalFormRef"
        label-placement="left"
        label-align="left"
        :label-width="80"
        :model="modalForm"
      >

        <NFormItem label="" path="platform_type">
          <NRadioGroup v-model:value="modalForm.menu_type">
            <NRadio label="哔哩" value="bili" />
            <NRadio label="爱奇艺" value="iqiyi" />
            <NRadio label="腾讯" value="vqq" />
            <NRadio label="芒果" value="mgtv" />
            <NRadio label="WeTV" value="wetv" />
            <NRadio label="爱奇艺(国际)" value="iq" />
          </NRadioGroup>
        </NFormItem>
        <NFormItem label="上级菜单" path="parent_id">
          <NTreeSelect
            v-model:value="modalForm.parent_id"
            key-field="id"
            label-field="name"
            :options="menuOptions"
            default-expand-all="true"
          />
        </NFormItem>
        <NFormItem
          label="名称"
          path="fileName"
          :rule="{
            required: true,
            message: '请输入唯一名称',
            trigger: ['input', 'blur'],
          }"
        >
          <NInput v-model:value="modalForm.fileName" placeholder="请输入唯一菜单名称" />
        </NFormItem>
        <NFormItem
          label="画质"
          path="quality"
          :rule="{
            required: true,
            message: '请输入画质',
            trigger: ['blur'],
          }">
          <NInput v-model:value="modalForm.quality" placeholder="请输入画质" />
        </NFormItem>
      </NForm>
    </CrudModal>
  </CommonPage>
</template>
