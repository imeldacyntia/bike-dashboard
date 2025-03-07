import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Memuat data dari file CSV
file_path = "dashboard/all_data.csv"
bike_df = pd.read_csv(file_path)

# Judul Dashboard
st.title("Dashboard Analisis Data Bike Sharing")

# Sidebar untuk navigasi dan eksplorasi data
with st.sidebar:
    st.subheader('🚲 Bike Sharing Insights')
    st.image("https://tse1.mm.bing.net/th?id=OIP.8r_4XwVRYvwavNJx3Yq6awHaE8&pid=Api&P=0&h=180")
    
    st.header("🔍 Eksplorasi Data")
    with st.expander("📊 Opsi Tampilan Data"):
        show_summary = st.toggle("Tampilkan Ringkasan Informasi", value=True)
        show_first_rows = st.toggle("Tampilkan Lima Baris Pertama", value=True)
        show_duplicates = st.toggle("Periksa Duplikasi", value=True)
        show_statistics = st.toggle("Tampilkan Statistik", value=True)
        show_visualizations = st.toggle("Tampilkan Visualisasi", value=True)

# Menampilkan data berdasarkan status toggle
if show_summary:
    st.subheader("Ringkasan Informasi Dataset")
    st.write("""
    Dataset ini berisi informasi tentang penggunaan layanan berbagi sepeda, dengan fokus pada pengaruh cuaca, 
    hari kerja, dan waktu dalam sehari terhadap jumlah penyewaan. Dataset telah dibersihkan untuk memastikan 
    tidak ada nilai yang hilang atau anomali yang signifikan. Fitur utama dalam dataset mencakup waktu penyewaan, 
    kondisi cuaca, suhu, kelembapan, kecepatan angin, serta jumlah pengguna casual dan registered.
    """)

if show_first_rows:
    st.subheader("Lima Baris Pertama DataFrame")
    st.write(bike_df.head())

if show_duplicates:
    num_duplicates = bike_df.duplicated().sum()
    st.subheader("Periksa Duplikasi")
    st.write(f"Jumlah Duplikasi: {num_duplicates}")

if show_statistics:
    st.subheader("Ringkasan Statistik DataFrame")
    st.write(bike_df.describe())

# Visualisasi data
if show_visualizations:
    st.subheader("Visualisasi Data")
    
    # 1. Pie chart: Rata-rata penyewaan sepeda pada hari kerja vs akhir pekan
    avg_workingday = bike_df.groupby('workingday_day')['cnt_day'].mean()
    labels = ['Akhir Pekan', 'Hari Kerja']
    fig, ax = plt.subplots()
    ax.pie(avg_workingday, labels=labels, autopct='%1.1f%%', colors=['lightcoral', 'skyblue'])
    ax.set_title("Rata-rata Penyewaan Sepeda: Hari Kerja vs Akhir Pekan")
    st.pyplot(fig)
    
    # 2. Bar chart: Pengaruh cuaca terhadap jumlah penyewaan sepeda (PERBAIKAN DENGAN PALET VIRIDIS)
    weather_impact = bike_df.groupby('weather_label')['cnt_day'].mean().reset_index()
    weather_impact_sorted = weather_impact.sort_values("cnt_day", ascending=False)
    
    # Menggunakan warna viridis dari Seaborn
    viridis_colors = sns.color_palette("viridis", len(weather_impact_sorted)).as_hex()
    
    fig2 = px.bar(
        weather_impact_sorted, 
        x='cnt_day', 
        y='weather_label', 
        orientation='h',
        title='Pengaruh Cuaca terhadap Rata-rata Penyewaan Sepeda',
        labels={'cnt_day': 'Rata-rata Jumlah Penyewaan', 'weather_label': 'Kondisi Cuaca'},
        color='weather_label',  
        color_discrete_sequence=viridis_colors  # Menggunakan warna dari palet viridis Seaborn
    )
    st.plotly_chart(fig2)
    
    # 3. Line chart: Perbedaan pola penyewaan sepeda antara pengguna casual dan registered per jam
    hourly_trend = bike_df.groupby('hr')[['casual_hour', 'registered_hour']].mean().reset_index()
    fig3, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(x='hr', y='casual_hour', data=hourly_trend, label='Casual', marker='o', color='blue')
    sns.lineplot(x='hr', y='registered_hour', data=hourly_trend, label='Registered', marker='s', color='red')
    ax.set_title("Perbandingan Pola Penyewaan Sepeda antara Casual dan Registered per Jam")
    ax.set_xlabel("Jam dalam Sehari")
    ax.set_ylabel("Rata-rata Jumlah Penyewaan Sepeda")
    ax.set_xticks(range(0, 24))
    ax.legend(title="Tipe Pengguna")
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    st.pyplot(fig3)
    
st.caption('Copyright (c) Imelda Cyntia')
