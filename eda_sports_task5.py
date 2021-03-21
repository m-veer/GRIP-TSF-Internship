# Exploratory Data Analysis - Sports
# Task No. 5
# Mayur Veer
# m.veer@somaiya.edu
# https://www.linkedin.com/in/mayur-veer-a66838185/
# Dataset: https://bit.ly/34SRn3b

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
import dash_table
import plotly.express as px
from collections import Counter
from dash.exceptions import PreventUpdate

data = pd.read_csv("C://Users/mayur/Desktop/Uber_SA/matches.csv")
data1 = pd.read_csv("C://Users/mayur/Desktop/Uber_SA/deliveries.csv")
pd_for_matches = data[['id', 'season', 'team1', 'team2', 'winner']]
for_op_df_bat = pd.DataFrame({'Batsmen' : [1],
                          'Six' : [1],
                          'Four' : [1],
                          'Total_runs' : [1],
                          'Total_balls_faced' : [1],
                          'Strike_rate' : [1]
})

for_op_df_bowl = pd.DataFrame({'Bowler' : [1],
                               'Overs' : [1],
                               'Wickets' : [1],
                               'Total_runs' : [1],
                               'Extra_runs' : [1],
                               'Economy' : [1],
                               })

for_points_table = pd.DataFrame({'Teams': [1],
                          'Matches': [1],
                          'Wins': [1],
                          'Lost': [1],
                          'NR': [1],
                          'NRR' : [1],
                          'Points': [1]
                                 })

#############################################################################################################

def wicket_calc(df):
    a = df['dismissal_kind'].to_list()
    b = [x for x in a if str(x) != 'nan']
    return len(b)

def fours_sixes_count(df):
    fc = 0
    sc = 0
    for i1 in df['batsman_runs']:
        if i1 == 4:
            fc += 1
        elif i1 == 6:
            sc += 1
    return fc, sc

def remove_items(test_list, item):
    res = [i for i in test_list if i != item] # using list comprehension to perform the task
    return res

def wicket_calc_for_bowler(df):
    a = df['dismissal_kind'].to_list()
    b = [x for x in a if str(x) != 'nan']
    # b1 = Counter(b)
    # print(b1)
    # print(len(b))
    item = ['run out', 'retired hurt', 'obstructing the field']
    output = [b for b in b if
              all(a not in b for a in item)]
    # o2 = Counter(output)
    # print(o2)
    # print(len(output))
    return len(output)

#############################################################################################################

teams = data1['batting_team'].unique()
teams_wn = [x for x in teams if str(x) != 'nan']
team_list = sorted(teams_wn)

wickets = data1['dismissal_kind']

ids1 = list(data['id'])
season1 = list(data['season'])

id_season_dict = {ids1[i]: season1[i] for i in range(len(season1))}

seasons_for_df = [id_season_dict[key] for key in data1['match_id']]
data1['season'] = seasons_for_df

batsman = data1['batsman'].unique() # name column
bowler = data1['bowler'].unique()

seasons = sorted(data1['season'].unique())

wkp = data1[data1['dismissal_kind'] == 'stumped']
wkp_list1 = wkp['fielder'].unique()
wkp_list = [x for x in wkp_list1 if str(x) != 'nan']
# print(wkp_list)
wkp_count = Counter(wkp['fielder'])
# print(wkp_count)

motm_list1 = data['player_of_match']
motm_list = [x for x in motm_list1 if str(x) != 'nan']
motm_counter = Counter(motm_list)
motm_keys = [x for x in motm_counter.keys()]
motm_values = [x for x in motm_counter.values()]
motm_df = pd.DataFrame({'Player' : motm_keys,
                        'Count' : motm_values
                        })
# print(motm_counter)

fielder = data1[data1['dismissal_kind'] == 'caught']
f_list1 = fielder['fielder'].unique()
f_list = [x for x in f_list1 if str(x) != 'nan']
fielder_count = Counter(fielder['fielder'])

winner_list = []
season2 = []
for s in seasons:
    s1 = data1[data1['season'] == s]
    #s1 = s1[['winner']]
    s1 = s1.iloc[-1,:].reset_index(drop=True)
    #print(s1)
    #print(s1)
    winner_list.append(s1[6])
    season2.append(s1[1])
    #print(s1)
    #winner_list.append()
winner_df = pd.DataFrame({'Season' : season2,
                          'Winner' : winner_list})
winner_count = Counter(winner_list)

# wicket-keeper per team per season.......name, season, matches played, team, wickets
wk_pt_ps_name = []
wk_pt_ps_season = []
# wk_pt_ps_mp = []
wk_pt_ps_oppo_team = []
wk_pt_ps_wickets = []

# wicket-keeper per team overall.........name, seasons played, matches played, team, wickets
wk_pt_ovr_name = []
wk_pt_ovr_sp = []
# wk_pt_ovr_mp = []
wk_pt_ovr_oppo_team = []
wk_pt_ovr_wickets = []

# wicket-keeper per season.........name, season, matches played, team, wickets
wk_ps_name = []
wk_ps_season = []
# wk_ps_mp = []
wk_ps_team = []
wk_ps_wickets = []

# wicket-keeper overall......name, seasons played, matches played, wickets
wk_ovr_name = []
wk_ovr_sp = []
# wk_ovr_mp = []
wk_ovr_wickets = []

for w in wkp_list:  # for ovr and pt_ovr
    dwk = wkp[wkp['fielder'] == w].reset_index(drop=True)
    wk_ovr_name.append(w)
    wk_ovr_sp.append(len(dwk['season'].unique()))
    # for_mp = data[data['batsman'] ==w]
    # wk_ovr_mp.append(len(for_mp['match_id'].unique()))
    # wk_ovr_mp.append(len(dwk['match_id'].unique()))
    wk_ovr_wickets.append(len(dwk['fielder']))
    # print(dwk)
    for ss in seasons:  # for season and pt_season
        dwk_ps = dwk[dwk['season'] == ss].reset_index(drop=True)
        if dwk_ps.empty:
            pass
        else:
            wk_ps_name.append(w)
            wk_ps_season.append(dwk_ps['season'][0])
            # wk_ps_team.append(dwk_ps['bowling_team'][0])
            wk_ps_wickets.append(len(dwk_ps['match_id']))
        for tt in team_list:  # for pt
            dwk_pt = dwk_ps[dwk_ps['batting_team'] == tt].reset_index(drop=True)
            if dwk_pt.empty:
                pass
            else:
                # print(dwk_pt)
                wk_pt_ps_name.append(w)
                wk_pt_ps_oppo_team.append(dwk_pt['batting_team'][0])
                # wk_pt_ps_mp.append(len(dwk_pt['match_id']))
                wk_pt_ps_season.append(ss)
                wk_pt_ps_wickets.append(len(dwk_pt['fielder']))
    for tt1 in team_list:  # for pt_ovr
        for_teams = dwk[dwk['batting_team'] == tt1].reset_index(drop=True)
        if for_teams.empty:
            pass
        else:
            wk_pt_ovr_name.append(w)
            wk_pt_ovr_oppo_team.append(for_teams['batting_team'][0])
            wk_pt_ovr_sp.append(len(for_teams['season'].unique()))
            wk_pt_ovr_wickets.append(len(for_teams['match_id']))

wk_pt_ps = pd.DataFrame({'Name': wk_pt_ps_name,
                         'Season': wk_pt_ps_season,
                         'Opponent team': wk_pt_ps_oppo_team,
                         'Wickets': wk_pt_ps_wickets,
                         })
# print(wk_pt_ps)

wk_ps = pd.DataFrame({'Name': wk_ps_name,
                      'Season': wk_ps_season,
                      'Wickets': wk_ps_wickets,
                      })
# print(wk_ps)

wk_ovr = pd.DataFrame({'Name': wk_ovr_name,
                       'Seasons played': wk_ovr_sp,
                       'Wickets': wk_ovr_wickets
                       })
# print(wk_ovr)

wk_pt_ovr = pd.DataFrame({'Name': wk_pt_ovr_name,
                          'Opponent team': wk_pt_ovr_oppo_team,
                          'Wickets': wk_pt_ovr_wickets,
                          })
# print(wk_pt_ovr.head(15))

###################################################################################################################

# fielder per team per season
f_pt_ps_name = []
f_pt_ps_season = []
f_pt_ps_oppo_team = []
f_pt_ps_wickets = []

# fielder per team overall
f_pt_ovr_name = []
f_pt_ovr_sp = []
f_pt_ovr_oppo_team = []
f_pt_ovr_wickets = []

# fielder per season
f_ps_name = []
f_ps_season = []
f_ps_team = []
f_ps_wickets = []

# fielder overall
f_ovr_name = []
f_ovr_sp = []
f_ovr_wickets = []

for f in f_list:  # for ovr and pt_ovr
    dff = fielder[fielder['fielder'] == f].reset_index(drop=True)
    f_ovr_name.append(f)
    f_ovr_sp.append(len(dff['season'].unique()))
    f_ovr_wickets.append(len(dff['fielder']))
    for ss in seasons:  # for season and pt_season
        dff_ps = dff[dff['season'] == ss].reset_index(drop=True)
        if dff_ps.empty:
            pass
        else:
            f_ps_name.append(f)
            f_ps_season.append(dff_ps['season'][0])
            f_ps_wickets.append(len(dff_ps['match_id']))
        for tt in team_list:  # for pt
            dff_pt = dff_ps[dff_ps['batting_team'] == tt].reset_index(drop=True)
            if dff_pt.empty:
                pass
            else:
                f_pt_ps_name.append(f)
                f_pt_ps_oppo_team.append(dff_pt['batting_team'][0])
                f_pt_ps_season.append(ss)
                f_pt_ps_wickets.append(len(dff_pt['fielder']))
    for tt1 in team_list:  # for pt_ovr
        for_teams = dff[dff['batting_team'] == tt1].reset_index(drop=True)
        if for_teams.empty:
            pass
        else:
            f_pt_ovr_name.append(f)
            f_pt_ovr_oppo_team.append(for_teams['batting_team'][0])
            f_pt_ovr_sp.append(len(for_teams['season'].unique()))
            f_pt_ovr_wickets.append(len(for_teams['match_id']))

f_pt_ps = pd.DataFrame({'Name': f_pt_ps_name,
                        'Season': f_pt_ps_season,
                        'Opponent team': f_pt_ps_oppo_team,
                        'Wickets': f_pt_ps_wickets,
                        })
# print(f_pt_ps)

f_ps = pd.DataFrame({'Name': f_ps_name,
                     'Season': f_ps_season,
                     'Wickets': f_ps_wickets,
                     })
# print(f_ps)

f_ovr = pd.DataFrame({'Name': f_ovr_name,
                      'Seasons played': f_ovr_sp,
                      'Wickets': f_ovr_wickets
                      })
# print(f_ovr)

f_pt_ovr = pd.DataFrame({'Name': f_pt_ovr_name,
                         'Opponent team': f_pt_ovr_oppo_team,
                         'Wickets': f_pt_ovr_wickets,
                         })
# print(f_pt_ovr.head(15))

##################################################################################################################

# batsman per team per season......batsman, season, team, matches_played, strike rate, batsman runs, 4s, 6s, 50s, 100s
b_pt_ps_name = []
b_pt_ps_season = []
b_pt_ps_oppo_team = []
b_pt_ps_mp = []
b_pt_ps_sr = []
b_pt_ps_br = []
b_pt_ps_f = []
b_pt_ps_s = []

# batsman per team overall........batsman, seasons played, matches_played, strike rate, batsman runs, 4s, 6s, 50s, 100s
b_pt_ovr_name = []
b_pt_ovr_sp = []
b_pt_ovr_oppo_team = []
b_pt_ovr_mp = []
b_pt_ovr_sr = []
b_pt_ovr_br = []
b_pt_ovr_f = []
b_pt_ovr_s = []

# overall batsman df
total_runs1 = []  # total runs column
total_balls_faced1 = []  # total balls faced column
strike_rate1 = []  # strike rate column
total_sixes1 = []
total_fours1 = []
total_boundaries1 = []
total_fifty = []
total_hundred = []
season_for_d2 = []
total_seasons = []
total_matches = []

# per over batsman df
bpo_match_id = []
bpo_batsman = []
bpo_batting_team = []
bpo_bowling_team = []
bpo_over = []
bpo_batman_runs = []

# per match batsman df....match_id, name, team, season, total runs, 50s, 100s, 6s, 4s, boundaries, strike rate
bpm_match_id = []
bpm_batsman = []
bpm_batting_team = []
bpm_bowling_team = []
bpm_batsman_runs = []
bpm_fifty = []
bpm_hundred = []
bpm_sixes = []
bpm_fours = []
bpm_boundaries = []
bpm_sr = []
bpm_season = []

# per season batsman df......name, season, team, total_runs, 4s, 6s, 100s, 50s, boundaries, strike rate
bps_batsman = []
bps_season = []
bps_batting_team = []
bps_batsman_runs = []
bps_fifty = []
bps_hundred = []
bps_sixes = []
bps_fours = []
bps_boundaries = []
bps_sr = []
bps_tc = []
bps_matches_played = []

# team runs and wickets per season.....season name total_batsman_runs total_6s total_4s total_boundaries total_runs_with_extra_runs total_wickets
trw_season = []
trw_team_name = []
trw_total_batsman_runs = []
trw_total_sixes = []
trw_total_fours = []
trw_total_boundaries = []
trw_total_runs = []  # with extra runs
trw_total_wickets = []
trw_trc = []
trw_wt = []
trw_mp = []
trw_wp = []
trw_now_bat = []
trw_now_bow = []

#####################################################################################

# bowler per over....match_id, bowler, over, economy, bowling_team, batting_team, wickets, maiden, 4s, 6s, batsman_runs, extra_runs, total_runs, wide_runs, no_ball_runs
# bye_and_legbye_runs
bow_po_match_id = []
bow_po_bowler = []
bow_po_over = []
bow_po_economy = []
bow_po_bowling_team = []
bow_po_batting_team = []
bow_po_wickets = []
bow_po_maiden = []
bow_po_four = []
bow_po_six = []
bow_po_batman_runs = []
bow_po_extra_runs = []
bow_po_total_runs = []
bow_po_wide_runs = []
bow_po_no_ball_runs = []
bow_po_bye_runs = []
bow_po_leg_bye_runs = []
bow_po_season = []

# bowler per match.....match_id, bowler, no. of overs, no. of wickets, economy, bowling_team, batting_team, maiden, 4s, 6s, batsman_runs, extra_runs
# total_runs, wide_runs, no_ball_runs, bye_and_legbye_runs
bow_pm_match_id = []
bow_pm_bowler = []
bow_pm_overs = []
bow_pm_economy = []
bow_pm_bowling_team = []
bow_pm_batting_team = []
bow_pm_wickets = []
bow_pm_maiden = []
bow_pm_four = []
bow_pm_six = []
bow_pm_batsman_runs = []
bow_pm_extra_runs = []
bow_pm_total_runs = []
bow_pm_wide_runs = []
bow_pm_no_ball_runs = []
bow_pm_bye_runs = []
bow_pm_leg_bye_runs = []
bow_pm_season = []

# bowler per season.....season , no. of matches, bowler, no. of overs, no. of wickets, economy, bowling_team, maiden, 4s, 6s, batsman_runs
# extra_runs, total_runs, wide_runs, no_ball_runs, bye_and_legbye_runs
bow_ps_season = []
bow_ps_matches = []
bow_ps_bowler = []
bow_ps_overs = []
bow_ps_wickets = []
bow_ps_economy = []
bow_ps_bowling_team = []
bow_ps_maiden = []
bow_ps_four = []
bow_ps_six = []
bow_ps_batsman_runs = []
bow_ps_extra_runs = []
bow_ps_total_runs = []
bow_ps_wide_runs = []
bow_ps_no_ball_runs = []
bow_ps_bye_runs = []
bow_ps_leg_bye_runs = []
bow_ps_tc = []

# bowler overall....., bowler,no. of seasons, no. of matches, no. of overs, no. of wickets, economy, maiden, 4s, 6s, batsman_runs
# # extra_runs, total_runs, wide_runs, no_ball_runs, bye_and_legbye_runs
bow_ovr_bowler = []
bow_ovr_seasons = []
bow_ovr_matches = []
bow_ovr_overs = []
bow_ovr_wickets = []
bow_ovr_economy = []
bow_ovr_maiden = []
bow_ovr_four = []
bow_ovr_six = []
bow_ovr_batsman_runs = []
bow_ovr_extra_runs = []
bow_ovr_total_runs = []
bow_ovr_wide_runs = []
bow_ovr_no_ball_runs = []
bow_ovr_bye_runs = []
bow_ovr_leg_bye_runs = []

# bowler per team per season.....name, opponent team, wickets
bow_pt_ps_name = []
bow_pt_ps_oppo_team = []
bow_pt_ps_wickets = []
bow_pt_ps_season = []

# bowler per team overall.....name, opponent team, wickets
bow_pt_ovr_name = []
bow_pt_ovr_oppo_team = []
bow_pt_ovr_sp = []
bow_pt_ovr_wickets = []

# team ovr
team_ovr_team = []
team_ovr_seasons = []
team_ovr_matches = []
team_ovr_trophies = []
team_ovr_win_per = []
team_ovr_br = []
team_ovr_four = []
team_ovr_six = []
team_ovr_tr = []
team_ovr_trc = []
team_ovr_wt = []
team_ovr_wc = []
team_ovr_now_bat = []
team_ovr_now_bow = []

# team per team per season for batting
tptps_team = []
tptps_oppo_team = []
tptps_season = []
tptps_win_per = []
tptps_br = []
tptps_f = []
tptps_s = []
tptps_tr = []
tptps_wc = []
tptps_sr = []
tptps_rr = []
tptps_now = []

# team per team per season for bowling
tptps_bow_team = []
tptps_bow_oppo_team = []
tptps_bow_season = []
tptps_bow_eco = []
tptps_bow_wt = []
tptps_bow_trc = []
tptps_bow_now = []

# team per team overall for batting team
tptovr_team = []
tptovr_oppo_team = []
tptovr_br = []
tptovr_f = []
tptovr_s = []
tptovr_tr = []
tptovr_wc = []
tptovr_sr = []
tptovr_rr = []
tptovr_now = []

# team per team overall for bowling team
tptovr_bow_team = []
tptovr_bow_oppo_team = []
tptovr_bow_eco = []
tptovr_bow_wt = []
tptovr_bow_trc = []
tptovr_bow_now = []

##########################################################################################

for t in team_list:  # for ovr
    team_ovr_team.append(t)
    ts = data1[data1['batting_team'] == t]
    for_now = data[data['team1'] == t]
    team_ovr_now_bat.append(len(for_now['winner']))
    team_ovr_seasons.append(len(ts['season'].unique()))
    team_ovr_matches.append(len(ts['match_id'].unique()))
    if winner_count.get(t) == 0:
        team_ovr_trophies.append(0)
    else:
        team_ovr_trophies.append(winner_count.get(t))
    ts2 = data[data['team1'] == t]
    if ts2.empty:
        pass
    else:
        wp1 = ((len(ts2[ts2['winner'] == t])) / (len(ts['match_id'].unique()))) * 100
        wp1 = round(wp1, 2)
        team_ovr_win_per.append(wp1)
    team_ovr_br.append(sum(ts['batsman_runs']))
    team_ovr_four.append(fours_sixes_count(ts)[0])
    team_ovr_six.append(fours_sixes_count(ts)[1])
    team_ovr_tr.append(sum(ts['total_runs']))
    team_ovr_wc.append(wicket_calc(ts))

    oppo_list1 = [item for item in team_list if item != t]  # opponent team list except t1
    for t2 in oppo_list1:  # for opponent team
        bat = ts[ts['bowling_team'] == t2].reset_index(drop=True)  # batting team is t1 for batting analysis
        if bat.empty:
            pass
        else:
            fn = for_now[for_now['team2'] == t2]
            tptovr_team.append(t)
            tptovr_oppo_team.append(t2)
            tptovr_br.append(sum(bat['batsman_runs']))
            tptovr_f.append(fours_sixes_count(bat)[0])
            tptovr_s.append(fours_sixes_count(bat)[1])
            tptovr_tr.append(sum(bat['total_runs']))
            tptovr_wc.append(wicket_calc(bat))
            tptovr_now.append(len(fn['winner']))

    for y in seasons:  # if df.empty append(0) # for season
        ts1 = ts[ts['season'] == y].reset_index(drop=True)  # deliveries
        # print(ts1)
        ts3 = ts2[ts2['season'] == y].reset_index(drop=True)  # matches
        for_now_ps = for_now[for_now['season'] == y]
        trw_now_bat.append(len(for_now_ps['winner']))
        # print(ts3)
        if ts3.empty:
            pass
        else:
            wp = ((len(ts3[ts3['winner'] == t])) / (len(ts1['match_id'].unique()))) * 100
            wp = round(wp, 2)
            trw_wp.append(wp)
        if ts1.empty:
            pass
        else:
            trw_mp.append(len(ts1['match_id'].unique()))
            trw_season.append(ts1['season'][0])
            trw_team_name.append(ts1['batting_team'][0])
            trw_total_batsman_runs.append(sum(ts1['batsman_runs']))
            trw_total_fours.append(fours_sixes_count(ts1)[0])
            trw_total_sixes.append(fours_sixes_count(ts1)[1])
            trw_total_boundaries.append(fours_sixes_count(ts1)[0] + fours_sixes_count(ts1)[1])
            trw_total_runs.append(sum(ts1['total_runs']))
            trw_total_wickets.append(wicket_calc(ts1))  # these are the wicket of team while batting
            # print(ts1)
            # break
            # for t1 in team_list: # for tptps # useless

        oppo_list = [item for item in team_list if item != t]  # opponent team list except t1
        for t2 in oppo_list:  # for opponent team
            bat = ts1[ts1['bowling_team'] == t2].reset_index(drop=True)  # batting team is t1 for batting analysis
            if bat.empty:
                pass
            else:
                bat1 = ts3[ts3['winner'] == t].reset_index(drop=True)
                fn = for_now_ps[for_now_ps['team2'] == t2]
                tptps_team.append(t)
                tptps_oppo_team.append(t2)
                tptps_season.append(bat['season'][0])
                wp_pt = ((len(bat1[bat1['winner'] == t])) / (len(bat['match_id'].unique()))) * 100
                wp_pt = round(wp_pt, 2)
                tptps_win_per.append(wp_pt)
                tptps_br.append(sum(bat['batsman_runs']))
                tptps_f.append(fours_sixes_count(bat)[0])
                tptps_s.append(fours_sixes_count(bat)[1])
                tptps_tr.append(sum(bat['total_runs']))
                tptps_wc.append(wicket_calc(bat))
                tptps_now.append(len(fn['winner']))

    bt = data1[data1['bowling_team'] == t]
    for_now1 = data[data['team2'] == t]
    team_ovr_now_bow.append(len(for_now1['winner']))
    team_ovr_trc.append(sum(bt['total_runs']))
    team_ovr_wt.append(wicket_calc(bt))
    for z in seasons:
        bt1 = bt[bt['season'] == z].reset_index(drop=True)
        for_now_ps = for_now1[for_now1['season'] == z]
        trw_now_bow.append(len(for_now_ps['winner']))
        if bt1.empty:
            pass
        else:
            trw_trc.append(sum(bt1['total_runs']))
            trw_wt.append(wicket_calc(bt1))

        oppo_list = [item for item in team_list if item != t]  # opponent team list except t1
        for t2 in oppo_list:  # for opponent team
            bow = bt1[bt1['batting_team'] == t2].reset_index(drop=True)  # bowling team is t1 for bowling analysis
            if bow.empty:
                pass
            else:
                fn1 = for_now_ps[for_now_ps['team1'] == t2]
                tptps_bow_team.append(t)
                tptps_bow_oppo_team.append(t2)
                tptps_bow_season.append(bow['season'][0])
                tptps_bow_wt.append(wicket_calc(bow))
                tptps_bow_trc.append(sum(bow['total_runs']))
                tptps_bow_now.append(len(fn1['winner']))

    oppo_list1 = [item for item in team_list if item != t]  # opponent team list except t1
    for t2 in oppo_list1:  # for opponent team
        bow = bt[bt['batting_team'] == t2].reset_index(drop=True)  # bowling team is t1 for bowling analysis
        if bow.empty:
            pass
        else:
            fn2 = for_now1[for_now1['team1'] == t2]
            tptovr_bow_team.append(t)
            tptovr_bow_oppo_team.append(t2)
            tptovr_bow_wt.append(wicket_calc(bow))
            tptovr_bow_trc.append(sum(bow['total_runs']))
            tptovr_bow_now.append(len(fn2['winner']))

team_runs_per_season = pd.DataFrame({'Season': trw_season,  # add win percentage column
                                     'Matches played': trw_mp,
                                     'Team': trw_team_name,
                                     'Batsman runs': trw_total_batsman_runs,
                                     '4s': trw_total_fours,
                                     '6s': trw_total_sixes,
                                     'Boundaries': trw_total_boundaries,
                                     'Total runs scored': trw_total_runs,  # with extra runs
                                     'Wickets conceded': trw_total_wickets,
                                     'Total runs conceded': trw_trc,
                                     'Total wickets taken': trw_wt,
                                     'Win %': trw_wp,
                                     })  # season name total_batsman_runs total_6s total_4s total_boundaries total_runs_with_extra_runs total_wickets
# print(team_runs_per_season.head(20))

#################################################################################3

team_ovr = pd.DataFrame({'Team': team_ovr_team,
                         'Seasons played': team_ovr_seasons,
                         'Matches played': team_ovr_matches,
                         'Trophies won': team_ovr_trophies,
                         'Win %': team_ovr_win_per,
                         'Batting runs': team_ovr_br,
                         '4s': team_ovr_four,
                         '6s': team_ovr_six,
                         'Runs': team_ovr_tr,
                         'Runs conceded': team_ovr_trc,
                         'Wickets': team_ovr_wt,
                         'Wickets conceded': team_ovr_wc,
                         })  # team, no. of seasons played, no. of matches played, no. of trophies won, win percentage, batsman runs, 4s, 6s, total_runs_scored, total_runs_conceded, wickets_taken, wickets_conceded
# print(team_ovr.head(20))

# team per team per season for batting
tptps = pd.DataFrame({'Team': tptps_team,
                      'Opponent team': tptps_oppo_team,
                      'Season': tptps_season,
                      'Win %' : tptps_win_per,
                      'Batsman runs' : tptps_br,
                      '4s' : tptps_f,
                      '6s' : tptps_s,
                      'Total runs' : tptps_tr,
                      'Wickets conceded': tptps_wc,
                      })
# print(tptps.head(20))

# team per team per season for bowling
tptps_bow = pd.DataFrame({'Team': tptps_bow_team,
                          'Opponent team': tptps_bow_oppo_team,
                          'Season' : tptps_bow_season,
                          'Wickets taken' : tptps_bow_wt,
                          'Total runs conceded': tptps_bow_trc,
                          })
# print(tptps_bow.head(20))

# team per team overall for batting team
tptovr = pd.DataFrame({'Team': tptovr_team,
                       'Opponent Team': tptovr_oppo_team,
                       'Batsman runs' : tptovr_br,
                       '4s' : tptovr_f,
                       '6s' : tptovr_s,
                       'Total runs' : tptovr_tr,
                       'Wickets conceded': tptovr_wc,
                       })
# print(tptovr.head(20))

# team per team overall for bowling team
tptovr_bow = pd.DataFrame({'Team': tptovr_bow_team,
                           'Opponent team': tptovr_bow_oppo_team,
                           'Wickets taken' : tptovr_bow_wt,
                           'Total runs conceded': tptovr_bow_trc,
                           })
# print(tptovr_bow.head(20))

#########################################################################################

for names in batsman:  # acc to player(overall) add season column for each dataframe and season-wise df is left(no. of matches column to be added)
    # match_id_df = data1[['id', 'season']]
    sum_over = []  # total batsman runs per over
    ovr_fifty = []  # total no. of 50s
    ovr_hundred = []  # total no. of 100s
    b_pt_fifty = []
    b_pt_hundred = []
    d1 = data1[data1['batsman'] == names]
    # tc = data[team_runs_per_season['Team'] == d1] # for team contribution
    d2 = d1[['match_id', 'batsman', 'batting_team', 'bowling_team', 'over', 'batsman_runs', 'season']].reset_index(
        drop=True)

    season_list = sorted(d2['season'].unique())
    total_seasons.append(len(season_list))
    total_matches.append(len(d2['match_id'].unique()))
    # print(season_list)
    for s in season_list:  # acc to season
        dfs = d2[d2['season'] == s].reset_index(drop=True)
        player_team = dfs['batting_team'][0]
        tc = team_runs_per_season[
            team_runs_per_season['Team'] == dfs['batting_team'][0]]  # this filter the db acc to the specific team
        tc1 = tc[tc['Season'] == s].reset_index(drop=True)  # for team contribution
        fifty_count = []  # the sum of this list is the no. of 50s in this 1 season and the same for the hundred count list
        hundred_count = []
        b_pt_ps_fifty_count = []
        b_pt_ps_hundred_count = []
        bps_batsman.append(dfs['batsman'][0])
        bps_season.append(s)
        bps_batting_team.append(dfs['batting_team'])
        bps_tr = sum(dfs['batsman_runs'])
        bps_batsman_runs.append(bps_tr)
        bps_bf = len(dfs['over'])
        srs = (bps_tr * 100) / bps_bf
        srs = round(srs, 2)
        bps_sr.append(srs)
        bps_fours.append(fours_sixes_count(dfs)[0])
        bps_sixes.append(fours_sixes_count(dfs)[1])
        bps_matches_played.append(len(dfs['match_id'].unique()))
        bps_boundaries.append(fours_sixes_count(dfs)[0] + fours_sixes_count(dfs)[1])
        if tc1.empty:
            pass
        else:
            tc2 = (bps_tr / tc1['Batsman runs'][0]) * 100
            tc2 = round(tc2, 2)
            bps_tc.append(tc2)

        ids = dfs['match_id'].unique()
        # print(ids)
        for ttt in team_list:  # for pt_ps
            ttt1 = dfs[dfs['bowling_team'] == ttt].reset_index(drop=True)
            if ttt1.empty:
                pass
            else:
                b_pt_ps_oppo_team.append(ttt1['batting_team'][0])
                b_pt_ps_name.append(names)
                b_pt_ps_season.append(ttt1['season'][0])
                b_pt_ps_mp.append(len(ttt1['match_id'].unique()))
                br1 = sum(ttt1['batsman_runs'])
                bf1 = len(ttt1['over'])
                sr1 = (br1 * 100) / bf1
                sr1 = round(sr1, 2)
                b_pt_ps_sr.append(sr1)
                b_pt_ps_br.append(br1)
                b_pt_ps_f.append(fours_sixes_count(ttt1)[0])
                b_pt_ps_s.append(fours_sixes_count(ttt1)[1])

        for m in ids:  # acc to match id(match-wise)
            dm = dfs[dfs['match_id'] == m].reset_index(drop=True)  # d2 should be dfs right?
            id3 = dm['match_id'].unique()
            o1 = dm['over'].unique()
            br = sum(dm['batsman_runs'])
            bf = len(dm['over'])
            # del dm['batsman_runs']
            idm = dm['match_id'][0]
            bpm_match_id.append(idm)
            bpm_batsman.append(dm['batsman'][0])
            bpm_batting_team.append(dm['batting_team'][0])
            bpm_bowling_team.append(dm['bowling_team'][0])
            bpm_batsman_runs.append(br)
            if br >= 50:
                if br <= 99:
                    bpm_fifty.append(1)
                    bpm_hundred.append(0)
                    fifty_count.append(1)
                    hundred_count.append(0)
                elif br >= 100:
                    bpm_hundred.append(1)
                    bpm_fifty.append(0)
                    hundred_count.append(1)
                    fifty_count.append(0)
            else:
                bpm_fifty.append(0)
                bpm_hundred.append(0)
                fifty_count.append(0)
                hundred_count.append(0)
            bpm_fours.append(fours_sixes_count(dm)[0])
            bpm_sixes.append(fours_sixes_count(dm)[1])
            bpm_boundaries.append(fours_sixes_count(dm)[0] + fours_sixes_count(dm)[1])
            srm = (br * 100) / bf
            srm = round(srm, 2)
            bpm_sr.append(srm)
            bpm_season.append(dm['season'][0])
            for o in o1:  # acc to over(over-wise)
                do = dm[dm['over'] == o]
                rpo = sum(do['batsman_runs'])
                del do['batsman_runs']
                do = do.drop_duplicates().reset_index(drop=True)
                do['RPO'] = rpo
                bpo_match_id.append(do.match_id[0])
                bpo_batsman.append(do['batsman'][0])
                bpo_batting_team.append(do['batting_team'][0])
                bpo_bowling_team.append(do['bowling_team'][0])
                bpo_over.append(do['over'][0])
                bpo_batman_runs.append(do['RPO'][0])
        bps_fifty.append(sum(fifty_count))  # since these lists will be appended in the for loop for match
        bps_hundred.append(sum(hundred_count))
        ovr_fifty.append(sum(fifty_count))  # for overall 50s(this is acc to each season)
        ovr_hundred.append(sum(hundred_count))  # for overall 100s(this is acc to each season)

    t_r = sum(d1['batsman_runs'])
    total_runs1.append(t_r)
    t_bf = len(d1['ball'])
    total_balls_faced1.append(t_bf)
    sr = (t_r * 100) / t_bf
    sr = round(sr, 2)
    strike_rate1.append(sr)
    total_sixes1.append(fours_sixes_count(d1)[1])
    total_fours1.append(fours_sixes_count(d1)[0])
    total_boundaries1.append(fours_sixes_count(d1)[0] + fours_sixes_count(d1)[1])
    total_fifty.append(sum(ovr_fifty))  # this is the total no. of 50s
    total_hundred.append(sum(ovr_hundred))  # this is the total no. of 100s
    for ttt in team_list:  # for pt_ps
        ttt1 = d2[d2['bowling_team'] == ttt].reset_index(drop=True)
        if ttt1.empty:
            pass
        else:
            b_pt_ovr_oppo_team.append(ttt1['batting_team'][0])
            b_pt_ovr_name.append(names)
            b_pt_ovr_sp.append(len(ttt1['season'].unique()))
            b_pt_ovr_mp.append(len(ttt1['match_id'].unique()))
            br1 = sum(ttt1['batsman_runs'])
            bf1 = len(ttt1['over'])
            sr1 = (br1 * 100) / bf1
            sr1 = round(sr1, 2)
            b_pt_ovr_sr.append(sr1)
            b_pt_ovr_br.append(br1)
            b_pt_ovr_f.append(fours_sixes_count(ttt1)[0])
            b_pt_ovr_s.append(fours_sixes_count(ttt1)[1])

###########################################################################################

for names1 in bowler:  # acc to names and for ovr
    dd1 = data1[data1['bowler'] == names1].reset_index(drop=True)
    bow_ovr_bowler.append(dd1['bowler'][0])
    bow_ovr_matches.append(len(dd1['match_id'].unique()))
    maiden_count2 = []
    over_count_ovr = []
    bow_ovr_wickets.append(wicket_calc_for_bowler(dd1))
    bow_ovr_four.append(fours_sixes_count(dd1)[0])
    bow_ovr_six.append(fours_sixes_count(dd1)[1])
    bow_ovr_batsman_runs.append(sum(dd1['batsman_runs']))
    bow_ovr_extra_runs.append(sum(dd1['extra_runs']))
    tr3 = sum(dd1['total_runs'])
    bow_ovr_total_runs.append(tr3)
    bow_ovr_wide_runs.append(sum(dd1['wide_runs']))
    bow_ovr_no_ball_runs.append(sum(dd1['noball_runs']))
    bow_ovr_bye_runs.append(sum(dd1['bye_runs']))
    bow_ovr_leg_bye_runs.append(sum(dd1['legbye_runs']))

    season_list1 = sorted(dd1['season'].unique())
    bow_ovr_seasons.append(len(season_list1))
    # print(season_list1)
    for s1 in season_list1:  # acc to seasons
        dfs1 = dd1[dd1['season'] == s1].reset_index(drop=True)
        maiden_count1 = []
        over_count = []
        season_total_wickets = wicket_calc_for_bowler(dfs1)
        tc3 = team_runs_per_season[team_runs_per_season['Team'] == dfs1['bowling_team'][
            0]]  # this filter the db acc to the specific team for team contribution
        tc4 = tc3[tc3['Season'] == s1].reset_index(
            drop=True)  # this filter the season so there's either only row of the player of season and team or empty
        if tc4.empty:
            pass
        else:
            tc5 = (season_total_wickets / tc4['Total wickets taken'][0]) * 100
            tc5 = round(tc5, 2)
            bow_ps_tc.append(tc5)

        bow_ps_season.append(dfs1['season'][0])
        bow_ps_bowler.append(dfs1['bowler'][0])
        bow_ps_wickets.append(wicket_calc_for_bowler(dfs1))
        tr2 = sum(dfs1['total_runs'])
        bow_ps_total_runs.append(tr2)
        bow_ps_bowling_team.append(dfs1['bowling_team'][0])
        bow_ps_four.append(fours_sixes_count(dfs1)[0])
        bow_ps_six.append(fours_sixes_count(dfs1)[1])
        bow_ps_batsman_runs.append(sum(dfs1['batsman_runs']))
        bow_ps_extra_runs.append(sum(dfs1['extra_runs']))
        bow_ps_wide_runs.append(sum(dfs1['wide_runs']))
        bow_ps_no_ball_runs.append(sum(dfs1['noball_runs']))
        bow_ps_bye_runs.append(sum(dfs1['bye_runs']))
        bow_ps_leg_bye_runs.append(sum(dfs1['legbye_runs']))

        for bb in team_list:
            bb1 = dfs1[dfs1['batting_team'] == bb].reset_index(drop=True)
            if bb1.empty:
                pass
            else:
                bow_pt_ps_name.append(names1)
                bow_pt_ps_oppo_team.append(bb)
                bow_pt_ps_season.append(bb1['season'][0])
                bow_pt_ps_wickets.append(wicket_calc_for_bowler(bb1))

        ids1 = dfs1['match_id'].unique()
        bow_ps_matches.append(len(ids1))
        for m1 in ids1:  # acc to match_id # economy
            maiden_count = []
            dm1 = dfs1[dfs1['match_id'] == m1].reset_index(drop=True)
            bow_pm_match_id.append(dm1['match_id'][0])
            bow_pm_bowler.append(dm1['bowler'][0])
            over = dm1['over'].unique()
            bow_pm_overs.append(len(over))
            bow_pm_bowling_team.append(dm1['bowling_team'][0])
            bow_pm_batting_team.append(dm1['batting_team'][0])
            bow_pm_wickets.append(wicket_calc_for_bowler(dm1))
            bow_pm_four.append(fours_sixes_count(dm1)[0])
            bow_pm_six.append(fours_sixes_count(dm1)[1])
            bow_pm_batsman_runs.append(sum(dm1['batsman_runs']))
            bow_pm_extra_runs.append(sum(dm1['extra_runs']))
            tr1 = sum(dm1['total_runs'])
            bow_pm_total_runs.append(tr1)
            eco = tr1 / len(over)
            eco = round(eco, 2)
            bow_pm_economy.append(eco)
            bow_pm_wide_runs.append(dm1['wide_runs'])
            bow_pm_no_ball_runs.append(sum(dm1['noball_runs']))
            bow_pm_bye_runs.append(sum(dm1['bye_runs']))
            bow_pm_leg_bye_runs.append(dm1['legbye_runs'])
            bow_pm_season.append(dm1['season'][0])

            o2 = dm1['over'].unique()
            # print(o2)
            for o in o2:  # acc to over
                do1 = dm1[dm1['over'] == o].reset_index(drop=True)
                bow_po_match_id.append(do1['match_id'][0])
                bow_po_bowler.append(do1['bowler'][0])
                bow_po_over.append(do1['over'][0])
                bow_po_bowling_team.append(do1['bowling_team'][0])
                bow_po_batting_team.append(do1['batting_team'][0])
                bow_po_wickets.append(wicket_calc_for_bowler(do1))
                bow_po_four.append(fours_sixes_count(do1)[0])
                bow_po_six.append(fours_sixes_count(do1)[1])
                bow_po_batman_runs.append(sum(do1['batsman_runs']))
                bow_po_extra_runs.append(sum(do1['extra_runs']))
                bow_po_wide_runs.append(sum(do1['wide_runs']))
                bow_po_no_ball_runs.append(sum(do1['noball_runs']))
                bow_po_bye_runs.append(sum(do1['bye_runs']))
                bow_po_leg_bye_runs.append(do1['legbye_runs'])
                trb = sum(do1['total_runs'])
                bow_po_economy.append(trb)
                bow_po_total_runs.append(trb)
                if trb == 0:
                    bow_po_maiden.append(1)
                    maiden_count.append(1)
                else:
                    bow_po_maiden.append(0)
                    maiden_count.append(0)
                bow_po_season.append(do1['season'][0])
                # break
            over_count.append(len(over))
            bow_pm_maiden.append(sum(maiden_count))
            maiden_count1.append(sum(maiden_count))
            # break
        bow_ps_overs.append(sum(over_count))
        eco1 = tr2 / sum(over_count)
        eco1 = round(eco1, 2)
        bow_ps_economy.append(eco1)
        bow_ps_maiden.append(sum(maiden_count1))
        over_count_ovr.append(sum(over_count))
        maiden_count2.append(sum(maiden_count1))
    bow_ovr_overs.append(sum(over_count_ovr))
    eco2 = tr3 / sum(over_count_ovr)
    eco2 = round(eco2, 2)
    bow_ovr_economy.append(eco2)
    bow_ovr_maiden.append(sum(maiden_count2))
    for bb in team_list:
        bb1 = dd1[dd1['batting_team'] == bb]
        if bb1.empty:
            pass
        else:
            bow_pt_ovr_name.append(names1)
            bow_pt_ovr_sp.append(len(bb1['season'].unique()))
            bow_pt_ovr_oppo_team.append(bb)
            bow_pt_ovr_wickets.append(wicket_calc_for_bowler(bb1))

###########################################################################################

# team wins ovr.....counter
twc = list(data['winner'])
twc_wn = [x for x in twc if str(x) != 'nan']
twc1 = Counter(twc_wn)
# print(twc1)

twc_teams = [x for x in twc1.keys()]
# print(twc_teams)

twc_count = [x for x in twc1.values()]
# print(twc_count)

ovr_wins_count = pd.DataFrame({'Teams': twc_teams,
                               'Wins': twc_count
                               })
ovr_wins_count = ovr_wins_count.sort_values(by='Wins', ascending=False).reset_index(drop=True)
# print(ovr_wins_count)

# team wins per season.....counter

twps_team = []
twps_season = []
twps_wins = []

for ss in seasons:
    ss1 = data[data['season'] == ss]
    ss_count = Counter(ss1['winner'])
    # print(len(ss_count))
    for keys in ss_count.keys():
        twps_team.append(keys)
    for i in range(0, len(ss_count)):
        twps_season.append(ss)
    for values in ss_count.values():
        twps_wins.append(values)
    # print(ss_count)

# print(len(twps_team))
# print(len(twps_season))
# print(len(twps_wins))

twps = pd.DataFrame({'Team': twps_team,
                     'Season': twps_season,
                     'Wins': twps_wins})
# print(twps.head(40))

#############################################################################################

# toss analysis....team, no. of toss won, toss win%, decision, decision%, toss won match won %
for_ta = data[['toss_winner', 'toss_decision', 'winner']]
ta_team = []
ta_toss_winner_count = []
toss_d_f = []
toss_d_f_p = []
toss_d_b = []
toss_d_b_p = []
toss_winner_match_winner = []

for ta in teams:
    ta1 = for_ta[for_ta['toss_winner'] == ta]
    ta_team.append(ta)
    ta_toss_winner_count.append(len(ta1['toss_winner']))
    tdf = len(ta1[ta1['toss_decision'] == 'field'])
    toss_d_f.append(tdf)
    tdfp = (tdf / len(ta1['toss_winner'])) * 100
    tdfp = round(tdfp, 2)
    toss_d_f_p.append(tdfp)
    tdb = len(ta1[ta1['toss_decision'] == 'bat'])
    toss_d_b.append(tdb)
    tdbp = (tdb / len(ta1['toss_winner'])) * 100
    tdbp = round(tdbp, 2)
    toss_d_b_p.append(tdbp)
    mwp = ((len(ta1[ta1['winner'] == ta])) / len(ta1['winner'])) * 100
    mwp = round(mwp, 2)
    toss_winner_match_winner.append(mwp)

ta_df = pd.DataFrame({'Team': ta_team,
                      'Toss wins': ta_toss_winner_count,
                      'Field' : toss_d_f,
                      'Field %': toss_d_f_p,
                      'Bat' : toss_d_b,
                      'Bat %': toss_d_b_p,
                      'Toss win match win %': toss_winner_match_winner,
                      })
# print(ta_df.head(20))

###########################################################################################

# venue analysis.....no. of matches, toss win decisions,toss won match won %, most winning team and no. of matches won

venues = data['venue'].unique()
venue_list = [x for x in venues if str(x) != 'nan']

for_va = data[['venue', 'toss_winner', 'toss_decision', 'winner']]
va_venue = []
va_nom = []
va_twdfp = []
va_twdbp = []
va_twmwp = []
va_mwt = []
va_now = []
for va in venue_list:
    twmw = []
    va1 = for_va[for_va['venue'] == va].reset_index(drop=True)
    va_venue.append(va)
    va_nom.append(len(va1['venue']))
    twf = len(va1[va1['toss_decision'] == 'field'])
    twfp = (twf / len(va1['toss_winner'])) * 100
    twfp = round(twfp, 2)
    va_twdfp.append(twfp)
    twb = len(va1[va1['toss_decision'] == 'bat'])
    twbp = (twb / len(va1['toss_winner'])) * 100
    twbp = round(twbp, 2)
    va_twdbp.append(twbp)
    for t in range(0, len(va1['winner'])):
        if va1['toss_winner'][t] == va1['winner'][t]:
            twmw.append(1)
    twmwp = (sum(twmw) / len(va1['winner'])) * 100
    twmwp = round(twmwp, 2)
    va_twmwp.append(twmwp)

    winner_list = va1['winner']
    wl_wn = [x for x in winner_list if str(x) != 'nan']
    mvt = Counter(wl_wn)
    mvt_tuples = sorted(mvt.items(), key=lambda item: item[1])
    sorted_mvt = {k: v for k, v in mvt_tuples}
    # print(sorted_mvt)
    for keys in sorted_mvt.keys():
        pass
    va_mwt.append(keys)
    for values in sorted_mvt.values():
        pass
    va_now.append(values)

va_df = pd.DataFrame({'Venue': va_venue,
                      'No. of matches': va_nom,
                      'Field %': va_twdfp,
                      'Bat %': va_twdbp,
                      'Toss win match win %': va_twmwp,
                      'Most winning team': va_mwt,
                      'No. of wins': va_now,
                      })
# print(va_df.head(30))

###########################################################################################

batsman_per_over_db = pd.DataFrame({'match_id': bpo_match_id,
                                    'Batsman': bpo_batsman,
                                    'Batting Team': bpo_batting_team,
                                    'Bowling Team': bpo_bowling_team,
                                    'Over': bpo_over,
                                    'Runs per over': bpo_batman_runs
                                    })
# print(batsman_per_over_db.head(30))
# print(batsman_per_over_db.tail(30))

# print(len(bpm_match_id))
# print(len(bpm_season))
batsman_per_match_db = pd.DataFrame({'match_id': bpm_match_id,
                                     'Season': bpm_season,
                                     'Batsman': bpm_batsman,
                                     'Batting team': bpm_batting_team,
                                     'Bowling team': bpm_bowling_team,
                                     'Total runs': bpm_batsman_runs,
                                     '50s': bpm_fifty,
                                     '100s': bpm_hundred,
                                     '6s': bpm_sixes,
                                     '4s': bpm_fours,
                                     'Boundaries': bpm_boundaries,
                                     'Strike rate': bpm_sr
                                     })  # name, team, season, total runs, 50s, 100s, 6s, 4s, boundaries, strike rate, highest runs in which over(can use the over-wise df for this column)
# batsman_per_match_db = batsman_per_match_db.sort_values('Total runs', ascending=True)
# print(batsman_per_match_db.head(10))

batsman_per_season = pd.DataFrame({'Name': bps_batsman,  # add team contribution column to this df
                                   'Season': bps_season,
                                   'Matches played': bps_matches_played,
                                   'Team': bps_batting_team,
                                   'Runs': bps_batsman_runs,
                                   '50s': bps_fifty,
                                   '100s': bps_hundred,
                                   '6s': bps_sixes,
                                   '4s': bps_fours,
                                   'Boundaries': bps_boundaries,
                                   'Strike rate': bps_sr,
                                   'Team runs contribution(in %)': bps_tc
                                   })  # edit the bpm db for this df....name, season, team, total_runs, 4s, 6s, 100s, 50s, boundaries, strike rate
# print(batsman_per_season.head(10))

batsman_overall_db = pd.DataFrame({'Name': batsman,
                                   'Seasons played': total_seasons,
                                   'Matches played': total_matches,
                                   'Runs': total_runs1,
                                   'Balls faced': total_balls_faced1,
                                   'Strike rate': strike_rate1,
                                   'Sixes': total_sixes1,
                                   'Fours': total_fours1,
                                   'Boundaries': total_boundaries1,
                                   '50s': total_fifty,
                                   '100s': total_hundred
                                   })
# print(batsman_overall_db.head(10))

b_pt_ps = pd.DataFrame({'Name': b_pt_ps_name,
                        'Season': b_pt_ps_season,
                        'Matches played': b_pt_ps_mp,
                        'Opponent team': b_pt_ps_oppo_team,
                        'Batsman runs': b_pt_ps_br,
                        'Strike Rate': b_pt_ps_sr,
                        '4s': b_pt_ps_f,
                        '6s': b_pt_ps_s,
                        })
# print(b_pt_ps.head(30))

bt_pt_ovr = pd.DataFrame({'Name': b_pt_ovr_name,
                          'Seasons played': b_pt_ovr_sp,
                          'Matches played': b_pt_ovr_mp,
                          'Opponent team': b_pt_ovr_oppo_team,
                          'Batsman runs': b_pt_ovr_br,
                          '4s': b_pt_ovr_f,
                          '6s': b_pt_ovr_s,
                          'Strike rate': b_pt_ovr_sr
                          })
# print(bt_pt_ovr.head(30))

#################################################################################################

bowler_per_over = pd.DataFrame({'Match_id': bow_po_match_id,
                                'Season': bow_po_season,
                                'Bowler': bow_po_bowler,
                                'Over': bow_po_over,
                                'Economy': bow_po_economy,
                                'Bowling_team': bow_po_bowling_team,
                                'Batting_team': bow_po_batting_team,
                                'Wickets': bow_po_wickets,
                                'Maiden': bow_po_maiden,
                                '4s': bow_po_four,
                                '6s': bow_po_six,
                                'Batsman_runs': bow_po_batman_runs,
                                'Extra_runs': bow_po_extra_runs,
                                'Total_runs': bow_po_total_runs,
                                'Wide_runs': bow_po_wide_runs,
                                'No_ball_runs': bow_po_no_ball_runs,
                                'Bye_runs': bow_po_bye_runs,
                                'Leg_bye_runs': bow_po_leg_bye_runs
                                })  # name over total_batsman_runs extra_runs wide_runs no_ball_runs bye_and_lb_runs total_runs
# print(bowler_per_over.head(20))

bowler_per_match = pd.DataFrame({'Match_id': bow_pm_match_id,
                                 'Bowler': bow_pm_bowler,
                                 'Overs': bow_pm_overs,
                                 'Economy': bow_pm_economy,
                                 'Bowling_team': bow_pm_bowling_team,
                                 'Batting_team': bow_pm_batting_team,
                                 'Wickets': bow_pm_wickets,
                                 'Maiden': bow_pm_maiden,
                                 '4s': bow_pm_four,
                                 '6s': bow_pm_six,
                                 'Batsman_runs': bow_pm_batsman_runs,
                                 'Extra_runs': bow_pm_extra_runs,
                                 'Total_runs': bow_pm_total_runs,
                                 'Wide_runs': bow_pm_wide_runs,
                                 'No_ball_runs': bow_pm_no_ball_runs,
                                 'Bye_runs': bow_pm_bye_runs,
                                 'Leg_bye_runs': bow_pm_leg_bye_runs,
                                 'Season': bow_pm_season,
                                 })
# print(bowler_per_match.head(10))

bowler_per_season = pd.DataFrame({'Season': bow_ps_season,
                                  'Matches': bow_ps_matches,
                                  'Bowler': bow_ps_bowler,
                                  'Overs': bow_ps_overs,
                                  'Wickets': bow_ps_wickets,
                                  'Economy': bow_ps_economy,
                                  'Bowling_team': bow_ps_bowling_team,
                                  'Maiden': bow_ps_maiden,
                                  '4s': bow_ps_four,
                                  '6s': bow_ps_six,
                                  'Batsman_runs': bow_ps_batsman_runs,
                                  'Extra_runs': bow_ps_extra_runs,
                                  'Total_runs': bow_ps_total_runs,
                                  'Wide_runs': bow_ps_wide_runs,
                                  'No_ball_runs': bow_ps_no_ball_runs,
                                  'Bye_runs': bow_ps_bye_runs,
                                  'Leg_bye_runs': bow_ps_leg_bye_runs,
                                  'Team_contribution(in %)': bow_ps_tc
                                  })
# print(bowler_per_season.head(10))

bowler_overall = pd.DataFrame({'Bowler': bow_ovr_bowler,
                               'Seasons played': bow_ovr_seasons,
                               'Matches played': bow_ovr_matches,
                               'Overs': bow_ovr_overs,
                               'Wickets': bow_ovr_wickets,
                               'Economy': bow_ovr_economy,
                               'Maiden': bow_ovr_maiden,
                               '4s': bow_ovr_four,
                               '6s': bow_ovr_six,
                               'Batsman_runs': bow_ovr_batsman_runs,
                               'Extra_runs': bow_ovr_extra_runs,
                               'Total_runs': bow_ovr_total_runs,
                               'Wide_runs': bow_ovr_wide_runs,
                               'No_ball_runs': bow_ovr_no_ball_runs,
                               'Bye_runs': bow_ovr_bye_runs,
                               'Leg_bye_runs': bow_ovr_leg_bye_runs
                               })
# print(bowler_overall.head(10))

bow_pt_ps = pd.DataFrame({'Name': bow_pt_ps_name,
                          'Season': bow_pt_ps_season,
                          'Opponent team': bow_pt_ps_oppo_team,
                          'Wickets': bow_pt_ps_wickets,
                          })
# print(bow_pt_ps.head(30))

bow_pt_ovr = pd.DataFrame({'Name': bow_pt_ovr_name,
                           'Seasons played': bow_pt_ovr_sp,
                           'Opponent team': bow_pt_ovr_oppo_team,
                           'Wickets': bow_pt_ovr_wickets,
                           })


# print(bow_pt_ovr.head(30))

#####################################################################################

def over_calc(df):
    overs = [('Over' + str(i)) for i in range(1, 21)]
    sum_over12 = []
    for m13 in range(1, 21):
        only_over = list(df[(df.over != m13)].index)
        over12 = df.drop(index=only_over, axis=0).reset_index(drop=True)
        sum_over12.append(sum(over12['total_runs']))
    for_graph = []
    result = 0
    for i in sum_over12:
        result = i + result
        for_graph.append(result)
    return sum_over12, overs, for_graph

def for_wicket_graph(df):
    wickets_df = df.dropna()
    wicket_x_axis = []
    wicket_y_axis = []
    for i in list(wickets_df.index):
        length = i
        over13 = wickets_df.over[i]
        ball13 = wickets_df.ball[i]
        z13 = int(str(over13) + str(ball13))  # to convert these no. to a decimal of over.ball for x-axis locations
        z1 = z13 / 10
        wicket_x_axis.append(z1)
        wicket_y_axis.append(sum(df.total_runs[0:length]))
    return wicket_x_axis, wicket_y_axis

def bats_bow(df): # return 2 dfs
    team_batsman = []
    team_br = []
    team_bow = []
    team_w = []
    bats = df['batsman'].unique()
    bow13 = df['bowler'].unique()
    for i in bats:
        bt13 = df[df['batsman'] == i]
        team_batsman.append(i)
        team_br.append(sum(bt13['batsman_runs']))
    for j in bow13:
        bow14 = df[df['bowler'] == j]
        team_bow.append(j)
        team_w.append(wicket_calc(bow14))
    return team_batsman, team_br, team_bow, team_w

def extra_runs_calc(inning, name, b):
    for x in inning.iloc[:,b]:  # this line is doubtful
        if x != 0:
            name.append(x)
    return name


def inning_runs(x):
    y16 = []
    for i in x:
        if i != 0:
            y16.append(i)
    yt = sum(y16)
    return yt

def batsmen_table(df):
    batsmen = df['batsman'].unique()
    # print(batsmen)
    six = []
    four = []
    total_bruns = []
    total_balls_faced = []
    strike_rate = []
    for i in batsmen:
        s_count = 0
        f_count = 0
        x = df[df.batsman == i]
        tr = sum(x.batsman_runs)
        total_bruns.append(tr)
        tbf = len(x.ball)
        total_balls_faced.append(tbf)
        sr16 = (tr*100)/tbf
        sr16 = round(sr16, 2)
        strike_rate.append(sr16)
        for j in x['batsman_runs']:
            if j == 6:
                s_count += 1
            elif j == 4:
                f_count += 1
        six.append(s_count)
        four.append(f_count)

    return batsmen, six, four, total_bruns, total_balls_faced, strike_rate

def bowler_table(df):
    bowler14 = df.bowler.unique()
    overs = []
    wickets14 = []
    total_runs = []
    extra_runs = []
    economy = []
    for i in bowler14:
        dbs = df[df['bowler'] == i]
        dbs = dbs[['bowler', 'over', 'dismissal_kind', 'total_runs', 'extra_runs']]
        wickets14.append(wicket_calc_for_bowler(dbs))
        tr = sum(dbs['total_runs'])
        total_runs.append(tr)
        tb = len(dbs['over'].unique())
        eco_bow = tr/tb
        eco_bow = round(eco_bow, 2)
        economy.append(eco_bow)
        extra_runs.append(sum(dbs['extra_runs']))
        dbo = dbs[['bowler', 'over']]
        dbo = dbo.drop_duplicates()
        overs.append(len(dbo['over']))

    return bowler14, overs, wickets14, total_runs, extra_runs, economy

def motm(idss):
    fid = data[data['id'] == idss].reset_index(drop=True)
    return fid['player_of_match'][0]


def winner(match_id):  #  function to calculate the total runs in 1 inning
    extra_runs = []
    legbye_runs = []
    bye_runs = []
    only_idm = list(data[(data.id !=match_id)].index)
    idm1 = data.drop(index=only_idm, axis=0).reset_index(drop=True)
    #print(idm)
    only_match_id = list(data1[(data1.match_id !=match_id)].index)
    match = data1.drop(index=only_match_id, axis=0)
    only_first_inning = list(match[(match.inning != 1)].index)
    first_inning = match.drop(index=only_first_inning, axis=0)
    #print(first_inning)
    first_inning_runs = first_inning['total_runs'].to_list()
    total_first_inning_runs = inning_runs(first_inning_runs)
    e1 = extra_runs_calc(first_inning, extra_runs, 16)
    l1 = extra_runs_calc(first_inning, legbye_runs, 12)
    b1 = extra_runs_calc(first_inning, bye_runs, 11)
    first_inning_total_extra_balls = len(e1) - len(l1) - len(b1)
    first_inning_total_balls = len(first_inning['over']) - first_inning_total_extra_balls
    only_second_inning = list(match[(match.inning != 2)].index)
    second_inning = match.drop(index=only_second_inning, axis=0)
    second_inning_runs = second_inning['total_runs'].to_list()
    total_second_inning_runs = inning_runs(second_inning_runs)
    e2 = extra_runs_calc(second_inning, extra_runs, 16)
    l2 = extra_runs_calc(second_inning, legbye_runs, 12)
    b2 = extra_runs_calc(second_inning, bye_runs, 11)
    second_inning_total_extra_balls = len(e2) - len(l2) - len(b2)
    second_inning_total_balls = len(second_inning['over']) - second_inning_total_extra_balls

    batsmen_table(first_inning)
    batsmen_table(second_inning)

    bowler_table(first_inning) # make it as print() for output
    bowler_table(second_inning)

    # win by runs or win by wickets....
    if total_first_inning_runs > total_second_inning_runs:#win by runs(all out or no balls left)....second team's runs, balls, wickets
        if wicket_calc(second_inning) == 10:# for all out
            return "All out"
        elif (120-second_inning_total_extra_balls) == 120 and total_second_inning_runs != total_first_inning_runs: # no balls left and score not same as first team
            return "No balls left"
        diff = total_first_inning_runs - total_second_inning_runs
        #print(win1)
        return ""+str(idm1['winner'][0])+" won by "+str(diff)+" runs"
    elif total_second_inning_runs >= total_first_inning_runs: #win by wicket condition(balls left after winning and wickets)
        #diff = total_second_inning_runs - total_first_inning_runs
        if (120-second_inning_total_balls) != 0:
            return ""+str(idm1['winner'][0])+" won with "+str(120 - second_inning_total_balls)+" balls in hand and by "+str(10 - wicket_calc(second_inning))+" wickets"
        elif second_inning_total_balls == 120:
            return ""+str(idm1['winner'][0])+" won by "+str(10 - wicket_calc(second_inning))+" wickets"
    else:
        return 'Draw'

def league_table(year):
    teams12 = []
    won = []
    lost = []
    matches1 = []
    points = []
    dl = []
    nrr = []
    index_year = list(data[(data.season != year)].index)
    only_year = data.drop(index=index_year, axis=0).reset_index(drop=True)
    teams1 = only_year['team1'].unique()
    b = [x for x in teams1 if str(x) != 'nan']
    teams_not_nan = []
    for i in b:
        if i not in teams_not_nan:
            teams_not_nan.append(i)
    nom = (len(teams_not_nan)-1)*len(teams_not_nan)
    if year == 2008 or year == 2015 or year == 2017:
        nom = 55
    elif year == 2009:
        nom = 54
    elif year == 2011:
        nom = 69
    elif year == 2012:
        nom = 70
    only_year1 = only_year.iloc[:nom,:]
    for i in teams_not_nan: # acc to team
        m146 = []
        dl1 = []
        team_tr = [] # total runs scored in each match # this is for the calculation of nrr and this sum can be used for the formula of nrr at the end of this for loop
        team_to = [] # total overs played in each match
        team_rc = [] # total runs conceded in each match
        team_ob = [] # total overs bowled in each match
        teams12.append(i)
        index_team1 = list(only_year1[(only_year1.team1 != i)].index)
        index_team2 = list(only_year1[(only_year1.team2 != i)].index)
        only_team1 = only_year1.drop(index=index_team1, axis=0)  #
        only_team2 = only_year1.drop(index=index_team2, axis=0)  #
        total = [only_team1, only_team2]
        result = pd.concat(total).reset_index(drop=True)
        ids_for_nrr = result['id'].unique()
        for idnr0 in ids_for_nrr: # acc to match_id
            idnr = data1[data1['match_id'] == idnr0]
            bt4 = idnr[idnr['batting_team'] == i]
            team_tr.append(sum(bt4['total_runs']))
            team_to.append(len(bt4['over'].unique()))
            bo = idnr[idnr['bowling_team'] == i]
            team_rc.append(sum(bo['total_runs']))
            team_ob.append(len(bo['over'].unique()))

        for_won = list(result[(result.winner != i)].index)  ##
        for_won1 = result.drop(index=for_won, axis=0).reset_index(drop=True)  ##

        won.append(len(for_won1['winner']))
        lost.append(len(result['winner']) - len(for_won1['winner']))

        for_dl = list(result[(result.dl_applied != 1)].index)  ##
        only_dl = result.drop(index=for_dl, axis=0).reset_index(drop=True)
        only_dl1 = list(only_dl.winner.values)

        if len(only_dl1) == 0 :
            dl1.append(0)
        elif only_dl1[0] != i:
            dl1.append(1)
            m146.append(1)

        dl.append(sum(dl1))
        m146.append(len(result['id']))
        matches1.append(sum(m146))
        points.append((len(for_won1['winner']) * 2) + sum(dl1))
        nrr1 = (sum(team_tr)/sum(team_to))-(sum(team_rc)/sum(team_ob))
        nrr1 = round(nrr1, 3)
        nrr.append(nrr1)


    table = pd.DataFrame({'Teams': teams12,
                          'Matches': matches1,
                          'Wins': won,
                          'Lost': lost,
                          'NR': dl,
                          'NRR' : nrr,
                          'Points': points
})
    table = table.sort_values(['Points', 'NRR'], axis=0, ascending=[False, False]).reset_index(drop=True) # i sorted using points but if the points are same they will be sorted according to NRR
    return table

def over_wise(match_id):
    over_no = [x for x in range(1, 21)]
    only_idm = list(data1[(data1.match_id != match_id)].index)
    idm15 = data1.drop(index=only_idm, axis=0).reset_index(drop=True)
    only_first_inning = list(idm15[(idm15.inning != 1)].index)
    first_inning = idm15.drop(index=only_first_inning, axis=0).reset_index(drop=True)
    only_second_inning = list(idm15[(idm15.inning != 2)].index)
    second_inning = idm15.drop(index=only_second_inning, axis=0).reset_index(drop=True)
    team1_bat = bats_bow(first_inning)[0]
    team1_br = bats_bow(first_inning)[1]
    team1_bow = bats_bow(second_inning)[2]
    team1_bw = bats_bow(second_inning)[3]
    team2_bat = bats_bow(second_inning)[0]
    team2_br = bats_bow(second_inning)[1]
    team2_bow = bats_bow(first_inning)[2]
    team2_bw = bats_bow(first_inning)[3]

    return over_no, over_calc(first_inning)[2], over_calc(second_inning)[2], first_inning.batting_team[0], \
           first_inning.bowling_team[0], team1_bat, team1_br, team1_bow, team1_bw, team2_bat, team2_br, \
           team2_bow, team2_bw, over_calc(first_inning)[0], over_calc(second_inning)[0], for_wicket_graph(first_inning)[0], \
           for_wicket_graph(first_inning)[1], for_wicket_graph(second_inning)[0], for_wicket_graph(second_inning)[1], \
           batsmen_table(first_inning), batsmen_table(second_inning), bowler_table(first_inning), bowler_table(second_inning)


#####################################################################################################

app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


index_page = html.Div([
    html.H5("Click on the links below for information!"),
    html.Br(),
    dcc.Link('Team', href='/page-1'),
    html.Br(),
    dcc.Link('Batsman', href='/page-2'),
    html.Br(),
    dcc.Link('Bowler', href='/page-3'),
    html.Br(),
    dcc.Link('Fielder', href='/page-4'),
    html.Br(),
    dcc.Link('Wicket-keeper', href='/page-5'),
    html.Br(),
    dcc.Link('Match', href='/page-6'),
    html.Br(),
    dcc.Link('Points table', href='/page-7'),
    html.Br(),
    dcc.Link('Venue', href='/page-8'),
    html.Br(),
    dcc.Link('Toss', href='/page-9'),
    html.Br(),
    dash_table.DataTable(id='motm',
        columns=[
            {"name": i, "id": i, "deletable": True, "selectable": True} for i in motm_df.columns
        ],
        data=motm_df.to_dict('records'),
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        page_action="native",
        page_current=0,
        page_size=10,
    ),
    html.Br(),
    html.Br(),
    html.H5("For more information click on the link on the top left corner")
])

#############################################################################################################

# Team

fig_team_wins_ovr = px.bar(data_frame=ovr_wins_count, x='Teams', y='Wins', title='Wins overall')

page_1_layout = html.Div([
    html.H1("Team"),
    html.Br(),
    dash_table.DataTable(
        id='datatable-interactivity21',
        columns=[
            {"name": i, "id": i, "deletable": True, "selectable": True} for i in team_ovr.columns
        ],
        data=team_ovr.to_dict('records'),
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_selectable="multi",
        row_deletable=True,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current=0,
        page_size=10,
    ),
    html.Br(),
    html.Br(),
    html.Div(id='datatable-interactivity-container21'),
    html.Br(),
    dcc.Graph(id='two', figure=fig_team_wins_ovr),
    html.Br(),
    dcc.Dropdown(id='drop11',
                 options= [{'label' : x,'value' : x} for x in team_list],
                 placeholder='Select Team',
                 clearable=False
                 ),
    html.Br(),
    dcc.Graph(id='fig10a', figure={}, style = {'display' : 'none'}), # per season graph
    html.Br(),
    dcc.Graph(id='fig12a', figure={}, style = {'display' : 'none'}), # per season graph
    html.Br(),
    dcc.Graph(id='fig12ab', figure={}, style = {'display' : 'none'}), # per season graph
    html.Br(),
    dcc.Graph(id='fig12ac', figure={}, style = {'display' : 'none'}), # per season graph
    html.Br(),
    dcc.Graph(id='fig12ad', figure={}, style = {'display' : 'none'}), # per season graph
    html.Br(),
    dcc.Dropdown(id='drop12', options=[], placeholder='Select Opponent Team', clearable=False),
    dcc.Graph(id='fig13a', figure={}, style = {'display' : 'none'}), # per team per season graph
    dcc.Graph(id='fig13ab', figure={}, style = {'display' : 'none'}), # per team per season graph
    dcc.Graph(id='fig14a', figure={}, style = {'display' : 'none'}), # per team ovr graph
    dcc.Graph(id='fig14ab', figure={}, style = {'display' : 'none'}), # per team ovr graph
    dcc.Link('Go back to home', href='/'),
])
@app.callback(
    Output('datatable-interactivity21', 'style_data_conditional'),
    Input('datatable-interactivity21', 'selected_columns')
)
def update_styles(selected_columns):
    if selected_columns is None:
        raise PreventUpdate
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]

@app.callback(
    Output('datatable-interactivity-container21', "children"),
    Input('datatable-interactivity21', "derived_virtual_data"),
    Input('datatable-interactivity21', "derived_virtual_selected_rows"))
def update_graphs(rows, derived_virtual_selected_rows):
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    dff1 = team_ovr if rows is None else pd.DataFrame(rows)

    colors = ['#7FDBFF' if i in derived_virtual_selected_rows else '#0074D9'
              for i in range(len(dff1))]

    return [
        dcc.Graph(
            id=column,
            figure={
                "data": [
                    {
                        "x": dff1["Team"],
                        "y": dff1[column],
                        "type": "bar",
                        "marker": {"color": colors},
                    }
                ],
                "layout": {
                    "xaxis": {"automargin": True},
                    "yaxis": {
                        "automargin": True,
                        "title": {"text": column}
                    },
                    "height": 250,
                    "margin": {"t": 10, "l": 10, "r": 10},
                },
            },
        )
        for column in ['Runs', 'Seasons played', 'Matches played', 'Strike rate', 'Sixes', 'Fours', '50s', '100s'] if column in dff1
    ]


@app.callback(
    Output(component_id='drop12', component_property='options'),
    Output(component_id='fig10a', component_property='style'),
    Output(component_id='fig10a', component_property='figure'),
    Output(component_id='fig12a', component_property='style'),
    Output(component_id='fig12a', component_property='figure'),
    Output(component_id='fig12ab', component_property='style'),
    Output(component_id='fig12ab', component_property='figure'),
    Output(component_id='fig12ac', component_property='style'),
    Output(component_id='fig12ac', component_property='figure'),
    Output(component_id='fig12ad', component_property='style'),
    Output(component_id='fig12ad', component_property='figure'),
    Input(component_id='drop11', component_property='value')
)
def after_dd1(value21):
    if value21 is None:
        raise PreventUpdate
    else:
        twps1 = twps[twps['Team'] == value21]
        if value21 is None or twps1.empty:
            raise PreventUpdate
        else:
            d11 = team_runs_per_season[team_runs_per_season['Team'] == value21]
            d12 = tptovr[tptovr['Team'] == value21]
            d12_list = d12['Opponent Team'].unique()
            fig10 = px.bar(data_frame=twps1, x='Season', y='Wins', title='Wins per season')
            fig12 = px.bar(data_frame=d11, x='Season', y='Batsman runs', title='Runs per season')
            fig12b = px.bar(data_frame=d11, x='Season', y='Boundaries', title='Boundaries per season')
            fig12c = px.bar(data_frame=d11, x='Season', y='Total runs scored', title='Total runs per season')
            fig12d = px.bar(data_frame=d11, x='Season', y='Win %', title='Win % per season')####
            return [{'label': d, 'value': d} for d in sorted(d12_list)], {'display' : 'block'},  fig10, {'display' : 'block'},  fig12, {'display' : 'block'},  \
                   fig12b, {'display' : 'block'},  fig12c, {'display' : 'block'},  fig12d

@app.callback(
    Output(component_id='fig13a', component_property='style'),
    Output(component_id='fig13a', component_property='figure'),
    Output(component_id='fig13ab', component_property='style'),
    Output(component_id='fig13ab', component_property='figure'),
    Output(component_id='fig14a', component_property='style'),
    Output(component_id='fig14a', component_property='figure'),
    Output(component_id='fig14ab', component_property='style'),
    Output(component_id='fig14ab', component_property='figure'),
    Input(component_id='drop12', component_property='value')
)
def after_dd2(value1):
    if value1 is None:
        raise PreventUpdate
    else:
        d13 = tptovr[tptovr['Opponent Team'] == value1] # per team ovr bat
        d14 = tptps[tptps['Team'] == value1] # per team per season bat
        d15 = tptovr_bow[tptovr_bow['Opponent team'] == value1]  # per team ovr bowl
        d16 = tptps_bow[tptps_bow['Opponent team'] == value1]  # per team per season bowl
        if d13.empty or d14.empty or d15.empty or d16.empty:
            raise PreventUpdate
        else:
            fig13 = px.bar(data_frame=d13, x='Opponent Team', y=['Batsman runs', '4s', '6s', 'Total runs'], title='Runs per team overall')
            fig13a = px.bar(data_frame=d14, x='Season', y=['Batsman runs', '4s', '6s', 'Total runs', 'Win %'], title='Strike rate per team overall')
            fig14 = px.bar(data_frame=d15, x='Opponent team', y='Wickets taken', title='Runs per team per season')
            fig14a = px.bar(data_frame=d16, x='Season', y='Wickets taken', title='Strike rate per team overall')
            return {'display' : 'block'}, fig13, {'display' : 'block'}, fig13a, {'display' : 'block'}, fig14,\
                   {'display' : 'block'}, fig14a


#############################################################################################################

# Batsman

page_2_layout = html.Div([
    html.H1("Batsman"),
    html.Br(),
    dash_table.DataTable(
        id='datatable-interactivity2',
        columns=[
            {"name": i, "id": i, "deletable": True, "selectable": True} for i in batsman_overall_db.columns
        ],
        data=batsman_overall_db.to_dict('records'),
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_selectable="multi",
        row_deletable=True,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current=0,
        page_size=10,
    ),
    html.Br(),
    html.Br(),
    html.Div(id='datatable-interactivity-container2'),
    html.Br(),
    html.H5("Textarea is case sensitive!"),
    dcc.Textarea(id='text21', value='', style={'width': '25%', 'height': 50},),
    html.Br(),
    dcc.Graph(id='fig22a', figure={}, style = {'display' : 'none'}), # per season graph
    html.Br(),
    dcc.Graph(id='fig22ab', figure={}, style = {'display' : 'none'}), # per season graph
    html.Br(),
    dcc.Graph(id='fig22ac', figure={}, style = {'display' : 'none'}), # per season graph
    html.Br(),
    dcc.Graph(id='fig22ad', figure={}, style = {'display' : 'none'}), # per season graph
    html.Br(),
    dcc.Dropdown(id='drop21', options=[], placeholder='Select Team', clearable=False),
    dcc.Graph(id='fig23a', figure={}, style = {'display' : 'none'}), # per team per season graph
    dcc.Graph(id='fig23ab', figure={}, style = {'display' : 'none'}), # per team per season graph
    dcc.Graph(id='fig24a', figure={}, style = {'display' : 'none'}), # per team ovr graph
    dcc.Graph(id='fig24ab', figure={}, style = {'display' : 'none'}), # per team ovr graph
    dcc.Link('Go back to home', href='/'),
])
@app.callback(
    Output('datatable-interactivity2', 'style_data_conditional'),
    Input('datatable-interactivity2', 'selected_columns')
)
def update_styles(selected_columns):
    if selected_columns is None:
        raise PreventUpdate
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]

@app.callback(
    Output('datatable-interactivity-container2', "children"),
    Input('datatable-interactivity2', "derived_virtual_data"),
    Input('datatable-interactivity2', "derived_virtual_selected_rows"))
def update_graphs(rows, derived_virtual_selected_rows):
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    dff2 = batsman_overall_db if rows is None else pd.DataFrame(rows)

    colors = ['#7FDBFF' if i in derived_virtual_selected_rows else '#0074D9'
              for i in range(len(dff2))]

    return [
        dcc.Graph(
            id=column,
            figure={
                "data": [
                    {
                        "x": dff2["Name"],
                        "y": dff2[column],
                        "type": "bar",
                        "marker": {"color": colors},
                    }
                ],
                "layout": {
                    "xaxis": {"automargin": True},
                    "yaxis": {
                        "automargin": True,
                        "title": {"text": column}
                    },
                    "height": 250,
                    "margin": {"t": 10, "l": 10, "r": 10},
                },
            },
        )
        for column in ['Runs', 'Seasons played', 'Matches played', 'Strike rate', 'Sixes', 'Fours', '50s', '100s'] if column in dff2
    ]


@app.callback(
    Output(component_id='drop21', component_property='options'),
    Output(component_id='fig22a', component_property='style'),
    Output(component_id='fig22a', component_property='figure'),
    Output(component_id='fig22ab', component_property='style'),
    Output(component_id='fig22ab', component_property='figure'),
    Output(component_id='fig22ac', component_property='style'),
    Output(component_id='fig22ac', component_property='figure'),
    Output(component_id='fig22ad', component_property='style'),
    Output(component_id='fig22ad', component_property='figure'),
    Input(component_id='text21', component_property='value')
)
def after_text(value2):
    if value2 is None:
        raise PreventUpdate
    else:
        d21 = batsman_per_season[batsman_per_season['Name'] == value2]
        d22 = bt_pt_ovr[bt_pt_ovr['Name'] == value2]
        d22_list = d22['Opponent team'].unique()
        fig22 = px.bar(data_frame=d21, x='Season', y='Runs', title='Runs per season')
        fig22b = px.bar(data_frame=d21, x='Season', y='Strike rate', title='Strike rate per season')
        fig22c = px.bar(data_frame=d21, x='Season', y='Boundaries', title='Boundaries per season')
        fig22d = px.bar(data_frame=d21, x='Season', y='Team runs contribution(in %)', title='Team contribution per season')####
        return [{'label': d, 'value': d} for d in sorted(d22_list)],{'display' : 'block'},  fig22, {'display' : 'block'},  \
               fig22b, {'display' : 'block'},  fig22c, {'display' : 'block'},  fig22d

@app.callback(
    Output(component_id='fig23a', component_property='style'),
    Output(component_id='fig23a', component_property='figure'),
    Output(component_id='fig23ab', component_property='style'),
    Output(component_id='fig23ab', component_property='figure'),
    Output(component_id='fig24a', component_property='style'),
    Output(component_id='fig24a', component_property='figure'),
    Output(component_id='fig24ab', component_property='style'),
    Output(component_id='fig24ab', component_property='figure'),
    Input(component_id='drop21', component_property='value')
)
def after_dd(value1):
    if value1 is None:
        raise PreventUpdate
    else:
        d23 = bt_pt_ovr[bt_pt_ovr['Opponent team'] == value1] # per team ov3
        d24 = b_pt_ps[b_pt_ps['Opponent team'] == value1] # per team per season
        if d23.empty or d24.empty:
            raise PreventUpdate
        else:
            fig23 = px.bar(data_frame=d23, x='Batsman runs', y='Opponent team', title='Runs per team overall')
            fig23a = px.bar(data_frame=d23, x='Strike rate', y='Opponent team', title='Strike rate per team overall')
            fig24 = px.bar(data_frame=d24, x='Season', y='Batsman runs', title='Runs per team per season')
            fig24a = px.bar(data_frame=d24, x='Season', y='Strike Rate', title='Strike rate per team overall')
            return {'display' : 'block'}, fig23, {'display' : 'block'}, fig23a, {'display' : 'block'}, fig24, {'display' : 'block'}, fig24a


###########################################################################################################

# Bowler

page_3_layout = html.Div([
    html.H1("Bowler"),
    html.Br(),
    dash_table.DataTable(
        id='datatable-interactivity3',
        columns=[
            {"name": i, "id": i, "deletable": True, "selectable": True} for i in bowler_overall.columns
        ],
        data=bowler_overall.to_dict('records'),
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_selectable="multi",
        row_deletable=True,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current=0,
        page_size=10,
    ),
    html.Br(),
    html.Br(),
    html.Div(id='datatable-interactivity-container3'),
    html.Br(),
    html.H5("Textarea is case sensitive!"),
    dcc.Textarea(id='text31', value='', style={'width': '25%', 'height': 50},),
    html.Br(),
    dcc.Graph(id='fig32a', figure={}, style = {'display' : 'none'}), # per season graph
    html.Br(),
    dcc.Graph(id='fig32ab', figure={}, style = {'display' : 'none'}), # per season graph
    html.Br(),
    dcc.Graph(id='fig32ac', figure={}, style = {'display' : 'none'}), # per season graph
    html.Br(),
    dcc.Dropdown(id='drop31', options=[], placeholder='Select Team', clearable=False),
    dcc.Graph(id='fig33a', figure={}, style = {'display' : 'none'}), # per team per season graph
    dcc.Graph(id='fig34a', figure={}, style = {'display' : 'none'}), # per team ovr graph
    dcc.Link('Go back to home', href='/'),
])
@app.callback(
    Output('datatable-interactivity3', 'style_data_conditional'),
    Input('datatable-interactivity3', 'selected_columns')
)
def update_styles(selected_columns):
    if selected_columns is None:
        raise PreventUpdate
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]

@app.callback(
    Output('datatable-interactivity-container3', "children"),
    Input('datatable-interactivity3', "derived_virtual_data"),
    Input('datatable-interactivity3', "derived_virtual_selected_rows"))
def update_graphs(rows, derived_virtual_selected_rows):
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    dff3 = bowler_overall if rows is None else pd.DataFrame(rows)

    colors = ['#7FDBFF' if i in derived_virtual_selected_rows else '#0074D9'
              for i in range(len(dff3))]

    return [
        dcc.Graph(
            id=column,
            figure={
                "data": [
                    {
                        "x": dff3["Bowler"],
                        "y": dff3[column],
                        "type": "bar",
                        "marker": {"color": colors},
                    }
                ],
                "layout": {
                    "xaxis": {"automargin": True},
                    "yaxis": {
                        "automargin": True,
                        "title": {"text": column}
                    },
                    "height": 250,
                    "margin": {"t": 10, "l": 10, "r": 10},
                },
            },
        )
        for column in ['Wickets', 'Seasons played', 'Matches played', 'Economy', 'Team_contribution(in %)'] if column in dff3
    ]


@app.callback(
    Output(component_id='drop31', component_property='options'),
    Output(component_id='fig32a', component_property='style'),
    Output(component_id='fig32a', component_property='figure'),
    Output(component_id='fig32ab', component_property='style'),
    Output(component_id='fig32ab', component_property='figure'),
    Output(component_id='fig32ac', component_property='style'),
    Output(component_id='fig32ac', component_property='figure'),
    Input(component_id='text31', component_property='value')
)
def after_text(value):
    if value is None:
        raise PreventUpdate
    else:
        d31 = bowler_per_season[bowler_per_season['Bowler'] == value]
        d32 = bow_pt_ovr[bow_pt_ovr['Name'] == value]
        d32_list = d32['Opponent team'].unique()
        fig32 = px.bar(data_frame=d31, x='Season', y='Wickets', title='Wickets per season')
        fig32b = px.bar(data_frame=d31, x='Season', y='Economy', title='Economy per season')
        fig32c = px.bar(data_frame=d31, x='Season', y='Team_contribution(in %)', title='Team contribution per season')####
        return [{'label': d, 'value': d} for d in sorted(d32_list)],{'display' : 'block'},  fig32, {'display' : 'block'},  \
               fig32b, {'display' : 'block'},  fig32c

@app.callback(
    Output(component_id='fig33a', component_property='style'),
    Output(component_id='fig33a', component_property='figure'),
    Output(component_id='fig34a', component_property='style'),
    Output(component_id='fig34a', component_property='figure'),
    Input(component_id='drop31', component_property='value')
)
def after_dd(value1):
    if value1 is None:
        raise PreventUpdate
    else:
        d33 = bow_pt_ovr[bow_pt_ovr['Opponent team'] == value1] # per team ov3
        d34 = bow_pt_ps[bow_pt_ps['Opponent team'] == value1] # per team per season
        if d33.empty or d34.empty:
            raise PreventUpdate
        else:
            fig33 = px.bar(data_frame=d33, x='Wickets', y='Opponent team', title='Wickets per team overall')
            fig34 = px.bar(data_frame=d34, x='Season', y='Wickets', title='Wickets per team per season')
            return {'display' : 'block'}, fig33, {'display' : 'block'}, fig34

###########################################################################################################

# fielder

page_4_layout = html.Div([
    html.H1("Fielder"),
    html.Br(),
    dash_table.DataTable(
        id='datatable-interactivity4',
        columns=[
            {"name": i, "id": i, "deletable": True, "selectable": True} for i in f_ovr.columns
        ],
        data=f_ovr.to_dict('records'),
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_selectable="multi",
        row_deletable=True,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current=0,
        page_size=10,
    ),
    html.Br(),
    html.Br(),
    html.Div(id='datatable-interactivity-container4'),
    html.Br(),
    html.H5("Textarea is case sensitive!"),
    dcc.Textarea(id='text41', value='', style={'width': '25%', 'height': 50},),
    html.Br(),
    dcc.Graph(id='fig42a', figure={}, style = {'display' : 'none'}), # per season graph
    html.Br(),
    dcc.Dropdown(id='drop41', options=[], placeholder='Select Team', clearable=False),
    dcc.Graph(id='fig43a', figure={}, style = {'display' : 'none'}), # per team per season graph
    dcc.Graph(id='fig44a', figure={}, style = {'display' : 'none'}), # per team ovr graph
    dcc.Link('Go back to home', href='/'),
])
@app.callback(
    Output('datatable-interactivity4', 'style_data_conditional'),
    Input('datatable-interactivity4', 'selected_columns')
)
def update_styles(selected_columns):
    if selected_columns is None:
        raise PreventUpdate
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]

@app.callback(
    Output('datatable-interactivity-container4', "children"),
    Input('datatable-interactivity4', "derived_virtual_data"),
    Input('datatable-interactivity4', "derived_virtual_selected_rows"))
def update_graphs(rows, derived_virtual_selected_rows):
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    dff4 = f_ovr if rows is None else pd.DataFrame(rows)

    colors = ['#7FDBFF' if i in derived_virtual_selected_rows else '#0074D9'
              for i in range(len(dff4))]

    return [
        dcc.Graph(
            id=column,
            figure={
                "data": [
                    {
                        "x": dff4["Name"],
                        "y": dff4[column],
                        "type": "bar",
                        "marker": {"color": colors},
                    }
                ],
                "layout": {
                    "xaxis": {"automargin": True},
                    "yaxis": {
                        "automargin": True,
                        "title": {"text": column}
                    },
                    "height": 250,
                    "margin": {"t": 10, "l": 10, "r": 10},
                },
            },
        )
        for column in ["Wickets"] if column in dff4
    ]


@app.callback(
    Output(component_id='drop41', component_property='options'),
    Output(component_id='fig42a', component_property='style'),
    Output(component_id='fig42a', component_property='figure'),
    Input(component_id='text41', component_property='value')
)
def after_text(value):
    if value is None:
        raise PreventUpdate
    else:
        d41 = f_ps[f_ps['Name'] == value]
        d42 = f_pt_ovr[f_pt_ovr['Name'] == value]
        d42_list = d42['Opponent team'].unique()
        fig42 = px.bar(data_frame=d41, x='Season', y='Wickets', title='Wickets per season')
        return [{'label': d, 'value': d} for d in sorted(d42_list)],{'display' : 'block'},  fig42

@app.callback(
    Output(component_id='fig43a', component_property='style'),
    Output(component_id='fig43a', component_property='figure'),
    Output(component_id='fig44a', component_property='style'),
    Output(component_id='fig44a', component_property='figure'),
    Input(component_id='drop41', component_property='value')
)
def after_dd(value1):
    if value1 is None:
        raise PreventUpdate
    else:
        d43 = f_pt_ovr[f_pt_ovr['Opponent team'] == value1] # per team ovr
        d44 = f_pt_ps[f_pt_ps['Opponent team'] == value1] # per team per season
        if d43.empty or d44.empty:
            raise PreventUpdate
        else:
            fig43 = px.bar(data_frame=d43, x='Wickets', y='Opponent team', title='Wickets per team overall')
            fig44 = px.bar(data_frame=d44, x='Season', y='Wickets', title='Wickets per team per season')
            return {'display' : 'block'}, fig43, {'display' : 'block'}, fig44



###########################################################################################################

# wicket-keeper

page_5_layout = html.Div([
    html.H1("Wicket-keeper"),
    html.Br(),
    dash_table.DataTable(
        id='datatable-interactivity5',
        columns=[
            {"name": i, "id": i, "deletable": True, "selectable": True} for i in wk_ovr.columns
        ],
        data=wk_ovr.to_dict('records'),
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_selectable="multi",
        row_deletable=True,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current=0,
        page_size=10,
    ),
    html.Br(),
    html.Br(),
    html.Div(id='datatable-interactivity-container5'),
    html.Br(),
    html.H5("Textarea is case sensitive!"),
    dcc.Textarea(id='text51', value='', style={'width': '25%', 'height': 50},),
    html.Br(),
    dcc.Graph(id='fig52a', figure={}, style = {'display' : 'none'}), # per season graph
    html.Br(),
    dcc.Dropdown(id='drop51', options=[], placeholder='Select Team', clearable=False),
    dcc.Graph(id='fig53a', figure={}, style = {'display' : 'none'}), # per team per season graph
    dcc.Graph(id='fig54a', figure={}, style = {'display' : 'none'}), # per team ovr graph
    dcc.Link('Go back to home', href='/'),
])
@app.callback(
    Output('datatable-interactivity5', 'style_data_conditional'),
    Input('datatable-interactivity5', 'selected_columns')
)
def update_styles(selected_columns):
    if selected_columns is None:
        raise PreventUpdate
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]

@app.callback(
    Output('datatable-interactivity-container5', "children"),
    Input('datatable-interactivity5', "derived_virtual_data"),
    Input('datatable-interactivity5', "derived_virtual_selected_rows"))
def update_graphs(rows, derived_virtual_selected_rows):
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    dff5 = wk_ovr if rows is None else pd.DataFrame(rows)

    colors = ['#7FDBFF' if i in derived_virtual_selected_rows else '#0074D9'
              for i in range(len(dff5))]

    return [
        dcc.Graph(
            id=column,
            figure={
                "data": [
                    {
                        "x": dff5["Name"],
                        "y": dff5[column],
                        "type": "bar",
                        "marker": {"color": colors},
                    }
                ],
                "layout": {
                    "xaxis": {"automargin": True},
                    "yaxis": {
                        "automargin": True,
                        "title": {"text": column}
                    },
                    "height": 250,
                    "margin": {"t": 10, "l": 10, "r": 10},
                },
            },
        )
        for column in ["Wickets"] if column in dff5
    ]


@app.callback(
    Output(component_id='drop51', component_property='options'),
    Output(component_id='fig52a', component_property='style'),
    Output(component_id='fig52a', component_property='figure'),
    Input(component_id='text51', component_property='value')
)
def after_text(value):
    if value is None:
        raise PreventUpdate
    else:
        d51 = wk_ps[wk_ps['Name'] == value]
        d52 = wk_pt_ovr[wk_pt_ovr['Name'] == value]
        d52_list = d52['Opponent team'].unique()
        fig52 = px.bar(data_frame=d51, x='Season', y='Wickets', title='Wickets per season')
        return [{'label': d, 'value': d} for d in sorted(d52_list)],{'display' : 'block'},  fig52

@app.callback(
    Output(component_id='fig53a', component_property='style'),
    Output(component_id='fig53a', component_property='figure'),
    Output(component_id='fig54a', component_property='style'),
    Output(component_id='fig54a', component_property='figure'),
    Input(component_id='drop51', component_property='value')
)
def after_dd(value1):
    if value1 is None:
        raise PreventUpdate
    else:
        d53 = wk_pt_ovr[wk_pt_ovr['Opponent team'] == value1] # per team ovr
        d54 = wk_pt_ps[wk_pt_ps['Opponent team'] == value1] # per team per season
        if d53.empty or d54.empty:
            raise PreventUpdate
        else:
            fig53 = px.bar(data_frame=d53, x='Wickets', y='Opponent team', title='Wickets per team overall')
            fig54 = px.bar(data_frame=d54, x='Season', y='Wickets', title='Wickets per team per season')
            return {'display' : 'block'}, fig53, {'display' : 'block'}, fig54


###########################################################################################################

# match

page_6_layout = html.Div([
    html.H1("Match-wise"),
    dcc.Slider(id='my-slider',
               min=pd_for_matches['season'].min(),
               max=pd_for_matches['season'].max(),
               value=pd_for_matches['season'].min(),
               marks={str(year): str(year) for year in pd_for_matches['season'].unique()},
               step=None
               ),
    dcc.Dropdown(id='my-team1', options=[],
                 #value='Mumbai Indians',
                 placeholder='Select Team',
                 clearable=False
                 ),
    dash_table.DataTable(id='my-table', columns=[{"name": i, "id": i} for i in pd_for_matches.columns],
                         data=pd_for_matches.to_dict('records'),
                         # editable=True,
                         filter_action="native",
                         sort_action="native",
                         sort_mode="multi",
                         column_selectable="single",
                         row_selectable="single",
                         # row_deletable=True,
                         selected_columns=[],
                         selected_rows=[],
                         page_action="native",
                         page_current=0,
                         page_size=20,
                         virtualization=True,
                         style_cell={
                             'minWidth':95, 'maxWidth':95, 'width':95
                         },
                         style_data={
                             'whiteSpace': 'normal',
                             'height': 'auto'
                         },
                         ),
    html.Div(id='hidden-div_for_dt', style={'display':'none'}),
    html.Br(),
    html.Br(),
    html.Div(id='winner'),
    html.Br(),
    html.Div(id='motm'),
    html.Label(id='my-label'),
    dcc.Graph(id='my-graph', figure={}, style={'display' : 'none'}), # working
    dcc.Graph(id='team1-bat', figure={}, style={'display' : 'none'}), # , responsive= 'auto'
    dcc.Graph(id='team1-bowl', figure={}, style={'display' : 'none'}),
    dcc.Graph(id='team2-bat', figure={}, style={'display' : 'none'}), # , responsive= 'auto'
    dcc.Graph(id='team2-bowl', figure={}, style={'display' : 'none'}),
    dcc.Graph(id='for_rpo', figure={}, style={'display' : 'none'}),
    dcc.Graph(id='wicket_graph', figure={}, style={'display' : 'none'}),
    dcc.Graph(id='wicket_graph1', figure={}, style={'display' : 'none'}),
    html.H5("Team1 batting:"),
    dash_table.DataTable(id='team1_bat',columns =  [{"name": i, "id": i,} for i in for_op_df_bat.columns]),
    html.H5("Team1 bowling:"),
    dash_table.DataTable(id='team1_bowl',columns =  [{"name": i, "id": i,} for i in for_op_df_bowl.columns]),
    html.H5("Team2 batting:"),
    dash_table.DataTable(id='team2_bat',columns =  [{"name": i, "id": i,} for i in for_op_df_bat.columns]),
    html.H5("Team2 bowling:"),
    dash_table.DataTable(id='team2_bowl',columns =  [{"name": i, "id": i,} for i in for_op_df_bowl.columns]),
    dcc.Link('Go back to home', href='/'),
])

# first callback will be for slider
@app.callback(
    Output(component_id='my-team1', component_property='options'), # to dd1
    Output(component_id='hidden-div_for_dt', component_property='children'),
    Input(component_id='my-slider', component_property='value') # from slider
)
def from_slider(value):
    dff12 = pd_for_matches[pd_for_matches.season == value]
    a = dff12['team1'].unique()
    b = [x for x in a if str(x) != 'nan']
    return [{'label': d, 'value': d} for d in sorted(b)], dff12.to_json(date_format='iso', orient='split')

# second callback for team select and dt display
@app.callback(
    Output(component_id='my-table', component_property='data'),
    Input(component_id='hidden-div_for_dt', component_property='children'), # from json saved dt
    Input(component_id='my-team1',component_property='value') # from dd1 selected value
)
def from_dd1(jsonified_dff, value1):
    dff1 = pd.read_json(jsonified_dff, orient='split') # importing saved dt
    dff2 = dff1[dff1.team1 == value1]
    dff3 = dff1[dff1.team2 == value1]
    total = [dff2, dff3]
    result = pd.concat(total).reset_index(drop=True)
    return result.to_dict('records')

@app.callback(
    Output(component_id='winner', component_property='children'),
    Output(component_id='motm', component_property='children'),
    Output(component_id='my-graph', component_property='style'),
    Output(component_id='my-graph', component_property='figure'),
    Output(component_id='team1-bat', component_property='style'),
    Output(component_id='team1-bat', component_property='figure'),
    Output(component_id='team1-bowl', component_property='style'),
    Output(component_id='team1-bowl', component_property='figure'),
    Output(component_id='team2-bat', component_property='style'),
    Output(component_id='team2-bat', component_property='figure'),
    Output(component_id='team2-bowl', component_property='style'),
    Output(component_id='team2-bowl', component_property='figure'),
    Output(component_id='for_rpo', component_property='style'),
    Output(component_id='for_rpo', component_property='figure'),
    Output(component_id='wicket_graph', component_property='style'),
    Output(component_id='wicket_graph', component_property='figure'),
    Output(component_id='wicket_graph1', component_property='style'),
    Output(component_id='wicket_graph1', component_property='figure'),
    Output(component_id='team1_bat', component_property='data'),
    Output(component_id='team1_bowl', component_property='data'),
    Output(component_id='team2_bat', component_property='data'),
    Output(component_id='team2_bowl', component_property='data'),
    Input(component_id='my-table', component_property='selected_row_ids')
)
def print_id(selected_row_ids):
    if selected_row_ids is None:
        raise PreventUpdate
    elif selected_row_ids != 0:
        g = pd_for_matches[pd_for_matches['id'] == selected_row_ids[0]].reset_index(drop=True)
        # h = data2[data2['match_id'] == selected_row_ids[0]].reset_index(drop=True)
        x15 = over_wise(selected_row_ids[0])[0]
        y15 = over_wise(selected_row_ids[0])[1]
        x1 = over_wise(selected_row_ids[0])[0]
        y1 = over_wise(selected_row_ids[0])[2]
        op = pd.DataFrame({'Overs': x15,
                           over_wise(selected_row_ids[0])[3]: y15,
                           'Team2 O' : x1,
                           over_wise(selected_row_ids[0])[4] : y1
        })

        team1_bat = pd.DataFrame({'Batsman': over_wise(selected_row_ids[0])[5],
                                  'Runs' : over_wise(selected_row_ids[0])[6]
                                 })
        team1_bow = pd.DataFrame({'Bowler' : over_wise(selected_row_ids[0])[7],
                                  'Wickets' : over_wise(selected_row_ids[0])[8]
                                 })
        team2_bat = pd.DataFrame({'Batsman' : over_wise(selected_row_ids[0])[9],
                                  'Runs' : over_wise(selected_row_ids[0])[10]
                                 })
        team2_bow = pd.DataFrame({'Bowler' : over_wise(selected_row_ids[0])[11],
                                  'Wickets' : over_wise(selected_row_ids[0])[12]
                                 })

        for_runs_per_over = pd.DataFrame({'Overs' : over_wise(selected_row_ids[0])[0],
                                          over_wise(selected_row_ids[0])[3] : over_wise(selected_row_ids[0])[13],
                                          over_wise(selected_row_ids[0])[4] : over_wise(selected_row_ids[0])[14]
                                          })

        wicket_graph = pd.DataFrame({'over.ball' : over_wise(selected_row_ids[0])[15],
                                     'Runs': over_wise(selected_row_ids[0])[16],
                                    })

        wicket_graph1 = pd.DataFrame({'over.ball': over_wise(selected_row_ids[0])[17],
                                     'Runs': over_wise(selected_row_ids[0])[18],
                                     })

        team1_bat1 = pd.DataFrame({'Batsmen' : over_wise(selected_row_ids[0])[19][0],
                                  'Six' : over_wise(selected_row_ids[0])[19][1],
                                  'Four' : over_wise(selected_row_ids[0])[19][2],
                                  'Total_runs' : over_wise(selected_row_ids[0])[19][3],
                                  'Total_balls_faced' : over_wise(selected_row_ids[0])[19][4],
                                  'Strike_rate' : over_wise(selected_row_ids[0])[19][5],
        })

        team1_bowl1 = pd.DataFrame({'Bowler' : over_wise(selected_row_ids[0])[22][0],
                                    'Overs' : over_wise(selected_row_ids[0])[22][1],
                                    'Wickets' : over_wise(selected_row_ids[0])[22][2],
                                    'Total_runs' : over_wise(selected_row_ids[0])[22][3],
                                    'Extra_runs' : over_wise(selected_row_ids[0])[22][4],
                                    'Economy' : over_wise(selected_row_ids[0])[22][5],
        })

        team2_bat1 = pd.DataFrame({'Batsmen': over_wise(selected_row_ids[0])[20][0],
                                  'Six' : over_wise(selected_row_ids[0])[20][1],
        'Four' : over_wise(selected_row_ids[0])[20][2],
        'Total_runs' : over_wise(selected_row_ids[0])[20][3],
        'Total_balls_faced' : over_wise(selected_row_ids[0])[20][4],
        'Strike_rate' : over_wise(selected_row_ids[0])[20][5],
        })

        team2_bowl1 = pd.DataFrame({'Bowler': over_wise(selected_row_ids[0])[21][0],
                                   'Overs' : over_wise(selected_row_ids[0])[21][1],
        'Wickets' : over_wise(selected_row_ids[0])[21][2],
        'Total_runs' : over_wise(selected_row_ids[0])[21][3],
        'Extra_runs' : over_wise(selected_row_ids[0])[21][4],
        'Economy' : over_wise(selected_row_ids[0])[21][5],
        })

        fig = px.line(data_frame=op, x='Overs', y=[over_wise(selected_row_ids[0])[3], over_wise(selected_row_ids[0])[4]], title='Runs per over', labels={'Teams' : [over_wise(selected_row_ids[0])[3], over_wise(selected_row_ids[0])[4]]}) # , template='plotly_dark'
        fig51 = px.bar(data_frame=for_runs_per_over, x='Overs', y=[over_wise(selected_row_ids[0])[13], over_wise(selected_row_ids[0])[14]],
                      title='Runs per over', barmode='group', labels=[over_wise(selected_row_ids[0])[3], over_wise(selected_row_ids[0])[4]])
        fig52 = px.scatter(data_frame=wicket_graph, x='over.ball', y='Runs', title=(str(over_wise(selected_row_ids[0])[3]))+' fall of wickets', size = 'over.ball')
        fig53 = px.scatter(data_frame=wicket_graph1, x='over.ball', y='Runs', title=(str(over_wise(selected_row_ids[0])[4]))+' fall of wickets', size = 'over.ball')
        fig54 = px.pie(data_frame=team1_bat, values=team1_bat['Runs'], names=team1_bat['Batsman'], hole=.6, title= str(g['team1'][0])+' Batting:') # for team1 bat
        fig55 = px.pie(data_frame=team1_bow, values=team1_bow['Wickets'], names=team1_bow['Bowler'], hole=.6, title= str(g['team1'][0])+' Bowling:') # for team1 bowl
        fig56 = px.pie(data_frame=team2_bat, values=team2_bat['Runs'], names=team2_bat['Batsman'], hole=.6, title= str(g['team2'][0])+' Batting:')  # for team2 bat
        fig57 = px.pie(data_frame=team2_bow, values=team2_bow['Wickets'], names=team2_bow['Bowler'], hole=.6, title= str(g['team2'][0])+' Bowling:')  # for team2 bowl

        return winner(selected_row_ids[0]), 'Man Of The Match: '+str(motm(selected_row_ids[0])), {'display' : 'block'}, fig, {'display' : 'block'}, fig51, {'display' : 'block'}, fig52, {'display' : 'block'}, \
               fig53, {'display' : 'block'}, fig54, {'display' : 'block'}, fig55, {'display' : 'block'}, fig56, {'display' : 'block'}, \
               fig57, team1_bat1.to_dict('records'), team1_bowl1.to_dict('records'), team2_bat1.to_dict('records'), team2_bowl1.to_dict('records')

#####################################################################################################

# points table

page_7_layout = html.Div([
    html.H1("IPL Points Table"),
    dcc.Slider(id='for-year',
               min=pd_for_matches['season'].min(),
               max=pd_for_matches['season'].max(),
               value=pd_for_matches['season'].min(),
               marks={str(year): str(year) for year in pd_for_matches['season'].unique()},
               step=None
                ),
    html.Br(),
    dash_table.DataTable(id='for-pt',columns =  [{"name": i, "id": i,} for i in for_points_table.columns]),
    html.Br(),
    dcc.Link('Go back to home', href='/'),
])

@app.callback(
    Output(component_id='for-pt', component_property='data'),
    Input(component_id='for-year', component_property='value')
)
def for_points_table(slider_value):
    return league_table(slider_value).to_dict('records')

#############################################################################################################

# venue

fig81 = px.bar(data_frame=va_df, x='Venue', y='No. of matches', title='No. of matches in venues')

fig82 = px.bar(data_frame=va_df, x='Venue', y=['Field %', 'Bat %'], title='Toss decision %', barmode='group')

fig83 = px.bar(data_frame=va_df, x='Venue', y='Toss win match win %', title='Toss winner winning match %')

fig84 = px.bar(data_frame=va_df, x='Venue', y='No. of wins', title='Most winning team in venues',
       hover_name='Most winning team')

page_8_layout = html.Div([
    html.H1("Venue Analysis"),
    dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i} for i in va_df.columns
        ],
        data=va_df.to_dict('records'),
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        page_action="native",
        page_current= 0,
        page_size= 10,
    ),
    html.Br(),
    html.Br(),
    dcc.Graph(id='fig81', figure=fig81),
    html.Br(),
    dcc.Graph(id='fig82', figure=fig82),
    html.Br(),
    dcc.Graph(id='fig83', figure=fig83),
    html.Br(),
    dcc.Graph(id='fig84', figure=fig84),
    html.Br(),
    dcc.Link('Go back to home', href='/'),
])

#############################################################################################################

# toss

fig91 = px.bar(data_frame=ta_df, x='Team', y='Toss wins', title='Toss won')

fig92 = px.bar(data_frame=ta_df, x='Team', y=['Field %', 'Bat %'], title='Toss decision %', barmode='group')

fig93 = px.bar(data_frame=ta_df, x='Team', y='Toss win match win %', title='Toss winner winning match %')


page_9_layout = html.Div([
    html.H1("Toss Analysis"),
    dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i} for i in ta_df.columns
        ],
        data=ta_df.to_dict('records'),
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        page_action="native",
        page_current= 0,
        page_size= 10,
    ),
    html.Br(),
    html.Br(),
    dcc.Graph(id='fig91', figure=fig91),
    html.Br(),
    dcc.Graph(id='fig92', figure=fig92),
    html.Br(),
    dcc.Graph(id='fig93', figure=fig93),
    html.Br(),
    dcc.Link('Go back to home', href='/'),
])



#############################################################################################################

# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    elif pathname == '/page-3':
        return page_3_layout
    elif pathname == '/page-4':
        return page_4_layout
    elif pathname == '/page-5':
        return page_5_layout
    elif pathname == '/page-6':
        return page_6_layout
    elif pathname == '/page-7':
        return page_7_layout
    elif pathname == '/page-8':
        return page_8_layout
    elif pathname == '/page-9':
        return page_9_layout
    else:
        return index_page
    # You could also return a 404 "URL not found" page here


if __name__ == '__main__':
    app.run_server(debug=True)