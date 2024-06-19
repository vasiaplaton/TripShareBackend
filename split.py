def split_csv(file_path, lines_per_file=30000):
    """
    Разделить CSV файл на несколько файлов по заданному количеству строк.

    :param file_path: Путь к исходному CSV файлу.
    :param lines_per_file: Количество строк в каждом результирующем файле.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    header = lines[0]
    data_lines = lines[1:]

    for i in range(0, len(data_lines), lines_per_file):
        chunk = data_lines[i:i + lines_per_file]
        chunk.insert(0, header)

        output_file_path = f"{file_path.rsplit('.', 1)[0]}_{i // lines_per_file + 1}.csv"
        with open(output_file_path, 'w', encoding='utf-8', newline='') as output_file:
            output_file.writelines(chunk)

        print(f"Created file: {output_file_path}")


# Пример использования
file_path = 'data.csv'
split_csv(file_path)