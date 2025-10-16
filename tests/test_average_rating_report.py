import os
import sys
import reports.average_rating_report as avg_report

# Добавляем корень проекта в sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def test_flag_name_exists():
    assert hasattr(avg_report, "FLAG_NAME")
    assert hasattr(avg_report, "execute")
    assert isinstance(avg_report.FLAG_NAME, str)


def test_execute_prints_average(capsys):
    data = [
        ["Item 1", "Brand A", 100, 4.0],
        ["Item 2", "Brand A", 200, 2.0],
        ["Item 3", "Brand B", 300, 3.33],
    ]
    avg_report.execute(data)
    # Перехватываем вывод в консоль и проверяем
    captured = capsys.readouterr()
    assert "Brand A" in captured.out
    assert "Brand B" in captured.out
    assert "3.0" in captured.out
    assert "3.33" in captured.out
