import pytest
from reports import ReportGenerator


@pytest.fixture
def sample_files(tmp_path):
    """
    Генерирует файлы для тестов
    :return: список файлов
    """
    # Создаём временные файлы для тестов
    file1 = tmp_path / "data1.csv"
    file1.write_text("""id,name,department,hours_worked,rate
1,Alice Johnson,Marketing,160,50
2,Bob Smith,Design,150,40""")

    file2 = tmp_path / "data2.csv"
    file2.write_text("""department,name,hours_worked,salary,id
Design,Carol Williams,170,60,3""")

    return [str(file1), str(file2)]


def test_read_csv_files(sample_files):
    """Тестирует чтение CSV файлов"""
    employees = ReportGenerator.read_csv_files(sample_files)

    # Проверяем количество сотрудников
    assert len(employees) == 3

    # Проверяем, что все данные корректно прочитаны
    assert employees[0]['name'] == 'Alice Johnson'
    assert employees[1]['rate'] == '40'
    assert employees[2]['salary'] == '60'


def test_generate_payout_report_calculations():
    """Тестирует корректность расчётов"""
    test_employees = [
        {'name': 'Test1', 'department': 'Test', 'hours_worked': '100', 'rate': '10'},
        {'name': 'Test2', 'department': 'Test', 'hours_worked': '50', 'rate': '20'}
    ]

    report = ReportGenerator.generate_payout_report(test_employees)

    # Проверяем расчёты (100*10 + 50*20 = 2000)
    assert "$1000" in report  # Для первого сотрудника
    assert "$1000" in report  # Для второго сотрудника
    assert "$2000" in report  # Общий итог по отделу


def test_negative_values_handling():
    """Тестирует обработку отрицательных значений"""
    test_employees = [
        {'name': 'Test', 'department': 'Test', 'hours_worked': '-100', 'rate': '10'},
        {'name': 'Test', 'department': 'Test', 'hours_worked': '50', 'rate': '-20'}
    ]

    report = ReportGenerator.generate_payout_report(test_employees)

    # Отрицательные значения должны обрабатываться как 0
    assert "$0" in report  # Для обоих случаев
    assert "$0" in report  # В общем итоге


def test_unknown_report_type(sample_files):
    """Тестирует обработку неизвестного типа отчёта"""
    with pytest.raises(ValueError, match="Неизвестный тип отчёта: unknown"):
        ReportGenerator.get_report('unknown', sample_files)
