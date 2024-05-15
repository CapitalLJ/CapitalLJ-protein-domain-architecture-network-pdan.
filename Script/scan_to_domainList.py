import re
import sys

def process_block(block):
    # 使用正则表达式匹配并提取需要的信息
    query_match = re.search(r'Query:\s+(.*?)\s+', block)
    description_match = re.search(r'Description:\s+(.*?)\s+', block)
    domains_match = re.findall(r'>>\s+(.*?)\s+', block)

    # 根据要求组织输出信息
    query = query_match.group(1) if query_match else ''
    description = description_match.group(1) if description_match else ''
    domains = '\t'.join(domains_match) if domains_match else ''

    return f"Query: {query}\nDescription: {description}\nDomains: {domains}\n"

if len(sys.argv) != 3:
    print("Usage: python process_text_files.py input_file output_file")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

# 读取输入文件内容
with open(input_file, 'r') as file:
    content = file.read()

# 使用正则表达式将文本内容分割成块
blocks = re.split(r'(?<!//)\n//\s*\n', content)

# 处理每个块并写入输出文件
with open(output_file, 'w') as outfile:
    for block in blocks:
        processed_block = process_block(block)
        outfile.write(processed_block)
        outfile.write("\n")  # 用于分隔不同块的输出
