import csv
import os
import sys
import argparse
import importlib.util
from typing import List, Dict
from types import ModuleType

MODULES_DIR = "reports"


def init_modules(directory: str) -> Dict[str, ModuleType]:
    """Автоматическая инициализация модулей отчётов"""
    available_reports = {}
    module_files = [f for f in os.listdir(directory) if f.endswith("_report.py")]
    for file_name in module_files:
        module_path = os.path.join(directory, file_name)
        module_name = file_name[:-3]

        # Используем importlib для динамической загрузки
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        if spec is None:
            continue

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        # Проверяем, что модуль имеет необходимые метаданные
        if hasattr(module, "FLAG_NAME") and hasattr(module, "execute"):
            available_reports[module.FLAG_NAME] = module
        else:
            print(
                f"Предупреждение: Модуль {file_name} не имеет необходимых метаданных."
            )

    return available_reports


def parse_csv(path: str) -> List[List[str | float]] | None:
    """Парсинг CSV файлов и возврат результата в виде списка списков значений для дальнейшей обработки"""
    try:
        with open(path, encoding="utf-8") as f:
            data = []
            csv_data = csv.reader(f)
            # Пропускаем заголовок
            next(csv_data)
            for row in csv_data:
                data.append([row[0], row[1], float(row[2]), float(row[3])])
            return data
    except Exception as e:
        print(f"ОШИБКА: не удаётся обработать файл {path}. {str(e)}")


def get_data(args) -> List[List[str | None]]:
    """Обработка отдельных файлов и директорий, содержащих csv файлы и их последующий парсинг."""
    data_rows = []
    for arg in args:
        is_exists = os.path.exists(arg)
        is_file = os.path.isfile(arg)

        if is_exists:
            # Аргумент является файлом - парсим его
            if is_file:
                data = parse_csv(arg)
                if data:
                    data_rows += data
            # Аргумент является директорией - проходим по всем файлам
            else:
                csv_files = [file for file in os.listdir(arg) if file.endswith(".csv")]
                for file in csv_files:
                    data = parse_csv(f"{arg}/{file}")
                    if data:
                        data_rows += data
        else:
            print(f"ОШИБКА: {arg} не является файлом или директорией")
    return data_rows


def main() -> None:
    # 1. Обнаружение модулей
    modules = init_modules(MODULES_DIR)

    # 2. Настройка Argparse
    parser = argparse.ArgumentParser(
        description="Программ формирования отчётов из .csv файлов"
    )
    parser.add_argument(
        "-f",
        "--files",
        type=str,
        nargs="+",
        help="Список файлов и/или директорий через пробел, содержащий .csv файлы",
        required=True,
    )
    parser.add_argument(
        "-r",
        "--report",
        type=str,
        choices=modules.keys(),
        help="Список отчётов, которые необходимо сформировать",
        required=True,
    )
    args = parser.parse_args()

    # 3. Выполнение кода модуля выбранного отчёта
    data = get_data(args.files)
    modules[args.report].execute(data)


if __name__ == "__main__":
    main()
