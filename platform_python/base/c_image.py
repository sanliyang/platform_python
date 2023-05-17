# -*- coding: utf-8 -*- 
""" ++++++++++++++++++++++++++++++++++++++
@product->name PyCharm
@project->name platform_python
@editor->name Sanliy
@file->name c_image.py
@create->time 2023/5/12-10:42
@desc->
++++++++++++++++++++++++++++++++++++++ """
import cv2


class CImage:

    @classmethod
    def show(cls, img):
        cv2.imshow("img_show", img)
        key = cv2.waitKey(0)
        if key == 27:
            cv2.destroyAllWindows()

    @classmethod
    def open(cls, image_path):
        image_obj = cv2.imread(image_path)
        return image_obj

    @classmethod
    def clip(cls, image_obj, xmin, xmax, ymin, ymax):
        return image_obj[xmin:xmax, ymin:ymax]

    @classmethod
    def shape(cls, image_obj):
        return image_obj.shape

    @classmethod
    def type(cls, image_obj):
        return image_obj.dtype

    @classmethod
    def size(cls, image_obj):
        return image_obj.size

    @classmethod
    def recover(cls, image_obj_src, xmin, xmax, ymin, ymax, image_obj_dst):
        image_obj_src[xmin:xmax, ymin,ymax] = image_obj_dst
        return image_obj_src

    @classmethod
    def get_bgr(cls, image_obj):
        return cv2.split(image_obj)

    @classmethod
    def merge(cls, b, g, r):
        return cv2.merge((b, g, r))

    @classmethod
    def conversion(cls, image_obj, conversion_type):
        """
        通道转换
        :param image_obj:
        :param conversion_type:
        cv2.COLOR_BGR2RGB, 等等
        :return:
        """
        cv2.cvtColor(image_obj, conversion_type)

    @classmethod
    def make_board(cls, image_obj, top, buttom, left, right, board_type, board_color:None):
        """
        设置图片外边框
        :param image_obj:
        :param top: 单位像素
        :param buttom:
        :param left:
        :param right:
        :param board_type:
        cv2.BORDER_CONSTANT, 带颜色的边界，需要传入另外一个颜色值
        cv2.BORDER_REFLECT, 边缘元素的镜像反射做为边界
        cv2.BORDER_REFLECT_101/cv2.BORDER_DEFAULT
        cv2.BORDER_REPLICATE, 边缘元素的复制做为边界
        CV2.BORDER_WRAP
        :param board_color: 传入值类型 [0,255,0]  RGB
        :return:
        """
        return cv2.copyMakeBorder(
            image_obj,
            top, buttom, left, right,
            board_type,
            board_color
        )

    @classmethod
    def add(cls, img1, img2, mask=None):
        """
        两个图像相加
        :param img1:
        :param img2:
        :param mask:掩膜
        :return:
        """
        return cv2.add(img1, img2, mask=mask)

    @classmethod
    def add_weight(cls, img1, img1_weight, img2, img2_weight, image_const, image_type=-1):
        """
        根据不同的权重进行相加
        :param img1:
        :param img1_weight:
        :param img2:
        :param img2_weight:
        :param image_const:
        :param image_type:
        :return:
        """
        return cv2.addWeighted(img1, img1_weight, img2, img2_weight, gamma=image_const, dtype=image_type)


if __name__ == '__main__':
    image1 = CImage.open(r"D:\images\wallhaven-exxypk_2560x1600.png")
    image2 = CImage.open(r"D:\images\wallhaven-8557xj_2560x1600.png")
    add_img = CImage.add(image1, image2)
    clip_image = CImage.clip(add_img, 400, 1200, 900, 1800)
    print(clip_image)
    CImage.show(clip_image)