# -*- coding: utf-8 -*- 
""" ++++++++++++++++++++++++++++++++++++++
@product->name PyCharm
@project->name platform_python
@editor->name Sanliy
@file->name monitor_node_worker.py
@create->time 2023/4/21-23:12
@desc->
++++++++++++++++++++++++++++++++++++++ """
from base.c_logger import CLogger
from base.c_mysql import CMysql
from base.c_resource import CResource
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_MISSED, EVENT_JOB_EXECUTED, EVENT_JOBSTORE_ADDED, \
    EVENT_SCHEDULER_STARTED
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.blocking import BlockingScheduler

from c_json import CJson
from c_result import CResult
from c_utils import CUtils
from scheduler.base.base_worker import BaseWorker
import importlib


class MonitorNodeWorker(BaseWorker):
    def __init__(self):
        super(MonitorNodeWorker, self).__init__()
        self.logger = CLogger(False)
        self.executor = {
            "node节点wait监控工人": ThreadPoolExecutor(3),
            "node节点finish监控工人": ThreadPoolExecutor(3)
        }
        self.order_worker_sch = BlockingScheduler(executors=self.executor, timezone='Asia/Shanghai')
        self.base_sch = self.order_worker_sch
        self.order_worker_sch._logger = self.logger
        self.cm = CMysql()

    def get_class_name(self):
        return self.__class__.__name__

    def wait_monitor(self):
        # 这里不会进行第一个节点的创建
        # 检查到有等待的节点， 会去数据库中查询到等待节点的信息，然后开始执行
        # 这里会随时监控节点， 正在执行中？ 执行成功？ 执行失败？
        # 执行成功 将此节点的状态改为 0
        # 获取成功下一个节点，当前节点任务完成， 状态为 -2
        # 如果当前节点失败， 将当前节点的状态 改为失败 3
        node_config = self.cm.fetchall(
            '''
            select node_id, node_name, node_type, node_model_name 
            from python_platform.do_nodes 
            where node_status =:node_status
            ''', {
                "node_status": CResource.NODE_WAIT
            }
        )
        if node_config:
            node_id, node_name, node_type, node_model_name = node_config[0]

            node_obj = importlib.import_module(f"node.{node_type}.{node_model_name}")
            class_obj = getattr(node_obj, node_name)
            real_class_obj = class_obj()
            real_class_obj.get_node_id(node_id)
            result = real_class_obj.run()
            if CResult.result_sucess(result):
                self.update_status(CResource.NODE_SUCESS, node_id)
            else:
                self.update_status(CResource.NODE_FAILD, node_id)

    def finish_monitor(self):
        """
        当前算法已经完成， 创建下一个算法，并将当前算法的状态设置为NODE_FINISH(-1)
        :return:
        """
        id_set = self.cm.fetchall(
            '''
            select node_id, workflow_id
            from python_platform.do_nodes 
            where node_status =:node_status
            ''', {
                "node_status": CResource.NODE_SUCESS
            }
        )
        if id_set:
            node_id, workflow_id = id_set[0]
            # 将当前状态改为finish，并创建下一个算法到数据库
            self.cm.execute(
                '''
                update python_platform.do_nodes 
                set node_status =:node_status 
                where node_id =:node_id
                ''', {
                    "node_status": CResource.NODE_FINISH,
                    "node_id": node_id
                }
            )
            # todo 通过查找，尝试创建下一个算法， 如果有下一个算法就创建， 没有就不创建， 并且对算法和流程进行监控
            workflow_config = self.cm.fetchall(
                '''
                select workflow_line, workflow_node_list, workflow_params
                from python_platform.platform_queue_workflow 
                where workflow_id =:workflow_id
                ''', {
                    "workflow_id": workflow_id
                }
            )
            workflow_line = workflow_config[0][0]
            workflow_node_list = workflow_config[0][1]
            workflow_params = workflow_config[0][2]
            cj = CJson()
            cj.load(workflow_line)
            lines = cj.json_path("line")
            to_node = None
            for line in lines:
                cj.load(line)
                from_node = cj.json_path_one("from")
                if from_node == node_id:
                    to_node = cj.json_path_one("to")
                    break
            if to_node is None:
                return
            cj.load(workflow_node_list)
            node_list = cj.json_path("node_list")
            for node in node_list:
                cj.load(node)
                node_list_id = cj.json_path_one("id")
                if node_list_id == to_node:
                    node_config = cj.json_path_one("config")
                    node_type = cj.json_path_one("node_type")
                    class_name = cj.json_path_one("class_name")
                    model_name = cj.json_path_one("model_name")
                    node_zh_name = cj.json_path_one("node_zh_name")
                    break
            # 这里对node_config进行赋值，保证写到数据库中的值都存在
            cj.load(node_config)
            node_params = cj.json_path_one("params")

            node_params = CUtils.replace_params(str(node_params), workflow_params)

            node_params = CUtils.replace_output(node_params, workflow_id)

            node_config["params"] = node_params
            self.cm.execute(
                '''
                insert into python_platform.do_nodes(
                node_id, workflow_id, node_config, node_name, 
                node_zh_name, node_status, node_type, node_model_name
                ) values (
                :node_id, :workflow_id, :node_config, :node_name, 
                :node_zh_name, :node_status, :node_type, :node_model_name
                )
                ''', {
                    "node_id": to_node,
                    "workflow_id": workflow_id,
                    "node_config": CJson.dict_2_json(node_config),
                    "node_name": class_name,
                    "node_zh_name": node_zh_name,
                    "node_status": CResource.NODE_WAIT,
                    "node_type": node_type,
                    "node_model_name": model_name
                }
            )


if __name__ == '__main__':
    mnw = MonitorNodeWorker()
    mnw.order_worker_sch.add_job(
        func=mnw.wait_monitor,
        trigger="interval",
        seconds=10,
        executor="node节点wait监控工人",
        id='monitor_node_worker',
        name="node节点监控"
    )

    mnw.order_worker_sch.add_job(
        func=mnw.finish_monitor,
        trigger="interval",
        seconds=10,
        executor="node节点finish监控工人",
        id='finish_monitor_worker',
        name="node节点监控"
    )

    mnw.order_worker_sch.add_listener(
        mnw.job_status_listener,
        EVENT_JOB_ERROR | EVENT_JOB_MISSED | EVENT_JOB_EXECUTED
    )
    mnw.order_worker_sch.add_listener(
        mnw.job_list_listener,
        EVENT_JOBSTORE_ADDED
    )
    mnw.order_worker_sch.add_listener(
        mnw.job_start_listener,
        EVENT_SCHEDULER_STARTED
    )
    mnw.order_worker_sch.start()
