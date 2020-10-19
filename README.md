# Soft-work（华容道）

## 徽章

<img src="https://img.shields.io/badge/Language-python-brightgreen" alt="Language" align="left"/><img src="https://img.shields.io/badge/Tool-PyQt5-yellowgreen" alt="Tools" align="left"/><img src="https://img.shields.io/badge/Tool-unittest-orange" alt="Tools" align="left"/>



## 运行环境

- Win64 or Linux

## 编译方法

### 游戏GUI：

- 命令行python start.py
- IDE运行

### AI算法：

- 命令行python AstarFind2.py
- IDE运行

## AI大比拼文件：

- AIFighting.py跑的是我们队当前没挑战的所有题目，可以修改为跑所有题目，具体修改方法看“使用方法”
- AIFightingSingle.py负责针对单个问题进行测试。
- 运行方法也是IDE运行/命令行直接运行py文件（不需要传参数） 

## 使用方法

### 游戏GUI：

- 上下左右或WASD控制

- 简单游戏分为3X3、4X4和5X5的数字华容道，其中仅有3X3模式提供AI演示功能

- 通关挑战首先为3X3，当通关数达到2关后变为4X4，当通关数为4关后变为5X5，其中3X3模式提供

- AI演示功能，当您打开AI演示，计时器会增加20秒时间，并且不会停止

- AI挑战能够记录您完成游戏后走的步数与游戏AI走的步数差，并记录您的完成时间

- AI演示功能分为动画演示功能和逐步演示功能，当您打开AI演示后，将关闭您的按键直到您关闭

  AI演示·通关排名和AI排名将分别记录您的游戏记录

### AI算法

- AstarFind2.py:本程序采用了requests获取和提交题目，我们只要在**main程序第一行的getProblemOrder函数参数修改学号**即可完成题目要求的拿题->解题->交题操作，非常的轻便，不需要用到Postman

- AIFighting.py:如果需要**改成跑所有题目的话，把main程序段下第一行的url改为"http://47.102.118.1:8089/api/challenge/list"**

- AIFightingSingle.py:main程序第一行getProblemOrder函数的**第一个参数是teamid，第二个参数是问题的uuid，第三个参数是我们team的token，在这里作修改即可对单个问题进行测试**

  





















