import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.cluster import KMeans
import statsmodels.api as sm
from pages_config import section_header, problem_box, method_box, interpret_box, info_box


def page_pandas(df):
    section_header("🐼", "Prelucrări Pandas: Grupare și Agregare",
                   "Analiza comparativă a performanței CDPR pe perioade strategice")

    problem_box("Cum se compară performanța financiară a CDPR în diferite perioade strategice? "
                "Gruparea datelor pe ere de dezvoltare permite identificarea tendințelor și evaluarea "
                "impactului deciziilor strategice asupra indicatorilor cheie.")

    method_box("• <code>df.groupby()</code> — gruparea observațiilor pe criterii categoriale<br>"
               "• <code>.agg()</code> — aplicarea simultană a mai multor funcții de agregare<br>"
               "• Funcții utilizate: <code>mean, sum, max, min, std, count</code><br>"
               "• <code>pd.cut()</code> — discretizarea variabilelor continue în intervale")

    st.markdown("## 📊 Grupare 1: Era Witcher vs. Era Cyberpunk")
    df_g = df.copy()
    df_g['Era'] = df_g['Year'].apply(lambda x: '🎯 Pre-Cyberpunk (2010-2019)' if x < 2020 else '🌐 Post-Cyberpunk (2020-2025)')
    grouped = df_g.groupby('Era').agg(
        Venituri_Medie=('Revenue', 'mean'),
        Venituri_Total=('Revenue', 'sum'),
        Profit_Mediu=('NetProfit', 'mean'),
        Profit_Max=('NetProfit', 'max'),
        Marketing_Mediu=('MarketingCosts', 'mean'),
        Nr_Ani=('Year', 'count')
    ).round(0)
    st.dataframe(grouped, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(grouped.reset_index(), x='Era', y='Venituri_Medie', color='Era',
                     color_discrete_sequence=['#00e5ff', '#f3e600'], template='plotly_dark',
                     title="Venituri Medii pe Eră")
        fig.update_layout(font=dict(family="Inter"), showlegend=False)
        st.plotly_chart(fig, width='stretch')
    with c2:
        fig2 = px.bar(grouped.reset_index(), x='Era', y='Profit_Mediu', color='Era',
                      color_discrete_sequence=['#00e5ff', '#f3e600'], template='plotly_dark',
                      title="Profit Net Mediu pe Eră")
        fig2.update_layout(font=dict(family="Inter"), showlegend=False)
        st.plotly_chart(fig2, width='stretch')

    st.markdown("## 📊 Grupare 2: Nivele de Profitabilitate")
    df_g['Profit_Category'] = pd.cut(df_g['NetProfit'], bins=3, labels=['📉 Scăzut', '📊 Mediu', '📈 Ridicat'])
    grouped2 = df_g.groupby('Profit_Category', observed=True).agg(
        Ani=('Year', lambda x: list(x)),
        Revenue_Medie=('Revenue', 'mean'),
        Marketing_Medie=('MarketingCosts', 'mean'),
        Marja_Profit=('NetProfit', lambda x: (x.mean() / df_g.loc[x.index, 'Revenue'].mean() * 100))
    )
    grouped2['Marja_Profit'] = grouped2['Marja_Profit'].round(1)
    st.dataframe(grouped2, width='stretch')

    st.markdown("## 📊 Grupare 3: Statistici Descriptive Agregate")
    desc = df[['Revenue', 'NetProfit', 'MarketingCosts', 'Assets']].describe().round(0)
    st.dataframe(desc, use_container_width=True)

    st.markdown("## 📊 Pivot: Eficiența Marketingului pe Eră")
    df_g['Marketing_ROI'] = (df_g['NetProfit'] / df_g['MarketingCosts']).round(2)
    pivot = df_g.pivot_table(values='Marketing_ROI', index='Era', aggfunc=['mean', 'min', 'max']).round(2)
    st.dataframe(pivot, use_container_width=True)

    interpret_box("Era Post-Cyberpunk are venituri medii de <b>~2x</b> față de Pre-Cyberpunk, dar cu o variabilitate "
                  "mult mai mare (std ridicat). ROI-ul marketingului s-a îmbunătățit semnificativ în 2024-2025 "
                  "(~3.5x profit/cost marketing), sugerând o strategie de marketing mai eficientă post-lecțiile Cyberpunk.")


def page_logistic(df):
    section_header("🤖", "Scikit-learn: Regresie Logistică",
                   "Predicția anilor cu profitabilitate ridicată")

    problem_box("Putem prezice dacă un an va avea profitabilitate ridicată pe baza indicatorilor financiari? "
                "Regresia logistică clasifică anii în două categorii: profit ridicat vs. profit scăzut.")

    method_box("• <b>Variabila țintă (Y):</b> Is_High_Profit = 1 dacă NetProfit > mediană, 0 altfel<br>"
               "• <b>Predictori (X):</b> Revenue, OperatingProfit, MarketingCosts<br>"
               "• <b>Formula:</b> P(Y=1) = 1 / (1 + e<sup>−(β₀ + β₁X₁ + β₂X₂ + ...)</sup>)<br>"
               "• <b>Funcția de cost:</b> Cross-Entropy Loss<br>"
               "• <b>Implementare:</b> <code>sklearn.linear_model.LogisticRegression</code>")

    info_box("Setul de date are doar <b>16 observații</b> — insuficient pentru un model robust. "
             "Rezultatele sunt demonstrative și ilustrează metodologia, nu au valoare predictivă reală.")

    df_ml = df.copy()
    median_profit = df_ml['NetProfit'].median()
    df_ml['Is_High_Profit'] = (df_ml['NetProfit'] > median_profit).astype(int)

    features = ['Revenue', 'OperatingProfit', 'MarketingCosts']
    X = df_ml[features].fillna(0)
    y = df_ml['Is_High_Profit']

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = LogisticRegression(random_state=42, max_iter=1000)
    model.fit(X_scaled, y)
    df_ml['Predicție'] = model.predict(X_scaled)
    df_ml['Probabilitate'] = model.predict_proba(X_scaled)[:, 1].round(3)
    accuracy = model.score(X_scaled, y) * 100

    st.markdown("## 📊 Rezultatele Modelului")
    c1, c2, c3 = st.columns(3)
    c1.metric("Acuratețe", f"{accuracy:.1f}%")
    c2.metric("Prag Profit", f"{median_profit:,.0f} PLN")
    c3.metric("Observații", f"{len(df_ml)}")

    st.markdown("### Tabel Predicții vs. Realitate")
    display = df_ml[['Year', 'Revenue', 'NetProfit', 'Is_High_Profit', 'Predicție', 'Probabilitate']].copy()
    display.columns = ['An', 'Venituri', 'Profit Net', 'Real (0/1)', 'Predicție', 'P(High)']
    display['✓'] = display.apply(lambda r: '✅' if r['Real (0/1)'] == r['Predicție'] else '❌', axis=1)
    st.dataframe(display, use_container_width=True)

    st.markdown("### Coeficienții Modelului")
    coef_df = pd.DataFrame({'Variabilă': features, 'Coeficient': model.coef_[0].round(4)})
    coef_df['Impact'] = coef_df['Coeficient'].apply(lambda x: '📈 Pozitiv' if x > 0 else '📉 Negativ')
    st.dataframe(coef_df, use_container_width=True)

    fig = px.bar(df_ml, x='Year', y='Probabilitate', color='Predicție',
                 color_discrete_sequence=['#ff6ec7', '#00e5ff'],
                 template='plotly_dark', title="Probabilitatea de Profit Ridicat pe An")
    fig.add_hline(y=0.5, line_dash="dash", line_color="#f3e600", annotation_text="Prag 50%")
    fig.update_layout(font=dict(family="Inter"))
    st.plotly_chart(fig, width='stretch')

    interpret_box("Modelul atinge o acuratețe de <b>" + f"{accuracy:.0f}%" + "</b> pe setul de antrenare. "
                  "Coeficienții arată că <b>Revenue</b> și <b>OperatingProfit</b> sunt cei mai puternici predictori. "
                  "Anul 2020 are probabilitatea cea mai mare de profit ridicat, confirmat de lansarea CP2077.")


def page_regression(df):
    section_header("📐", "Statsmodels: Regresie Multiplă",
                   "Analiza impactului veniturilor și costurilor de marketing asupra profitului net")

    problem_box("Care sunt factorii determinanți ai profitului net la CDPR? Regresia multiplă cuantifică "
                "relația liniară între profit (Y) și predictori (Revenue, MarketingCosts).")

    method_box("• <b>Model:</b> NetProfit = β₀ + β₁·Revenue + β₂·MarketingCosts + ε<br>"
               "• <b>Metoda:</b> OLS (Ordinary Least Squares) — minimizarea sumei pătratelor reziduurilor<br>"
               "• <b>Indicatori cheie:</b> R², R² ajustat, p-value, t-statistic, F-statistic<br>"
               "• <b>Implementare:</b> <code>statsmodels.api.OLS</code>")

    df_reg = df.dropna(subset=['MarketingCosts', 'Revenue', 'NetProfit']).copy()
    X = df_reg[['Revenue', 'MarketingCosts']]
    y = df_reg['NetProfit']
    X_const = sm.add_constant(X)
    model = sm.OLS(y, X_const).fit()

    st.markdown("## 📊 Sumar Model OLS")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("R²", f"{model.rsquared:.4f}")
    c2.metric("R² Ajustat", f"{model.rsquared_adj:.4f}")
    c3.metric("F-statistic", f"{model.fvalue:.2f}")
    c4.metric("Prob (F)", f"{model.f_pvalue:.4f}")

    st.markdown("### Coeficienții Regresiei")
    coef_data = pd.DataFrame({
        'Variabilă': model.params.index,
        'Coeficient (β)': model.params.values.round(4),
        'Std. Error': model.bse.values.round(4),
        't-value': model.tvalues.values.round(4),
        'p-value': model.pvalues.values.round(4),
        'Semnificativ (α=0.05)': ['✅ Da' if p < 0.05 else '❌ Nu' for p in model.pvalues]
    })
    st.dataframe(coef_data, use_container_width=True)

    with st.expander("📋 Sumar OLS Complet (Statsmodels)"):
        st.text(model.summary().as_text())

    st.markdown("## 📈 Vizualizări Regresie")
    c1, c2 = st.columns(2)
    with c1:
        df_reg['Predicted'] = model.predict(X_const)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_reg['Year'], y=df_reg['NetProfit'], name='Real',
                                 mode='lines+markers', line=dict(color='#00e5ff', width=3)))
        fig.add_trace(go.Scatter(x=df_reg['Year'], y=df_reg['Predicted'], name='Predicție OLS',
                                 mode='lines+markers', line=dict(color='#f3e600', width=3, dash='dash')))
        fig.update_layout(template='plotly_dark', title='Profit Real vs. Predicție',
                          font=dict(family="Inter"), yaxis_title='Profit Net (mii PLN)')
        st.plotly_chart(fig, width='stretch')
    with c2:
        residuals = model.resid
        fig2 = px.scatter(x=model.fittedvalues, y=residuals, template='plotly_dark',
                          title='Reziduuri vs. Valori Estimate', labels={'x': 'Fitted', 'y': 'Residuals'},
                          color_discrete_sequence=['#ff6ec7'])
        fig2.add_hline(y=0, line_dash='dash', line_color='#f3e600')
        fig2.update_layout(font=dict(family="Inter"))
        st.plotly_chart(fig2, width='stretch')

    r2_val = model.rsquared
    interpret_box(f"Modelul explică <b>{r2_val*100:.1f}%</b> din variația profitului net (R²={r2_val:.4f}). "
                  "Revenue are un impact pozitiv puternic — la fiecare creștere de 1 PLN în venituri, profitul net "
                  f"crește cu ~{model.params['Revenue']:.2f} PLN. Costurile de marketing au un efect "
                  f"{'pozitiv' if model.params['MarketingCosts'] > 0 else 'negativ'}, sugerând că "
                  "investițiile în marketing au contribuit la profitabilitate.")


def page_clustering(df):
    section_header("🎯", "Scikit-learn: Clusterizare K-Means",
                   "Segmentarea automată a anilor de performanță financiară")

    problem_box("Putem identifica automat grupuri (clustere) de ani cu performanță financiară similară? "
                "K-Means grupează observațiile pe baza similitudinii multidimensionale.")

    method_box("• <b>Algoritmul K-Means:</b> Partiționează n observații în k clustere<br>"
               "• <b>Pas 1:</b> Inițializare aleatorie a k centroizi<br>"
               "• <b>Pas 2:</b> Asignarea fiecărei observații la cel mai apropiat centroid (distanța euclidiană)<br>"
               "• <b>Pas 3:</b> Recalcularea centroizilor ca media observațiilor din cluster<br>"
               "• <b>Pas 4:</b> Repetare pași 2-3 până la convergență<br>"
               "• <b>Metoda Elbow:</b> Determinarea numărului optim de clustere (k)")

    num_cols = ['Revenue', 'NetProfit', 'MarketingCosts', 'Assets']
    X_raw = df[num_cols].fillna(0)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_raw)

    st.markdown("## 📊 Metoda Elbow — Determinarea k Optim")
    inertias = []
    K_range = range(2, min(8, len(df)))
    for k in K_range:
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        km.fit(X_scaled)
        inertias.append(km.inertia_)
    fig_elbow = px.line(x=list(K_range), y=inertias, markers=True, template='plotly_dark',
                        title='Metoda Elbow — Inerția vs. Număr Clustere',
                        labels={'x': 'Număr Clustere (k)', 'y': 'Inerție (WCSS)'})
    fig_elbow.update_traces(line_color='#f3e600', marker_size=10)
    fig_elbow.update_layout(font=dict(family="Inter"))
    st.plotly_chart(fig_elbow, width='stretch')

    k_sel = st.slider("Selectează numărul de clustere (k):", 2, min(6, len(df)-1), 3)

    kmeans = KMeans(n_clusters=k_sel, random_state=42, n_init=10)
    df_c = df.copy()
    df_c['Cluster'] = kmeans.fit_predict(X_scaled)
    cluster_names = {i: f"Cluster {i}" for i in range(k_sel)}
    df_c['Cluster_Name'] = df_c['Cluster'].map(cluster_names)

    st.markdown("## 🎯 Rezultatele Clusterizării")
    c1, c2 = st.columns(2)
    with c1:
        fig = px.scatter(df_c, x='Revenue', y='NetProfit', color='Cluster_Name', size='Assets',
                         hover_data=['Year', 'MarketingCosts'], template='plotly_dark',
                         title='Clusterizarea Performanței: Revenue vs. Profit Net',
                         color_discrete_sequence=['#f3e600', '#00e5ff', '#ff6ec7', '#7b68ee', '#00ff88', '#ff4444'])
        fig.update_layout(font=dict(family="Inter"))
        st.plotly_chart(fig, width='stretch')
    with c2:
        fig2 = px.scatter(df_c, x='MarketingCosts', y='NetProfit', color='Cluster_Name', size='Revenue',
                          hover_data=['Year'], template='plotly_dark',
                          title='Marketing vs. Profit pe Clustere',
                          color_discrete_sequence=['#f3e600', '#00e5ff', '#ff6ec7', '#7b68ee', '#00ff88', '#ff4444'])
        fig2.update_layout(font=dict(family="Inter"))
        st.plotly_chart(fig2, width='stretch')

    st.markdown("### 📋 Detalii pe Clustere")
    for cl in sorted(df_c['Cluster'].unique()):
        subset = df_c[df_c['Cluster'] == cl]
        years = ', '.join(subset['Year'].astype(str).tolist())
        with st.expander(f"🔹 Cluster {cl} — Anii: {years}"):
            st.dataframe(subset[['Year','Revenue','NetProfit','MarketingCosts','Assets']], use_container_width=True)

    st.markdown("### 📊 Statistici Medii pe Cluster")
    cluster_stats = df_c.groupby('Cluster')[num_cols].mean().round(0)
    st.dataframe(cluster_stats, use_container_width=True)

    interpret_box("K-Means identifică <b>segmente distincte</b> de performanță: "
                  "anul 2020 formează aproape invariabil un cluster separat datorită veniturilor record. "
                  "Anii 2010-2019 (era pre-Cyberpunk) se grupează împreună, iar 2021-2025 (recuperare post-Cyberpunk) "
                  "formează al treilea segment. Această segmentare confirmă cele 3 faze strategice ale companiei.")
