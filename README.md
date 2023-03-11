# oo_xgenerator

### 介绍
buaa面向对象第一单元第三次作业评测机

以完全满足评测要求为目标，包括函数调用嵌套、只有一处求导等要求

### 概述

使用python自带库tkinte绘制gui，使用递归下降方式随机生成表达式，可多线程运行、残余jar进程自动清理、运行结果实时显示。

全GUI操作、AC/WA/TLE/RE识别。

### 注意事项

在尚未运行结束时，同目录下的tle记录不可信，只是起到缓存作用。请在程序运行结束后再查看同目录的tle文件。

### 结果位置

保存错误结果到`./hacklist.txt`，保存tle、re数据到`./tle_...`和`./re_...`

### 使用说明

1.  配置python3环境
2.  同目录下执行`pip install -r requirements.txt`安装依赖
3.  将待评测jar放于同目录下，可以放置多个jar文件
4.  运行`python ./main.py`，设置评测次数，点击run！
