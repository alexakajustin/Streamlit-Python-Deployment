import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pages_config import apply_theme, load_data, section_header, problem_box, interpret_box
from pages_part1 import page_streamlit, page_geopandas, page_missing_outliers, page_encoding, page_scaling
from pages_part2 import page_pandas, page_logistic, page_regression, page_clustering

# --- INIT ---
apply_theme()
df = load_data()

# --- SIDEBAR ---
st.sidebar.markdown("""
<div style="text-align:center; padding: 10px;">
    <h2 style="color:#f3e600; font-family:'Orbitron',monospace; font-size:1.1rem; margin:0;">CD PROJEKT RED</h2>
    <p style="color:#00e5ff; font-size:0.8rem; margin:5px 0;">Analiză Financiară 2010–2025</p>
    <hr style="border-color:#f3e60033;">
</div>
""", unsafe_allow_html=True)

st.sidebar.title("📋 Cerințe Seminar")

page = st.sidebar.radio("Selectează Cerința:", [
    "🏠 Prezentare Generală",
    "1. Metode Streamlit (UI/Grafice)",
    "2. Utilizarea Geopandas",
    "3. Valori Lipsă & Extreme",
    "4. Codificarea Datelor",
    "5. Metode de Scalare",
    "6. Pandas (Grupare/Agregare)",
    "7. Regresie Logistică (Sklearn)",
    "8. Regresie Multiplă (Statsmodels)",
    "9. Clusterizare K-Means (Sklearn)"
])

st.sidebar.markdown("---")

# --- HOME PAGE ---
if page == "🏠 Prezentare Generală":
    st.markdown("""
    # 🎮 CD PROJEKT RED — Analiză Financiară Completă
    ### Proiect Seminar Pachete Software | Python & Streamlit
    ---
    """)

    st.markdown("""
    <div class="info-box">
    📋 <b>Despre Proiect:</b><br>
    Acest dashboard interactiv analizează performanța financiară a <b>CD Projekt Red</b> (2010–2025),
    studioul polonez de gaming responsabil pentru <i>The Witcher 3</i> și <i>Cyberpunk 2077</i>.
    Proiectul demonstrează utilizarea a <b>9 cerințe obligatorii</b> din programul de seminar, pe baza a <b>16 observații</b> anuale,
    fiecare cu definirea problemei, metodologie, rezultate și interpretare economică.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## 📈 Sumar Executiv")
    c1, c2, c3, c4 = st.columns(4)
    latest = df.iloc[-1]
    c1.metric("Venituri 2025", f"{latest['Revenue']:,.0f} PLN")
    c2.metric("Profit Net 2025", f"{latest['NetProfit']:,.0f} PLN")
    c3.metric("Marja Profit", f"{latest['NetProfit']/latest['Revenue']*100:.1f}%")
    c4.metric("Active Totale", f"{latest['Assets']:,.0f} PLN")

    st.markdown("## 📊 Evoluția Financiară (2010–2025)")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Year'], y=df['Revenue'], name='Venituri',
                             fill='tozeroy', line=dict(color='#f3e600', width=3),
                             fillcolor='rgba(243,230,0,0.1)'))
    fig.add_trace(go.Scatter(x=df['Year'], y=df['NetProfit'], name='Profit Net',
                             fill='tozeroy', line=dict(color='#00e5ff', width=3),
                             fillcolor='rgba(0,229,255,0.1)'))
    fig.add_trace(go.Scatter(x=df['Year'], y=df['MarketingCosts'], name='Costuri Marketing',
                             line=dict(color='#ff6ec7', width=2, dash='dot')))
    fig.update_layout(template='plotly_dark', hovermode='x unified',
                      font=dict(family='Inter'), yaxis_title='mii PLN',
                      legend=dict(orientation='h', yanchor='bottom', y=1.02))
    fig.add_vrect(x0=2019.5, x1=2020.5, fillcolor='#f3e600', opacity=0.08,
                  annotation_text="Launch CP2077", annotation_position="top")
    st.plotly_chart(fig, width='stretch')

    st.markdown("""
    ## 🎯 Structura Proiectului — Cele 9 Cerințe

    | # | Cerința | Pachet/Metodă | Descriere |
    |---|---------|---------------|-----------|
    | 1 | **Metode Streamlit** | `streamlit`, `plotly` | Dashboard interactiv, KPI-uri, grafice |
    | 2 | **Geopandas** | `geopandas`, `plotly` | Hartă coropletica — distribuția geografică |
    | 3 | **Valori Lipsă & Extreme** | `pandas`, `scipy` | Detectare missing values, outlieri IQR/Z-score |
    | 4 | **Codificarea Datelor** | `sklearn.LabelEncoder` | Label Encoding, One-Hot Encoding |
    | 5 | **Metode de Scalare** | `sklearn.preprocessing` | StandardScaler, MinMaxScaler, RobustScaler |
    | 6 | **Pandas Grupare** | `pandas.groupby` | Agregare pe ere, pivot tables |
    | 7 | **Regresie Logistică** | `sklearn.LogisticRegression` | Clasificare profitabilitate ridicată/scăzută |
    | 8 | **Regresie Multiplă** | `statsmodels.OLS` | Impact Revenue & Marketing asupra Profitului |
    | 9 | **Clusterizare K-Means** | `sklearn.KMeans` | Segmentarea anilor de performanță |

    ---
    *Selectează o cerință din meniul lateral pentru a explora analiza detaliată.*
    """)

    st.markdown("""
    <div class="interpret-box">
    💡 <b>Context Economic: Eșecul și "The Redemption Arc" Cyberpunk 2077</b><br>
    Analiza de față ilustrează trei faze distincte ale companiei:<br><br>
    <b>1. Fondare și Creștere (2010-2019):</b> O perioadă de dezvoltare continuă, de la succesul inițial al seriei The Witcher la construirea reputației de studio AAA.<br><br>
    <b>2. Boom & Criză (2020-2021):</b> Lansarea Cyberpunk 2077 a fost un paradox financiar. Deși 2020 a adus venituri record de peste 2.1 mld PLN din precomenzi, lansarea a fost un <b>eșec tehnic catastrofal</b> pe consolele old-gen. Jocul a fost retras temporar de pe PlayStation Store, s-au oferit refund-uri masive, investitorii au dat în judecată compania, iar acțiunile s-au prăbușit. Anul 2021 reflectă costurile imense ale acestui dezastru (scădere de 58% a veniturilor și o marjă de profit de doar 23.5%).<br><br>
    <b>3. Recuperarea Reputației (2022-2025):</b> În loc să abandoneze proiectul, CDPR a investit timp și bani în repararea jocului. Succesul uriaș al anime-ului <i>Cyberpunk: Edgerunners</i>, alături de lansarea Patch-ului 2.0 și a expansiunii <i>Phantom Liberty</i> (2023), au transformat jocul dintr-un fail absolut într-un masterclass de RPG. Acest <i>"redemption arc"</i> se traduce vizibil în datele financiare: veniturile s-au stabilizat la peste 1 mld PLN anual, iar eficiența s-a maximizat, marja de profit ajungând la un nivel record de <b>60% în 2025</b>.
    </div>
    """, unsafe_allow_html=True)

# --- PAGES ---
elif page == "1. Metode Streamlit (UI/Grafice)":
    page_streamlit(df)
elif page == "2. Utilizarea Geopandas":
    page_geopandas(df)
elif page == "3. Valori Lipsă & Extreme":
    page_missing_outliers(df)
elif page == "4. Codificarea Datelor":
    page_encoding(df)
elif page == "5. Metode de Scalare":
    page_scaling(df)
elif page == "6. Pandas (Grupare/Agregare)":
    page_pandas(df)
elif page == "7. Regresie Logistică (Sklearn)":
    page_logistic(df)
elif page == "8. Regresie Multiplă (Statsmodels)":
    page_regression(df)
elif page == "9. Clusterizare K-Means (Sklearn)":
    page_clustering(df)
