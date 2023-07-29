import pandas as pd

input_df = pd.read_excel('files/solar_dataset.xlsx',
                         na_values=['?', '-', '-999.00'])

df_cleared = pd.DataFrame()

tmp_df = input_df['Дата_время'].str.split(' ', expand=True)
date = tmp_df[0]
time = tmp_df[1]

date = tmp_df[0].str.split('/', expand=True)
date = date.astype('int32')
day = date[0]
month = date[1]
year = date[2]
df_cleared['День'] = date[0]
df_cleared['Месяц'] = date[1]
df_cleared['Год'] = date[2]

time = tmp_df[1].str.split(':', expand=True)
time = time.astype('int32')
df_cleared['Часы'] = time[0]

df_cleared['Температура градусы Цельсия'] = input_df['Температура']

df_cleared['Влажность проценты'] = input_df['Влажность']. \
    str.replace('%', '').astype('float')

df_cleared['Скорость_ветра м/с'] = input_df['Скорость_ветра']

df_cleared['Точка_росы градусы Цельсия'] = input_df['Точка_росы']. \
    str.replace('[', '').str.replace(']', '').astype('float')

df_cleared['Осадки мм/ч'] = input_df['Осадки']
df_cleared['Угол_солнечного_зенита градусы'] = input_df['Угол_солнечного_зенита']

df_cleared['Инсоляция_атмосфера Вт*ч/м^2'] = input_df['Инсоляция_атмосфера']

df_cleared['Инсоляция_поверхность Вт*ч/м^2'] = input_df['Инсоляция_поверхность']

df_cleared['Влажность проценты'] = input_df['Влажность']. \
    str.replace('%', '').astype('float')

df_cleared = df_cleared[:-5423]
df_cleared['Температура градусы Цельсия'] = round(
    df_cleared['Температура градусы Цельсия'].interpolate(method='polynomial', order=2), 2)
df_cleared['Инсоляция_атмосфера Вт*ч/м^2'] = round(
    df_cleared['Инсоляция_атмосфера Вт*ч/м^2'].interpolate(method='polynomial', order=2), 2)
df_cleared['Инсоляция_поверхность Вт*ч/м^2'] = round(
    df_cleared['Инсоляция_поверхность Вт*ч/м^2'].interpolate(method='polynomial', order=2), 2)

df_cleared['Угол_солнечного_зенита градусы'] = round(
    df_cleared['Угол_солнечного_зенита градусы'].interpolate(method='polynomial', order=2), 2)
df_cleared['Осадки мм/ч'] = round(df_cleared['Осадки мм/ч'].interpolate(method='polynomial', order=2), 2)

df_cleared_0 = df_cleared.drop(df_cleared[(df_cleared['Инсоляция_поверхность Вт*ч/м^2'] < -40) | (
            df_cleared['Инсоляция_поверхность Вт*ч/м^2'] > 500)].index)
df_cleared_1 = df_cleared_0.drop(df_cleared_0[(df_cleared_0['Угол_солнечного_зенита градусы'] < 0) | (
            df_cleared_0['Угол_солнечного_зенита градусы'] >= 180)].index)
df_cleared_2 = df_cleared_1.drop(df_cleared_1[(df_cleared_1['Инсоляция_атмосфера Вт*ч/м^2'] < -40) | (
            df_cleared_1['Инсоляция_атмосфера Вт*ч/м^2'] > 100)].index)
df_cleared_3 = df_cleared_2.drop(df_cleared_2[(df_cleared_2['Температура градусы Цельсия'] < -40) | (
            df_cleared_2['Температура градусы Цельсия'] > 50)].index)

df_cleared_3['Температура градусы Цельсия'] = df_cleared_3['Температура градусы Цельсия'].shift(24)
df_cleared_3['Влажность проценты'] = df_cleared_3['Влажность проценты'].shift(24)
df_cleared_3['Скорость_ветра м/с'] = df_cleared_3['Скорость_ветра м/с'].shift(24)
df_cleared_3['Осадки мм/ч'] = df_cleared_3['Осадки мм/ч'].shift(24)
df_cleared_3['Угол_солнечного_зенита градусы'] = df_cleared_3['Угол_солнечного_зенита градусы'].shift(24)
df_cleared_3['Инсоляция_поверхность Вт*ч/м^2_previous'] = df_cleared_3['Инсоляция_поверхность Вт*ч/м^2'].shift(24)

df_cleared_3 = df_cleared_3.iloc[25:, :]

df_cleared_3 = df_cleared_3[
    ['День', 'Месяц', 'Год', 'Часы', 'Температура градусы Цельсия', 'Влажность проценты', 'Точка_росы градусы Цельсия',
     'Осадки мм/ч', 'Угол_солнечного_зенита градусы', 'Инсоляция_атмосфера Вт*ч/м^2',
     'Инсоляция_поверхность Вт*ч/м^2_previous', 'Инсоляция_поверхность Вт*ч/м^2']]


df_cleared_3.to_excel('files/solar_cleared_data.xlsx', index=False)