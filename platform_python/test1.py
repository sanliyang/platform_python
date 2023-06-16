# -*- coding: utf-8 -*- 
""" ++++++++++++++++++++++++++++++++++++++
@product->name PyCharm
@project->name platform_python
@editor->name Sanliy
@file->name test1.py
@create->time 2023/4/1-14:45
@desc->
++++++++++++++++++++++++++++++++++++++ """
import time

import cv2
import matplotlib.pyplot as plt

img_obj = cv2.imread(r"D:\1661686208.jpg")
cv2.imshow("test", img_obj)

img_gray = cv2.cvtColor(img_obj, cv2.COLOR_BGR2GRAY)
ret, img_threshold = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)
cv2.imshow("test2", img_threshold)
print(ret)

print(img_obj.shape)

roi = img_obj[100:800, 300:1000]
cv2.imshow("test3", roi)

roi_1 = cv2.copyMakeBorder(
    roi,
    20, 20, 20, 20,
    cv2.BORDER_CONSTANT,
    value=[0,255,0]
)
cv2.imshow("test4", roi_1)
key = cv2.waitKey(0)
