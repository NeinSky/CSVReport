from tabulate import tabulate

MODULE_NAME = "Средний рейтинг бренда"
FLAG_NAME = "average-rating"
DESCRIPTION = "Выводит средний рейтинг брендов в консоль"


def execute(args) -> None:
    """Основная функция модуля, вызываемая при активации флага --report average-rating"""
    brands = {}
    for arg in args:
        name, brand, price, rating = arg
        if brand not in brands.keys():
            brands[brand] = {"count": 0, "rating_sum": 0}
        brands[brand]["count"] += 1
        brands[brand]["rating_sum"] += rating

    rating = []
    for brand, values in brands.items():
        rating_sum = values["rating_sum"]
        count = values["count"]
        rating.append([brand, round(rating_sum / count, 2)])

    rating.sort(key=lambda item: item[1], reverse=True)
    row_ids = [row_id for row_id in range(1, len(rating) + 1)]
    if rating:
        print(
            tabulate(
                rating,
                headers=["brand", "rating"],
                tablefmt="pretty",
                showindex=row_ids,
                stralign="left",
            )
        )
    else:
        print("Нет данных для отображения")
