#!/usr/bin/env python3
import argparse
import itertools
import os.path
import string
import sys
import typing


class ATBashCipher:
    """
    https://en.wikipedia.org/wiki/Atbash
    """

    def __init__(self, **kwargs):
        # in case we want to create own lookup_table
        if lt := kwargs.get("lookup_table"):
            if not isinstance(lt, dict):
                raise ValueError(f"lookup_table is not dict!")

            self.lookup_table = lt
        else:
            # use default ASCII
            self.lookup_table = {}

            reversed_ascii = list(string.ascii_uppercase[::-1])
            self.lookup_table = {l1: l2 for l1, l2 in
                                 itertools.zip_longest(list(string.ascii_uppercase), reversed_ascii, fillvalue=None)}

    def encrypt(self, plain_text: str):
        if not self.lookup_table:
            raise ValueError(f"lookup_table is empty!")
        chars = []
        for c in plain_text:
            # check if char exists in lookup table
            transformed_char: str
            if transformed_char := self.lookup_table.get(c.upper()):
                if not c.isupper():
                    chars.append(
                        transformed_char.lower())
                else:
                    chars.append(transformed_char)
            else:
                chars.append(c)

        return "".join(chars)

    def decrypt(self, cipher_text: str):
        chars = []
        reverse_lookup_table = {v: k for k, v in dict(self.lookup_table).items()}
        for c in cipher_text:
            transformed_char: str
            if transformed_char := reverse_lookup_table.get(c.upper()):
                if not c.isupper():
                    chars.append(
                        transformed_char.lower())
                else:
                    chars.append(transformed_char)
            else:
                chars.append(c)
        return "".join(chars)


class SharedARGS:

    def __call__(self, parser: argparse.ArgumentParser, *args, **kwargs):
        parser.add_argument(
            "--text",
            required=False
        )
        parser.add_argument(
            "--file",
            required=False
        )
        parser.add_argument(
            "--output",
            required=False,
            default=None,
        )
        parser.add_argument(
            "--lookup-table",
            required=False
        )


class CliManager:
    usage = """
    ./atbash.py <command> [<args>] -h 
        The most commonly used commands are:
        - encrypt     encrypt plain text to "Atbash".
        - decrypt     decrypt from "Atbash" to plain text.
    """
    epilog = ""
    description = ""

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            usage=self.usage,
            epilog=self.epilog,
            description=self.description,
        )

    def __call__(self, *args, **kwargs):
        self.parser.add_argument('command', help='Sub-Command to run')
        args = self.parser.parse_args(sys.argv[1:2])
        sub_command = "_" + args.command
        if not hasattr(self, sub_command):
            print('Unrecognized command')
            self.parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        handler = getattr(self, sub_command)
        parser = argparse.ArgumentParser()
        try:
            handler(parser)
        except Exception as exc:
            print(exc)

    def _encrypt(self, parser: argparse.ArgumentParser = None):

        argument_classes = [
            SharedARGS(),
        ]
        [cls(parser) for cls in argument_classes]
        args: argparse.Namespace = parser.parse_args(sys.argv[2:])
        self.exec_encrypt(args)

    def _decrypt(self, parser: argparse.ArgumentParser = None):
        argument_classes = [
            SharedARGS(),
        ]
        [cls(parser) for cls in argument_classes]
        args: argparse.Namespace = parser.parse_args(sys.argv[2:])
        self.exec_decrypt(args)

    @staticmethod
    def read_file(path: str) -> typing.Tuple[str, str]:

        if os.path.exists(path) and os.path.isfile(path):
            file_name: str = os.path.split(path)[-1]
            with open(path, 'r') as f:
                return file_name, f.read()
        else:
            raise ValueError(f"path: {path} dose not exists or is not file!")

    @staticmethod
    def write_file(path: str, content: str):

        with open(path, 'w') as f:
            f.write(content)

    def exec_encrypt(self, args: argparse.Namespace):
        kwargs = {}
        if args.lookup_table:
            kwargs["lookup_table"] = args.lookup_table

        cipher = ATBashCipher(**kwargs)

        if args.text:
            print(cipher.encrypt(args.text))
        elif args.file:
            file_name, content = self.read_file(args.file)
            if not args.output:
                output = "atbash_" + file_name
            else:
                output = args.output
            cipher_text: str = cipher.encrypt(content)
            self.write_file(output, cipher_text)
            print(f"Encrypted: {output}")

        else:
            raise ValueError(f"No --text or --file ")

    def exec_decrypt(self, args: argparse.Namespace):
        kwargs = {}
        if args.lookup_table:
            kwargs["lookup_table"] = args.lookup_table

        cipher = ATBashCipher(**kwargs)
        if args.text:
            print(cipher.decrypt(args.text))
        elif args.file:
            file_name, content = self.read_file(args.file)
            if not args.output:
                output = "decrypted_" + file_name
            else:
                output = args.output
            cipher_text: str = cipher.decrypt(content)
            self.write_file(output, cipher_text)
            print(f"Decrypted: {output}")
        else:
            raise ValueError(f"No --text or --file ")


if __name__ == '__main__':
    cli = CliManager()
    cli()
