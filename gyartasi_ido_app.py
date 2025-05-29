import streamlit as st
import pandas as pd

# === Alapbeállítás ===
st.set_page_config(page_title="Gyártási műszak kalkulátor")

st.title("🛠️ Gyártási idő kalkulátor")
st.write("Válaszd ki a cikkszámot, add meg a darabszámot, és megtudod hány műszak alatt készül el.")

# === Adatbetöltés Excelből ===
@st.cache_data
def load_data():
    df = pd.read_excel("BC gyártás számítás.xlsx", sheet_name="Komponensek")
    df = df[
        (df['Tipus'] == 'Megmunkalas') &
        (df['mertekegyseg'].str.contains('óra', na=False))
    ].copy()
    grouped = df.groupby('Cikkszam')['Mennyiseg'].sum().reset_index()
    grouped.rename(columns={'Mennyiseg': 'OraPerDarab'}, inplace=True)
    return grouped

data = load_data()
cikkszamok = data['Cikkszam'].unique()

# === Bemenetek ===
selected_cikkszam = st.selectbox("Cikkszám kiválasztása:", cikkszamok)
darabszam = st.number_input("Darabszám megadása:", min_value=1, value=100)

# === Számítás ===
ora_per_darab = data[data['Cikkszam'] == selected_cikkszam]['OraPerDarab'].values[0]
osszora = ora_per_darab * darabszam
muszak = osszora / 8  # 1 műszak = 8 óra

# === Eredmény megjelenítése ===
st.markdown(f"**Egy darabra szükséges idő:** `{ora_per_darab:.4f}` óra")
st.markdown(f"**Összesen szükséges idő:** `{osszora:.2f}` óra")
st.success(f"🔧 **Szükséges műszakok száma:** `{muszak:.2f}` műszak")

st.caption("Az eredmény 8 órás műszakkal számol.")
