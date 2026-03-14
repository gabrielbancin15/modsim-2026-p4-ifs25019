import streamlit as st
import numpy as np
import math
from scipy.integrate import solve_ivp
import plotly.graph_objects as go

st.set_page_config(page_title="Simulasi Tangki Air", layout="wide")

st.title("💧 Simulasi Kontinu Sistem Tangki Air")

st.write(
"Aplikasi ini mensimulasikan perubahan ketinggian air dalam tangki "
"berdasarkan debit masuk dan debit keluar secara kontinu."
)

# =========================================
# SIDEBAR INPUT
# =========================================

st.sidebar.header("Parameter Tangki")

radius = st.sidebar.number_input("Radius Tangki (m)",0.5,10.0,1.0)

height_max = st.sidebar.number_input("Tinggi Tangki (m)",1.0,20.0,5.0)

qin = st.sidebar.slider("Debit Masuk (m³/s)",0.0,0.5,0.05)

qout = st.sidebar.slider("Debit Keluar (m³/s)",0.0,0.5,0.03)

initial_h = st.sidebar.slider("Tinggi Awal Air (m)",0.0,float(height_max),0.0)

sim_time = st.sidebar.slider("Durasi Simulasi (menit)",1,120,30)


# =========================================
# MODEL MATEMATIKA
# =========================================

area = math.pi * radius**2

def tank_model(t,y):

    h = y[0]

    q_in = qin
    q_out = qout

    if h <= 0 and q_out > q_in:
        q_out = q_in

    if h >= height_max and q_in > q_out:
        q_in = q_out

    dhdt = (q_in - q_out) / area

    return [dhdt]


# =========================================
# SIMULASI
# =========================================

t_eval = np.linspace(0,sim_time*60,300)

sol = solve_ivp(
    tank_model,
    [0,sim_time*60],
    [initial_h],
    t_eval=t_eval
)

time = sol.t/60
height = np.clip(sol.y[0],0,height_max)
volume = height*area

# =========================================
# STATUS
# =========================================

st.success("✅ Simulasi selesai!")

# =========================================
# METRIK DASHBOARD
# =========================================

col1,col2,col3,col4 = st.columns(4)

col1.metric("Volume Maksimum",f"{area*height_max:.2f} m³")
col2.metric("Volume Akhir",f"{volume[-1]:.2f} m³")
col3.metric("Tinggi Maksimum",f"{max(height):.2f} m")
col4.metric("Tinggi Akhir",f"{height[-1]:.2f} m")

col5,col6,col7,col8 = st.columns(4)

col5.metric("Debit Masuk",f"{qin:.2f} m³/s")
col6.metric("Debit Keluar",f"{qout:.2f} m³/s")
col7.metric("Luas Alas Tangki",f"{area:.2f} m²")
col8.metric("Durasi Simulasi",f"{sim_time} menit")

# =========================================
# TAB MENU
# =========================================

tab1,tab2,tab3 = st.tabs([
"📈 Profil Ketinggian Air",
"📊 Volume Tangki",
"📋 Data Simulasi"
])

# =========================================
# TAB 1 GRAFIK KETINGGIAN
# =========================================

with tab1:

    st.header("Profil Ketinggian Air")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=time,
            y=height,
            mode="lines",
            name="Tinggi Air"
        )
    )

    fig.add_hline(
        y=height_max,
        line_dash="dash",
        annotation_text="Kapasitas Maks"
    )

    fig.update_layout(
        xaxis_title="Waktu (menit)",
        yaxis_title="Tinggi Air (m)",
        height=500
    )

    st.plotly_chart(fig,use_container_width=True)


# =========================================
# TAB 2 GRAFIK VOLUME
# =========================================

with tab2:

    st.header("Volume Air di Tangki")

    fig2 = go.Figure()

    fig2.add_trace(
        go.Scatter(
            x=time,
            y=volume,
            mode="lines",
            name="Volume Air"
        )
    )

    fig2.update_layout(
        xaxis_title="Waktu (menit)",
        yaxis_title="Volume (m³)",
        height=500
    )

    st.plotly_chart(fig2,use_container_width=True)


# =========================================
# TAB DATA
# =========================================

with tab3:

    st.write("Data hasil simulasi")

    st.dataframe({
        "Waktu (menit)":time,
        "Tinggi Air (m)":height,
        "Volume (m3)":volume
    })