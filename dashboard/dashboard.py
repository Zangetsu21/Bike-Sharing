import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Load data dari URL
day_df = pd.read_csv('https://raw.githubusercontent.com/Zangetsu21/Bike-Sharing/main/dashboard/day_clean.csv')

# Set judul untuk dashboard
st.write("# Bike Rental Dashboard 🚵")

# Menampilkan metrik penyewaan harian
st.write('## Daily Basis Rental')
col1, col2, col3 = st.columns(3)
total_users = day_df['casual'].sum() + day_df['registered'].sum()

with col1:
    percentage_casual = (day_df['casual'].sum() / total_users) * 100
    st.metric('Casual User', value=f"{percentage_casual:.2f}%")
with col2:
    percentage_registered = (day_df['registered'].sum() / total_users) * 100
    st.metric('Registered User', value=f"{percentage_registered:.2f}%")
with col3:
    st.metric('Total User', value=total_users)

# Pemilihan rentang tanggal
min_date = pd.to_datetime(day_df['date_day']).dt.date.min()
max_date = pd.to_datetime(day_df['date_day']).dt.date.max()
 
with st.sidebar:
    st.image('https://lh3.googleusercontent.com/pw/AP1GczOp-JsFTtiSIPYMbszoaXDjw912tC1QjPVTE3wg6hPT31sbm4hElOLPAEQT4f-Ocnq8MLu4kH08qSizEsgSkIgb1VSOzzc19mEhexl5Lsh5OQDM-_O8LmlbPKZ9skME8rseDtT7QeR6bMj0BQFuT_YC=w2395-h889-s-no-gm?authuser=0')
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Tren penyewaan sepeda berdasarkan bulan
st.write("## Bike Rental Trends By Month")

# Mengelompokkan data berdasarkan tahun dan bulan, dan hitung total penggunaan sepeda
usage_by_year_month = day_df.groupby(['year', 'month'])['count'].sum()
usage_by_year_month = usage_by_year_month.reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
for year in usage_by_year_month['year'].unique():
    data_year = usage_by_year_month[usage_by_year_month['year'] == year]
    ax.plot(data_year['month'], data_year['count'], label=f"Tahun {year+2011}")

ax.set_xlabel('Bulan')
ax.set_ylabel('Total Penggunaan Sepeda (Count)')
ax.set_xticks(range(1, 13))
ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Ags', 'Sep', 'Okt', 'Nov', 'Des'])
ax.legend()
ax.grid(True)

st.pyplot(fig)

# Pola penggunaan sepeda berdasarkan hari dalam seminggu
st.write("## Bike Rental By Day")
usage_by_weekday = day_df.groupby('week_day')[['count', 'casual', 'registered']].mean()
fig, ax = plt.subplots()
usage_by_weekday[['casual', 'registered']].plot(kind='barh', stacked=True, color=['skyblue', 'salmon'], ax=ax)
plt.ylabel('Hari')
plt.xlabel('Rata-rata Penggunaan Sepeda')
plt.grid(axis='x', linestyle='--', alpha=0.7)
st.pyplot(fig)

# Pengaruh cuaca terhadap penggunaan sepeda
st.write("## Bike Rental Based on Weather")
fig, ax = plt.subplots()
sns.boxplot(x='weather_sit', y='count', color='springgreen', data=day_df)
plt.xlabel('Cuaca')
plt.ylabel('Penggunaan Sepeda')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig)

# Penyewaan sepeda berdasarkan musim
st.write("## Bike Rental Based on Season")
usage_by_season = day_df.groupby('season')[['count', 'casual', 'registered']].mean()
fig, ax = plt.subplots()
usage_by_season[['casual', 'registered']].plot(kind='bar', stacked=True, color=['skyblue', 'salmon'], ax=ax)
plt.xlabel('Musim')
plt.ylabel('Rata-rata Penggunaan Sepeda')
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig)

# Tambahkan caption
st.caption('© 2024 Tan Bima Wiragama')