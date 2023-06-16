import csv
from bs4 import BeautifulSoup
import requests
import time
html = requests.get('https://book24.ru/').content # Загружаем страницу
more_books = []

bs = BeautifulSoup(html, 'html.parser')
html_literature = bs.find_all('article', class_='product-card _without-button')

for book in html_literature: # В цикле обращаемся к всем тегам
    discount_type = "Это не лучшая цена."
    name = book.find('a', class_='product-card__name').text.strip() # Поиск названия книги
    print(name)
    author = book.find('div', class_='author-list product-card__authors-holder').get_text() # Поиск автора книги
    print(author)
    discount = book.find('span', class_='product-card-badge-best-price__text') # Поиск оценки книги
    if discount != None:
        discount_type = 'Лучшая цена!'
    print(discount_type)
    more_books.append({'name': name, 'author': author, 'discount': discount_type}) # Теги сохраняем в список и приписываем ключи

with open('base.xml', 'w', encoding='utf-8') as file: # Сохранение списка в xml
    for book in more_books:
        file.write('    <item>\n')
        file.write(f'       <name>{book["name"]}</name>\n')
        file.write(f'       <author>{book["author"]}</author>\n')
        file.write(f'       <discount>{book["discount"]}</discount>\n')
        file.write('    </item>\n')
    file.write('</items>\n')

with open('base.csv', 'w', encoding='utf-8') as file: # Сохранение списка в csv
    names = ['name', 'author', 'discount']
    writer = csv.DictWriter(file, fieldnames=names)

    writer.writeheader()
    writer.writerows(more_books)