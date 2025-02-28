# -*- coding: utf-8 -*-
# @author: xiaobai
import typing

from pydantic import BaseModel, Field

from zerorunner.model.base import VariablesMapping, MethodEnum, Url, Headers, Cookies


class RequestStat(BaseModel):
    content_size: float = Field(0, description="响应内容大小")
    response_time_ms: float = Field(0, description="响应时间 毫秒")
    elapsed_ms: float = Field(0, description="过程时间")


class AddressData(BaseModel):
    client_ip: str = Field("N/A", description="客户端ip")
    client_port: int = Field(0, description="客户端端口")
    server_ip: str = Field("N/A", description="服务端ip")
    server_port: int = Field(0, description="服务端端口")


class RequestData(BaseModel):
    method: typing.Optional[MethodEnum] = Field(MethodEnum.GET, description="请求方法")
    url: Url = Field(..., description="url")
    headers: Headers = Field({}, description="请求头")
    cookies: Cookies = Field({}, description="cookies")
    body: typing.Union[str, bytes, typing.List, typing.Dict, None] = Field({}, description="body")


class ResponseData(BaseModel):
    status_code: int = Field(..., description="状态码")
    headers: typing.Dict = Field(..., description="响应头")
    cookies: typing.Optional[Cookies] = Field(..., description="cookies")
    encoding: typing.Union[str, None] = Field(None, description="encoding")
    content_type: str = Field(..., description="类型")
    body: typing.Union[str, bytes, typing.List, typing.Dict, None] = Field(..., description="body")


class ReqRespData(BaseModel):
    request: RequestData = Field(..., description="请求数据")
    response: ResponseData = Field(..., description="响应数据")


class SessionData(BaseModel):
    """请求会话数据，包括请求、响应、验证器和stat数据"""

    success: bool = Field(False, description="是否成功")
    req_resp: ReqRespData = Field({}, description="请求，响应数据")
    stat: RequestStat = Field(RequestStat(), description="时间")
    address: AddressData = Field(AddressData(), description="地址")
    validators: typing.Dict = Field({}, description="校验")


class StepResult(BaseModel):
    """测试步骤数据"""

    name: str = Field("", description="步骤名称")  # 步骤名称
    case_id: str = Field("", description="case_id")  # case_id
    index: int = Field(0, description="index")  # case_id
    start_time: float = Field(0, description="开始时间")  # case_id
    duration: float = Field(0, description="执行耗时")  # duration
    success: bool = Field(False, description="是否成功")
    status: str = Field("", description="步骤状态  success 成功  fail 失败  skip 跳过  err 错误")
    step_type: str = Field("", description="步骤类型")
    step_tag: typing.Union[str, None] = Field(None, description="步骤标签")  # 标签
    message: str = Field("", description="信息")  # err or message
    env_variables: VariablesMapping = Field({}, description="环境变量")
    variables: VariablesMapping = Field({}, description="变量")
    case_variables: VariablesMapping = Field({}, description="用例变量")
    step_result: typing.List['StepResult'] = Field([], description="步骤结果")
    session_data: SessionData = Field(None, description="请求信息")  # 请求信息
    # pre_hook_data: typing.List['StepResult'] = Field([], description="")  # 前置
    # post_hook_data: typing.List['StepResult'] = Field([], description="")  # 后置
    setup_hook_results: typing.List['StepResult'] = Field([], description="前置hook")  # 前置hook
    teardown_hook_results: typing.List['StepResult'] = Field([], description="后置hook")  # 后置hook
    export_vars: VariablesMapping = Field({}, description="")
    log: str = Field("", description="log")
    attachment: str = Field("", description="附件")

    def dict(self, *args, **kwargs):
        """获取报告时去除 请求信息 避免报告数据太大"""
        kwargs["exclude"] = {"request", "response"}
        return super(StepResult, self).dict(*args, **kwargs)


class TestCaseInOut(BaseModel):
    config_vars: VariablesMapping = Field({}, description="配置参数")
    export_vars: typing.Dict = Field({}, description="导出参数")


class TestCaseSummary(BaseModel):
    name: str = Field(..., description="报告名称")
    success: bool = Field(..., description="是否成功")
    case_id: typing.Union[str, int] = Field(None, description="用例id")
    start_time: typing.Union[float, str] = Field(0, description="开始时间")
    response_time: float = Field(0, description="请求时间")
    duration: float = Field(0, description="耗时")
    run_count: int = Field(0, description="运行数量")
    actual_run_count: int = Field(0, description="时间执行数量")
    run_success_count: int = Field(0, description="运行成功数")
    run_fail_count: int = Field(0, description="运行错误数")
    run_skip_count: int = Field(0, description="运行跳过数")
    run_err_count: int = Field(0, description="运行错误数")
    start_time_iso_format: str = Field("", description="运行时间系统时间")
    in_out: TestCaseInOut = Field({}, description="输出")
    # message 记录错误信息
    message: str = Field("", description="信息")
    log: str = Field("", description="日志")
    step_results: typing.List[StepResult] = Field([], description="步骤结果")


class PlatformInfo(BaseModel):
    zerorunner_version: str = Field(..., description="版本号")
    python_version: str = Field(..., description="python版本")
    platform: str = Field(..., description="机器信息")


# class TestSuite(BaseModel):
#     config: TConfig
#     testcases: typing.List[TestCase]


class Stat(BaseModel):
    total: int = Field(0, description="总数")
    success: int = Field(0, description="成功数量")
    fail: int = Field(0, description="失败数量")


class TestCaseTime(BaseModel):
    start_at: float = Field(0, description="时间")
    duration: float = Field(0, description="过程耗时")
    start_at_iso_format: str = Field("", description="开始系统时间")


class TestSuiteSummary(BaseModel):
    success: bool = Field(False, description="是否成功")
    stat: Stat = Field(Stat(), description="")
    time: TestCaseTime = Field(TestCaseTime(), description="")
    platform: PlatformInfo = Field(..., description="")
    testcases: typing.List[TestCaseSummary] = Field(..., description="")
