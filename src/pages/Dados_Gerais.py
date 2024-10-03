import streamlit as st
from statsbombpy import sb
from mplsoccer import Pitch
import matplotlib.pyplot as plt


def macth_metrics(match_id):
    events_metrics = sb.events(match_id=match_id)
    metrics = events_metrics.groupby('type')
    return metrics

def shots_t(df_macthes):
    shots = 0
    for id in df_macthes['match_id']:
        events = sb.events(match_id=id)
        shots += events[events['type'] == 'Shot'].shape[0]
    return shots

def pass_t(df_macthes):
    pass_match = 0
    for id in df_macthes['match_id']:
        events = sb.events(match_id=id)
        pass_match += events[events['type'] == 'Pass'].shape[0]
    return pass_match

def load_shots(match_id):
    events = sb.events(match_id=match_id)
    shots = events[events['type'] == 'Shot']
    return shots

if 'salve_competition' in st.session_state:
    competition = st.session_state['salve_competition']
    df = sb.competitions().loc[sb.competitions().competition_name == competition]

if 'salve_season' in st.session_state:
    season = st.session_state['salve_season']
    df_macthes = sb.matches(competition_id=df['competition_id'].values[0],season_id=df['season_id'].values[0])

st.subheader(f'Dados Gerais da Competição {competition} da temporada {season} na Base StatsBomb')
    
shots_total = shots_t(df_macthes)
pass_match = pass_t(df_macthes)
col1, col2,col3,col4 = st.columns(4)

col1.metric('Total de Partidas', df_macthes.shape[0])
col2.metric('Total de Gols', df_macthes['home_score'].sum() + df_macthes['away_score'].sum())
col3.metric('Total de Chutes', shots_total)
col4.metric('Total de Passes', pass_match)


st.subheader(f'Dados das partidas')
st.dataframe(df_macthes)
st.write('Clique no botão abaixo para baaixar os dados das partidas da temporada selecionada.')

csv = df_macthes.to_csv(index=False)

st.download_button(
    label="Download dos Dados",
    data=csv,
    file_name='matches.csv',
    mime='text/csv',
)


st.subheader('Análise  de Chutes por Partida')

match_pag2 = st.selectbox('Selecione a partida para análise', sorted(df_macthes['home_team'] + ' x ' + df_macthes['away_team']), key='match_tab2') 

match_id_pag2 = df_macthes.loc[df_macthes['home_team'] + ' x ' + df_macthes['away_team'] == match_pag2]['match_id'].values[0]



pitch = Pitch(pitch_color='grass', line_color='white', stripe=True)
fig, ax = pitch.draw()

# for  end_x, end_y in sb.events(match_id=match_id_pag2)['pass_end_location']:
#     pitch.arrows(end_x, end_y, color='blue', width=2)
st.pyplot(fig)



