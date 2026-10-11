import os
import subprocess
import tempfile
def read_file(file_path: str) -> str:
    """读取代码文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        return f"错误：文件 '{file_path}' 不存在"
    except Exception as e:
        return f"读取文件出错：{str(e)}"
def execute_code(code: str, language: str = "python") -> str:
    """执行代码并返回结果"""
    if language == "python":
        try:
            with tempfile.NamedTemporaryFile(
                mode='w', suffix='.py', delete=False, encoding='utf-8'
            ) as f:
                f.write(code)
                temp_path = f.name
            result = subprocess.run(
                ['python', temp_path],
                capture_output=True,
                text=True,
                timeout=5
            )
            output = ""
            if result.stdout:
                output += f"标准输出：\n{result.stdout}\n"
            if result.stderr:
                output += f"错误输出：\n{result.stderr}\n"
            if not output:
                output = "代码执行成功，无输出"
            return output
        except subprocess.TimeoutExpired:
            return "错误：代码执行超时（超过5秒）"
        except Exception as e:
            return f"执行出错：{str(e)}"
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
    else:
        return f"暂不支持 {language} 语言的执行"
def count_lines(code: str) -> dict:
    """统计代码行数信息"""
    lines = code.split('\n')
    total = len(lines)
    blank = sum(1 for line in lines if line.strip() == '')
    comment = sum(1 for line in lines if line.strip().startswith('#'))
    code_lines = total - blank - comment
    return {
        "总行数": total,
        "代码行": code_lines,
        "空白行": blank,
        "注释行": comment
    }
def detect_language(filename: str) -> str:
    """根据文件扩展名检测编程语言"""
    ext_map = {
        '.py': 'python',
        '.js': 'javascript',
        '.ts': 'typescript',
        '.java': 'java',
        '.cpp': 'cpp',
        '.c': 'c',
        '.go': 'go',
        '.rs': 'rust',
    }
    _, ext = os.path.splitext(filename)
    return ext_map.get(ext, 'unknown')