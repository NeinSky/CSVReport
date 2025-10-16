import os
import tempfile
import sys
import csvreport

# Добавляем корень проекта в sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def test_parse_csv_valid():
    with tempfile.NamedTemporaryFile(
        "w+", delete=False, suffix=".csv", encoding="utf-8"
    ) as f:
        f.write("name,brand,price,rating\n")
        f.write("Item 1,Brand A,100,3.9\n")
        f.write("Item 2,Brand B,200,4.5\n")
        f.write("Item 3,Brand B,400,4.6\n")
        path = f.name
    data = csvreport.parse_csv(path)
    os.remove(path)
    assert data == [
        ["Item 1", "Brand A", 100, 3.9],
        ["Item 2", "Brand B", 200, 4.5],
        ["Item 3", "Brand B", 400, 4.6],
    ]


def test_parse_csv_invalid_file():
    assert csvreport.parse_csv("dummy.csv") is None


def test_get_data_files_and_dirs(tmp_path):
    # Создаём два файла
    file1 = tmp_path / "a.csv"
    file1.write_text("name,brand,price,rating\nItem 1,Brand A,200,3.9\n")
    file2 = tmp_path / "b.csv"
    file2.write_text("name,brand,price,rating\nItem 2,Brand B,400, 4.0\n")
    # Проверяем обработку директории
    data = csvreport.get_data([str(tmp_path)])
    assert ["Item 1", "Brand A", 200, 3.9] in data
    assert ["Item 2", "Brand B", 400, 4.0] in data


def test_init_modules(tmp_path):
    # Создаём фейковые модули отчёта
    valid_module_code = "FLAG_NAME = 'valid';\ndef execute(data): pass"
    invalid_module_code = "FLAG_NAME = 'invalid';\ndef exec(data): pass"

    valid_report_file = tmp_path / "valid_report.py"
    valid_report_file.write_text(valid_module_code)

    invalid_report_file = tmp_path / "invalid_report.py"
    invalid_report_file.write_text(invalid_module_code)

    modules = csvreport.init_modules(str(tmp_path))
    assert "valid" in modules
    assert "invalid" not in modules
    assert hasattr(modules["valid"], "execute")
