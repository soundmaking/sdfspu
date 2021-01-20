
file_path = 'temp.txt'

if __name__ == '__main__':
    print(f'file = {file_path}')
    select = False
    prev_line = ''
    with open(file_path, 'r') as file:
        for line in file:
            if not select and 'test_' in line and 'sfailed' in line:
                print(line.split('sfailed')[1][:-1])
                select = True
            elif select and 'self.assert' in line:
                print('   ', line[:-1])
            elif select and 'begin captured logging' in line:
                select = False
                if "<html>" in prev_line:
                    print('   ', prev_line[:65], " ...'\n")
                else:
                    print('   ', prev_line[:-1], '\n')
            else:
                if 'Exception: ' in line:
                    prev_line = line




