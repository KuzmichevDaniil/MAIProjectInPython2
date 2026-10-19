import argparse
import logging
import sys
from pathlib import Path

from streamstats.analysis import *
from streamstats.errors import *
from streamstats.parsers import *
from streamstats.report import *

logg = logging.getLogger("streamstats")

def parse_file(file, parser_name, stats, skip_invalid):
    """
    Читаем файл парсером parser_name и добавляем события в статистику.
    Если строка некорректна: без skip_invalid рейзится ошибка
    и обработка останавливается, с skip_invalid строка пропускается,
    увеличивается счётчик skipped_invalid и в лог пишется WARNING.
    """
    for num_line, line in parser_name(file):
        try:
            make_event(num_line, line, file.name)
        except StreamStatsErrors as err:
            if not skip_invalid:
                raise 
            stats["skipped_invalid"] += 1
            stats["by_level"]["WARNING"] += 1
            logg.warning("%s", err)
            continue
        analyzer(stats, make_event(num_line, line, file.name))
            
        

def validation_data(args, file):
    """
    Проверяем аргументы командной строки и входной файл.
    Рейзим UnknownFormat, FileNotFound или UnsupportedExtention.
    """
    for arg in args.format:
        if arg not in ['csv', 'jsonl']:
            raise UnknownFormat(arg)
            
    if not file.is_file():
        raise FileNotFound(file)
                
    elif file.suffix.lower() not in ['.csv', '.jsonl']:
        raise UnsupportedExtention(file)
                

def main():
    """
    Точка входа: разбираем аргументы, обрабатываем файлы и выводим отчёт.
    Отчёт записывается в файл из --output или печатается в консоль.
    """
    parser = argparse.ArgumentParser(prog = "streamstats")
    subparsers = parser.add_subparsers(dest = "command", required = True)
    
    sub_analyze = subparsers.add_parser("analyze")
    sub_analyze.add_argument("input", nargs = "+", type = Path)
    sub_analyze.add_argument("--format", dest = "format", required = True, nargs = "+")
    sub_analyze.add_argument("--output", dest = "output", type = Path)
    sub_analyze.add_argument("--skip-invalid", dest = "skip_invalid", action = "store_true")
    
    args = parser.parse_args()
    logging.basicConfig(level = logging.WARNING, format = "%(levelname)s: %(message)s")
    stats = make_stats()
    
    if args.command == "analyze":
        try:
            for file in args.input:
                
                validation_data(args, file)
                
                if file.suffix.lower() == '.csv' and 'csv' in args.format:
                    parse_file(file, parser_csv, stats, args.skip_invalid)
                                            
                elif file.suffix.lower() == '.jsonl' and 'jsonl' in args.format:
                    parse_file(file, parser_jsonl, stats, args.skip_invalid)
                
                else:
                    print("Несовместимый файл с форматом!", file = sys.stderr)
                    sys.exit(2)
            
            if args.output:
                make_report(final_result(stats, args.skip_invalid), args.output)
            else:
                print(final_result(stats, args.skip_invalid))
        
        except StreamStatsErrors as err:
            print(err, file = sys.stderr)
            sys.exit(2)
     
if __name__ == "__main__":
    main()