import streamlit as st
from statsbombpy import sb

def macth_metrics(match_id):
    events_metrics = sb.events(match_id=match_id)
    metrics = events_metrics.groupby('type')
    return metrics


if 'salve_competition' in st.session_state:
    competition = st.session_state['salve_competition']
    st.subheader(f'Dados Gerais da Competição {competition} na Base StatsBomb')
    df = sb.competitions().loc[sb.competitions().competition_name == competition]
    st.dataframe(df)
    
st.write('Caso ')
