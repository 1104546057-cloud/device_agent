from pathlib import Path
import re

# 读取文本文件内容
def load_text(file_path: str| Path) -> str: 

    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")

    text = path.read_text(encoding="utf-8")

    return text

# 清理文本内容，去除多余的空格和换行符
def clean_text(text:str) -> str:

    text = text.replace("\r\n", "\n")  # 将 Windows 风格的换行符替换为 Unix 风格
    text = text.replace("\r", "\n")    # 将旧 Mac 风格的换行符替换为 Unix 风格

    text = re.sub(r"[ \t]+", " ", text)  # 将多个空格或制表符替换为一个空格
    text = re.sub(r"\n{3,}", "\n\n", text)  # 将三个或更多连续的换行符替换为两个换行符

    return text.strip()  # 去除文本开头和结尾的空白字符

if __name__ == "__main__":

    path = Path("/Users/hu/device_agent/manuals/agv_manual.txt")

    content = load_text(path)
    print("原始内容:\n", content)
    print(type(content))
    content = clean_text(content)
    print("\n=== 清理后的内容 ===\n", content)

