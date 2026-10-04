import argparse
from pathlib import Path
import sys
from streamstats.parsers import parser_csv

def main():
    parser = argparse.ArgumentParser(prog = "streamstats", add_help = False)
    subparsers = parser.add_subparsers(dest = "command", required = True)
    
    sub_analyze = subparsers.add_parser("analyze", add_help = False)
    sub_analyze.add_argument("input", nargs = "+", type = Path)
    sub_analyze.add_argument("--format", dest = "format", choices = ["csv", "jsonl"], required = True)
    sub_analyze.add_argument("--output", dest = "output", type = Path)
    sub_analyze.add_argument("--skip-invalid", dest = "skip_invalid")
    
    args = parser.parse_args()
    
    if args.command == "analyze":
        for file in args.input:
            if not file.is_file():
                print(f"Ошибка, файл {file} не найден!", file = sys.stderr)
                sys.exit(2)
                
        if args.format == "csv":
            parser_csv(args.input)
        elif args.format == "jsonl":
            pass
                
    
    
if __name__ == "__main__":
    main()