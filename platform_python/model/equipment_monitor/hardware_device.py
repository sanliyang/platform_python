import psutil
import pynvml


class HardwareDevice:

    def __init__(self):
        # 初始化
        pynvml.nvmlInit()
        self.handle = 0

    def gpu_handle(self, gpu_id):
        self.handle = pynvml.nvmlDeviceGetHandleByIndex(gpu_id)

    @staticmethod
    def close():
        # 关闭gpu管理工具
        pynvml.nvmlShutdown()

    @staticmethod
    def gpu_driver_version():
        return pynvml.nvmlSystemGetDriverVersion()

    @staticmethod
    def gpu_count():
        return pynvml.nvmlDeviceGetCount()

    def gpu_name(self):
        return pynvml.nvmlDeviceGetName(self.handle)

    def gpu_total_memory(self):
        return str(pynvml.nvmlDeviceGetMemoryInfo(self.handle).total / 1024 / 1024) + "MB"

    def gpu_used_memory(self):
        return str(pynvml.nvmlDeviceGetMemoryInfo(self.handle).used / 1024 / 1024) + "MB"

    def gpu_free_memory(self):
        return str(pynvml.nvmlDeviceGetMemoryInfo(self.handle).free / 1024 / 1024) + "MB"

    def gpu_temperature(self):
        return pynvml.nvmlDeviceGetTemperature(self.handle, 0)

    def gpu_fan_speed(self):
        return pynvml.nvmlDeviceGetFanSpeed(self.handle)

    def gpu_power_state(self):
        return pynvml.nvmlDeviceGetPowerState(self.handle)

    @staticmethod
    def cpu_count():
        """
        查看cpu物理个数
        :return:
        """
        return psutil.cpu_count(logical=False)

    @staticmethod
    def get_cpu_use_percent():
        """
        获取cpu使用率
        :return:
        """
        return str(psutil.cpu_percent(interval=2, percpu=False))

    @staticmethod
    def get_totle_memory():
        """
        获取总内存
        :return:
        """
        return f"{str(round(psutil.virtual_memory().total / (1024.0 * 1024.0 * 1024.0), 2))}GB"

    @staticmethod
    def get_free_memory():
        """
        获取空闲内存
        :return:
        """
        return f"{str(round(psutil.virtual_memory().free / (1024.0 * 1024.0 * 1024.0), 2))}GB"

    @staticmethod
    def user():
        """
        获取用户个数和登录的用户名称
        :return:
        """
        users_count = len(psutil.users())
        user_name = ",".join([u.name for u in psutil.users()])
        return [users_count, user_name]

    @staticmethod
    def network():
        """
        获取网卡的入网流量和出网流量
        :return:
        """
        net = psutil.net_io_counters()
        bytes_rcvd = '{0:.2f} Mb'.format(net.bytes_sent / 1024 / 1024)  # 网卡接收流量
        bytes_sent = '{0:.2f} Mb'.format(net.bytes_recv / 1024 / 1024)  # 网卡发送流量
        return [bytes_rcvd, bytes_sent]


if __name__ == '__main__':
    cm = HardwareDevice()
    print(cm.cpu_count())
    print(cm.get_cpu_use_percent())
    print(cm.get_totle_memory())
    print(cm.get_free_memory())
    print(cm.network())
    print(cm.user())
    for gpu_id in range(0, cm.gpu_count()):
        cm.gpu_handle(gpu_id)
        print(cm.gpu_driver_version())
        print(cm.gpu_name())
        print(cm.gpu_total_memory())
        print(cm.gpu_used_memory())
        print(cm.gpu_free_memory())
    cm.close()
