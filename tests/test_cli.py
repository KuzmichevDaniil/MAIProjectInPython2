import json

import pytest

from streamstats.__main__ import main


def event():
    """Возвращаем одно корректное событие."""
    return {"timestamp": "2024-03-01T08:02:30",
            "level": "ERROR",
            "source": "бд",
            "message": "Таймаут запроса"}
    
def make_file_for_bad_events(tmp_path):
    """
    Создаём JSONL файл из трёх строк: корректная строка, битая строка, корректная строка.
    Возвращаем путь к файлу.
    """
    file = tmp_path / "broken.jsonl"
    file.write_text(json.dumps(event()) + "\n{brake}\n" + json.dumps(event()) + "\n", encoding="utf-8")
    return file
    
def test_cli_bad_line(tmp_path, monkeypatch):
    """
    Без режима --skip-invalid битая строка останавливает обработку;
    выходим с кодом 2.
    """
    file_bad = make_file_for_bad_events(tmp_path)
    monkeypatch.setattr("sys.argv", ["streamstats", "analyze", str(file_bad), "--format", "jsonl"])
    with pytest.raises(SystemExit) as err:
        main()
    assert err.value.code == 2


def test_cli_skip_invalid_for_jsonl(tmp_path, monkeypatch):
    """
    С режимом --skip-invalid битая строка в файле JSONL пропускается, 
    остальные учитываются, а число пропущенных строк попадает в отчёт (report).
    """
    file_bad = make_file_for_bad_events(tmp_path)
    output = tmp_path / "REPORT.json"
    monkeypatch.setattr("sys.argv", ["streamstats", "analyze", str(file_bad), "--format", "jsonl", "--skip-invalid", "--output", str(output)])
    main()
    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["total"] == 2
    assert report["skipped_invalid"] == 1

def test_cli_skip_invalid_for_csv(tmp_path, monkeypatch):
    """
    С режимом --skip-invalid битая строка в файле CSV пропускается, 
    остальные учитываются, а число пропущенных строк попадает в отчёт (report).
    """
    file_bad = tmp_path / "file_bad.csv"
    file_bad.write_text("timestamp,level,source,message\n"
                        "2024-03-01T08:02:30,ERROR,бд,Таймаут запроса\n"
                        "2024-03-01T08:00:00,INFO,web,Сервер запущен, сервер неисправен\n", encoding="utf-8")
    output = tmp_path / "REPORT.json"
    monkeypatch.setattr("sys.argv", ["streamstats", "analyze", str(file_bad), "--format", "csv", "--skip-invalid", "--output", str(output)])
    main()
    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["total"] == 1
    assert report["skipped_invalid"] == 1
    
def test_cli_error_for_jsonl(tmp_path, monkeypatch, capsys):
    """Сообщение об ошибке в файле JSONL содержит номер битой строки и имя файла."""
    file_bad = make_file_for_bad_events(tmp_path)
    file_bad.write_text(json.dumps(event()) + "\n{broken}\n", encoding="utf-8")
    monkeypatch.setattr("sys.argv", ["streamstats", "analyze", str(file_bad), "--format", "jsonl"])
    with pytest.raises(SystemExit):
        main()
    err = capsys.readouterr().err
    assert "2" in err and "broken.jsonl" in err

def test_cli_error_for_csv(tmp_path, monkeypatch, capsys):
    """Сообщение об ошибке в файле CSV содержит номер битой строки и имя файла."""
    file_bad = tmp_path / "broken.csv"
    file_bad.write_text("timestamp,level,source,message\n"
                        "2024-03-01T08:02:30,ERROR,бд,Таймаут запроса\n"
                        "2024-03-01T08:00:00,INFO,web,Сервер запущен, сервер неисправен\n", encoding="utf-8")
    monkeypatch.setattr("sys.argv", ["streamstats", "analyze", str(file_bad), "--format", "csv"])
    with pytest.raises(SystemExit):
        main()
    err = capsys.readouterr().err
    assert "3" in err and "broken.csv" in err
    
def test_cli_for_more_files(tmp_path, monkeypatch):
    """Статистика из нескольких файлов CSV и JSONL объединяется в общий отчёт."""
    file_csv = tmp_path / "file_csv.csv"
    file_csv.write_text("timestamp,level,source,message\n"
                    "2024-03-01T08:02:30,ERROR,бд,Таймаут запроса\n"
                    "2024-03-01T08:00:00,INFO,web,Сервер запущен\n"
                    "2024-03-01T08:00:05,DEBUG,кэш,Кэш прогрет\n"
                    "2024-03-01T08:10:00Z,CRITICAL,платежи,Шлюз недоступен\n", encoding="utf-8")
    
    file_jsonl = tmp_path / "file_jsonl.jsonl"
    file_jsonl.write_text(json.dumps(event(), ensure_ascii = False) + "\n" + json.dumps(event(), ensure_ascii = False) + "\n", encoding = "utf-8")
    
    output = tmp_path / "REPORT.json"
    monkeypatch.setattr("sys.argv", ["streamstats", "analyze", str(file_jsonl), str(file_csv), "--format", "jsonl", "csv", "--output", str(output)])
    
    main()
    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["total"] == 6
    assert report["by_source"] == {"бд": 3, "web": 1, "кэш": 1, "платежи": 1,}
    assert report["first_timestamp"] == "2024-03-01T08:00:00"
    assert report["last_timestamp"] == "2024-03-01T08:10:00Z"