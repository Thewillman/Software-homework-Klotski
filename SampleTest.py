import unittest
import CreateSample as sample
import AstarFind as answer
from BeautifulReport import BeautifulReport

class KlotskiTestCase(unittest.TestCase):


    def test_normalMap(self):

        origin, order, swap, step = sample.CreateNormalSample()
        print("开始处理正常样例……")
        answer.SampleSolve(order,origin,swap,step)

    def test_noSwapMap(self):
        print("正在处理不需交换的样例……")
        origin, order, swap, step = sample.CreateNoSwapSample()
        answer.SampleSolve(order, origin, swap, step)

    def test_noAnswerAfterSwapMap(self):

        origin, order, swap, step = sample.CreateNoAnswerAfterSwapSample()
        print("正在处理无解判定在交换要求步数后的样例……")
        answer.SampleSolve(order, origin, swap, step)

    def test_noAnswerBeforeSwapMap(self):

        origin, order, swap, step = sample.CreateNoAnswerBeforeSwapSample()
        print("正在处理无解判定在交换要求步数前的样例……")
        answer.SampleSolve(order, origin, swap, step)

    def test_selfMap(self):

        origin, order, swap, step = sample.CreateOriginMapCheck()
        print("自己和自己比对哦~~~")
        answer.SampleSolve(order, origin, swap, step)

    def test_findAnswerAfterSwapMap(self):

        origin, order, swap, step = sample.CreateFindAnswerAfterSwapSample()
        print("正在处理交换后得解的样例……")
        answer.SampleSolve(order, origin, swap, step)

    def test_answerOnlyBySwapMap(self):

        origin, order, swap, step = sample.CreateAnswerOnlyBySwapSample()
        print("正在处理只交换就出解的样例……")
        answer.SampleSolve(order, origin, swap, step)

if __name__ == '__main__':
    tests = unittest.makeSuite(KlotskiTestCase)
    runner = BeautifulReport(tests)  # => tests是通过discover查找并构建的测试套件
    runner.report(
        description='add函数测试报告',  # => 报告描述
        filename='Klotski.html',  # => 生成的报告文件名
        log_path='.'  # => 报告路径
    )
