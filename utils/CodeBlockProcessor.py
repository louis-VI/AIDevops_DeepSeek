# 在 CodeBlockProcessor 类中，添加一个参数 output_dir，用于指定代码保存的目录。默认情况下，代码将保存到 scripts 目录下。

import re
import os
from pathlib import Path

class CodeBlockProcessor:
    def __init__(self, text, output_dir=None):
        """
        初始化 CodeBlockProcessor 类。
        :param text: 包含代码块的文本。
        :param output_dir: 代码保存的目录，默认为项目根目录下的 "scripts" 文件夹。
        """
        self.text = text
        self.matches = []
        # 设置 output_dir 为绝对路径
        self.output_dir = output_dir if output_dir else str(Path(__file__).parent / "scripts")
        print(f"输出目录: {self.output_dir}")

    def extract_code_blocks(self):
        """
        使用正则表达式提取被 ``` 包裹的代码块。
        """
        pattern = r'```(.*?)```'
        self.matches = re.findall(pattern, self.text, re.DOTALL)
        print(f"提取到 {len(self.matches)} 个代码块")
        return self.matches

    def determine_code_type(self, code_block):
        """
        判断代码块的类型。
        :param code_block: 代码块内容。
        :return: 代码类型（'python' 或 'shell'）。
        """
        if code_block.startswith("python") or "import" in code_block or "def " in code_block:
            return "python"
        elif code_block.startswith("shell") or "#!/bin/bash" in code_block:
            return "shell"
        else:
            return "unknown"

    def save_code_block(self, code_block, index):
        """
        将代码块保存为文件。
        :param code_block: 代码块内容。
        :param index: 代码块的序号。
        """
        # 打印调试信息
        print(f"正在处理代码块 {index + 1}...")
        print(f"代码内容:\n{code_block}")

        # 判断代码类型
        code_type = self.determine_code_type(code_block)
        print(f"代码类型: {code_type}")

        # 去除代码块的第一行（如 "python" 或 "shell"）
        code_lines = code_block.split("\n")
        if len(code_lines) > 1 and (code_lines[0].strip() in ["python", "shell"]):
            code_content = "\n".join(code_lines[1:]).strip()
        else:
            code_content = code_block.strip()

        # 如果是 Python 代码，处理缩进
        if code_type == "python":
            code_lines = code_content.split("\n")
            if code_lines:
                # 找到 def 行的缩进量
                def_indent = 0
                for line in code_lines:
                    if line.strip().startswith("def "):
                        def_indent = len(line) - len(line.lstrip())
                        break
                # 调整缩进：函数定义和方法体保持原样，函数调用与 def 对齐
                adjusted_lines = []
                in_function = False
                for line in code_lines:
                    stripped_line = line.strip()
                    if stripped_line.startswith("def "):
                        in_function = True
                        adjusted_lines.append(line[def_indent:])  # 保持 def 行的缩进
                    elif in_function and stripped_line:  # 方法体部分
                        adjusted_lines.append(line[def_indent:])  # 保持方法体的缩进
                    elif in_function and not stripped_line:  # 方法体内的空行
                        adjusted_lines.append(line[def_indent:])  # 保持空行的缩进
                    else:  # 函数调用部分
                        adjusted_lines.append(line[def_indent:].lstrip())  # 与 def 对齐
                code_content = "\n".join(adjusted_lines)

        # 创建输出目录（如果不存在）
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"创建目录: {self.output_dir}")

        # 生成文件名
        if code_type == "python":
            file_name = f"{self.output_dir}/code_block_{index + 1}.py"
        elif code_type == "shell":
            file_name = f"{self.output_dir}/code_block_{index + 1}.sh"
        else:
            file_name = f"{self.output_dir}/code_block_{index + 1}.txt"

        # 保存文件
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(code_content)

        print(f"代码块 {index + 1} 已保存为 {file_name}")

    def process(self):
        """
        处理文本中的所有代码块。
        """
        # 提取代码块
        self.extract_code_blocks()

        # 保存每个代码块
        for i, match in enumerate(self.matches):
            self.save_code_block(match, i)