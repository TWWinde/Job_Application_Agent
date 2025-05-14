

def read_txt_as_single_line(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    # 替换换行符和多余空白，将多段合并为一行
    single_line = ' '.join(text.split())
    return single_line



if __name__ == "__main__":
    # 示例用法
    file_path = '/Users/tangwenwu/Documents/GitHub/Job_Application_Agent/job_txt/PhD Position Embedded Active Inference for Autonomous Robots.txt'  # 替换成你的文件路径
    result = read_txt_as_single_line(file_path)
    print(result)