"""
Пример подключаемого модуля.
Модули отчётов обязательно должны содержать строковую переменную FLAG_NAME и функцию execute.
Пример вызова: python cvsreport.py --files dummy --report test
"""

MODULE_NAME = "Тестовый модуль"
FLAG_NAME = "test"
DESCRIPTION = "Тестовый модуль для проверки подключения"


def execute(args) -> None:
    """Основная функция модуля, вызываемая при активации флага --report test"""
    print(
        f"""
    + Название модуля: {MODULE_NAME}
    + Флаг: {FLAG_NAME}
    + Описание: {DESCRIPTION}
    + Аргументы: {args}
    + Статус: Модуль успешно подключен и работает!
    """
    )
