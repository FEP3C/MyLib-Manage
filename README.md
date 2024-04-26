# 图书管理系统

这是一个基于Python编写的简单图书管理系统，使用rich库美化输出，数据存储于json文件，通过命令行界面（CLI）实现图书记录的增删查操作。

＃＃功能特性

	•	数据存储：图书数据持久化保存在library_data.json文件中，便于数据管理和跨会话使用。
	•	美化输出：利用rich库呈现美观、易读的表格形式展示图书记录。
	•	命令行交互：通过命令行界面提供便捷的操作方式，无需编写Python代码即可进行图书管理。

安装与使用

1. 安装依赖

确保已安装Python环境，然后使用pip安装所需库：

```Python
pip install rich
```

2. 运行程序

将本项目克隆至本地或下载源码文件，进入项目目录，执行以下命令启动图书管理系统：

```Bash
python main.py
```

或指定具体的Python解释器路径：

```Bash
/path/to/python main.py
```

### 命令行接口

图书管理系统提供以下命令行操作：

- 列出所有记录

python main.py --list

或简写：

python main.py -l

- 添加记录

python main.py --add BOOK_ID TITLE AUTHOR ISBN [BORROWED]

其中：

	•	BOOK_ID: 图书唯一标识符。
	•	TITLE: 图书标题。
	•	AUTHOR: 作者姓名。
	•	ISBN: 图书ISBN号码。
	•	BORROWED（可选）：借阅日期，格式为YYYY-MM-DD。若图书未被借出，此项可省略。

例如：

python main.py --add B001 "Python Crash Course" "Eric Matthes" "978-1593276034" 2023-04-01

简写：

python main.py -a B001 "Python Crash Course" "Eric Matthes" "978-1593276034" 2023-04-01

删除记录

python main.py --delete BOOK_ID

例如：

python main.py --delete B001

简写：

python main.py -d B001

查看记录

python main.py --show BOOK_ID

例如：

python main.py --show B001

简写：

python main.py -s B001

数据文件

图书数据存储在library_data.json文件中。您可以直接编辑此文件以批量导入或更新图书记录，但请注意保持JSON格式的正确性。程序运行时会自动加载并保存此文件中的数据。

贡献与反馈

欢迎提出改进建议、报告问题或提交 Pull Request。如有任何疑问或需求，请创建一个 GitHub Issue 或联系项目维护者。
