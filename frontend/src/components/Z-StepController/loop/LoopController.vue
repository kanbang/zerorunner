<template>
  <el-collapse-transition>
    <div v-show="data.showDetail" class="w100" @pointerdown.stop @click.stop>
<!--      <el-divider style="margin: 10px 0 5px 0;"/>-->

      <div v-if="data.loop_request.loop_type === 'count'" class="controller-content">

        <el-row>

          <el-col :span="6">
            <div>
              <span style="padding-right: 5px">循环次数</span>
              <el-input v-model="data.loop_request.count_number"
                        @pointerdown.stop.native
                        @click.stop.native
                        placeholder="循环次数"></el-input>
            </div>
          </el-col>

          <el-col :span="6" :offset="2">
            <div>
              <span style="padding-right: 5px">循环间隔</span>
              <el-input-number v-model.number="data.loop_request.count_sleep_time"
                               controls-position="right"
                               @pointerdown.stop.native
                               @click.stop.native
                               placeholder="秒">
              </el-input-number>
            </div>
          </el-col>

        </el-row>

      </div>

      <div v-else-if="data.loop_request.loop_type === 'for'" class="controller-content">

        <el-row>
          <el-col :span="6">
            <el-input v-model="data.loop_request.for_variable_name"
                      @pointerdown.stop.native
                      @click.stop.native
                      placeholder="定义变量名称"
            >
              <template #suffix>
                  <span class="el-input__suffix-inner" @click="copyText('${'+ data.loop_request.for_variable_name +'}')">
                    <el-icon color="#303133">
                      <ele-DocumentCopy/>
                    </el-icon>
                  </span>
              </template>

            </el-input>
          </el-col>
          <el-col :span="1">
            <span style="padding: 0 8px">in</span>
          </el-col>
          <el-col :span="6">
            <el-input v-model="data.loop_request.for_variable"
                      @pointerdown.stop.native
                      @click.stop.native
                      placeholder="变量,例如：${var}"></el-input>
          </el-col>
          <el-col :span="6">
            <span>循环间隔</span>
            <el-input v-model="data.loop_request.for_sleep_time"
                      @pointerdown.stop.native
                      @click.stop.native
                      placeholder="秒"
            ></el-input>
          </el-col>
        </el-row>

      </div >

      <div v-else-if="data.loop_request.loop_type === 'while'" class="controller-content">

        <el-row>
          <el-col :span="5">
            <el-input v-model="data.loop_request.while_variable"
                      @pointerdown.stop.native
                      @click.stop.native
                      class="com-padding"
                      placeholder="变量,例如：${var}"></el-input>
          </el-col>
          <el-col :span="5">
            <el-select size="small"
                       @pointerdown.stop.native
                       @click.stop.native
                       v-model="data.loop_request.while_comparator"
                       placeholder="请选择"
                       filterable
                       class="w100 com-padding">
              <el-option
                  v-for="(value, key) in state.comparatorOptions"
                  :key="key"
                  :label="value"
                  :value="key">
              </el-option>

            </el-select>
          </el-col>
          <el-col :span="5">
            <el-input @pointerdown.stop.native
                      @click.stop.native
                      v-model="data.loop_request.while_value"
                      class="com-padding"
                      placeholder="值"></el-input>
          </el-col>
          <el-col :span="5">
            <span>循环超时时间</span>
            <el-input-number @pointerdown.stop.native
                             controls-position="right"
                             @click.stop.native
                             v-model="data.loop_request.while_timeout"
                             placeholder="秒"></el-input-number>
          </el-col>
        </el-row>

      </div>
    </div>
  </el-collapse-transition>
</template>

<script lang="ts" setup name="LoopController">
import {PropType, reactive} from 'vue';
import commonFunction from '/@/utils/commonFunction';

const {copyText} = commonFunction()


const props = defineProps({
  data: {
    type: Object as PropType<TStepDataStat>,
    default: () => {
      return {
      }
    }
  }
})

const state = reactive({
  // data
  showDetail: false,
  comparatorOptions: {
    equals: "等于",
    not_equals: "不等于",
    contains: "包含",
    not_contains: "不包含",
    gt: "大于",
    lt: "小于",
    none: "空",
    not_none: "非空",
  }
});

</script>

<style lang="scss" scoped>
.com-padding {
  padding: 0 3px;
}

.el-input {
  //display: inline-block;
}

.controller-content {
  padding: 5px 20px;
}
</style>