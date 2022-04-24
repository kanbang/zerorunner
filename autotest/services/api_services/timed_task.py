import datetime
import json
import traceback
from typing import Dict, Any, NoReturn, Union

from loguru import logger

from autotest.exc import codes
from autotest.exc.partner_message import partner_errmsg
from autotest.serialize.api_serializes.timed_task import (
    TimedTasksQuerySchema,
    TimedTasksListSchema,
    TimedTasksSaveOrUpdateSchema,
    CrontabSaveSchema)
from autotest.models.api_models import TimedTask, Crontab, \
    PeriodicTaskChanged
from autotest.utils.api import parse_pagination
from autotest.utils.common import get_user_info_by_token


class CrontabService:
    @staticmethod
    def save_or_update(**kwargs: Any) -> Crontab:
        try:
            parsed_data = CrontabSaveSchema().load(kwargs)
            crontab_time = parsed_data.get('crontab_time')
            minute = crontab_time[0],  # 分
            hour = crontab_time[1],  # 小时
            day_of_month = crontab_time[2],  # 日期
            day_of_week = crontab_time[3],  # 周
            month_of_year = crontab_time[-1],  # 月份
        except Exception as err:
            raise ValueError(err)
        crontab_query_params = {
            'minute': minute,
            'hour': hour,
            'day_of_week': day_of_week,
            'day_of_month': day_of_month,
            'month_of_year': month_of_year
        }
        crontab = Crontab.get_crontab_by_parameter(**crontab_query_params)
        if not crontab:
            try:
                crontab = Crontab()
                crontab.minute = minute
                crontab.hour = hour
                crontab.day_of_month = day_of_month
                crontab.month_of_year = month_of_year
                crontab.day_of_week = day_of_week
                crontab.save()
            except Exception as err:
                logger.error(err)
                raise ValueError(err)
        return crontab


class TimedTasksService:
    @staticmethod
    def list(**kwargs: Any) -> Dict:
        """定时任务列表"""
        query_data = TimedTasksQuerySchema().load(kwargs)
        data = parse_pagination(TimedTask.get_list(**query_data))
        _result, pagination = data.get('result'), data.get('pagination')
        result = {
            'rows': TimedTasksListSchema().dump(_result, many=True)
        }
        result.update(pagination)
        return result

    @staticmethod
    def save_or_update(**kwargs: Any) -> TimedTask:
        parsed_data = TimedTasksSaveOrUpdateSchema().load(kwargs)
        case_ids = parsed_data.get('case_ids')
        name = parsed_data.get('name')
        task = parsed_data.get('task')
        task_type = parsed_data.get('task_type')
        task_id = parsed_data.get('id')

        timed_task = TimedTask.get(task_id) if task_id else TimedTask()

        try:
            crontab = CrontabService.save_or_update(**kwargs)
            user_info = get_user_info_by_token()

            task_kwargs = {
                'c_ids': case_ids,
                'task_type': task_type,
                'base_url': '',
                'ex_user_id': user_info.get('id'),
                'ex_user_name': user_info.get('nickname')
            }
            parsed_data['case_ids'] = ','.join(case_ids)
            parsed_data['crontab_id'] = crontab.id
            parsed_data['kwargs'] = json.dumps(task_kwargs)
            timed_task.update(**parsed_data)

            PeriodicTaskChangedService.update()
            return timed_task
        except Exception as err:
            raise ValueError(err)

    @staticmethod
    def deleted(task_id: Union[str, int]) -> NoReturn:
        task_info = TimedTask.get(task_id)
        task_info.delete(True) if task_info else ...
        PeriodicTaskChangedService.update()


class PeriodicTaskChangedService:
    @staticmethod
    def update() -> PeriodicTaskChanged:
        try:
            periodic_task_changed = PeriodicTaskChanged.get_data()
            periodic_task_changed.last_update = datetime.datetime.now()
            periodic_task_changed.save()
            return periodic_task_changed
        except Exception as err:
            logger.error(traceback.format_exc())
            raise ValueError(err)
