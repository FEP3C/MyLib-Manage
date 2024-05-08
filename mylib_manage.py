import json
import argparse
from rich import print as rprint
from rich.table import Table
import sys


class LibraryManagementSystem:
    def __init__(self, data_file="library_data.json"):
        self.library = {}  # 初始化一个空字典作为图书数据库
        self.data_file = data_file  # JSON数据文件名
        self._load_library_from_json()

    def add_record(self, book_id, title, author, isbn, borrowed=None, returned=None):
        """
        添加图书记录
        :param book_id: 书籍号
        :param title: 书名
        :param author: 作者
        :param isbn: ISBN
        :param borrowed: 借入日期（默认为None，表示未被借出）
        :param returned: 归还日期（默认为None，表示未归还）
        """
        record = {
            "title": title,
            "author": author,
            "isbn": isbn,
            "borrowed": borrowed,
            "returned": returned,
            "ratings": []
        }
        self.library[book_id] = record
        self._save_library_to_json()

    def show_record(self, book_id):
        """
        查看指定书籍号的图书记录
        :param book_id: 书籍号
        """
        if book_id in self.library:
            record = self.library[book_id]
            table = Table(title=f"Book Record for {book_id}")
            table.add_column("Attribute", justify="left")
            table.add_column("Value", justify="left")

            table.add_row("Title", record["title"])
            table.add_row("Author", record["author"])
            table.add_row("ISBN", record["isbn"])
            table.add_row("Borrowed", record["borrowed"] or "Not Borrowed")
            table.add_row("Returned", record["returned"] or "Not Returned")

            rprint(table)
        else:
            rprint(f"[red]No record found for Book ID: {book_id}")

    def delete_record(self, book_id):
        """
        删除指定书籍号的图书记录
        :param book_id: 书籍号
        """
        if book_id in self.library:
            del self.library[book_id]
            self._save_library_to_json()
            rprint(f"Record for Book ID {book_id} has been deleted.")
        else:
            rprint(f"[red]No record found for Book ID: {book_id}")

    def list_all_records(self):
        """
        列出所有图书记录
        """
        if not self.library:
            rprint("[yellow]No records in the library.")
        else:
            table = Table(title="All Book Records")
            table.add_column("Book ID", justify="center")
            table.add_column("Title", justify="left")
            table.add_column("Author", justify="left")
            table.add_column("ISBN", justify="left")
            table.add_column("Borrowed", justify="left")
            table.add_column("Returned", justify="left")

            for book_id, record in self.library.items():
                borrowed_status = record["borrowed"] or "Not Borrowed"
                returned_status = record["returned"] or "Not Returned"
                table.add_row(
                    book_id,
                    record["title"],
                    record["author"],
                    record["isbn"],
                    borrowed_status,
                    returned_status,
                )

            rprint(table)

    def search_books(self, keyword):

            """根据书名、作者或ISBN搜索图书"""
            results = []
            for book_id, record in self.library.items():
                if keyword.lower() in record["title"].lower() or \
                keyword.lower() in record["author"].lower() or \
                keyword.lower() in record["isbn"]:
                    results.append((book_id, record))
                
            if results:
                table = Table(title=f"Search Results for '{keyword}'")
                table.add_column("Book ID", justify="center")
                table.add_column("Title", justify="left")
                table.add_column("Author", justify="left")
                table.add_column("ISBN", justify="left")

                for book_id, record in results:
                    table.add_row(book_id, record["title"], record["author"], record["isbn"])
                rprint(table)
            else:
                rprint(f"[yellow]No results found for '{keyword}'.")


    def rate_book(self, book_id, rating):

        """给书籍打分"""

        if book_id in self.library and 1 <= rating <= 5:
            self.library[book_id]["ratings"].append(rating)
            rprint(f"感谢您的评分！书籍 {book_id} 已经被打分为 {rating} 分。")
        else:
            rprint("[red]无法为该书籍打分，请检查书籍号是否正确或分数是否在1-5之间。")


    def show_rating(self, book_id):
        """显示书籍的平均评分"""
        if book_id in self.library:
            ratings = self.library[book_id].get("ratings", [])
            if ratings:
                average_rating = sum(ratings) / len(ratings)
                rprint(f"书籍 {book_id} 的平均评分为 {average_rating:.2f} 分。")
            else:
                rprint(f"[yellow]书籍 {book_id} 尚无评分。")
        else:
            rprint("[red]未找到该书籍。")

    def borrow_book(self, book_id, borrower_name):
        """借阅书籍"""
        if book_id in self.library and self.library[book_id]["borrower"] is None:
            self.library[book_id]["borrower"] = borrower_name
            self.library[book_id]["borrowed"] = "Now"  # 假设添加借出日期逻辑
            rprint(f"书籍 {book_id} 已被 {borrower_name} 借走。")
            self._save_library_to_json()
        else:
            rprint("[red]该书籍已被借出或不存在。")

    def return_book(self, book_id):
        """归还书籍"""
        if book_id in self.library and self.library[book_id]["borrower"] is not None:
            self.library[book_id]["borrower"] = None
            self.library[book_id]["borrowed"] = None  # 假设修改归还日期逻辑
            rprint(f"书籍 {book_id} 已成功归还。")
            self._save_library_to_json()
        else:
            rprint("[red]该书籍未被借出或不存在。")


    def _load_library_from_json(self):
        try:
            with open(self.data_file, "r") as f:
                self.library = json.load(f)
        except FileNotFoundError:
            pass  # 如果文件不存在，保持空字典即可

    def _save_library_to_json(self):
        with open(self.data_file, "w") as f:
            json.dump(self.library, f, indent=4)

def main():
    parser = argparse.ArgumentParser(description="图书管理系统命令行界面",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-l", "--list", action="store_true", help="列出所有图书记录")
    parser.add_argument("-a", "--add", action="store_true", help="交互式添加一本图书记录")
    parser.add_argument("-d", "--delete", metavar="BOOK_ID", help="根据书籍号删除一条记录")
    parser.add_argument("-s", "--show", metavar="BOOK_ID", help="查看书籍号对应的图书记录")


    # 当没有提供任何参数时，显示欢迎和使用说明
    if len(sys.argv) == 1:
        print_welcome_and_usage()
        return

    args = parser.parse_args()

    library_system = LibraryManagementSystem()

    if args.list:
        library_system.list_all_records()
    elif args.add:
        rprint("[bold green]欢迎来到图书管理系统！")
        book_id = input("请输入书籍号：")
        title = input("请输入书名：")
        author = input("请输入作者：")
        isbn = input("请输入ISBN：")
        library_system.add_record(book_id, title, author, isbn)
        rprint("[bold green]添加中...")
        rprint("[bold green]添加成功！")
    elif args.show:
        library_system.show_record(args.show)
    elif args.rate:
        book_id, rating = args.rate
        library_system.rate_book(book_id, int(rating))
    elif args.get_rating:
        library_system.show_rating(args.get_rating)
    elif args.borrow:
        book_id, borrower_name = args.borrow
        library_system.borrow_book(book_id, borrower_name)
    elif args.return_book:
        library_system.return_book(args.return_book)
    elif args.search:
        keyword = args.search
        library_system.search_books(keyword)
    else:
        parser.print_help()

def print_welcome_and_usage():
        """打印欢迎信息及使用说明"""
        rprint("[bold magenta]欢迎使用图书管理系统 MyLib-Manage！[/]")
        rprint("请输入以下命令之一以开始操作:")
        rprint("[bold cyan]-l, --list[/]: 列出所有图书记录。")
        rprint("[bold cyan]-a, --add[/]: 交互式添加一本图书记录。")
        rprint("[bold cyan]-d, --delete BOOK_ID[/]: 根据书籍号删除一条记录。")
        rprint("[bold cyan]-s, --show BOOK_ID[/]: 查看书籍号对应的图书记录。")
        rprint("[bold cyan]-r, --rate BOOK_ID RATING[/]: 为书籍打分。")
        rprint("[bold cyan]-g, --get-rating BOOK_ID[/]: 获取书籍的平均评分。")
        rprint("[bold cyan]-b, --borrow BOOK_ID BORROWER_NAME[/]: 借阅书籍。")
        rprint("[bold cyan]-rt, --return-book BOOK_ID[/]: 归还书籍。")
        rprint("[bold cyan]-search KEYWORD[/]: 根据书名、作者或ISBN搜索图书。")
        rprint("若需更多帮助，请使用 [--help] 参数。")

if __name__ == "__main__":
    main()
