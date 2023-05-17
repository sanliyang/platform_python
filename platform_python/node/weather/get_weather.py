# -*- coding: utf-8 -*- 
""" ++++++++++++++++++++++++++++++++++++++
@product->name PyCharm
@project->name platform_python
@editor->name Sanliy
@file->name get_weather.py
@create->time 2023/4/20-17:09
@desc->
++++++++++++++++++++++++++++++++++++++ """
from base.c_json import CJson
from base.c_resource import CResource
from base.c_result import CResult
from base.c_utils import CUtils
from node.base.node_base import NodeBase
from model.weather.catch_weather import CatchWeather


class GetWeather(NodeBase):

    def __init__(self):
        super().__init__()
        self.weather_pass = None
        self.weather_user = None
        self.weather_url = None
        self.city = None

    def help(self):
        return '''
                算法名称: 获取天气算法
                分属类别：weather
                算法作用：从一刻天气网站获取天气情况
                算法接收参数
                {
                    "input": [],
                    "output": [],
                    "params": {
                        "city": "xxxxxxxx"
                    }
                }
                '''

    def check_params(self):
        result = super().check_params()
        if CResult.result_faild(result):
            return result
        if self.params is None:
            return CResult.merge_result(
                self.NODE_EXCEPTION,
                "请选择设置算法的参数， 因为有一些必要参数未设置，算法将停止运行，请检查后重试!"
            )
        self.city = CUtils.dict_value_by_name(self.params, "city", None)

        if self.city is None:
            return CResult.merge_result(
                self.NODE_EXCEPTION,
                "部分必要参数未设定， 请检查修正！"
            )
        return CResult.merge_result(
            self.RESULT_SUCCESS,
            "输入参数检查成功，算法将继续运行..."
        )

    def get_weather(self):
        cw = CatchWeather()
        response = cw.get_weather(self.city)
        if response.status_code == 200:
            return CResult.merge_result(
                CResource.RESULT_SUCCESS,
                response.text
            )
        return CResult.merge_result(
            CResource.RESULT_FAILD,
            f"{self.city}天气获取失败，请检查后重试!"
        )

    def run(self):
        result = super().run()
        if CResult.result_faild(result):
            return result
        weather_result = self.get_weather()
        if CResult.result_faild(weather_result):
            return result
        weather = CResult.result_msg(weather_result)
        weather_format = self.format_weather(weather)
        self.update_output(weather_format)
        self.save_ouput()
        self.cm.close()
        return CResult.merge_result(
            self.RESULT_SUCCESS,
            f"{self.city}天气情况获取成功！"
        )

    def format_weather(self, weather):
        cj = CJson()
        cj.load(weather)
        data_list = cj.json_path("data")
        html_header = """
        <!DOCTYPE html>
            <html>
            <head>
            <title>天气信息展示</title>
            <style>
                /* 设置整个页面的字体 */
                body {
                font-family: Arial, sans-serif;
                }
                
                /* 设置天气信息区域的样式 */
                .weather-info {
                background-color: #f1f1f1;
                border: 1px solid #ddd;
                padding: 20px;
                width: 500px;
                margin: 0 auto;
                }
                
                /* 设置日期、城市、天气和风的样式 */
                .weather-info h2,
                .weather-info p {
                margin: 0;
                font-size: 18px;
                }
                
                /* 设置白天和夜晚温度的样式 */
                .weather-info .temperature {
                font-size: 24px;
                font-weight: bold;
                }
                
                /* 设置风的等级的样式 */
                .weather-info .wind-level {
                font-size: 14px;
                color: #888;
                }
            </style>
            </head>
            <body>
        """
        html_foot = """
                </body>
            </html>
        """
        html_body = ""
        for data in data_list:
            cj = CJson()
            cj.load(data)
            html_body += """
                <div class="weather-info">
                    <h2>{0}年{1}月{2}日</h2>
                    <p>城市：{3}</p>
                    <p class="temperature">白天温度：{4}℃，夜晚温度：{5}℃</p>
                    <p>天气：{6}</p>
                    <p>风：{7}</p>
                    <p class="wind-level">风力：{8}</p>
                </div>
                <br>
            """.format(
                cj.json_path_one("date").split("-")[0],
                cj.json_path_one("date").split("-")[1],
                cj.json_path_one("date").split("-")[2],
                self.city,
                cj.json_path_one("tem_day"),
                cj.json_path_one("tem_night"),
                cj.json_path_one("wea"),
                cj.json_path_one("win"),
                cj.json_path_one("win_speed")
            )
        return html_header+html_body+html_foot


if __name__ == '__main__':
    gw = GetWeather.run_test(
        '''
        {
            "input": [],
            "output": [],
            "params": {
                "city": "郑州"
            }
        }
        '''
    )
