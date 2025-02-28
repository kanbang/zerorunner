<template>
  <div class="app-container">
    <el-card>
      <div class="mb15">
        <el-input v-model="state.listQuery.name" placeholder="请输入名称" style="max-width: 180px"></el-input>
        <el-button type="primary" class="ml10" @click="getList">
          <el-icon>
            <ele-Search/>
          </el-icon>
          查询
        </el-button>
        <el-button type="success" class="ml10" @click="onOpenSaveOrUpdate('save', null)">
          <el-icon>
            <ele-FolderAdd/>
          </el-icon>
          新增
        </el-button>
      </div>
      <z-table
          :columns="state.columns"
          :data="state.listData"
          v-model:page-size="state.listQuery.pageSize"
          v-model:page="state.listQuery.page"
          :total="state.total"
          @pagination-change="getList"
      />
    </el-card>
    <EditTimedTask ref="saveOrUpdateRef" @getList="getList"/>
  </div>
</template>

<script lang="ts" setup name="TimedTask">
import {h, onMounted, reactive, ref} from 'vue';
import {ElButton, ElMessage, ElMessageBox} from 'element-plus';
import EditTimedTask from './EditTimedTask.vue';
import {useTimedTasksApi} from "/@/api/useAutoApi/timedTasks";
import {formatLookup} from "/@/utils/lookup";


const saveOrUpdateRef = ref();
const state = reactive({
  columns: [
    {
      key: 'name', label: '任务名称', width: '', align: 'center', show: true,
      render: (row: any) => h(ElButton, {
        type: "primary",
        link: true,
        onClick: () => {
          onOpenSaveOrUpdate("update", row)
        }
      }, () => row.name)
    },
    {
      key: 'task_type',
      label: '调度模式',
      width: '',
      align: 'center',
      show: true,
      render: (row: any) => handleTaskType(row)
    },
    {key: 'project_name', label: '所属项目', width: '', align: 'center', show: true},
    {
      key: 'enabled',
      label: '任务状态',
      width: '',
      align: 'center',
      show: true,
      render: (row: any) => {
        let value = formatLookup("api_timed_task_status", row.enabled)
        return h("span", {style: {color: row.enabled ? '#0cbb52' : '#e6a23c'}}, value)
      }
    },
    {key: 'description', label: '任务描述', width: '', align: 'center', show: true},
    {key: 'updation_date', label: '更新时间', width: '150', align: 'center', show: true},
    {key: 'updated_by_name', label: '更新人', width: '', align: 'center', show: true},
    {key: 'creation_date', label: '创建时间', width: '150', align: 'center', show: true},
    {key: 'created_by_name', label: '创建人', width: '', align: 'center', show: true},
    {
      label: '操作', columnType: 'string', fixed: 'right', width: '200',
      render: (row: any) => h("div", null, [
        h(ElButton, {
          type: "success",
          onClick: () => {
            taskSwitch(row)
          }
        }, () => row.enabled ? '停止' : '启动'),

        h(ElButton, {
          type: "primary",
          onClick: () => {
            onOpenSaveOrUpdate("update", row)
          }
        }, () => '编辑'),

        h(ElButton, {
          type: "danger",
          onClick: () => {
            deleted(row)
          }
        }, () => '删除')
      ])
    },
  ],
  // list
  listData: [],
  tableLoading: false,
  total: 0,
  listQuery: {
    page: 1,
    pageSize: 20,
    name: '',
  },
});
// 初始化表格数据
const getList = () => {
  state.tableLoading = true
  useTimedTasksApi().getList(state.listQuery)
      .then(res => {
        state.listData = res.data.rows
        state.total = res.data.rowTotal
        state.tableLoading = false
      })
};

// 新增或修改
const onOpenSaveOrUpdate = (editType: string, row: any) => {
  saveOrUpdateRef.value.openDialog(editType, row);
};

// 新增或修改
const taskSwitch = (row: any) => {
  ElMessageBox.confirm(`${row.enabled ? '停止' : '启动'}当前任务, 是否继续?`, '提示', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(() => {
    useTimedTasksApi().taskSwitch({id: row.id})
        .then(() => {
          ElMessage.success('操作成功！');
          getList()
        })
  })

};

// 删除
const deleted = (row: any) => {
  ElMessageBox.confirm('是否删除该条数据, 是否继续?', '提示', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    type: 'warning',
  })
      .then(() => {
        useTimedTasksApi().deleted({id: row.id})
            .then(() => {
              ElMessage.success('删除成功');
              getList()
            })
      })
      .catch(() => {
      });
};

const handleTaskType = (row: any) => {
  if (row.task_type === 'crontab') {
    return `${row.task_type}[${row.crontab}]`
  } else if (row.task_type === 'interval') {
    return `${row.task_type}[${row.interval_every} ${row.interval_period}]`;
  }
}

// 页面加载时
onMounted(() => {
  getList();
});

</script>

<style>

.stop {
  background-color: #c1bfc7;
}

.start {
  background-color: #0cbb52;
}

.request-editor-tabs-badge {
  display: inline-flex;
  width: 8px;
  height: 8px;
  margin-right: 5px;
  border-radius: 8px;
}
</style>