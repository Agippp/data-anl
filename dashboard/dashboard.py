import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
# from babel.numbers import format_currency
sns.set(style='dark')

def create_seasonal_changes(df):
    seasonal_changes = df.groupby(by=['month', 'weather_cond']).count_rent.mean().sort_values(ascending=False).reset_index()
    return seasonal_changes

def create_holiday_changes(df):
    holiday_changes =  df.groupby(by='holiday').count_rent.mean().reset_index()
    return holiday_changes

def create_weekday_changes(df):
    weekday_changes = df.groupby(by='weekday').count_rent.mean().reset_index()
    return weekday_changes

sepeda_df = pd.read_csv("sepeda_df.csv")
datetime_columns = ['dateday']
sepeda_df.sort_values(by='dateday', inplace=True)
sepeda_df.reset_index(inplace=True)

for column in datetime_columns:
    sepeda_df[column] = pd.to_datetime(sepeda_df['dateday'])

min_date = sepeda_df['dateday'].min()
max_date = sepeda_df['dateday'].max()



with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://i.pinimg.com/564x/17/3c/8e/173c8e1a393602c7eb0aa963e4af3f71.jpg")
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

    time_df = sepeda_df[(sepeda_df['dateday'] >= str(start_date)) & 
                (sepeda_df['dateday'] <= str(end_date))]
    seasonal_changes = create_seasonal_changes(time_df)
    holiday_changes = create_holiday_changes(time_df)
    weekday_changes = create_weekday_changes(time_df)

st.set_option('deprecation.showPyplotGlobalUse', False)

st.header('Pengaruh perubahan kondisi cuaca terhadap perentalan sepeda')
# Visualisasi Bar Chart
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x='month', y='count_rent', hue='weather_cond', data= seasonal_changes)
ax.set_title('Bar Chart of Sepeda Counts by Month and Weather Condition')
st.pyplot()

st.header('Pengaruh perubahan kondisi perentalan sepeda pada Holiday')
# Visualisasi Pie Chart 1
labels = holiday_changes['holiday']
sizes = holiday_changes['count_rent']
colors = ['#D3D3D3', '#72BCD4']
fig, ax = plt.subplots(figsize=(10, 5))
ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
ax.set_title('Percentage of Total Rental Bikes by Holiday')
st.pyplot()

st.header('Pengaruh perubahan kondisi perentalan sepeda pada Weekday')
# Visualisasi Pie Chart 2
labels = weekday_changes['weekday']
sizes = weekday_changes['count_rent']
colors = [
    '#003f5c',
    '#374c80',
    '#7a5195',
    '#bc5090',
    '#ef5675',
    '#ff764a',
    '#ffa600',
]
fig, ax = plt.subplots(figsize=(10, 5))
ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
ax.set_title('Percentage of Total Rental Bikes by Weekday')
st.pyplot()