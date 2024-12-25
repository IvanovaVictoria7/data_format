import pandas as pd
import json


def read_csv_file(file_path):
    """Считывает CSV-файл и возвращает DataFrame."""
    return pd.read_csv(file_path)


def preprocess_data(data):
    """Обрабатывает данные: преобразует дату и устанавливает индекс."""
    # Преобразуем колонку 'timestamp' в формат даты
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    # Устанавливаем 'timestamp' в качестве индекса
    data.set_index('timestamp', inplace=True)
    return data


def calculate_monthly_average(data, column_name='close'):
    """Рассчитывает средние значения по месяцам для указанной колонки."""
    # Проверяем наличие колонки
    if column_name not in data.columns:
        raise ValueError(f"Колонка '{column_name}' отсутствует в данных.")
    # Группируем и рассчитываем среднее значение для конца месяца
    monthly_average = data.resample('ME').mean()[column_name]
    # Преобразуем результат в словарь
    return {str(key.date()): value for key, value in monthly_average.items()}


def save_to_json(data, output_path):
    """Сохраняет данные в JSON-файл."""
    with open(output_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)


def main():
    # Пути к файлам
    file_path = r"C:\Users\user\envs\data_format\data\fx_daily_EUR_USD.csv"
    output_path = 'monthly_average_close.json'

    try:
        # Чтение и обработка данных
        data = read_csv_file(file_path)
        processed_data = preprocess_data(data)
        monthly_average = calculate_monthly_average(processed_data)

        # Сохранение и вывод результата
        save_to_json(monthly_average, output_path)
        print(monthly_average)

    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "main":
    main()