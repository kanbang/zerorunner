<template>
  <div class="app-container">
    <el-card>
      <template #header v-if="!isView">
        <z-detail-page-header
            class="page-header"
            style="margin: 5px 0;"
            @back="goBack"
        >
          <template #content>
            <span style="padding-right: 10px;">{{ route.query.editType === 'update' ? "更新" : "新增" }}</span>
          </template>
        </z-detail-page-header>
      </template>
      <div class="h100">
        <ApiInfo ref="ApiInfoRef" @saveOrUpdateOrDebug="saveOrUpdateOrDebug"/>

        <el-collapse-transition>
          <div v-show="state.showRequestBody">
            <el-card>
              <template #header>
                <strong>Request</strong>
              </template>
              <div style="min-height: 500px">
                <el-tabs v-model="state.activeName" style="overflow-y: auto">
                  <el-tab-pane name='ApiRequestBody'>
                    <template #label>
                      <strong>请求体</strong>
                    </template>
                    <div class="case-tabs">
                      <ApiRequestBody ref="ApiRequestBodyRef" @updateHeader="updateHeader"/>
                    </div>
                  </el-tab-pane>

                  <el-tab-pane name='ApiRequestHeaders'>
                    <template #label>
                      <el-badge :hidden="!getDataLength('header')"
                                :value="getDataLength('header')"
                                class="badge-item"
                                type="primary">
                        <strong>请求头</strong>
                      </el-badge>
                    </template>
                    <div class="case-tabs">
                      <ApiRequestHeaders ref="ApiRequestHeadersRef"/>
                    </div>
                  </el-tab-pane>

                  <el-tab-pane name='ApiVariables'>
                    <template #label>
                      <el-badge :hidden="!getDataLength('variables')"
                                :value="getDataLength('variables')"
                                class="badge-item"
                                type="primary">
                        <strong>变量</strong>
                      </el-badge>
                    </template>
                    <div class="case-tabs">
                      <ApiVariables ref="ApiVariablesRef"/>
                    </div>
                  </el-tab-pane>

                  <el-tab-pane name='extracts' class="h100">
                    <template #label>
                      <el-badge :hidden="!getDataLength('extracts')"
                                :value="getDataLength('extracts')"
                                class="badge-item" type="primary">
                        <strong>提取</strong>
                      </el-badge>
                    </template>
                    <div class="case-tabs">
                      <ApiExtracts ref="ApiExtractsRef"/>
                    </div>
                  </el-tab-pane>

                  <el-tab-pane name='Code' class="h100">
                    <template #label>
                      <!--                      <el-badge :hidden="!getDataLength('hook')"-->
                      <!--                                :value="getDataLength('hook')"-->
                      <!--                                class="badge-item"-->
                      <!--                                type="primary">-->
                      <strong>Code</strong>
                      <!--                      </el-badge>-->
                    </template>
                    <ApiCode ref="ApiCodeRef"/>
                  </el-tab-pane>

                  <el-tab-pane name='Hook' class="h100">
                    <template #label>
                      <el-badge :hidden="!getDataLength('hook')"
                                :value="getDataLength('hook')"
                                class="badge-item"
                                type="primary">
                        <strong>Hook</strong>
                      </el-badge>
                    </template>
                    <ApiHooks ref="ApiHookRef"/>
                  </el-tab-pane>

                  <!--                  <el-tab-pane name='preOperation' class="h100">-->
                  <!--                    <template #label>-->
                  <!--                      <el-badge :hidden="!getDataLength('pre')"-->
                  <!--                                :value="getDataLength('pre')"-->
                  <!--                                class="badge-item"-->
                  <!--                                type="primary">-->
                  <!--                        <strong>前置操作</strong>-->
                  <!--                      </el-badge>-->
                  <!--                    </template>-->
                  <!--                    <div class="case-tabs">-->
                  <!--                      <ApiPreSteps ref="ApiPreStepsRef"/>-->
                  <!--                    </div>-->
                  <!--                  </el-tab-pane>-->

                  <!--                  <el-tab-pane name='postOperation' class="h100">-->
                  <!--                    <template #label>-->
                  <!--                      <el-badge :hidden="!getDataLength('post')"-->
                  <!--                                :value="getDataLength('post')"-->
                  <!--                                class="badge-item"-->
                  <!--                                type="primary">-->
                  <!--                        <strong>后置操作</strong>-->
                  <!--                      </el-badge>-->
                  <!--                    </template>-->
                  <!--                    <div class="case-tabs">-->
                  <!--                      <ApiPostSteps ref="ApiPostStepsRef"/>-->
                  <!--                    </div>-->
                  <!--                  </el-tab-pane>-->


                  <el-tab-pane name='assertController' class="h100">
                    <template #label>
                      <el-badge :hidden="!getDataLength('validators')"
                                :value="getDataLength('validators')"
                                class="badge-item"
                                type="primary">
                        <strong>断言规则</strong>
                      </el-badge>
                    </template>
                    <div class="case-tabs">
                      <ApiValidators ref="ApiValidatorsRef"/>
                    </div>
                  </el-tab-pane>

                </el-tabs>
              </div>
            </el-card>
          </div>
        </el-collapse-transition>


        <el-card id="Response" ref="ResponseRef" v-show="state.reportData" style="margin-top: 20px">
          <template #header>
            <div style="display: flex; justify-content: space-between">
              <div>
                <strong>Response</strong>
              </div>
              <div style="font-size: 12px" v-if="state.apiReportStat">
            <span style="vertical-align: middle;">
              <el-icon>
                <ele-CircleCheck v-if="state.apiReportStat.success" style="color: #0cbb52"/>
                <ele-CircleClose v-else style="color: red"/>
              </el-icon>
              </span>
                <span class="pl10">
              Status:
              <span :style="{color: state.apiReportStat.status_code === 200 ? '#67c23a': 'red'}">
                {{ state.apiReportStat.status_code === 200 ? '200 OK' : state.apiReportStat.status_code }}
                </span>
            </span>
                <span class="pl10">Time:
            <span style="color:#67c23a;">{{ state.apiReportStat.response_time_ms }} ms</span>
              </span>
                <span class="pl10">
              Size:
            <span style="color:#67c23a;">{{ formatSizeUnits(state.apiReportStat.content_size) }}</span>
              </span>
              </div>
            </div>
          </template>
          <div style="height: 500px; overflow-y: auto" v-if="state.showReport">
            <z-api-report :reportData="state.reportData" ref="ApiReportRef"></z-api-report>
          </div>
        </el-card>
      </div>
    </el-card>
  </div>
</template>

<script lang="ts" setup name="ApiSaveOrUpdate">
import {defineProps, nextTick, onMounted, reactive, ref, watch} from 'vue'
import {useRoute, useRouter} from "vue-router"
import {useApiInfoApi} from '/@/api/useAutoApi/apiInfo'
import {ElLoading, ElMessage} from 'element-plus'
import {formatSizeUnits} from "/@/utils/case"

import ApiInfo from './ApiInfo.vue'
import ApiRequestBody from './ApiRequestBody.vue'
import ApiRequestHeaders from './ApiRequestHeaders.vue'
import ApiVariables from './ApiVariables.vue'
import ApiValidators from './ApiValidators.vue'
import ApiExtracts from './ApiExtracts.vue'
import ApiCode from "./ApiCode.vue"
import ApiHooks from "./ApiHooks.vue"


// 定义父组件传过来的值
const props = defineProps({
  api_id: {
    type: [String, Number],
    default: () => {
      return null;
    },
  },
  isView: {
    type: Boolean,
    default: () => {
      return false;
    },
  },
});

const route = useRoute();
const router = useRouter();

const ApiInfoRef = ref()
const ApiRequestBodyRef = ref()
const ApiRequestHeadersRef = ref()
const ApiVariablesRef = ref()
const ApiValidatorsRef = ref()
const ApiExtractsRef = ref()
const ResponseRef = ref()
const ApiReportRef = ref()
// const APiSetupHooksRef = ref()
// const APiTeardownHooksRef = ref()
const ApiCodeRef = ref()
const ApiHookRef = ref()

const state = reactive({
  isShowDialog: false,
  activeName: 'ApiRequestBody',
  editType: '',

  // report
  showTestReportDialog: false,
  reportContent: [],

  api_id: null,

  // show
  showRequestBody: true,

  //report
  showReport: false,
  reportData: null,
  apiReportStat: null,
});


const saveOrUpdateOrDebug = (type: string) => {
  // if (!store.state.env?.envId) {
  //   console.log("store.state.env", store.state.env)
  //   showDriver()
  //   // ElMessage.warning("请选择运行环境！")
  //   return
  // }
  try {

    let caseInfoData = ApiInfoRef.value.getData()
    let bodyData = ApiRequestBodyRef.value.getData()
    let headerData = ApiRequestHeadersRef.value.getData()
    let variableData = ApiVariablesRef.value.getData()
    let validatorsData = ApiValidatorsRef.value.getData()
    let extractsData = ApiExtractsRef.value.getData()
    let hookData = ApiHookRef.value.getData()
    let codeData = ApiCodeRef.value.getData()

    // 组装表单
    let apiCaseData = {
      id: state.api_id,
      name: caseInfoData.name,
      project_id: caseInfoData.project_id,
      module_id: caseInfoData.module_id,
      code_id: caseInfoData.code_id,
      code: caseInfoData.code,
      priority: caseInfoData.priority,
      method: caseInfoData.method,
      url: caseInfoData.url,
      tags: caseInfoData.tags,
      step_type: "api",
      remarks: caseInfoData.remarks,
      env_id: caseInfoData.env_id,
      request: {
        ...bodyData,
        headers: headerData,
        method: caseInfoData.method,
        url: caseInfoData.url,
      },
      variables: variableData,
      setup_code: codeData.setup_code,
      teardown_code: codeData.teardown_code,
      validators: validatorsData,
      extracts: extractsData,
      setup_hooks: hookData.setup_hooks,
      teardown_hooks: hookData.teardown_hooks,
    }

    // 保存用例
    if (type === 'save') {
      useApiInfoApi().saveOrUpdate(apiCaseData)
        .then(res => {
          ElMessage.success('保存成功！')
          state.api_id = res.data.id
        })
    } else {
      // testCaseData.type = type
      // testCaseData.base_url = urlForm.base_url
      const loading = ElLoading.service({
        lock: true,
        text: '用例执行中,请稍候。。。',
        spinner: 'el-icon-loading',
        background: 'rgba(0, 0, 0, 0.8)',
        customClass: 'loading-class'
      })
      useApiInfoApi().debugApi(apiCaseData)
        .then(res => {
          state.reportData = null

          if (type === 'debug') {
            console.log('-----------------debug---------------')
            state.reportData = res.data
            state.showReport = true
            toResponse()
            loading.close()
          } else {
            // this.drawer = true
            loading.close()
          }
        })
        .catch(() => {
          loading.close()
        })
    }
  } catch (err: any) {
    console.log(err)
    ElMessage.warning(err.message || '信息表单填写不完整')

  }
}

const initApi = () => {
  let api_id: any
  if (props.api_id) {
    api_id = props.api_id
    state.reportData = null
    state.showReport = false
  } else {
    api_id = route.query.id
  }
  console.log("api_id------>", api_id)
  if (api_id) {
    state.api_id = api_id
    useApiInfoApi().getApiInfo({id: state.api_id})
      .then(res => {
        let apiCaseData = res.data
        ApiInfoRef.value.setData(apiCaseData)
        ApiRequestBodyRef.value.setData(apiCaseData.request)
        ApiRequestHeadersRef.value.setData(apiCaseData.headers)
        ApiVariablesRef.value.setData(apiCaseData.variables)
        ApiExtractsRef.value.setData(apiCaseData.extracts)
        ApiValidatorsRef.value.setData(apiCaseData.validators)
        ApiCodeRef.value.setData(apiCaseData.setup_code, apiCaseData.teardown_code)
        // APiSetupHooksRef.value.setData(apiCaseData.setup_hooks, state.api_id)
        // APiTeardownHooksRef.value.setData(apiCaseData.teardown_hooks, state.api_id)
        ApiHookRef.value.setData(apiCaseData.setup_hooks, apiCaseData.teardown_hooks, state.api_id)

      })
  } else {
    state.api_id = null
    state.reportData = null
    ApiInfoRef.value.setData()
    ApiRequestBodyRef.value.setData()
    ApiRequestHeadersRef.value.setData()
    ApiVariablesRef.value.setData()
    ApiExtractsRef.value.setData()
    ApiValidatorsRef.value.setData()
    ApiCodeRef.value.setData()
    ApiHookRef.value.setData()
    // APiSetupHooksRef.value.setData()
    // APiTeardownHooksRef.value.setData()
  }
}

// 返回到列表
const goBack = () => {
  router.push({name: 'apiInfo'})
}

const getDataLength = (ref: string) => {
  switch (ref) {
    case "header":
      return ApiRequestHeadersRef?.value.getDataLength()
    case "variables":
      return ApiVariablesRef.value.getDataLength()
    case "validators":
      return ApiValidatorsRef.value.getDataLength()
    case "extracts":
      return ApiExtractsRef.value.getDataLength()
    case "hook":
      return ApiHookRef.value.getDataLength()
    default:
      return 0
  }
}

// updateHeader
const updateHeader = (headerData: any, remove: any) => {
  ApiRequestHeadersRef.value.updateHeader(headerData, remove)
}

const toResponse = () => {
  nextTick(() => {
    ResponseRef.value.$el.scrollIntoView({
      behavior: "smooth",
      // 定义动画过渡效果， "auto"或 "smooth" 之一。默认为 "auto"
      block: "center",
      // 定义垂直方向的对齐， "start", "center", "end", 或 "nearest"之一。默认为 "start"
      inline: "nearest"
    })
    state.apiReportStat = {...ApiReportRef.value.getStat(), success: state.reportData.success}
  })
}

watch(
  () => props.api_id,
  () => {
    initApi()
  },
)

onMounted(() => {
  initApi()
})

</script>

<style lang="scss" scoped>

// el-badge
:deep(.el-badge__content) {
  border-radius: 50%;
  width: 18px;
}

:deep(.el-badge__content.is-fixed) {
  top: 8px;
  right: calc(-7px + var(--el-badge-size) / 2);
}

</style>