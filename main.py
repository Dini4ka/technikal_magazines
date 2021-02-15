from technikal_magazines.saving_to_csv.saving_to_csv import saving_to_csv
from technikal_magazines.saving_to_csv.saving_to_csv_from_file import saving_to_csv_from_file


print("Привет, введите название магазина!")
print('1. МВидео' )
print('2. Эльдорадо' )
print('3. ДНС' )
print('4. РБТ' )
print('5. Ситилинк' )
print('6. Холодильник' )
shop_name_number = input()
shop_name = ''

if shop_name_number == '1':
    shop_name = 'МВидео'
elif shop_name_number == '2':
    shop_name = 'Эльдорадо'
elif shop_name_number == '3':
    shop_name = 'ДНС'
elif shop_name_number == '4':
    shop_name = 'РБТ'
elif shop_name_number == '5':
    shop_name = 'Ситилинк'
elif shop_name_number == '6':
    shop_name = 'Холодильник'
print('\n')
print("Что будем делать ?")
print("1. Ищем все товары по ссылке")
print("2. Оцениваем все товары по загружаемому файлу")
what_should_we_do = input()

if what_should_we_do == '1':
    print('Введите ссылку на товары. Обятаельно учтите чтобы ссылка совпадала с магазином, который вы выбрали')
    link = input()
    print('Начинаем поиск товаров')
    saving_to_csv(link, shop_name)
    print('Работа выполнена')
if what_should_we_do == '2':
    print('Введите полный путь до вашего файла xlsx')
    file_name = input()
    saving_to_csv_from_file(file_name,shop_name)
    print('Работа выполнена')

