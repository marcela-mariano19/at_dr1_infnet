import streamlit as st
from statsbombpy import sb


def load_shots(match_id):
    events = sb.events(match_id=match_id)
    shots = events[events['type'] == 'Shot']
    return shots

def load_pass(match_id):
    events = sb.events(match_id=match_id)
    pass_match = events[events['type'] == 'Pass']
    return pass_match

def load_goals(match_id):
    events = sb.events(match_id=match_id)
    goals = events[events['shot_outcome'] == 'Goal']
    return goals

def player_stats(match_id, player):
    events = sb.events(match_id=match_id)
    player_events = events[events['player'] == player]
    pressure = player_events[player_events['type'] == 'Pressure'].shape[0]
    try:
        yellow_card = player_events[player_events['bad_behaviour_card'] == 'Yellow Card'].shape[0]
        goals = player_events[player_events['shot_outcome'] == 'Goal'].shape[0]
    except KeyError:
        yellow_card = 0
        goals = player_events[player_events['shot_outcome'] == 'Goal'].shape[0]

    return pressure, yellow_card, goals
   

def main ():
    st.title('AT - Marcela Mariano')


    st.sidebar.title('Menu')
    competition = st.sidebar.selectbox('Competição', sb.competitions().competition_name.unique())

    if competition:
        st.session_state['salve_competition'] = competition



    with st.container():
        st.subheader(f'Dados da Competição {competition} na Base StatsBomb')
        df = sb.competitions().loc[sb.competitions().competition_name == competition]
        st.dataframe(df)

        
        season  = st.sidebar.radio('Selecione a temporada para análise', df['season_name'],horizontal=True)
        if season:
            st.session_state['salve_season'] = season

        st.subheader(f'Dados da Temporada {season} na Base StatsBomb')
        df_macthes = sb.matches(competition_id=df['competition_id'].values[0],season_id=df['season_id'].values[0])


        team = st.multiselect('Caso queira selecione os times mandantes que deseja visualizar', df_macthes['home_team'].unique())
        if team:
            df_macthes_selected = df_macthes[df_macthes['home_team'].isin(team)]
            st.dataframe(df_macthes_selected)
        else:
            st.dataframe(df_macthes)

        tab1, tab2 = st.tabs(['Análise por Partida','Análise por Jogador'])

        with tab1:
            col1, col2 = st.columns(2)
            match = col1.selectbox('Selecione a partida para análise', sorted(df_macthes['home_team'] + ' x ' + df_macthes['away_team'])) 
            #col2.metric('Totais de Gols',df_macthes.loc[df_macthes['home_team'] + ' x ' + df_macthes['away_team'] == match]['home_score'] + df_macthes.loc[df_macthes['home_team'] + ' x ' + df_macthes['away_team'] == match]['away_score'])
            match_id = df_macthes.loc[df_macthes['home_team'] + ' x ' + df_macthes['away_team'] == match]['match_id'].values[0]

            #Carregando estatísticas da partida
            shots_match = load_shots(match_id)
            pass_match = load_pass(match_id)
            goals = load_goals(match_id)

            col2.metric('Total de Chutes', shots_match.shape[0])
            col2.metric('Total de Passes', pass_match.shape[0])
            col2.metric('Total de Gols', goals.shape[0])

            df_events = sb.events(match_id=match_id)

        with tab2:
            #sb.players_season(competition_id=loc[sb.competitions().competition_name == competition])

            # competition_id = df[df['competition_name'] == competition]['competition_id'].values[0]
            # season_id = df[df['season_name'] == season]['season_id'].values[0]

            # players = sb.player_season_stats(competition_id=competition_id, season_id=season_id)
            # st.dataframe(players)

            col1, col2 = st.columns(2)

            match_tab2 = col1.selectbox('Selecione a partida para análise', sorted(df_macthes['home_team'] + ' x ' + df_macthes['away_team']), key='match_tab2') 

            match_id_tab2 = df_macthes.loc[df_macthes['home_team'] + ' x ' + df_macthes['away_team'] == match_tab2]['match_id'].values[0]

            events = sb.events(match_id=match_id_tab2)

            player = col1.selectbox('Selecione o jogador para análise', events['player'].unique(),key='player')
            player_events = events[events['player'] == player]

            #Pressão
            player_pressure, yellow_cards,player_goals = player_stats(match_id_tab2, player)

            #Total de pressões
            col2.metric('Total de Pressões', player_pressure)
            col2.metric('Total de Cartões Amarelos', yellow_cards)
            col2.metric('Total de Gols', player_goals)

            events = sb.events(match_id=match_id)
            st.dataframe(events)



    
            
           



        
        


if __name__ == '__main__':
    main()