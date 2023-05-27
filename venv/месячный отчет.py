import os
import pandas as pd
import json
files = os.listdir("C:\\Users\Iamem\Desktop\Апрель")
os.chdir("C:\\Users\Iamem\Desktop\Апрель")
json_files = [i for i in files if i.endswith('.json')]
filesList = []
names = []
for file in json_files:
    with open(file, encoding='utf-8') as f:
        a = json.load(f)
        filesList.append(a)
job_times = []
contract_names = []
b = []
for i in filesList:
    for j in i[50:]:
        try:
            if j['Column36'] > 0:
                names.append(i[1]['Column3'])
                job_times.append(round(j['Column36'], 1))
                contract_names.append(j['Отчет по загрузке специалиста'])
                b.append({'Name': i[1]['Column3'],
                        j['Отчет по загрузке специалиста']: round(j['Column36'], 1)})
        except (KeyError, TypeError):
            pass
set_names = sorted(set(names))
set_contracts = list(sorted(set(contract_names)))


#print(filesList[4][50:])
df = pd.DataFrame(columns=set_names, index=set_contracts)
for i in filesList:
    for j in i[50:]:
        try:
            if j['Column36'] > 0:
                df.at[j['Отчет по загрузке специалиста'], i[1]['Column3']] = round(j['Column36'], 1)
        except (KeyError, TypeError):
            pass
print(df)
df.to_excel("C:\\Users\Iamem\Desktop\отчеты.xlsx")
# df.at[contract_names.index(j['Отчет по загрузке специалиста']), i[1]['Column3']]
