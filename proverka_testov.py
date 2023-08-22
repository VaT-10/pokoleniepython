'''Вставьте свой код в переменную my_code.
Архив с тестами перенесите в папку с программой, и вставьте его название в переменную filname'''

from zipfile import ZipFile
import sys

my_code = r'''...'''
filename = '...' + '.zip'

orig_std = sys.stdout
count_true = 0
count_false = 0


def read_my_clue():
    sys.stdout = open('res.txt', 'w')
    exec(new_my_code, globals())
    if flag:
        exec(test)
    sys.stdout = orig_std
    with open('res.txt') as res_code:
        return ''.join(res_code.readlines())


try:
    with ZipFile(filename) as file:
        flag = input('Есть ли код в тестах? (да/нет)\n') == 'да'
        namelist = file.namelist()
        tests = filter(str.isdigit, namelist)

        for i in tests:
            new_my_code = my_code
            with file.open(f'{i}.clue') as clue:
                right_clue = clue.read().decode('utf-8')

            with file.open(i) as f:
                test = f.read().decode('utf-8')
                if not flag:
                    for j in test.split('\n'):
                        new_my_code = new_my_code.replace('input()', repr(j.strip('\r')), 1)
            try:
                my_clue = read_my_clue()
            except Exception as e:
                count_false += 1
                sys.stdout = orig_std
                error = str(type(e)).strip('<class \'')[:-2]
                print(f'ТЕСТ {i}/{len(namelist) // 2}: FAIL')
                print('\nТест:')
                print(test)
                print(f'\nПри выполнении кода произошла ошибка: {error}: {e}')
                print('Правильный ответ:')
                print(right_clue)
                if namelist[-2] != i:
                    continue_or_no = input('Продолжать проверку? (да/нет)\n')
                    if continue_or_no.lower() != 'да':
                        break
                continue
            if my_clue.strip('\n') == right_clue:
                count_true += 1
                print(f'ТЕСТ {i}/{len(namelist) // 2}: OK✔')
            else:
                count_false += 1
                print(f'ТЕСТ {i}/{len(namelist) // 2}: FAIL')
                print('\nТест:')
                print(test)
                print('\nВаш ответ:')
                print(my_clue)
                print('Правильный ответ:')
                print(right_clue)
                continue_or_no = input('Продолжать проверку? (да/нет)\n')
                if continue_or_no.lower() != 'да':
                    break
    print(f'\nПроверено тестов: {i}/{len(namelist) // 2}\nКоличество правильных ответов: {count_true}/{i}\nКоличество неправильных ответов: {count_false}/{i}')
except FileNotFoundError:
    print('Архив не найден.')
except:
    print('Неизвестная ошибка.')
