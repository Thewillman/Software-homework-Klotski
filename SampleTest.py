import unittest
import CreateSample as sample
import AstarFind as answer
from BeautifulReport import BeautifulReport


class NoSwapError(Exception):  # 文本不同相似度却100%

    def __init__(self):
        print("这是没强制交换前就能有解的样例欸！")

    def __str__(self, *args, **kwargs):
        return "再检查一下代码哦"


class SameMapError(Exception):  # 文本一致相似度不是100%

    def __init__(self):
        print("一样的图，为什么还要移动呢？")

    def __str__(self, *args, **kwargs):
        return "再检查一下代码哦"


class SwapError(Exception):  # 比对文本压根没有汉字，相似度直接判0

    def __init__(self):
        print("怎么没交换就出解了？")

    def __str__(self, *args, **kwargs):
        return "再检查一下代码哦"


class MoveError(Exception):
    def __init__(self):
        print("不用移动呢")

    def __str__(self):
        return "再检查一下代码哦"


class KlotskiTestCase(unittest.TestCase):

    def test_normalMap(self):
        origin, order, swap, step = sample.CreateNormalSample()
        print("开始处理正常样例……")
        operation = answer.SampleSolve(order, origin, swap, step)

    def test_noSwapMap(self):
        print("正在处理不需交换的样例……")
        origin, order, swap, step = sample.CreateNoSwapSample()
        operation = answer.SampleSolve(order, origin, swap, step)
        if len(operation) > step:
            raise NoSwapError

    def test_noAnswerAfterSwapMap(self):
        origin, order, swap, step = sample.CreateNoAnswerAfterSwapSample()
        print("正在处理无解判定在交换要求步数后的样例……")
        operation = answer.SampleSolve(order, origin, swap, step)

    def test_noAnswerBeforeSwapMap(self):
        origin, order, swap, step = sample.CreateNoAnswerBeforeSwapSample()
        print("正在处理无解判定在交换要求步数前的样例……")
        operation = answer.SampleSolve(order, origin, swap, step)

    def test_selfMap(self):
        origin, order, swap, step = sample.CreateOriginMapCheck()
        print("自己和自己比对哦~~~")
        operation = answer.SampleSolve(order, origin, swap, step)
        if len(operation) > 0:
            raise SameMapError

    def test_findAnswerAfterSwapMap(self):
        origin, order, swap, step = sample.CreateFindAnswerAfterSwapSample()
        print("正在处理交换后得解的样例……")
        operation = answer.SampleSolve(order, origin, swap, step)
        if len(operation) < step:
            raise SwapError

    def test_answerOnlyBySwapMap(self):
        origin, order, swap, step = sample.CreateAnswerOnlyBySwapSample()
        print("正在处理只交换就出解的样例……")
        operation = answer.SampleSolve(order, origin, swap, step)
        if operation[0] != ' ':
            raise MoveError


if __name__ == '__main__':
    #unittest.main()

    tests = unittest.makeSuite(KlotskiTestCase)
    runner = BeautifulReport(tests)  # => tests是通过discover查找并构建的测试套件
    runner.report(
        description='华容道测试报告',  # => 报告描述
        filename='Klotski.html',  # => 生成的报告文件名
        log_path='.'  # => 报告路径
    )

