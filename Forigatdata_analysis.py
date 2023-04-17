import pandas as pd

df = pd.read_excel("ForigatDataExcel.xlsx")
#print(df)
df = df[df['MaritalStatus'] == 'متزوج']
#print(df)
df = df[df['NumberOfChildrens'] > 0 ]
#print(df)
SortedByRangeOfRemindedMoney= df[df['Reminded Dept'].between(20000,100000)]
#print(SortedByRangeOfRemindedMoney)

SortedByRangeOfRemindedMoney['Remined/Original']=(SortedByRangeOfRemindedMoney['Reminded Dept']/SortedByRangeOfRemindedMoney['OriginalDept'])*100


#print(SortedByRangeOfRemindedMoney)
RangeofRemindedPercent = SortedByRangeOfRemindedMoney[SortedByRangeOfRemindedMoney['Remined/Original'].between(20,50)]
#print(RangeofRemindedPercent)

SortedByAge=RangeofRemindedPercent.sort_values(by=['Age' ,'NumberOfChildrens'] , ascending= False )
print(SortedByAge)

SortedByAge.to_excel("ForigatFinal.xlsx")