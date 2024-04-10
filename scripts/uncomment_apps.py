






def delete_char_in_line(file_path, line_number, char_position):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    if line_number <= len(lines):
        line = lines[line_number - 1]
        if char_position < len(line):
            lines[line_number - 1] = line[:char_position] + line[char_position + 1:]

            with open(file_path, 'w') as file:
                file.writelines(lines)
        else:
            print(f"Character position {char_position} exceeds length of the line.")
    else:
        print(f"Line number {line_number} exceeds total lines in the file.")

delete_char_in_line('vibestock/urls.py', 30, 4)
delete_char_in_line('config/settings.py', 55, 4)
