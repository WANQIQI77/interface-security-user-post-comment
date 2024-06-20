# -*- coding: utf-8 -*-
# @Time    : 2024/6/13  21:51
# @Author  : WanQiQi
# @FileName: check.py
# @Software: PyCharm
"""
    Description:
        
"""
def resource_limit(check_dict={}, **kwargs):
    """
    资源限制函数
    :param check_dict: 检查字典，定义每个参数的最大值
    :param kwargs: 传入的参数
    :return: 处理后的参数
    """
    for param, value in kwargs.items():
        if param in check_dict:
            size = check_dict[param]
            if len(value) > size:
                del kwargs[param]
                break
    return kwargs
