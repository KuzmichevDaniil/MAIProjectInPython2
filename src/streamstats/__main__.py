import argparse
import sys
import csv
import json

from pathlib import Path
from streamstats.parsers import *
from streamstats.errors import *
from streamstats.analysis import *
from streamstats.report import *

def validation_data(args, file):
    for arg in args.format:
        if arg not in ['csv', 'jsonl']:
            raise UnknownFormat(arg)
            
    if not file.is_file():
        raise FileNotFound(file)
                
    elif file.suffix.lower() not in ['.csv', '.jsonl']:
        raise UnsupportedExtention(file)
                

def main():
    parser = argparse.ArgumentParser(prog = "streamstats", add_help = False)
    subparsers = parser.add_subparsers(dest = "command", required = True)
    
    sub_analyze = subparsers.add_parser("analyze", add_help = False)
    sub_analyze.add_argument("input", nargs = "+", type = Path)
    sub_analyze.add_argument("--format", dest = "format", required = True, nargs = "+")
    sub_analyze.add_argument("--output", dest = "output", type = Path)
    sub_analyze.add_argument("--skip-invalid", dest = "skip_invalid")
    
    args = parser.parse_args()
    stats = make_stats()
    
    if args.command == "analyze":
        try:
            for file in args.input:
                
                validation_data(args, file)
                
                if file.suffix.lower() == '.csv' and 'csv' in args.format:
                    for line in parser_csv(file):
                        analyzer(stats, make_event(line))
                                            
                elif file.suffix.lower() == '.jsonl' and 'jsonl' in args.format:
                    for line in parser_jsonl(file):
                        analyzer(stats, make_event(line))
                
                else:
                    print("Несовместимый файл с форматом!", file = sys.stderr)
                    sys.exit(2)
            
            if args.output:
                make_report(stats, args.output)
            else:
                print(final_result(stats))
        
        except StreamStatsErrors as err:
            print(err, file = sys.stderr)
            sys.exit(2)
     
if __name__ == "__main__":
    main()