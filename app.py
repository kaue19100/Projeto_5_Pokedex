import streamlit as st
import json 
import requests 
# python -m streamlit run app.py

with open("pokemon_index.json", "r", encoding= "utf-8") as arquivo: 
    nomes_pokemons = json.load(arquivo)
nome = st.selectbox('Escolha um Pokemon', nomes_pokemons.values())

url = f'https://pokeapi.co/api/v2/pokemon/{nome}'

dados_pokemon = requests.get(url).json()
col1, col2, col3 = st.columns(3)
altura = dados_pokemon['height'] / 10
peso = dados_pokemon['weight'] / 10
imc = round(peso / (altura ** 2))
with col1:
    st.image(dados_pokemon['sprites']['front_default'], width= 200 )
    st.write('Normal')
    st.write(f' Altura: {altura} M')
with col2:
    st.audio(dados_pokemon ['cries']['latest'])
    st.audio(dados_pokemon ['cries']['legacy'])
    st.write(f'IMC: {imc}')
with col3: 
    st.image(dados_pokemon['sprites']['front_shiny'], width= 200 )
    st.write(f'Peso: {peso} KG')

tipos, status, locais, habilidades = st.tabs(['Tipos', 'Status','Locais', 'Habilidades'])
with tipos:
    for i in dados_pokemon['types']:
        st.markdown(f'- {i['type']['name']}')
with status:

    hp, ataque, defesa, ataque_esp, defesa_esp, velocidade = st.columns(6)

with hp:
    st.metric('HP', dados_pokemon['stats'][0]['base_stat'])
with ataque:
    st.metric('Ataque', dados_pokemon['stats'][1]['base_stat'])
with defesa:
    st.metric('Defesa', dados_pokemon['stats'][2]['base_stat'])
with ataque_esp:
    st.metric('Ataque Especial', dados_pokemon['stats'][3]['base_stat'])
with defesa_esp:
    st.metric('Defesa Especial', dados_pokemon['stats'][4]['base_stat'])
with velocidade:
    st.metric('Velocidade', dados_pokemon['stats'][5]['base_stat'])

with locais: 
    locais = requests.get(dados_pokemon["location_area_encounters"]).json()
    for local in locais:
        st.markdown(f'- {local['location_area']['name']}')

with habilidades: 
    for habilidade in dados_pokemon['abilities']:
        st.markdown(f'-{habilidade['ability']['name']}') 