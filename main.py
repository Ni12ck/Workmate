import argparse
from reports import ReportGenerator

# Работа с входными параметрами скрипта
def main():
    """
    Обрабатывает входные аргументы и вызывает генерацию отчёта
    """
    parser = argparse.ArgumentParser(description='Генерирует отчёт по сотрудникам')
    parser.add_argument('files', nargs='+', help='CSV файлы с данными сотрудников')
    parser.add_argument('--report', required=True,
                        choices=ReportGenerator.REPORT_TYPES.keys(),
                        help='Тип генерируемого отчёта')

    args = parser.parse_args()

    try:
        report = ReportGenerator.get_report(args.report, args.files)
        print(report)
    except Exception as e:
        print(f"Ошибка генерации отчёта: {e}")
        # Выход из программы с ошибкой
        exit(1)


if __name__ == '__main__':
    main()
