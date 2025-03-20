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
    full_error = re.compile(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}) (ERROR|WARN) .*? - (.*)')
    full_errors = []

    with open(input_file, 'r', encoding='utf-8') as file:
        for line in file:
            if 'ERROR' in line:
                errors += 1
                match = error_pattern.search(line)
                if match:
                    message = match.group(1).strip()
                    error_messages[message] += 1
                    output_lines.append(message)

                full_match = full_error.match(line)
                if full_match:
                    full_errors.append(line.strip())
                    for next_line in file:
                        if next_line.startswith('2025-'):
                            break
                        full_errors.append(next_line.strip())

            elif 'WARN' in line:
                warns += 1
                match = warn_pattern.search(line)
                if match:
                    message = match.group(1).strip()
                    warn_messages[message] += 1
                    output_lines.append(message)

                full_match = full_error.match(line)
                if full_match:
                    full_errors.append(line.strip())
                    for next_line in file:
                        if next_line.startswith('2025-'):
                            break
                        full_errors.append(next_line.strip())

    with open(output_file, 'w', encoding='utf-8') as of:
        of.write(
            f"\nФайл {input_file}.\nКоличество ошибок ERROR: {errors}, предупреждений WARN: {warns}.\nВремя обработки: {datetime.now()}\n\n")

        of.write("ERRORS:\n")
        for message, count in error_messages.items():
            of.write(f"{message}: {count}\n")

        of.write("\nWARNS:\n")
        for message, count in warn_messages.items():
            of.write(f"{message}: {count}\n")

        of.write("\nПолные ошибки:\n")
        for i in full_errors:
            of.write(f"{i}\n")

input_log_file = 'files/testcommon.log'
output_log_file = 'files/output_logs.txt'

parse_logs(input_log_file, output_log_file)