import re
from datetime import datetime
from collections import defaultdict

def parse_logs(input_file, output_file):
    errors = 0
    warns = 0
    output_lines = []
    error_messages = defaultdict(int)
    warn_messages = defaultdict(int)
    error_pattern = re.compile(r'ERROR.*?- (.*)')
    warn_pattern = re.compile(r'WARN.*?- (.*)')

    with open(input_file, 'r') as file:
        for line in file:
            if 'ERROR' in line:
                errors += 1
                match = error_pattern.search(line)
                if match:
                    message = match.group(1).strip()  # Извлекаем сообщение об ошибке
                    error_messages[message] += 1
                    output_lines.append(message)  # Сохраняем только сообщение об ошибке
            elif 'WARN' in line:
                warns += 1
                match = warn_pattern.search(line)
                if match:
                    message = match.group(1).strip()  # Извлекаем сообщение о предупреждении
                    warn_messages[message] += 1
                    output_lines.append(message)  # Сохраняем только сообщение о предупреждении

    with open(output_file, 'w') as of:
        of.write(
            f"\nФайл {input_file}.\nКоличество ошибок ERROR: {errors}, предупреждений WARN: {warns}.\nОбработано: {datetime.now()}\n\n")

        of.write("ERRORS:\n")
        for message, count in error_messages.items():
            of.write(f"{message}: {count}\n")

        of.write("\nWARNS:\n")
        for message, count in warn_messages.items():
            of.write(f"{message}: {count}\n")


input_log_file = 'files/common.2025-03-19.0.log'
output_log_file = 'files/output_logs.txt'

parse_logs(input_log_file, output_log_file)