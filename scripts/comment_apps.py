











def insert_char_in_line_position(filename, line_number, position, char='#'):
    with open(filename, 'r') as file:
        lines = file.readlines()

    if line_number <= len(lines):
        lines[line_number - 1] = lines[line_number - 1][:position - 1] + char + lines[line_number - 1][position - 1:]

        with open(filename, 'w') as file:
            file.writelines(lines)
    else:
        print("Line number exceeds total lines in file.")

insert_char_in_line_position('vibestock/urls.py', 30, 5)
insert_char_in_line_position('config/settings.py', 55, 5)
