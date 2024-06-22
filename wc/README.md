# WC in python

Rewriting of WC program in python but with a pretty output

Install the following dependency

```
pip install prettytable
```

Usage:

```
python wc.py -h

usage: wc.py [-h] [-w] [-k] [-l] [-c] [file]

Word count in a file and display the size of the file

positional arguments:
  file             Path to the file or cat <filename> | python wc.py

options:
  -h, --help       show this help message and exit
  -w, --words      to count the number of words
  -k, --kilobytes  convert to kilobytes
  -l, --lines      total lines
  -c, --size       total lines
```


