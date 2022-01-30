
```text
usage: atbash.py [-h] [--text TEXT] [--file FILE] [--output OUTPUT] [--lookup-table LOOKUP_TABLE]

optional arguments:
  -h, --help            show this help message and exit
  --text TEXT
  --file FILE
  --output OUTPUT
  --lookup-table LOOKUP_TABLE

```
# Text Encrypt/Decrypt
- encrypt plain text message;
```bash
$ ./atbash.py encrypt --text 'Hello World'

Svool Dliow

```

- decrypt cipher text message:
```bash
$ ./atbash.py decrypt --text 'Svool Dliow' 

Hello World

```

# File Encrypt/Decrypt
- encrypt file;
```bash
$ ./atbash.py encrypt --file test.txt
```
- decrypt file:
```bash
$ ./atbash.py decrypt --file atbash_test.txt
```