"""
Generate test code tool


copyrigth https://github.com/shigeshige/py-ut-generator
"""
import argparse

from pyutgenerator import files, code_analysis


def parse_file(file_name: str, renew=False):
    """
    generate test code.
    """
    if code_analysis.check(file_name):
        print('File not Found :' + str(file_name))
        return

    module = files.get_package_moduel(file_name)
    t_file = module.get_test_file_name()

    t_txt = code_analysis.make_test_code(module, renew)

    files.write_file(t_file, t_txt, not renew)


def main():
    """
    main function.
    """
    pas = argparse.ArgumentParser()
    pas.add_argument("filename", help="input python filename")
    pas.add_argument("--overwrite", help="overwrite test code", action="store_true")
    args = pas.parse_args()
    print('input:' + args.filename)
    # print(args.ovewrite)
    parse_file(args.filename, args.overwrite)


if __name__ == "__main__":
    main()
