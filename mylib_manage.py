import json
import argparse
from rich import print as rprint
from rich.table import Table


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
    parser = argparse.ArgumentParser(description="Library Management System CLI")
    parser.add_argument("-l", "--list", action="store_true", help="List all records")
    parser.add_argument("-a", "--add", nargs=5, metavar=("BOOK_ID", "TITLE", "AUTHOR", "ISBN", "BORROWED"), help="Add a record")
    parser.add_argument("-d", "--delete", metavar="BOOK_ID", help="Delete a record")
    parser.add_argument("-s", "--show", metavar="BOOK_ID", help="Show a record")

    args = parser.parse_args()

    library_system = LibraryManagementSystem()

    if args.list:
        library_system.list_all_records()
    elif args.add:
        book_id, title, author, isbn, borrowed = args.add
        library_system.add_record(book_id, title, author, isbn, borrowed)
    elif args.delete:
        library_system.delete_record(args.delete)
    elif args.show:
        library_system.show_record(args.show)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
