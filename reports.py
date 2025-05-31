from collections import defaultdict
from typing import List, Dict, Any


class ReportGenerator:
    @staticmethod
    def read_csv_files(files: List[str]) -> List[Dict[str, Any]]:
        """
        Считывает csv файлы
        :param files: список путей к csv файлам
        :return: список с данными сотрудников
        """
        employees = []
        for file in files:
            with open(file, 'r') as f:
                headers = f.readline().strip().split(',')
                for line in f:
                    values = line.strip().split(',')
                    employee = dict(zip(headers, values))
                    employees.append(employee)
        return employees

    @staticmethod
    def generate_payout_report(employees: List[Dict[str, Any]]) -> str:
        """
        Генерирует отчёт заработных плат
        :param employees: данные сотрудников
        :return: строка, содержащая отчёт, готовый к выводу
        """
        department_data = defaultdict(list)
        department_totals = defaultdict(lambda: {'hours': 0, 'payout': 0})

        for emp in employees:
            department = emp['department']
            hours = float(emp.get('hours_worked', 0))
            # Пытаемся получить ставку заработной платы из одного из доступных полей
            rate = (float(emp.get('hourly_rate', 0)) or float(emp.get('rate', 0)) or
                    float(emp.get('salary', 0)))
            # Для отрицательных значений
            hours = hours if hours > 0 else 0
            rate = rate if rate > 0 else 0
            payout = hours * rate

            department_data[department].append({
                'name': emp['name'],
                'hours': hours,
                'rate': rate,
                'payout': payout
            })

            department_totals[department]['hours'] += hours
            department_totals[department]['payout'] += payout

        # Инициализируем отчёт с названием столбцов
        report_lines = [f"{' ' * 14} {'name':20} {'hours':6} {'rate':5} {'payout'}"]

        # Сортировка по ключам (department), чтобы выводить людей относящихся к department в одном месте
        for department in sorted(department_data.keys()):
            report_lines.append(f"{department}")

            for emp in department_data[department]:
                # Вывод имён, часов, рейтинга и зп
                report_lines.append(f"{'-' * 14} {emp['name']:20} {emp['hours']:3.0f} {emp['rate']:5.0f}    "
                                    f"${emp['payout']:4.0f}")

            # Вывод всех часов и зп
            report_lines.append(f"{' ' * 35} {department_totals[department]['hours']:3.0f} {' ' * 8} "
                                f"${department_totals[department]['payout']:.0f}")

        # Общий вывод
        total_payout = sum(d['payout'] for d in department_totals.values())
        # Вывод всей суммы
        report_lines.append(f"\nTotal {' ' * 42} ${total_payout:.0f}")

        return "\n".join(report_lines)

    # Инициализация типов отчётов, в будущем можно добавить другие типы отчётов с их генераторами
    REPORT_TYPES = {'payout': generate_payout_report}

    @classmethod
    def get_report(cls, report_type: str, files: List[str]) -> str:
        """
        Получение отчёта по его типу
        :param report_type: тип отчёта
        :param files: файлы для отчёта
        :return: отчёт
        """
        if report_type not in cls.REPORT_TYPES:
            raise ValueError(f"Неизвестный тип отчёта: {report_type}")

        employees = cls.read_csv_files(files)
        report_func = cls.REPORT_TYPES[report_type]
        return report_func(employees)
