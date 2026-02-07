import streamlit as st
import pandas as pd
import altair as alt

@st.cache_data
def load_data():
    df_data = pd.read_csv("CEN0101J.csv")

    df_data.rename(columns={
        "Druh PHM": "PalivoDruh",
        "CENPHM1": "PalivoId",
        "Měsíce": "RokMesicText",
        "CasM": "RokMesicId",
        "Hodnota": "Cena"},
        inplace=True)
    df_data = df_data[["PalivoDruh", "PalivoId", "RokMesicText", "RokMesicId", "Cena"]]

    df_data["Datum"] = pd.to_datetime(df_data["RokMesicId"])
    df_data["Rok"] = df_data["Datum"].dt.year
    df_data["Mesic"] = df_data["Datum"].dt.month

    palivo_rename = {"Benzin automobilový bezolovnatý Natural 95 [Kč/l]": "Natural 95",
                     "Benzin automobilový bezolovnatý Super plus 98 [Kč/l]": "Super Plus 98",
                     "LPG [Kč/l]": "LPG",
                     "Motorová nafta [Kč/l]": "Nafta",
                     "Stlačený zemní plyn - CNG [Kč/kg]": "CNG"}

    df_data["PalivoDruh"] = df_data["PalivoDruh"].replace(palivo_rename)

    df_data = df_data.groupby(["Rok", "PalivoDruh"])["Cena"].max().reset_index()

    return df_data

df_data=load_data()

def load_fuel_types():
    df_data = pd.read_csv("CEN0101J.csv")
    palivo_rename = {"Benzin automobilový bezolovnatý Natural 95 [Kč/l]": "Natural 95",
                    "Benzin automobilový bezolovnatý Super plus 98 [Kč/l]": "Super Plus 98",
                    "LPG [Kč/l]": "LPG",
                    "Motorová nafta [Kč/l]": "Nafta",
                    "Stlačený zemní plyn - CNG [Kč/kg]": "CNG"}

    df_data["Druh PHM"] = df_data["Druh PHM"].replace(palivo_rename)
    types = df_data["Druh PHM"].unique()
    return types
types = load_fuel_types()
     

chart = alt.Chart(df_data[df_data["Rok"] == 2025]).mark_bar().encode(
    y='PalivoDruh',
    x=alt.X('Cena', scale = alt.Scale(domain=[0,41])),
    color = alt.Color("PalivoDruh", legend = None),
    column = "Rok",
    tooltip = ["Cena", "PalivoDruh"]
    ).interactive()

chart_line = alt.Chart(df_data).mark_line().encode(
    x = "Rok:N",
    y = "Cena:Q",
    color = alt.Color("PalivoDruh:N", legend = None),
    tooltip = ["Cena", "PalivoDruh"]
    ).interactive()

st.title("Jak drahý je benzín letos?")
st.subheader("Pojďme se podívat na cenu benzínu, nafty i alternativních paliv v průběhu let. V detailu i v pouhém přehledu.")


st.error("Myslíte, že porozumění datům vám pomůže srovnat se se stále rostoucí cenou? Chyba! Na to vás nepřipraví nic.")

st.divider()

oblibene_palivo = st.text_input("Které palivo máš nejradši?")
if oblibene_palivo:
     st.write(f"Wow! {oblibene_palivo} mám taky nejradši!")
else:
     st.write("Tak nám řekni, jaký palivo máš rád!")


st.divider()
tab1, tab2, tab3 = st.tabs(["Grafy", "Data", "Vybraná data"])

with tab1:
        st.altair_chart(chart, use_container_width=True)
        st.altair_chart(chart_line, use_container_width=True)

with tab2:
    st.dataframe(load_data(), hide_index=True)

with tab3:
    selected_fuel = st.selectbox(label= "Vyberte palivo:", options=types)
    chart_selected = alt.Chart(df_data[df_data["PalivoDruh"] == selected_fuel]).mark_line().encode(
    x = "Rok:N",
    y = "Cena:Q",
    color = alt.Color("PalivoDruh:N", legend = None),
    tooltip = ["Cena", "PalivoDruh"]
    ).interactive()
    st.altair_chart(chart_selected, use_container_width=True)

st.code(language="python")