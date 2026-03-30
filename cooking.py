#Чтение книги рецептов
def get_cook_book(file_path):
    cook_book = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            dish_name = line.strip() # Читаем название (Омлет)
            if not dish_name:
                continue
            
            # Читаем следующую строку — это видимо число строк с ингридиентами (3)            
            ingredient_count = int(file.readline().strip())
            # даем циклу работать (3) раза и записываем ингридиенты в список
            ingredients = []
            for i in range(ingredient_count):
                # Читаем ровно столько строк, сколько пообещал счетчик
                item = file.readline().strip().split(' | ')
                ingredients.append({
                    'ingredient_name': item[0],
                    'quantity': int(item[1]),
                    'measure': item[2]
                })
            
            cook_book[dish_name] = ingredients
            file.readline() # Просто "проглатываем" пустую строку между блоками
            
    return cook_book

# проверяем что считали и что получилось
cook_book = get_cook_book(r'C:\Users\Troshin\YandexDisk\Нетология\03-files\recipes.txt')
#from pprint import pprint
#pprint(cook_book)

# задача 2
# задаём бюда и количество персон, берем книгу рецептов и считаем чего и сколько надо чтобы это приготовить
def get_shop_list_by_dishes(dishes, person_count, cook_book):
    shop_list = {} #корзинка с продуктами в виде словарика
    
    for dish in dishes:
        if dish in cook_book:
            for ingredient in cook_book[dish]:
                name = ingredient['ingredient_name']
                # Считаем количество на нужное число персон
                total_quantity = ingredient['quantity'] * person_count
                
                if name not in shop_list:
                    # Если продукта еще нет в списке — добавляем его
                    shop_list[name] = {
                        'measure': ingredient['measure'],
                        'quantity': total_quantity
                    }
                else:
                    # Если продукт уже есть (например, из другого блюда) — прибавляем количество
                    shop_list[name]['quantity'] += total_quantity
        else:
            print(f'Блюда "{dish}" нет в книге рецептов')
            
    return shop_list

# проверяем что получилось
# Вызываем функцию для 2 персон
result = get_shop_list_by_dishes(['Запеченный картофель', 'Омлет'], 2, cook_book)

# Красиво печатаем результат, даже ингридиенты выводятся по алфавиту
from pprint import pprint
pprint(result)

# слияние файлов в один в очередности по количеству в них строк
# попробуем считать все названия файлов с расширеним txt кроме result в папке и записать их в один список
import os
#без указания конкретного пути к папке с файлами ничего не получилось, пришлось ввести переменную path
path= r'C:\Users\Troshin\YandexDisk\Нетология\03-files\data'

all_files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.txt') and f != 'result.txt']
# проверяем что там получилось
from pprint import pprint
pprint(all_files)
#pprint(os.listdir('.'))

def merge_files(file_names, output_file):
    file_data = []

    # 1. Собираем информацию о файлах
    for name in file_names:
        with open(name, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            file_data.append({
                'name': name,
                'count': len(lines),
                'content': lines
            })

    # 2. Сортируем список словарей по количеству строк ('count')
    file_data.sort(key=lambda x: x['count'])

    # 3. Записываем всё в один итоговый файл
    with open(output_file, 'w', encoding='utf-8') as out_f:
        for file in file_data:
            out_f.write(f"{file['name']}\n")
            out_f.write(f"{file['count']}\n")
            out_f.writelines(file['content'])
            out_f.write("\n") # Добавим перенос, чтобы файлы не слипались

# Пример вызова:
files = all_files # Ваши файлы в папке
output_path = os.path.join(path, 'result.txt')
merge_files(files, output_path)