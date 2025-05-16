<template>
  <AppPage :show-footer="false">
    <div flex-1>
      <n-card rounded-10>
         <NForm
        ref="modalFormRef"
        label-placement="left"
        label-align="left"
        :label-width="80"
        :model="modalForm"
      >

        <NFormItem
          label="文件路径"
          path="filePath"
          :rule="{
            required: true,
            message: '请输入视频文件保存路径',
            trigger: ['blur'],
          }"
        >
          <NInput v-model="modalForm.filePath"  placeholder="请输入视频文件保存路径"/>
        </NFormItem>
         <NButton v-permission="'post/api/v1/task/create'" type="primary" @click="handleClickSave">
          <TheIcon icon="material-symbols:add" :size="18" class="mr-5" />保存
        </NButton>
      </NForm>
      </n-card>

    </div>
  </AppPage>
</template>

<script setup>
import { useUserStore } from '@/store'
import { useI18n } from 'vue-i18n'
import {onMounted} from "vue";
import {NButton} from "naive-ui";
import TheIcon from "@/components/icon/TheIcon.vue";
import api from "@/api";

const dummyText = '一个基于 Vue3.0、FastAPI、Naive UI 的轻量级后台管理模板'
const { t } = useI18n({ useScope: 'global' })

const statisticData = computed(() => [
  {
    id: 0,
    label: t('views.workbench.label_number_of_items'),
    value: '25',
  },
  {
    id: 1,
    label: t('views.workbench.label_upcoming'),
    value: '4/16',
  },
  {
    id: 2,
    label: t('views.workbench.label_information'),
    value: '12',
  },
])
const modalForm = ref({
  id: 1,
  filePath: '',
})

function loadSettings() {
  const sysConf = api.getSysConf()
  modalForm.value = sysConf
}

function handleClickSave() {
  const form = modalForm.value
  form.id = 1
  form.filePath = '../video/'

  console.log(11111)
  api.updateSysConf(form).then(() => {
    $message.success('保存成功')
  })
}

onMounted(() => {
  loadSettings()
})



const userStore = useUserStore()
</script>
