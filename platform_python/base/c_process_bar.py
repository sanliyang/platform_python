# -*- coding: utf-8 -*- 
""" ++++++++++++++++++++++++++++++++++++++
@product->name PyCharm
@project->name platform_python
@editor->name Sanliy
@file->name c_process_bar.py
@create->time 2023/3/17-17:20
@desc->
++++++++++++++++++++++++++++++++++++++ """
from tqdm import tqdm


class CProcessBar:

    def __init__(self, process_count, process_name):
        self.process_obj = None
        self.process_count = process_count
        self.process_name = process_name

    def __enter__(self):
        self.process_obj = tqdm(total=self.process_count, desc=self.process_name, leave=True, ncols=100, unit='B',
                                unit_scale=True)
        return self

    def display_process(self, update_count):
        self.process_obj.update(update_count)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.process_obj.close()
        return True


if __name__ == '__main__':
    from base.c_time import CTime

    with CProcessBar(100, "test") as f1:
        for i in range(10):
            CTime.sleep(0.5)
            f1.display_process(10)
