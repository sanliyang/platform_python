# -*- coding: utf-8 -*- 
""" ++++++++++++++++++++++++++++++++++++++
@product->name PyCharm
@project->name platform_python
@editor->name Sanliy
@file->name base_worker.py
@create->time 2023/4/21-23:07
@desc->
++++++++++++++++++++++++++++++++++++++ """
import threading

from apscheduler.events import EVENT_JOBSTORE_ADDED, EVENT_SCHEDULER_STARTED

from base.c_sys import CSys
from base.c_utils import CUtils
from c_mysql import CMysql


class BaseWorker:

    def __init__(self):
        self.base_sch = None
        self.logger = None

    def job_status_listener(self, Event):
        job = self.base_sch.get_job(Event.job_id)
        if not Event.exception:
            self.logger.info(
                "[{0}]--[{1}]正在执行编号为[{2}]的[{3}]类型的任务[{4}],"
                "执行此任务的小型工人名称为[{5}], 任务返回值为[{6}], 进程id为[{7}], 线程id为[{8}]\n".format(
                    Event.scheduled_run_time,
                    job.executor,
                    job.id,
                    job.trigger,
                    job.name,
                    job.func.__name__,
                    Event.retval,
                    CSys.get_pid(),
                    threading.get_ident()
                ))
        else:
            self.logger.error(
                "任务名称=[{0}]|任务执行类型=[{1}]|异常编号=[{2}]|引发的异常=[{3}]|"
                "异常格式化回溯=[{4}]|任务执行时间=[{5}]|进程id=[{6}]|线程id=[{7}]\n".format(
                    job.name,
                    job.trigger,
                    Event.code,
                    Event.exception,
                    Event.traceback,
                    Event.scheduled_run_time,
                    threading.get_ident(),
                    CSys.get_pid()()
                )
            )

    def job_list_listener(self, Event):
        if Event.code == EVENT_JOBSTORE_ADDED:
            for job_detail in self.base_sch.get_jobs():
                self.logger.info(
                    "[{0}]正在将编号为[{1}]的[{2}]类型的任务[{3}]加入到调度器中,"
                    "执行此调度的小型工人名称为[{4}]\n".format(
                        job_detail.executor,
                        job_detail.id,
                        job_detail.trigger,
                        job_detail.name,
                        job_detail.func.__name__
                    ))

    def job_start_listener(self, Event):
        if Event.code == EVENT_SCHEDULER_STARTED:
            self.logger.info("调度中心[{0}]已经准备就绪！\n".format(CUtils.one_id()))

    def wait_monitor(self):
        # 这里需要编写 对node 节点状态的监控， 等待（1） 执行（2）失败（3） 成功前处理（0） 成功后处理（-2）
        # 检查到有等待的节点， 会去数据库中查询到等待节点的信息，然后开始执行
        pass

    def processing_monitor(self):
        # 这里会随时监控节点， 正在执行中？ 执行成功？ 执行失败？
        pass

    def finish_monitor(self):
        # 执行成功 将此节点的状态改为 0
        # 获取成功下一个节点，当前节点任务完成， 状态为 -2
        # 如果当前节点失败， 将当前节点的状态 改为失败 3
        pass

    def update_status(self, node_status, node_id):
        cm = CMysql()
        cm.execute(
            '''
            update python_platform.do_nodes 
            set node_status =:node_status 
            where node_id =:node_id
            ''', {
                "node_status": node_status,
                "node_id": node_id
            }
        )
        cm.close()
