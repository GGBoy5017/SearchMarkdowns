# Markdown笔记检索系统

## 项目概述
基于BM25算法实现的本地Markdown笔记全文检索工具，支持中文分词和相关性排序

## 功能特性
✅ 递归遍历指定目录下的所有.md文件
✅ 中文分词处理（结巴分词+NLTK）
✅ BM25相关性排序算法
✅ 实时交互式检索界面

## 技术栈
- Python 3.8+
- jieba (中文分词)
- rank_bm25 (排序算法)
- nltk (自然语言处理)

## 快速开始
```bash
# 安装依赖
pip install jieba rank_bm25 nltk

# 下载nltk数据包
python -m nltk.downloader punkt

# 运行程序
python main.py
```

## 路径配置
修改main.py第8行的笔记目录路径：
```python
NOTEBOOK_PATH = r"你的笔记目录绝对路径"  # 例如：r"D:\MyNotes"
NUM_RES = 3  # 显示前3个匹配结果
```

## 使用示例
```
请输入需要检索的笔记内容：机器学习
搜索结果将按相关性排序显示前3个匹配文档
```

## 项目结构
```
SearchMarkdowns/
├── main.py        # 主程序
├── README.md      # 说明文档
└── 运行.bat       # 快速启动脚本
```