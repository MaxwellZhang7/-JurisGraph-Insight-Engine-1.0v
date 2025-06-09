class SimpleQASystem:
    def __init__(self):
        self.qa_data = {
            '什么是人工智能': '人工智能是一门研究如何使计算机能够完成一些通常需要人类智能才能完成的任务的学科。',
            'Python有什么特点': 'Python是一种高级、通用、解释型、交互式的编程语言。',
            'Flask是什么': 'Flask是一个轻量级的Web框架，用于快速构建Web应用程序。',
            '机器学习是什么': '机器学习是一种人工智能（AI）的分支，通过从数据中学习并进行模式识别，使计算机系统能够自动执行特定任务，而无需明确的编程。',
        }

    def answer_question(self, question):
        return self.qa_data.get(question, '抱歉，我不知道答案。')

# 在脚本末尾添加以下内容以测试
if __name__ == '__main__':
    qa_system = SimpleQASystem()
    while True:
        user_input = input('请输入你的问题（输入 q 退出）: ')
        if user_input.lower() == 'q':
            break
        answer = qa_system.answer_question(user_input)
        print('回答:', answer)
