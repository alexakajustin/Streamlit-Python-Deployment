import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from pages_config import section_header, problem_box, method_box, interpret_box, info_box


def page_streamlit(df):
    section_header("📊", "Metode Streamlit pentru Afișare și Grafice",
                   "Vizualizarea indicatorilor financiari cheie ai CD Projekt Red (2010–2025)")

    problem_box("Cum putem monitoriza și vizualiza performanța financiară a CD Projekt Red pe o perioadă de 16 ani? "
                "Compania a trecut prin cicluri dramatice — de la succesul The Witcher 3 la controversatul "
                "launch Cyberpunk 2077 — iar înțelegerea acestor dinamici necesită instrumente interactive de vizualizare.")

    info_box("Setul de date conține <b>16 observații</b> (2010–2025) cu indicatori financiari cheie extrași din rapoartele "
             "anuale CDPR: <i>Revenue, Operating Profit, Net Profit, Marketing Costs, Total Assets, Total Equity</i> — "
             "toate exprimate în mii PLN (zlotul polonez).")

    method_box("Utilizăm <b>Streamlit</b> pentru crearea dashboard-ului interactiv:<br>"
               "• <code>st.metric()</code> — afișarea KPI-urilor cu formatare numerică<br>"
               "• <code>st.columns()</code> — layout responsive pe coloane<br>"
               "• <code>plotly.express</code> — grafice interactive (line, bar, area)<br>"
               "• <code>st.tabs()</code> — organizarea conținutului pe tab-uri")

    st.markdown("## 📈 KPI-uri Cheie (Ultimul An Raportat — 2025)")
    latest = df.iloc[-1]
    prev = df.iloc[-2]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Venituri", f"{latest['Revenue']:,.0f} PLN", f"{((latest['Revenue']/prev['Revenue'])-1)*100:+.1f}%")
    c2.metric("Profit Net", f"{latest['NetProfit']:,.0f} PLN", f"{((latest['NetProfit']/prev['NetProfit'])-1)*100:+.1f}%")
    c3.metric("Active Totale", f"{latest['Assets']:,.0f} PLN", f"{((latest['Assets']/prev['Assets'])-1)*100:+.1f}%")
    c4.metric("Costuri Marketing", f"{latest['MarketingCosts']:,.0f} PLN", f"{((latest['MarketingCosts']/prev['MarketingCosts'])-1)*100:+.1f}%")

    st.markdown("## 📊 Vizualizări Interactive")
    tab1, tab2, tab3 = st.tabs(["📈 Evoluție Venituri", "📊 Structura Profitabilității", "📉 Costuri vs. Profit"])

    with tab1:
        fig = px.area(df, x='Year', y='Revenue', markers=True, template="plotly_dark",
                      title="Evoluția Veniturilor CDPR (2010–2025)",
                      labels={'Revenue': 'Venituri (mii PLN)', 'Year': 'An'})
        fig.update_traces(fill='tozeroy', line_color='#f3e600', fillcolor='rgba(243,230,0,0.15)')
        fig.update_layout(font=dict(family="Inter"), hovermode='x unified')
        st.plotly_chart(fig, width='stretch')
        st.markdown("> **Observație:** Anul 2020 marchează un vârf absolut de **2.14 miliarde PLN** datorat "
                    "lansării Cyberpunk 2077, urmat de o corecție semnificativă în 2021.")

    with tab2:
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(x=df['Year'], y=df['Revenue'], name='Venituri', marker_color='#f3e600'))
        fig2.add_trace(go.Bar(x=df['Year'], y=df['OperatingProfit'], name='Profit Operațional', marker_color='#00e5ff'))
        fig2.add_trace(go.Bar(x=df['Year'], y=df['NetProfit'], name='Profit Net', marker_color='#ff6ec7'))
        fig2.update_layout(template="plotly_dark", barmode='group', title="Structura Profitabilității pe Ani",
                           font=dict(family="Inter"), yaxis_title="mii PLN")
        st.plotly_chart(fig2, width='stretch')

    with tab3:
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=df['Year'], y=df['MarketingCosts'], name='Costuri Marketing',
                                  line=dict(color='#ff6ec7', width=3), mode='lines+markers'))
        fig3.add_trace(go.Scatter(x=df['Year'], y=df['NetProfit'], name='Profit Net',
                                  line=dict(color='#00e5ff', width=3), mode='lines+markers'))
        fig3.update_layout(template="plotly_dark", title="Costuri de Marketing vs. Profit Net",
                           font=dict(family="Inter"), yaxis_title="mii PLN")
        st.plotly_chart(fig3, width='stretch')

    df['Margin'] = (df['NetProfit'] / df['Revenue'] * 100).round(1)
    st.markdown("## 📋 Tabel Complet — Date Financiare CDPR")
    st.dataframe(df[['Year','Revenue','OperatingProfit','NetProfit','MarketingCosts','Assets','Margin']], use_container_width=True)

    interpret_box("Lansarea Cyberpunk 2077 în decembrie 2020 a generat venituri record de <b>2.14 mld PLN</b>, "
                  "de 4x față de 2019. Însă controversele legate de calitatea jocului pe console au dus la o scădere "
                  "de <b>58%</b> în 2021. Din 2022, compania și-a reconstruit încrederea — veniturile s-au stabilizat "
                  "iar marja de profit net a crescut de la 23.5% (2021) la <b>60% (2025)</b>, semn al maturizării "
                  "strategiei de monetizare post-launch.")


def page_geopandas(df):
    section_header("🗺️", "Utilizarea Pachetului Geopandas",
                   "Analiza distribuției geografice a veniturilor CD Projekt Red")

    problem_box("Care este distribuția geografică a veniturilor CDPR? Identificarea piețelor cheie este esențială "
                "pentru strategia de expansiune — compania depinde predominant de piața nord-americană.")

    info_box("Datele provin din raportul anual CDPR 2025 (Investor Relations):<br>"
             "• <b>America de Nord:</b> 75.5% din venituri<br>"
             "• <b>Europa:</b> 11.5%<br>"
             "• <b>Asia:</b> 9.3%<br>"
             "• <b>Polonia:</b> 3.3%<br>"
             "• <b>Altele:</b> 0.4%")

    method_box("Utilizăm <b>Geopandas</b> pentru procesarea datelor geospațiale:<br>"
               "• Încărcarea unui GeoJSON cu granițele țărilor<br>"
               "• Atribuirea ponderilor de venituri pe regiuni<br>"
               "• Vizualizarea cu <code>plotly.express.choropleth()</code> — hartă coropletica interactivă")

    st.markdown("## 🌍 Harta Distribuției Veniturilor")
    rev_data = pd.DataFrame({
        'Region': ['America de Nord', 'Europa', 'Asia', 'Polonia', 'Altele'],
        'Pondere (%)': [75.5, 11.5, 9.3, 3.3, 0.4],
        'Venituri Est. 2025 (mii PLN)': [
            round(df.iloc[-1]['Revenue'] * 0.755),
            round(df.iloc[-1]['Revenue'] * 0.115),
            round(df.iloc[-1]['Revenue'] * 0.093),
            round(df.iloc[-1]['Revenue'] * 0.033),
            round(df.iloc[-1]['Revenue'] * 0.004)]
    })

    col1, col2 = st.columns([2, 1])
    with col1:
        try:
            world = gpd.read_file("https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json")
            world['Revenue_Share'] = 0.0
            na_countries = ['United States of America', 'Canada', 'Mexico']
            eu_countries = ['Germany', 'France', 'United Kingdom', 'Italy', 'Spain', 'Netherlands', 'Sweden', 'Norway']
            asia_countries = ['China', 'Japan', 'South Korea', 'India', 'Australia']
            world.loc[world['name'].isin(na_countries), 'Revenue_Share'] = 75.5
            world.loc[world['name'] == 'Poland', 'Revenue_Share'] = 3.3
            world.loc[world['name'].isin(eu_countries), 'Revenue_Share'] = 11.5
            world.loc[world['name'].isin(asia_countries), 'Revenue_Share'] = 9.3

            fig = px.choropleth(world, geojson=world.__geo_interface__, locations=world.index,
                                color="Revenue_Share", hover_name="name",
                                color_continuous_scale=["#0a0a0f","#1a1a2e","#00e5ff","#f3e600"],
                                title="Harta Distribuției Veniturilor CDPR pe Regiuni (%)",
                                template="plotly_dark")
            fig.update_layout(font=dict(family="Inter"), geo=dict(bgcolor='#0a0a0f'))
            st.plotly_chart(fig, width='stretch')
        except Exception as e:
            st.warning(f"Nu s-a putut încărca harta GeoJSON: {e}")

    with col2:
        fig_pie = px.pie(rev_data, values='Pondere (%)', names='Region',
                         color_discrete_sequence=['#f3e600','#00e5ff','#ff6ec7','#7b68ee','#555'],
                         title="Structura Veniturilor pe Regiuni", template="plotly_dark")
        fig_pie.update_layout(font=dict(family="Inter"))
        st.plotly_chart(fig_pie, width='stretch')

    st.dataframe(rev_data, use_container_width=True)

    interpret_box("CDPR depinde masiv de piața <b>nord-americană (75.5%)</b>, ceea ce reprezintă un risc de concentrare. "
                  "Piața asiatică (9.3%) are un potențial de creștere semnificativ, mai ales prin expansiunea pe piața "
                  "mobilă din China. Diversificarea geografică va fi esențială pentru stabilitatea pe termen lung.")


def page_missing_outliers(df):
    section_header("🔍", "Tratarea Valorilor Lipsă și Extreme",
                   "Evaluarea integrității și calității datelor financiare CDPR")

    problem_box("Sunt datele financiare complete și coerente? Valorile lipsă sau extreme pot distorsiona analizele "
                "statistice ulterioare. Trebuie identificate, cuantificate și tratate corespunzător.")

    method_box("• <b>Valori lipsă:</b> <code>df.isnull().sum()</code> și heatmap cu <code>seaborn</code><br>"
               "• <b>Valori extreme (outliers):</b> Metoda IQR (Interquartile Range)<br>"
               "  <code>IQR = Q3 − Q1</code>; Outlier dacă <code>x < Q1 − 1.5·IQR</code> sau <code>x > Q3 + 1.5·IQR</code><br>"
               "• <b>Z-Score:</b> <code>z = (x − μ) / σ</code>; Outlier dacă <code>|z| > 2</code>")

    st.markdown("## 📋 Analiza Valorilor Lipsă")
    missing = df.isnull().sum().reset_index()
    missing.columns = ['Variabilă', 'Nr. Valori Lipsă']
    missing['Procent (%)'] = (df.isnull().mean() * 100).values.round(2)
    total = missing['Nr. Valori Lipsă'].sum()

    c1, c2 = st.columns(2)
    with c1:
        st.dataframe(missing, use_container_width=True)
    with c2:
        if total > 0:
            st.warning(f"⚠️ S-au identificat **{total}** valori lipsă în setul de date.")
            fig = px.imshow(df.isnull().astype(int).T, color_continuous_scale=['#1a1a2e','#f3e600'],
                            title="Heatmap Valori Lipsă", template="plotly_dark",
                            labels=dict(x="Observația", y="Variabila", color="Lipsă"))
            st.plotly_chart(fig, width='stretch')
        else:
            st.success("✅ Nu există valori lipsă în setul de date principal.")

    st.markdown("## 📊 Detectarea Valorilor Extreme (Outliers)")
    num_cols = ['Revenue', 'OperatingProfit', 'NetProfit', 'MarketingCosts', 'Assets']
    col_sel = st.selectbox("Selectează variabila pentru analiza outlierilor:", num_cols)

    c1, c2 = st.columns(2)
    with c1:
        fig = px.box(df, y=col_sel, points="all", template="plotly_dark",
                     title=f"Boxplot — {col_sel}", color_discrete_sequence=['#00e5ff'],
                     hover_data={'Year': True})
        fig.update_layout(font=dict(family="Inter"))
        st.plotly_chart(fig, width='stretch')
    with c2:
        fig2 = px.histogram(df, x=col_sel, nbins=8, template="plotly_dark",
                            title=f"Distribuția — {col_sel}", color_discrete_sequence=['#f3e600'])
        fig2.update_layout(font=dict(family="Inter"))
        st.plotly_chart(fig2, width='stretch')

    Q1 = df[col_sel].quantile(0.25)
    Q3 = df[col_sel].quantile(0.75)
    IQR = Q3 - Q1
    outliers = df[(df[col_sel] < Q1 - 1.5*IQR) | (df[col_sel] > Q3 + 1.5*IQR)]
    if len(outliers) > 0:
        ani_outlier = ", ".join([str(int(y)) for y in outliers['Year'].values])
        st.warning(f"🔴 S-au detectat **{len(outliers)} outlier(i)** pentru {col_sel}: anul/anii **{ani_outlier}**")
    else:
        st.success(f"✅ Nu s-au detectat outlieri pentru {col_sel} (metoda IQR).")

    interpret_box("Anul <b>2020</b> apare ca outlier pentru Revenue și NetProfit — veniturile de 2.14 mld PLN "
                  "sunt de ~4x față de media celorlalți ani. Acesta nu este o eroare, ci reflectă impactul real "
                  "al lansării Cyberpunk 2077. În analize, trebuie tratat ca <i>outlier legitim</i> și nu eliminat.")


def page_encoding(df):
    section_header("🏷️", "Metode de Codificare a Datelor",
                   "Transformarea variabilelor categoriale pentru analize cantitative")

    problem_box("Algoritmii de machine learning necesită date numerice. Cum transformăm variabilele categoriale "
                "(ex: era de dezvoltare, nivel de profitabilitate) în format numeric fără a pierde informația?")

    method_box("• <b>Label Encoding:</b> Atribuie un număr unic fiecărei categorii (0, 1, 2...)<br>"
               "  Utilizare: variabile ordinale (ex: Low < Medium < High)<br>"
               "• <b>One-Hot Encoding:</b> Creează coloane binare (dummy) pentru fiecare categorie<br>"
               "  Utilizare: variabile nominale fără ordine naturală<br>"
               "• <b>Implementare:</b> <code>sklearn.preprocessing.LabelEncoder</code>")

    st.markdown("## 🔄 Codificare 1: Era de Dezvoltare (Label Encoding)")
    df_enc = df.copy()
    df_enc['Era'] = df_enc['Year'].apply(lambda x: 'Witcher Era' if x < 2020 else 'Cyberpunk Era')
    le = LabelEncoder()
    df_enc['Era_Code'] = le.fit_transform(df_enc['Era'])
    st.dataframe(df_enc[['Year', 'Era', 'Era_Code']], use_container_width=True)

    st.markdown("## 🔄 Codificare 2: Nivel de Profitabilitate (Label Encoding Ordinal)")
    df_enc['Profit_Level'] = pd.cut(df_enc['NetProfit'], bins=3, labels=['Scăzut', 'Mediu', 'Ridicat'])
    le2 = LabelEncoder()
    df_enc['Profit_Level_Code'] = le2.fit_transform(df_enc['Profit_Level'])
    st.dataframe(df_enc[['Year', 'NetProfit', 'Profit_Level', 'Profit_Level_Code']], use_container_width=True)

    st.markdown("## 🔄 Codificare 3: One-Hot Encoding (Era)")
    onehot = pd.get_dummies(df_enc['Era'], prefix='Era')
    result = pd.concat([df_enc[['Year', 'Era']], onehot], axis=1)
    st.dataframe(result, use_container_width=True)

    interpret_box("Codificarea <b>Label Encoding</b> e potrivită pentru variabila 'Era' deoarece are doar 2 categorii. "
                  "Pentru 'Profit_Level' cu 3 categorii ordinale, Label Encoding păstrează ordinea naturală. "
                  "One-Hot Encoding evită impunerea unei ordini artificiale dar crește dimensionalitatea.")


def page_scaling(df):
    section_header("⚖️", "Metode de Scalare a Datelor",
                   "Normalizarea variabilelor financiare pentru comparabilitate")

    problem_box("Variabilele financiare au scale foarte diferite — Revenue (sute de mii – milioane) vs. procentaje "
                "regionale (0–1). Fără scalare, algoritmii ML vor fi dominați de variabilele cu valori mai mari.")

    method_box("• <b>StandardScaler (Z-score):</b> <code>z = (x − μ) / σ</code> → media=0, std=1<br>"
               "• <b>MinMaxScaler:</b> <code>x' = (x − min) / (max − min)</code> → interval [0, 1]<br>"
               "• <b>RobustScaler:</b> <code>x' = (x − Q2) / (Q3 − Q1)</code> → robust la outlieri")

    num_cols = ['Revenue', 'OperatingProfit', 'NetProfit', 'MarketingCosts', 'Assets']
    selected = st.multiselect("Selectează variabilele de scalat:", num_cols, default=['Revenue', 'NetProfit'])

    if selected:
        from sklearn.preprocessing import MinMaxScaler, RobustScaler
        df_comp = df[['Year'] + selected].copy()
        scaler_std = StandardScaler()
        scaler_mm = MinMaxScaler()
        scaler_rb = RobustScaler()

        tab1, tab2, tab3 = st.tabs(["StandardScaler", "MinMaxScaler", "RobustScaler"])

        for tab, scaler, name in [(tab1, scaler_std, "StandardScaler"),
                                   (tab2, scaler_mm, "MinMaxScaler"),
                                   (tab3, scaler_rb, "RobustScaler")]:
            with tab:
                scaled = pd.DataFrame(scaler.fit_transform(df[selected]), columns=[f"{c}_scaled" for c in selected])
                result = pd.concat([df[['Year']], df[selected], scaled], axis=1)
                st.dataframe(result, use_container_width=True)

                fig = go.Figure()
                for c in selected:
                    fig.add_trace(go.Scatter(x=df['Year'], y=scaled[f"{c}_scaled"], name=c, mode='lines+markers'))
                fig.update_layout(template="plotly_dark", title=f"Date scalate cu {name}",
                                  font=dict(family="Inter"), yaxis_title="Valoare scalată")
                st.plotly_chart(fig, width='stretch')

        st.markdown("## 📊 Comparație: Datele Originale vs. Scalate")
        c1, c2 = st.columns(2)
        with c1:
            fig_o = px.line(df, x='Year', y=selected, template="plotly_dark",
                            title="Date ORIGINALE (scale diferite)")
            st.plotly_chart(fig_o, width='stretch')
        with c2:
            scaled_all = pd.DataFrame(scaler_std.fit_transform(df[selected]), columns=selected)
            scaled_all['Year'] = df['Year'].values
            fig_s = px.line(scaled_all, x='Year', y=selected, template="plotly_dark",
                            title="Date SCALATE (StandardScaler)")
            st.plotly_chart(fig_s, width='stretch')

    interpret_box("<b>StandardScaler</b> este ideal pentru algoritmii bazați pe distanțe (KMeans, Regresie). "
                  "Observăm că Revenue 2020 are un z-score de ~2.5, confirmând statutul de valoare extremă. "
                  "<b>RobustScaler</b> atenuează acest efect folosind mediana și IQR în loc de medie și deviație standard.")
