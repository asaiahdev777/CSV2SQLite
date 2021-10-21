import csv
import io
import pathlib
import sqlite3
import tkinter.filedialog
from tkinter import Tk


def show_file_opener_dialog():
    tk = Tk()
    tk.withdraw()
    return tkinter.filedialog.Open(tk,
                                   title="Choose the file to convert",
                                   filetypes=[('CSV files', '.csv')]).show()


def show_save_as_dialog():
    tk = Tk()
    tk.withdraw()
    return tkinter.filedialog.SaveAs(tk,
                                     title="Choose the name of the converted file",
                                     filetypes=[('SQL DB file', '.db')],
                                     defaultextension="db").show()


def process_file(csv_path, db_path):
    with open(csv_path, mode='r', encoding='utf8') as reader:
        csv_reader = csv.reader(reader)
        first_row_read = False
        connection = sqlite3.connect(db_path)

        print('Starting...')
        for row in csv_reader:
            if not first_row_read:
                table_name = pathlib.Path(csv_path).name.split(".")[0]
                stringio = io.StringIO()
                for column in row:
                    stringio.write(f'{column} TEXT, ')
                column_statement = stringio.getvalue().rstrip(', ')
                connection.execute(f'DROP TABLE IF EXISTS {table_name}')
                connection.execute(f'CREATE TABLE {table_name} ({column_statement})')
                first_row_read = True
                stringio.close()
            else:
                for i in range(0, len(row)):
                    row[i] = f"'{row[i]}'"
                row_values = ', '.join(row)
                connection.execute(f'INSERT INTO {table_name} VALUES ({row_values})')

        print('Wrapping up...')
        connection.commit()
        print('Finished!')
        connection.close()


if __name__ == '__main__':
    process_file(show_file_opener_dialog(), show_save_as_dialog())
