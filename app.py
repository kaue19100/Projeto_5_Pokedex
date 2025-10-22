import streamlit as st
import requests
import json
import pandas as pd

st.set_page_config(layout="wide")

df = pd.read_csv('pokemon_1.csv')

st.title('POKEDEX')


with open('pokemon_index.json', 'r', encoding='utf-8') as f:
    index_pokemons = json.load(f)

nome = st.selectbox('Escolha um pokemon', index_pokemons.values())



try:
    pokemon = requests.get(f'https://pokeapi.co/api/v2/pokemon/{nome}').json()

    nome_p = pokemon['name']
    st.title(nome_p.capitalize())
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image(pokemon['sprites']['other']['showdown']['front_default'], width=200)
        st.write('Padrão')
        st.metric('Altura', f'{pokemon['height']/10}M')

    with col2:
        st.audio(pokemon['cries']['latest'])
        st.audio(pokemon['cries']['legacy'])
        try:
            geracao = df[df['name'] == nome.capitalize()]['generation'].iloc[0]
            st.metric('Geração', f'{geracao}')
            imc = round((pokemon['weight']/10) / ((pokemon['height']/10)**2),2)
            st.metric('IMC', imc)
        except:
            st.write('Informação sobre geração não encontrada.')
        

    with col3:
        st.image(pokemon['sprites']['other']['showdown']['front_shiny'], width=200)
        st.write('Shiny')
        st.metric('Peso', f'{pokemon['weight']/10}KG')

    tipos, status, locais, habilidades = st.tabs(['Tipos', 'Status', 'Locais', 'Habilidades'])
    with tipos:
        for i in pokemon['types']:
            st.markdown(f"- {i['type']['name'].capitalize()}")

    with status:
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            st.metric('HP', pokemon['stats'][0]['base_stat'])
        with col2:
            st.metric('Ataque', pokemon['stats'][1]['base_stat'])
        with col3:
            st.metric('Defesa', pokemon['stats'][2]['base_stat'])
        with col4:
            st.metric('Ataque Especial', pokemon['stats'][3]['base_stat'])
        with col5:
            st.metric('Defesa Especial', pokemon['stats'][4]['base_stat'])
        with col6:
            st.metric('Velocidade', pokemon['stats'][5]['base_stat'])
    
    with locais:
        locs = requests.get(pokemon['location_area_encounters']).json()
        for i in locs:
            st.markdown(f'- {i['location_area']['name'].capitalize()}')

    with habilidades:
        for i in pokemon['abilities']:
            st.markdown(f'- {i['ability']['name'].capitalize()}')


    st.markdown('---')

    
except:
    st.warning('Digite o nome do pokemon corretamente.')
