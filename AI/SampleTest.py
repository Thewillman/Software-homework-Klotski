import unittest
import CreateSample as sample
import AstarFind as answer
from BeautifulReport import BeautifulReport


class NoSwapError(Exception):

    def __init__(self):
        print("这是没强制交换前就能有解的样例欸！")

    def __str__(self, *args, **kwargs):
        return "再检查一下代码哦"


class SameMapError(Exception):

    def __init__(self):
        print("一样的图，为什么还要移动呢？")

    def __str__(self, *args, **kwargs):
        return "再检查一下代码哦"


class SwapError(Exception):

    def __init__(self):
        print("怎么没交换就出解了？")

    def __str__(self, *args, **kwargs):
        return "再检查一下代码哦"


class MoveError(Exception):
    def __init__(self):
        print("不用移动呢")

    def __str__(self):
        return "再检查一下代码哦"

origin1, order1, swap1, step1 = sample.CreateNormalSample()
origin2, order2, swap2, step2 = sample.CreateNoSwapSample()
origin3, order3, swap3, step3 = sample.CreateNoAnswerAfterSwapSample()
origin4, order4, swap4, step4 = sample.CreateNoAnswerBeforeSwapSample()
origin5, order5, swap5, step5 = sample.CreateOriginMapCheck()
origin6, order6, swap6, step6 = sample.CreateFindAnswerAfterSwapSample()
origin7, order7, swap7, step7 = sample.CreateAnswerOnlyBySwapSample()

class KlotskiTestCase(unittest.TestCase):

    def test_normalMap(self):
        print("开始处理正常样例……")
        operation = sample.SampleSolve(order1, origin1, swap1, step1)

    def test_noSwapMap(self):
        print("正在处理不需交换的样例……")
        operation = sample.SampleSolve(order2, origin2, swap2, step2)
        if len(operation) > step2:
            raise NoSwapError

    def test_noAnswerAfterSwapMap(self):
        print("正在处理无解判定在交换要求步数后的样例……")
        operation = sample.SampleSolve(order3, origin3, swap3, step3)

    def test_noAnswerBeforeSwapMap(self):
        print("正在处理无解判定在交换要求步数前的样例……")
        operation = sample.SampleSolve(order4, origin4, swap4, step4)

    def test_selfMap(self):
        print("自己和自己比对哦~~~")
        operation = sample.SampleSolve(order5, origin5, swap5, step5)
        if len(operation) > 0:
            raise SameMapError

    def test_findAnswerAfterSwapMap(self):
        print("正在处理交换后得解的样例……")
        operation = sample.SampleSolve(order6, origin6, swap6, step6)
        if len(operation) < step6:
            raise SwapError

    def test_answerOnlyBySwapMap(self):
        print("正在处理只交换就出解的样例……")
        operation = sample.SampleSolve(order7, origin7, swap7, step7)
        if operation[0] != ' ':
            raise MoveError

    def test_normalMap2(self):
        print("开始处理正常样例……")
        operation = sample.SampleSolve2(order1, origin1, swap1, step1)

    def test_noSwapMap2(self):
        print("正在处理不需交换的样例……")
        operation = sample.SampleSolve2(order2, origin2, swap2, step2)
        if len(operation) > step2:
            raise NoSwapError

    def test_noAnswerAfterSwapMap2(self):
        print("正在处理无解判定在交换要求步数后的样例……")
        operation = sample.SampleSolve2(order3, origin3, swap3, step3)

    def test_noAnswerBeforeSwapMap2(self):
        print("正在处理无解判定在交换要求步数前的样例……")
        operation = sample.SampleSolve2(order4, origin4, swap4, step4)

    def test_selfMa2p(self):
        print("自己和自己比对哦~~~")
        operation = sample.SampleSolve2(order5, origin5, swap5, step5)
        if len(operation) > 0:
            raise SameMapError

    def test_findAnswerAfterSwapMap2(self):
        print("正在处理交换后得解的样例……")
        operation = sample.SampleSolve2(order6, origin6, swap6, step6)
        if len(operation) < step6:
            raise SwapError

    def test_answerOnlyBySwapMap2(self):
        print("正在处理只交换就出解的样例……")
        operation = sample.SampleSolve2(order7, origin7, swap7, step7)
        if operation[0] != ' ':
            raise MoveError

    def test_normalMap3(self):
        print("开始处理正常样例……")
        operation = sample.SampleSolve3(order1, origin1, swap1, step1)

    def test_noSwapMap3(self):
        print("正在处理不需交换的样例……")
        operation = sample.SampleSolve3(order2, origin2, swap2, step2)
        if len(operation) > step2:
            raise NoSwapError

    def test_noAnswerAfterSwapMap3(self):
        print("正在处理无解判定在交换要求步数后的样例……")
        operation = sample.SampleSolve3(order3, origin3, swap3, step3)

    def test_noAnswerBeforeSwapMap3(self):
        print("正在处理无解判定在交换要求步数前的样例……")
        operation = sample.SampleSolve3(order4, origin4, swap4, step4)

    def test_selfMap3(self):
        print("自己和自己比对哦~~~")
        operation = sample.SampleSolve3(order5, origin5, swap5, step5)
        if len(operation) > 0:
            raise SameMapError

    def test_findAnswerAfterSwapMap3(self):
        print("正在处理交换后得解的样例……")
        operation = sample.SampleSolve3(order6, origin6, swap6, step6)
        if len(operation) < step6:
            raise SwapError

    def test_answerOnlyBySwapMap3(self):
        print("正在处理只交换就出解的样例……")
        operation = sample.SampleSolve3(order7, origin7, swap7, step7)
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

