import request from '/@/utils/request';

/**
 * 项目使用接口
 * @method getProjectList 获取项目列表
 * @method getMenuTest 获取后端动态路由菜单(test)
 */
export function useEnvApi() {
  return {
    getList: (data?: object) => {
      return request({
        url: '/env/list',
        method: 'POST',
        data,
      });
    },
    getEnvById: (data?: object) => {
      return request({
        url: '/env/getEnvById',
        method: 'POST',
        data,
      });
    },
    saveOrUpdate(data?: object) {
      return request({
        url: '/env/saveOrUpdate',
        method: 'POST',
        data
      })
    },
    deleted: (data?: object) => {
      return request({
        url: '/env/deleted',
        method: 'POST',
        data,
      });
    },
    // 数据库
    getDataSourceByEnvId: (data?: object) => {
      return request({
        url: '/env/getDataSourceByEnvId',
        method: 'POST',
        data,
      });
    },
    bindingDataSource: (data?: object) => {
      return request({
        url: '/env/bindingDataSource',
        method: 'POST',
        data,
      });
    },
    unbindingDataSource: (data?: object) => {
      return request({
        url: '/env/unbindingDataSource',
        method: 'POST',
        data,
      });
    },
    // 函数
    getFuncsByEnvId: (data?: object) => {
      return request({
        url: '/env/getFuncsByEnvId',
        method: 'POST',
        data,
      });
    },
    bindingFuncs: (data?: object) => {
      return request({
        url: '/env/bindingFuncs',
        method: 'POST',
        data,
      });
    },
    unbindingFuncs: (data?: object) => {
      return request({
        url: '/env/unbindingFuncs',
        method: 'POST',
        data,
      });
    },
  };
}
