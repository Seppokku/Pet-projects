import os
import json
import pandas as pd
import re
import itertools
files = os.listdir("C:\\Users\Iamem\Desktop\Март")

os.chdir("C:\\Users\Iamem\Desktop\Март")

excel_files = [i for i in files if i.endswith('.xls') or i.endswith('.xlsx')]

workers_names = []

contact_name_pattern = re.compile(r'\d\.\d\.\d{0,1}\s{0}')

contract_names = []


for file in excel_files:
     data = pd.read_excel(file)
     workers_names.append(data['Unnamed: 2'].loc[data.index[2]])
     for i, j in data.tail(22).iterrows():
         try:
             if j['Unnamed: 35'] > 0:  # если отработанное время не 0, то добавляем имя сот-ка,
                  # рабочие часы по контракту и имя контракта
                 contract_names.append(j['Unnamed: 1'])
         except (KeyError, TypeError, ValueError):
             pass

num_cts = [contact_name_pattern.findall(c_name) for c_name in contract_names]

num_contracts = list(itertools.chain(*num_cts)) # одномерный список контрактов

set_contracts = list(sorted(set(num_contracts))) # множество номеров контрактов

df = pd.DataFrame(columns=workers_names, index=set_contracts)

for i in excel_files:
    data = pd.read_excel(i)
    for k, j in data.tail(22).iterrows():
        try:
            if j['Unnamed: 35'] > 0:
                df.at[contact_name_pattern.search(j['Unnamed: 1']).group(), data['Unnamed: 2'].loc[data.index[2]]] = round(j['Unnamed: 35'], 1)
        except (KeyError, TypeError, ValueError):
            pass
print(df)

df.to_excel("C:\\Users\Iamem\Desktop\отчеты_март.xlsx")

