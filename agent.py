import dashscope
from dashscope import Generation
from config import DASHSCOPE_API_KEY, MODEL_NAME, TEMPERATURE
from prompts import SYSTEM_PROMPT, REVIEW_PROMPT, CHAT_PROMPT
from tools import read_file, execute_code, count_lines, detect_language


class CodeReviewAgent:
    """代码审查Agent"""

    def __init__(self):
        # 设置API Key
        dashscope.api_key = DASHSCOPE_API_KEY

        # 上下文记忆
        self.conversation_history = []

        # 初始化系统提示
        self.conversation_history.append({
            "role": "system",
            "content": SYSTEM_PROMPT
        })

        # 注册工具
        self.tools = {
            "read_file": read_file,
            "execute_code": execute_code,
            "count_lines": count_lines,
            "detect_language": detect_language
        }

        print("代码审查Agent已初始化")

    def call_llm(self, messages: list) -> str:
        """调用LLM获取回复"""
        try:
            response = Generation.call(
                model=MODEL_NAME,
                messages=messages,
                temperature=TEMPERATURE,
                result_format='message'
            )

            if response.status_code == 200:
                return response.output.choices[0].message.content
            else:
                return f"LLM调用失败：{response.code} - {response.message}"

        except Exception as e:
            return f"LLM调用异常：{str(e)}"

    def use_tool(self, tool_name: str, **kwargs):
        """调用工具"""
        if tool_name in self.tools:
            print(f"  调用工具：{tool_name}")
            result = self.tools[tool_name](**kwargs)
            print(f"  工具返回成功")
            return result
        else:
            return f"未找到工具：{tool_name}"

    def review_code(self, code: str, filename: str = "unknown.py") -> str:
        """
        Agent主循环：输入 -> 推理 -> 工具调用 -> 输出
        """
        print("\n" + "=" * 50)
        print("开始代码审查...")
        print("=" * 50)

        print("\n步骤1：检测编程语言")
        language = self.use_tool("detect_language", filename=filename)
        print(f"  检测结果：{language}")

        print("\n步骤2：统计代码信息")
        stats = self.use_tool("count_lines", code=code)
        for key, value in stats.items():
            print(f"  {key}：{value}")

        print("\n步骤3：尝试执行代码")
        if language == "python":
            exec_result = self.use_tool("execute_code", code=code, language=language)
            print(f"  执行结果：{exec_result[:100]}...")
        else:
            exec_result = "非Python代码，跳过执行"
            print(f"  {exec_result}")

        print("\n步骤4：调用LLM生成审查报告...")

        # 构造完整的审查请求
        review_message = REVIEW_PROMPT.format(
            language=language,
            filename=filename,
            code=code
        )

        # 添加工具收集到的额外信息
        review_message += f"\n\n--- 工具分析结果 ---\n"
        review_message += f"代码统计：{stats}\n"
        review_message += f"执行结果：{exec_result}\n"

        # 添加到对话历史
        self.conversation_history.append({
            "role": "user",
            "content": review_message
        })

        # 调用LLM
        report = self.call_llm(self.conversation_history)

        # 保存LLM回复到历史
        self.conversation_history.append({
            "role": "assistant",
            "content": report
        })

        print("审查报告生成完成！\n")
        return report

    def review_file(self, file_path: str) -> str:
        """审查代码文件"""
        print(f"\n读取文件：{file_path}")
        code = self.use_tool("read_file", file_path=file_path)

        if code.startswith("错误"):
            return code

        filename = file_path.split("/")[-1].split("\\")[-1]
        return self.review_code(code, filename)

    def chat(self, question: str) -> str:
        """追问/对话功能（支持上下文记忆）"""
        print(f"\n用户追问：{question}")

        chat_message = CHAT_PROMPT.format(question=question)

        self.conversation_history.append({
            "role": "user",
            "content": chat_message
        })

        response = self.call_llm(self.conversation_history)

        self.conversation_history.append({
            "role": "assistant",
            "content": response
        })

        return response

    def reset(self):
        """重置对话历史"""
        self.conversation_history = [{
            "role": "system",
            "content": SYSTEM_PROMPT
        }]
        print("对话历史已重置")