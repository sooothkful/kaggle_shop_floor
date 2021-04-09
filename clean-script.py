import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import statsmodels.formula.api as smf
import statsmodels.api as sm
import patsy as pt

pd.set_option('display.max_columns', 150)
pd.set_option('display.max_rows', 50)


err = pd.read_csv("errors.csv")
fail = pd.read_csv("failures.csv")
mach = pd.read_csv("machines.csv")




err_cnt_2015 = pd.crosstab(index=err["machineID"], columns=err["errorID"])
e = err_cnt_2015.reset_index()

fa_cnt_2015 = pd.crosstab(index=fail["machineID"], columns=fail["failure"])
fai_cnt_2015 = fa_cnt_2015.reset_index()

row_6 = {'machineID':6, 'comp1':0, 'comp2':0, 'comp3':0, 'comp4':0}
row_77 = {'machineID':77, 'comp1':0, 'comp2':0, 'comp3':0, 'comp4':0}
f = fai_cnt_2015.append(row_6, ignore_index=True)
fff = f.append(row_77, ignore_index=True)
ffff = fff.sort_values('machineID')
ffff_ = ffff.reset_index()




machine_dummies = pd.get_dummies(mach['machineID'])
model_dummies = pd.get_dummies(mach['model'])

machine_dummies_ = machine_dummies.reset_index()
model_dummies_ = model_dummies.reset_index()


merg = pd.merge(machine_dummies_, model_dummies_, on="index", how="inner")

merg['machineID'] = mach['machineID']
merg['age'] = mach['age']

merged_1 = pd.merge(ffff_, merg, on="machineID", how="inner")
merged_2 = pd.merge(e, merged_1, on="machineID", how="inner")

merged_3 = merged_2.drop(['index_x', 'index_y'], axis=1)

merged_3['total_error_cnt'] = pd.Series('')
merged_3['total_fail_cnt'] = pd.Series('')

for e in merged_3['total_error_cnt']:
    merged_3['total_error_cnt'] = merged_3['error1'] + merged_3['error2'] + merged_3['error3'] + merged_3['error4'] + merged_3['error5']

for f in merged_3['total_fail_cnt']:
    merged_3['total_fail_cnt'] = merged_3['comp1'] + merged_3['comp2'] + merged_3['comp3'] + merged_3['comp4']
    
merged_3.to_csv('cl-4-reg.csv')



