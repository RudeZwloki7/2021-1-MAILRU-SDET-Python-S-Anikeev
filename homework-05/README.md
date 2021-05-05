## Домашнее задание №5: Backend: Linux

### Bash/Python scripting 
Скрипты на bash и python написаны для анализа готового access.log (расположен в корневой директории).

Скрипты на bash расположены в директории **bash_scripts**.
Все скрипты заданы как исполняемые с помощью команды _chmod +x_. Вывод результата осуществляется в bash.

Скрипты на python расположены в директории **py_scripts**.
Вывод результата осуществляется в текстовые файлы в директории **py_scripts_output** с тем же именем, что у скрипта.


#### Общее количество запросов
_**Скрипт bash:**_
```shell
#!/bin/bash
cat ../access.log | grep -E "[A-Z]{3,} .+(HTTP)" |wc -l
```
Результат:
```commandline
225133
```
Работа скрипта:

Выводим содержимое файла лога с помощью cat -> 
ищем по регулярному выражению все запросы в файле с помощью grep и выводим совпавшую строку полностью -> считаем количество полученных строк c помощью wс.

_**Скрипт python**_
```python
def count_all_requests():
    regex = re.compile(r'[A-Z]{3,} .+HTTP', re.MULTILINE)
    count = 0

    with open(config.repo_root() +'/access.log', 'r') as f:
        f = f.read()
        lines = re.findall(regex, f)
        for match in lines:
            count += 1

    data = dict({'count': count})

    config.write_result('Count of all requests', 'count_all_requests', data)
```
Результат:
```
Count of all requests
225133
```
Работа скрипта:

Составляем регулярное выражение для поиска в файле -> открываем файл на чтение -> 
ищем по регулярному выражению все запросы в файле -> считаем количество полученных строк -> записываем результат в файл в простом виде или формате json.


#### Общее количество запросов по типу, например: GET - 20, POST - 10 и т.д.

_**Скрипт bash:**_
```shell
#!/bin/bash
cat ../access.log | grep -Eo "[A-Z]{3,} .+(HTTP)" | awk '{print $1}' | sort | uniq -c | sort -nr | awk '{print $2 "\t" $1}'

```
Результат:
```commandline
GET	122096
POST	102503
HEAD	528
PUT	6

```
Работа скрипта:

Выводим содержимое файла лога с помощью cat -> 
ищем по регулярному выражению все запросы в файле с помощью grep и выводим лишь результат совпадения -> 
выводим первый столбец из полученного вывода (тип запроса) с помощью утилиты awk -> сортируем полученные строки -> 
подсчитываем количество уникальных элементов -> сортируем строки по числовым значениям в обратном порядке ->
выводим сначала тип запроса, а затем количество запросов данного типа.

_**Скрипт python**_
```python
def count_requests_by_type():
    dict_counts = {}
    regex = re.compile(r'[A-Z]{3,} .+HTTP', re.MULTILINE)

    with open(config.repo_root() +'/access.log', 'r') as f:
        f = f.read()
        matches = re.findall(regex, f)
        for match in matches:
            type = match.split()[0]
            dict_counts.update({f'{type}': 0})
        for match in matches:
            type = match.split()[0]
            dict_counts[f'{type}'] += 1

    config.write_result('Count all requests by type of request', 'count_requests_by_type', dict_counts, print_keys=True)
```
Результат:
```
Count all requests by type of request
POST	102503
GET	122096
HEAD	528
PUT	6
```
Работа скрипта:

Составляем регулярное выражение для поиска в файле -> открываем файл на чтение -> 
ищем по регулярному выражению все запросы в файле -> разбиваем каждое совпадение по пробелам 
и добавляем тип запроса в словарь как ключ -> считаем количество запросов 
для каждого типа и добавляем это значение в словарь ->
записываем результат в файл в простом виде или формате json.


#### Топ 10 самых частых запросов 

_**Скрипт bash:**_
```shell
#!/bin/bash
cat ../access.log | grep -Eo "[A-Z]{3,} .+(HTTP)" | awk '{print $2}'| sort | uniq -c | sort -nr | head | awk '{print $2 "\t" $1}'
```
Результат:
```commandline
/administrator/index.php	103932
/apache-log/access.log	26336
/	6940
/templates/_system/css/general.css	4980
/robots.txt	3199
http://almhuette-raith.at/administrator/index.php	2356
/favicon.ico	2201
/wp-login.php	1644
/administrator/	1563
/templates/jp_hotel/css/template.css	1287

```
Работа скрипта:

Выводим содержимое файла лога с помощью cat -> 
ищем по регулярному выражению все запросы в файле с помощью grep и выводим лишь результат совпадения -> 
выводим второй столбец из полученного вывода (url) с помощью утилиты awk -> сортируем полученные строки -> 
подсчитываем количество уникальных элементов -> сортируем строки по числовым значениям в обратном порядке -> 
выводим первые 10 элементов (по умолчанию) с помощью head -> выводим сначала url, а затем количество запросов.

_**Скрипт python**_
```python
def most_frequent_requests():
    request_list = []
    regex = re.compile(r'[A-Z]{3,} .+HTTP', re.MULTILINE)

    with open(config.repo_root() +'/access.log', 'r') as f:
        f = f.read()
        matches = re.findall(regex, f)
        for match in matches:
            request_list.append(match.split()[1])
    request_list.sort()
    keys = Counter(request_list).keys()
    values = Counter(request_list).values()
    tuple_list = list(zip(keys, values))
    tuple_list.sort(key=lambda tup: tup[1], reverse=True)
    data = []
    for url, count in tuple_list[:10:]:
        data.append({'url': url, 'count': count})

    config.write_result('Top 10 most frequent requests ', 'most_frequent_requests', data)
```
Результат:
```
Top 10 most frequent requests 
/administrator/index.php	103932
/apache-log/access.log	26336
/	6940
/templates/_system/css/general.css	4980
/robots.txt	3199
http://almhuette-raith.at/administrator/index.php	2356
/favicon.ico	2201
/wp-login.php	1644
/administrator/	1563
/templates/jp_hotel/css/template.css	1287

```
Работа скрипта:

Составляем регулярное выражение для поиска в файле -> открываем файл на чтение -> 
ищем по регулярному выражению все запросы в файле -> разбиваем каждое совпадение по пробелам 
и добавляем url запроса в список запросов -> сортируем список запросов ->  
генерируем уникальные ключи для url из списка запросов и их количество ->
сортируем по количеству запросов по убыванию -> записываем первые 10 полученных пар в список в виде словарей -> 
записываем результат в файл в простом виде или формате json.

#### Топ 5 самых больших по размеру запросов, которые завершились клиентской (4ХХ) ошибкой 

_**Скрипт bash:**_
```shell
#!/bin/bash
cat ../access.log | grep -E "[A-Z]{3,} .+(HTTP)" | awk '{print $7 "\t" $9 "\t" $10 "\t" $1}'| awk '$2 ~/4../{print $0}' | sort -k 3 -n -r | head -n 5
```
Результат:
```commandline
/index.php?option=com_phocagallery&view=category&id=7806&Itemid=53	404	1417	189.217.45.73
/index.php?option=com_phocagallery&view=category&id=4025&Itemid=53	404	1417	189.217.45.73
/index.php?option=com_phocagallery&view=category&id=%28SELECT%20%28CASE%20WHEN%20%289168%3D4696%29%20THEN%209168%20ELSE%209168%2A%28SELECT%209168%20FROM%20INFORMATION_SCHEMA.CHARACTER_SETS%29%20END%29%29&Itemid=53	404	1417	189.217.45.73
/index.php?option=com_phocagallery&view=category&id=%28SELECT%20%28CASE%20WHEN%20%281753%3D1753%29%20THEN%201753%20ELSE%201753%2A%28SELECT%201753%20FROM%20INFORMATION_SCHEMA.CHARACTER_SETS%29%20END%29%29&Itemid=53	404	1417	189.217.45.73
/?view=videos&type=member&user_id=1%20and%201=0%20union%20select%201,2,3,4,5,6,7,8,9,10,11,12,concat%280x3c757365723e,username,0x3c757365723e3c706173733e,password,0x3c706173733e%29,14,15,16,17,18,19,20,21,22,23,24,25,26,27%20from+jos_users+where+gid=25+limit+0,1--&option=com_jomtube	404	1397	5.206.77.93
```
Работа скрипта:

Выводим содержимое файла лога с помощью cat -> 
ищем по регулярному выражению все запросы в файле с помощью grep и выводим всю строку с совпадением -> 
выводим нужные столбцы по условию задачи с помощью утилиты awk -> ищем по полученным данным запросы с клиентской ошибкой -> 
сортируем полученные строки по значению 3 столбца (размер запроса) в обратном порядке -> 
выводим данные в соответствии с условием задачи.

_**Скрипт python**_
```python
def count_requests_with_client_error():
    request_list = []
    regex = re.compile(r'\d+\.\d+\.\d+\..+[A-Z]{3,} .+HTTP.+" 4.. \d+', re.MULTILINE)

    with open(config.repo_root() +'/access.log', 'r') as f:
        f = f.read()
        matches = re.findall(regex, f)
        for match in matches:
            request_list.append({'url': match.split()[6],
                                 'status_code': match.split()[8],
                                 'size': int(match.split()[9]),
                                 'ip': match.split()[0]})
    request_list.sort(key=lambda d: d['size'], reverse=True)
    data = []
    for i in range(5):
        data.append(request_list[i])

    config.write_result('Top 5 requests with the biggest weight with client error (4xx)',
                        'count_requests_with_client_error', data)
```
Результат:
```
Top 5 requests with the biggest weight with client error (4xx)
/index.php?option=com_phocagallery&view=category&id=4025&Itemid=53	404	1417	189.217.45.73
/index.php?option=com_phocagallery&view=category&id=7806&Itemid=53	404	1417	189.217.45.73
/index.php?option=com_phocagallery&view=category&id=%28SELECT%20%28CASE%20WHEN%20%289168%3D4696%29%20THEN%209168%20ELSE%209168%2A%28SELECT%209168%20FROM%20INFORMATION_SCHEMA.CHARACTER_SETS%29%20END%29%29&Itemid=53	404	1417	189.217.45.73
/index.php?option=com_phocagallery&view=category&id=%28SELECT%20%28CASE%20WHEN%20%281753%3D1753%29%20THEN%201753%20ELSE%201753%2A%28SELECT%201753%20FROM%20INFORMATION_SCHEMA.CHARACTER_SETS%29%20END%29%29&Itemid=53	404	1417	189.217.45.73
/index.php?option=com_easyblog&view=dashboard&layout=write	404	1397	104.129.9.248
```
Работа скрипта:

Составляем регулярное выражение для поиска в файле -> открываем файл на чтение -> 
ищем по регулярному выражению все запросы в файле -> разбиваем каждое совпадение по пробелам 
и записываем в виде словаря нужные данные в список запросов -> сортируем список запросов по размеру запроса по убыванию ->  
записываем первые 5 полученных словарей в список -> 
записываем результат в файл в простом виде или формате json.


#### Топ 5 пользователей по количеству запросов, которые завершились серверной (5ХХ) ошибкой

_**Скрипт bash:**_
```shell
#!/bin/bash
cat ../access.log | grep -E "[A-Z]{3,} .+(HTTP)" | awk '$9~/5../{print $1}'| uniq -c| sort -nr |awk '{print $2 "\t" $1}' | head -n 5
```
Результат:
```commandline
189.217.45.73	225
82.193.127.15	4
91.210.145.36	3
198.38.94.207	2
195.133.48.198	2
```
Работа скрипта:

Выводим содержимое файла лога с помощью cat -> 
ищем по регулярному выражению все запросы в файле с помощью grep и выводим всю строку с совпадением -> 
ищем все запросы с серверной ошибкой и выводим для них первый столбец (ip адрес) с помощью утилиты awk ->  
подсчитываем количество запросов для уникальных ip адресов ->
сортируем полученные данные по количеству запросов в обратном порядке -> 
выводим сначала ip адрес пользователя, а затем количество запросов -> выводим первые 5 элементов полученного списка.

_**Скрипт python**_
```python
def count_requests_with_server_error():
    ip_list = []
    regex = re.compile(r'\d+\.\d+\.\d+\..+[A-Z]{3,} .+HTTP.+" 5.. \d+', re.MULTILINE)

    with open(config.repo_root() +'/access.log', 'r') as f:
        f = f.read()
        matches = re.findall(regex, f)
        for match in matches:
            ip_list.append(match.split()[0])
    keys = Counter(ip_list).keys()
    values = Counter(ip_list).values()
    tuple_list = list(zip(keys, values))
    tuple_list.sort(key=lambda tup: tup[1], reverse=True)
    data = []
    for ip, count in tuple_list[:5:]:
        data.append({'ip': ip, 'count': count})

    config.write_result('Top 5 users with the biggest number of requests with server error (5xx)',
                        'count_requests_with_server_error', data)
```
Результат:
```
Top 5 users with the biggest number of requests with server error (5xx)
189.217.45.73	225
82.193.127.15	4
91.210.145.36	3
194.87.237.6	2
198.38.94.207	2
```
Работа скрипта:

Составляем регулярное выражение для поиска в файле -> открываем файл на чтение -> 
ищем по регулярному выражению все запросы в файле -> разбиваем каждое совпадение по пробелам 
и записываем ip пользователя в список ip адресов -> 
генерируем уникальные ключи ip пользователей из списка ip адресов и количество запросов от этих пользователей ->
сортируем по количеству запросов по убыванию -> записываем первые 5 полученных пар в список в виде словарей -> 
записываем результат в файл в простом виде или формате json.

###Выводы
_**Bash**_

Плюсы:
* Меньший объём кода (многие задачи можно выполнить одной строкой скрипта)
* Скорость выполнения скрипта
* Возможность запуска из терминала с базовыми утилитами bash

Минусы:
* Не всегда удобно форматировать вывод (например json формат)

_**Python**_

Плюсы:
* Возможность сохранения вывода в любом формате, например, json
* Читаемость кода
* Кроссплатформерность (возможность запуска скриптов на Windows)

Минусы:
* Необходимость установки дополнительных зависимостей для работы скриптв
* Скрипты могут быть затратны по ресурсам и времени
* Объём кода по сравнению с bash скриптами