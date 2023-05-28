import os
import pandas as pd
import json
import re
import itertools
files = os.listdir("C:\\Users\Iamem\Desktop\Апрель")
os.chdir("C:\\Users\Iamem\Desktop\Апрель")
json_files = [i for i in files if i.endswith('.json')]
filesList = []
names = [] # список имен сотрудников

for file in json_files:  # создаем список словарей из json файлов ключ - строка, значения - с 1 по 36 колонку в таблицах
    with open(file, encoding='utf-8') as f:
        a = json.load(f)
        filesList.append(a)

job_times = []
contract_names = []

for i in filesList:
    for j in i[50:]: # отсекаем все до 50 строки
        try:
            if j['Column36'] > 0: # если отработанное время не 0, то добавляем имя сот-ка,
                                 # рабочие часы по контракту и имя контракта
                names.append(i[1]['Column3'])
                job_times.append(round(j['Column36'], 1))
                contract_names.append(j['Отчет по загрузке специалиста'])
        except (KeyError, TypeError):
            pass
set_names = sorted(set(names))

contact_name_pattern = re.compile(r'\d\.\d\.\d{0,1}\s{0}') # регялрное выражение для номера контракта

num_cts = [contact_name_pattern.findall(c_name) for c_name in contract_names] # список спиков номеров контрактов

num_contracts = list(itertools.chain(*num_cts)) # одномерный список контрактов

set_contracts = list(sorted(set(num_contracts))) # множество номеров контрактов

df = pd.DataFrame(columns=set_names, index=set_contracts)

for i in filesList:
    for j in i[50:]:
        try:
            if j['Column36'] > 0:
                df.at[contact_name_pattern.search(j['Отчет по загрузке специалиста']).group(),
                i[1]['Column3']] = round(j['Column36'], 1)
        except (KeyError, TypeError):
            pass


print(df)
print(set_contracts)
# print(set_contracts)
df.to_excel("C:\\Users\Iamem\Desktop\отчеты_апрель.xlsx")

