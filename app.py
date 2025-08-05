import streamlit as st
import pandas as pd
import joblib

modelo = joblib.load("model/model.pkl")

st.set_page_config(page_title="Predição de Imóveis SP", page_icon="🏠", layout="wide")
st.title("🏠 Predição de Preços de Imóveis - São Paulo")
st.markdown("Preencha os dados abaixo para estimar o preço do imóvel:")

elevator_map = {"Não": 0, "Sim": 1}
furnished_map = {"Não": 0, "Sim": 1}
swimming_map = {"Não": 0, "Sim": 1}
new_map = {"Novo": 0, "Usado": 1}


district = st.selectbox("Bairro", [
    "Centro/São Paulo", "Jardins/São Paulo", "Moema/São Paulo", "Pinheiros/São Paulo",
    "Vila Mariana/São Paulo", "Morumbi/São Paulo", "Tatuapé/São Paulo"
])

negotiation_pt = st.selectbox("Tipo de negociação", ['aluguel', 'venda'])
negociation_map = {'aluguel': 'rent', 'venda': 'sale'}
property_type_pt = st.selectbox("Tipo de imóvel", ['apartamento', 'casa'])
property_type_map = {'apartamento': 'apartment', 'casa': 'house'}

condo = st.number_input("Valor do condomínio (R$)", min_value=0, value=500, step=50)
size = st.number_input("Área do imóvel (m²)", min_value=10, max_value=1000, step=5)
rooms = st.number_input("Número de quartos", min_value=1, max_value=10, step=1)
toilets = st.number_input("Número de banheiros", min_value=1, max_value=10, step=1)
suites = st.number_input("Número de suítes", min_value=0, max_value=5, step=1)
parking = st.number_input("Vagas de garagem", min_value=0, max_value=5, step=1)

elevator = st.selectbox("Possui elevador?", list(elevator_map.keys()))
furnished = st.selectbox("Mobiliado?", list(furnished_map.keys()))
pool = st.selectbox("Piscina?", list(swimming_map.keys()))
new = st.selectbox("Imóvel novo?", list(new_map.keys()))

latitude = st.number_input("Latitude", value=-23.5505, format="%.6f")
longitude = st.number_input("Longitude", value=-46.6333, format="%.6f")


input_df = pd.DataFrame({
    "Condo": [condo],
    "Size": [size],
    "Rooms": [rooms],
    "Toilets": [toilets],
    "Suites": [suites],
    "Parking": [parking],
    "Elevator": [elevator_map[elevator]],
    "Furnished": [furnished_map[furnished]],
    "Swimming Pool": [swimming_map[pool]],
    "New": [new_map[new]],
    "District": [district],
    "Negotiation Type": [negociation_map[negotiation_pt]],
    "Property Type": [property_type_map[property_type_pt]],
    "Latitude": [latitude],
    "Longitude": [longitude]
})


if st.button("🔍 Prever Preço"):
    preco_previsto = modelo.predict(input_df)[0]
    st.success(f"💰 Preço estimado: R$ {preco_previsto:,.2f}")
