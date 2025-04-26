import jieba
import re
from rank_bm25 import BM25Okapi
from nltk.tokenize import word_tokenize
import os

#学习笔记的存放的总目录
NOTEBOOK_PATH= r"D:\BaiduSyncdisk\学习笔记"
NUM_RES=3


# 对文本进行分词
def tokenize(text):
    return word_tokenize(text)

def get_markdown_files(folder_path):
    """
    递归遍历指定文件夹下的所有Markdown文件，并返回它们的文件名和路径。
    """
    # 初始化Markdown文件列表
    markdown_files = []

    # 遍历文件夹内的所有文件和子文件夹
    for root, dirs, files in os.walk(folder_path):
        # 遍历当前文件夹内的所有Markdown文件
        for file_name in files:
            if file_name.endswith(".md"):
                # 如果当前文件是Markdown文件，将其文件名和路径添加到Markdown文件列表中
                file_path = os.path.join(root, file_name)
                markdown_files.append((file_name, file_path))

        # 遍历当前文件夹内的所有子文件夹
        for dir_name in dirs:
            # 递归调用get_markdown_files()函数，处理当前子文件夹内的所有文件
            dir_path = os.path.join(root, dir_name)
            markdown_files += get_markdown_files(dir_path)

    return markdown_files

def get_markdown_files_dict(folder_path):
    """
    递归遍历指定文件夹下的所有Markdown文件，并返回它们的文件名和路径。
    """
    # 初始化Markdown文件列表
    markdown_files = {}

    # 遍历文件夹内的所有文件和子文件夹
    for root, dirs, files in os.walk(folder_path):
        # 遍历当前文件夹内的所有Markdown文件
        for file_name in files:
            if file_name.endswith(".md"):
                # 如果当前文件是Markdown文件，将其文件名和路径添加到Markdown文件列表中
                file_path = os.path.join(root, file_name)
                markdown_files[file_name]=file_path


        # 遍历当前文件夹内的所有子文件夹
        for dir_name in dirs:
            # 递归调用get_markdown_files()函数，处理当前子文件夹内的所有文件
            dir_path = os.path.join(root, dir_name)
            markdown_files = {**markdown_files, **get_markdown_files_dict(dir_path)}

    return markdown_files


def get_html_files(markdown_files):
    html_files=[]

    # 遍历Markdown文件，并输出文件名和路径
    for file_name, file_path in markdown_files:
        with open(file_path, "r", encoding='utf-8') as f:
            markdown_string = f.read()
        html_files.append((file_name,markdown_string))
    return html_files
def init():
    """
    作用：初始化笔记路径
    return: html文件和文件路径
    """
    # 指定文件夹路径
    folder_path=NOTEBOOK_PATH

    #匹配所有Markdown文件
    markdown_files=get_markdown_files(folder_path)
    path_dict=get_markdown_files_dict(folder_path)

    # 将Markdown格式的文本转换为HTML格式的文本
    html_files=get_html_files(markdown_files)
    return html_files,path_dict


#第一个版本：使用正则表达式（regular expression，regex）对文本进行匹配，效率低，已经弃用。
def match(pattern):
    hit_htmls = {}
    for file_name, file_html in html_files:
        match = re.search(pattern, file_html, re.DOTALL)
        if match:  # 匹配成功，处理结果
            # 如果匹配很多需要采取何种方式排序呢？
            # print("file name:{0}\nfile path:{1}".format(file_name,path_dict[file_name]))
            hit_htmls[file_name] = file_html
        else:  # 匹配失败
            pass
    return hit_htmls

# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':

    #初始化
    html_files,path_dict=init()
    hit_htmls = {}
    for file_name, file_html in html_files:
        hit_htmls[file_name] = file_html

    # 定义文档集合
    documents = dict(html_files).values()
    print("将文档集合中的每个文档分词并转换为一个由单词组成的列表，时间过长请检查小文件是不是太多了")
    # 将文档集合中的每个文档分词并转换为一个由单词组成的列表
    tokenized_documents = [list(jieba.cut(document,cut_all=True,use_paddle=True)) for document in documents]

    # 构建 BM25 模型并对文档集合进行索引
    bm25 = BM25Okapi(tokenized_documents)
    #https://farer.org/2018/09/19/practical-bm25-part-2-the-bm25-algorithm-and-its-variables/

    while True:
        keyword=input("请输入需要检索的笔记内容：")
        tokenized_query = list(jieba.cut(keyword))
        doc_scores = bm25.get_scores(tokenized_query)
        i=1
        # 输出检索结果
        for document_index, score in sorted(enumerate(doc_scores), key=lambda x: x[1], reverse=True):
            print(f"Document {list(hit_htmls.keys())[document_index]} - Score: {score:.4f}")
            i+=1
            if(i>NUM_RES):
                break