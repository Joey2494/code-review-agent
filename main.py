from agent import CodeReviewAgent

def print_banner():
    print("""
==================================================
        Code Review Agent v1.0
        智能代码审查助手
==================================================
    """)


def print_help():
    """打印帮助信息"""
    print("""
使用说明：
  /review <文件路径>  - 审查代码文件
  /paste              - 粘贴代码进行审查
  /chat               - 针对审查结果追问
  /reset              - 重置对话历史
  /help               - 显示帮助
  /quit               - 退出程序
    """)


def main():
    print_banner()

    # 初始化Agent
    try:
        agent = CodeReviewAgent()
    except Exception as e:
        print(f"Agent初始化失败：{e}")
        return

    print_help()

    while True:
        try:
            user_input = input("\n请输入命令 > ").strip()

            if not user_input:
                continue

            # 退出
            if user_input in ["/quit", "/exit", "/q"]:
                print("再见！")
                break

            # 帮助
            elif user_input == "/help":
                print_help()

            # 审查文件
            elif user_input.startswith("/review"):
                parts = user_input.split(maxsplit=1)
                if len(parts) < 2:
                    print("请指定文件路径，例如：/review example.py")
                    continue

                file_path = parts[1]
                report = agent.review_file(file_path)
                print("\n" + "=" * 50)
                print(report)
                print("=" * 50)

            # 粘贴代码
            elif user_input == "/paste":
                print("请粘贴代码（输入 'END' 结束）：")
                lines = []
                while True:
                    line = input()
                    if line.strip() == "END":
                        break
                    lines.append(line)

                code = "\n".join(lines)
                if not code.strip():
                    print("代码为空")
                    continue

                filename = input("请输入文件名（如 main.py）：").strip()
                if not filename:
                    filename = "unknown.py"

                report = agent.review_code(code, filename)
                print("\n" + "=" * 50)
                print(report)
                print("=" * 50)

            # 追问
            elif user_input.startswith("/chat"):
                question = user_input.replace("/chat", "").strip()
                if not question:
                    question = input("请输入你的问题：").strip()
                if question:
                    response = agent.chat(question)
                    print(f"\n{response}")

            # 重置
            elif user_input == "/reset":
                agent.reset()

            else:
                # 默认当作追问处理
                response = agent.chat(user_input)
                print(f"\n{response}")

        except KeyboardInterrupt:
            print("\n再见！")
            break
        except Exception as e:
            print(f"发生错误：{e}")
            print("请重试...")


if __name__ == "__main__":
    main()