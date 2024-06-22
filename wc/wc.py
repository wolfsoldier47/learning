import argparse
import os
from prettytable import PrettyTable
import sys
def file_size_kilobytes(file):
    file_size_total = os.stat(file)
    return (file_size_total.st_size/1024.0)  

def file_size(file):
    file_size_total = os.stat(file)
    return file_size_total.st_size

def total_words_and_lines(file):
    try:
        with open(file, 'r') as file_open:
            lines = file_open.readlines()
            num_lines = len(lines)
            text = ' '.join(lines)  # Combine all lines into a single string
            words = text.split()    # Split the string into words
            num_words = len(words)

        return num_lines, num_words
    except Exception as e:
        raise Exception(f"Error reading file: {e}")

def total_words_only(file):
    try:
        with open(file, 'r') as file_open:
            lines = file_open.readlines()
            text = ' '.join(lines)  # Combine all lines into a single string
            words = text.split()    # Split the string into words
            num_words = len(words)

        return num_words
    except Exception as e:
        raise Exception(f"Error reading file: {e}")

def parse_arguments():
    parser = argparse.ArgumentParser(description="Word count in a file and display the size of the file")
    parser.add_argument('file', nargs='?',type=str, help="Path to the file or cat <filename> | python wc.py")
    # parser.add_argument('-h','--help',help="print helps",action='help')
    parser.add_argument("-w",'--words',help="to count the number of words",action="store_true")
    parser.add_argument('-k','--kilobytes',help="convert to kilobytes",action="store_true")
    parser.add_argument('-l','--lines',help="total lines",action="store_true")
    parser.add_argument('-c','--size',help="total lines",action="store_true")
    return parser.parse_args()



def parsing():
    stdin = False
    args = parse_arguments()


    if args.file:
        if args.kilobytes:
            size_file = file_size_kilobytes(args.file)
            type_unit = "KiloBytes"
        elif args.file:
            size_file = file_size(args.file)
            type_unit = "Bytes"
    elif sys.stdin:
        file_content = sys.stdin.read()
        stdin = True


    if not stdin:
        if args.lines and args.words:
            total_lines,total_words = total_words_and_lines(args.file)
            table = PrettyTable(["lines","Words", "File Name"])
            table.add_row([total_lines,total_words, args.file])
            print(table)
        elif args.lines:
            total_lines,total_words = total_words_and_lines(args.file)
            table = PrettyTable(["lines", "File Name"])
            table.add_row([total_lines, args.file])
            print(table)

        elif args.words:
            words_total = total_words_only(args.file)
            table = PrettyTable(["Total Words", "File Name"])
            table.add_row([words_total, args.file])
            print(table)
        elif args.size:
            table = PrettyTable([ f"Size ({type_unit})", "File Name"])
            table.add_row([ f"{size_file:.3f}", args.file])
            print(table)
        elif args.file:
            total_lines,total_words = total_words_and_lines(args.file)
            table = PrettyTable(["lines","Words", f"Size ({type_unit})", "File Name"])
            table.add_row([total_lines,total_words, f"{size_file:.3f}", args.file])
            print(table)
    elif stdin:
        if args.lines:
            line_count = len(file_content.split('\n')) 
            table = PrettyTable(["lines", "STDIN"])
            table.add_row([line_count, "STDIN"])
            print(table)
 

if __name__ == "__main__":
    parsing()