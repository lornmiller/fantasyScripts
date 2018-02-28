import json
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
#   0           1               2           3           4                   5       6           7           8      9    10    11    12      13      14    15       16      17    18     19
#"SEASON_ID","PLAYER_ID","PLAYER_NAME","TEAM_ID","TEAM_ABBREVIATION","TEAM_NAME","GAME_ID","GAME_DATE","MATCHUP","WL","MIN","FGM","FGA","FG_PCT","FG3M","FG3A","FG3_PCT","FTM","FTA","FT_PCT",
#   29      21    22    23    24    25    26    27  28         29           30
# "OREB","DREB","REB","AST","STL","BLK","TOV","PF","PTS","PLUS_MINUS","VIDEO_AVAILABLE"

def get_averages(file_name):
    with open("years/"+file_name) as file:
        data = json.load(file)
    for_averages = {}
    #For loop reads out the pertinent data from the json into a local object.  Data comes in in 1NF.
    #Needs to be seperated to achieve 2NF and 3NF.
    for row in data["resultSets"][0]["rowSet"]:
        #date = datetime.strptime(row[7][:-9], '%Y-%m-%d').date()
        season_id = row[0] if row[0] != None else ''
        player_id = row[1] if row[1] != None else ''
        player_name = row[2] if row[2] != None else ''
        team_id = row[3] if row[3] != None else ''
        team_abbreviation = row[4] if row[4] != None else ''
        team_name = row[5] if row[5] != None else ''
        game_id = row[6] if row[6] != None else 0
        matchup = row[8] if row[8] != None else ''
        wl = row[9] if row[9] != None else ''
        min = int(row[10]) if row[10] != None else 0
        fgm = row[11] if row[11] != None else 0
        fga = row[12] if row[12] != None else 0
        #fg_pct = row[13] if row[13] != None else 0,
        fg3m = row[14] if row[14] != None else 0
        fg3a = row[15] if row[15] != None else 0
        #fg3_pct = row[16] if row[16] != None else 0,
        ftm = row[17] if row[17] != None else 0
        fta = row[18] if row[18] != None else 0
        #ft_pct = row[19] if row[19] != None else 0,
        oreb = row[20] if row[20] != None else 0
        dreb = row[21] if row[21] != None else 0
        #treb = row[22] if row[22] != None else 0,
        ast = row[23] if row[23] != None else 0
        stl = row[24] if row[24] != None else 0
        blk = row[25] if row[25] != None else 0
        tov = row[26] if row[26] != None else 0
        pf = row[27] if row[27] != None else 0
        pts = row[28] if row[28] != None else 0
        plus_minus = row[29]if row[29] != None else 0

        #All star games and special pre season games against foreign teams are included.  Need to ensure only NBA teams are included
        if team_abbreviation not in ['GSW', 'CLE', 'OKC', 'TOR', 'MIA', 'SAS', 'POR', 'ATL', 'IND', 'CHA', 'LAC', 'LAL', 'HOU', 'BOS', 'SAC', 'PHI', 'NYK', 'BKN', 'PHX', 'DAL', 'MEM', 'UTA', 'SAS', 'DET', 'MIN', 'NOP', 'ORL', 'SAC', 'CHI', 'MIL', 'WAS', 'DEN']:
            print(team_abbreviation)
            continue

        #creates the averages for the season.
        if player_id in for_averages.keys():
            if season_id in for_averages[player_id].keys():
                for_averages[player_id][season_id]["min"].append(min)
                for_averages[player_id][season_id]["fga"].append(fga)
                for_averages[player_id][season_id]["fgm"].append(fgm)
                for_averages[player_id][season_id]["fg3a"].append(fg3a)
                for_averages[player_id][season_id]["fg3m"].append(fg3m)
                for_averages[player_id][season_id]["fta"].append(fta)
                for_averages[player_id][season_id]["ftm"].append(ftm)
                for_averages[player_id][season_id]["oreb"].append(oreb)
                for_averages[player_id][season_id]["dreb"].append(dreb)
                for_averages[player_id][season_id]["ast"].append(ast)
                for_averages[player_id][season_id]["stl"].append(stl)
                for_averages[player_id][season_id]["blk"].append(blk)
                for_averages[player_id][season_id]["tov"].append(tov)
                for_averages[player_id][season_id]["pf"].append(pf)
                for_averages[player_id][season_id]["pts"].append(pts)
                for_averages[player_id][season_id]["plus_minus"].append(plus_minus)
            else:
                for_averages[player_id][season_id] = {
                    "name": player_name,
                    "min": [min],
                    "fga": [fga],
                    "fgm": [fgm],
                    "fg3a": [fg3a],
                    "fg3m": [fg3m],
                    "fta": [ftm],
                    "oreb": [oreb],
                    "dreb": [dreb],
                    "ast": [ast],
                    "stl": [stl],
                    "blk": [blk],
                    "tov": [tov],
                    "pf": [pf],
                    "pts": [pts],
                    "plus_minus": [plus_minus]
                }
        else:
            for_averages[player_id] = {}
            for_averages[player_id][season_id] = {
                "name": player_name,
                "min": [min],
                "fga": [fga],
                "fgm": [fgm],
                "fg3a": [fg3a],
                "fg3m": [fg3m],
                "fta": [fta],
                "ftm": [ftm],
                "oreb": [oreb],
                "dreb": [dreb],
                "ast": [ast],
                "stl": [stl],
                "blk": [blk],
                "tov": [tov],
                "pf": [pf],
                "pts": [pts],
                "plus_minus": [plus_minus]
            }


    averages = []

    for player in for_averages:
        for season in for_averages[player]:
            if mean(for_averages[player][season]["min"]) >= 20.0:
                average = {
                    "player_id": player,
                    "player_name": for_averages[player][season]["name"],
                    "season_id": season,
                    "g": len(for_averages[player][season]["fga"]),
                    "fga": mean(for_averages[player][season]["fga"]),
                    "fgm": mean(for_averages[player][season]["fgm"]),
                    "fg3m": mean(for_averages[player][season]["fg3a"]),
                    "fg3a": mean(for_averages[player][season]["fg3m"]),
                    "fta": mean(for_averages[player][season]["fta"]),
                    "ftm": mean(for_averages[player][season]["ftm"]),
                    "oreb": mean(for_averages[player][season]["oreb"]),
                    "dreb": mean(for_averages[player][season]["dreb"]),
                    "ast": mean(for_averages[player][season]["ast"]),
                    "stl": mean(for_averages[player][season]["stl"]),
                    "blk": mean(for_averages[player][season]["blk"]),
                    "tov": mean(for_averages[player][season]["tov"]),
                    "pf": mean(for_averages[player][season]["pf"]),
                    "pts": mean(for_averages[player][season]["pts"]),
                    "plus_minus": mean(for_averages[player][season]["plus_minus"])
                }
                averages.append(average)

    return averages

def mean(numbers):
    number = float(sum(numbers)) / max(len(numbers), 1)
    #print(number)
    return round(number, 1)

def normalize_averages(averages):
    fgMinMax = [100000000,-1]
    ftMinMax = [100000000,-1]
    fg3MinMax = [100000000,-1]
    ptsMinMax = [100000000,-1]
    orebMinMax = [100000000,-1]
    drebMinMax = [100000000,-1]
    astMinMax = [100000000,-1]
    stlMinMax = [100000000,-1]
    blkMinMax = [100000000,-1]

    for player in averages:
        if player['fga'] != 0 and player['fgm']/player['fga'] > fgMinMax[1]:
            fgMinMax[1] = player['fgm']/player['fga']
        if player['fga'] != 0 and player['fgm']/player['fga'] < fgMinMax[0]:
            fgMinMax[0] = player['fgm']/player['fga']

        if player['fta'] != 0 and player['ftm']/player['fta'] > ftMinMax[1]:
            ftMinMax[1] = player['ftm']/player['fta']
        if player['fta'] != 0 and player['ftm']/player['fta'] < ftMinMax[0]:
            ftMinMax[0] = player['ftm']/player['fta']

        if player['fg3m'] > fg3MinMax[1]:
            fg3MinMax[1] = player['fg3m']
        if player['fg3m'] < fg3MinMax[0]:
            fg3MinMax[0] = player['fg3m']

        if player['pts'] > ptsMinMax[1]:
            ptsMinMax[1] = player['pts']
        if player['pts'] < ptsMinMax[0]:
            ptsMinMax[0] = player['pts']

        if player['oreb'] > orebMinMax[1]:
            orebMinMax[1] = player['oreb']
        if player['oreb'] < orebMinMax[0]:
            orebMinMax[0] = player['oreb']

        if player['dreb'] > drebMinMax[1]:
            drebMinMax[1] = player['dreb']
        if player['dreb'] < drebMinMax[0]:
            drebMinMax[0] = player['dreb']

        if player['ast'] > astMinMax[1]:
            astMinMax[1] = player['ast']
        if player['ast'] < astMinMax[0]:
            astMinMax[0] = player['ast']

        if player['stl'] > stlMinMax[1]:
            stlMinMax[1] = player['stl']
        if player['stl'] < stlMinMax[0]:
            stlMinMax[0] = player['stl']

        if player['blk'] > blkMinMax[1]:
            blkMinMax[1] = player['blk']
        if player['blk'] < blkMinMax[0]:
            blkMinMax[0] = player['blk']

    fgMinMax[1] = fgMinMax[1] - fgMinMax[0]
    ftMinMax[1] = ftMinMax[1] - ftMinMax[0]
    fg3MinMax[1] = fg3MinMax[1] - fg3MinMax[0]
    ptsMinMax[1] = ptsMinMax[1] - ptsMinMax[0]
    orebMinMax[1] = orebMinMax[1] - orebMinMax[0]
    drebMinMax[1] = drebMinMax[1] - drebMinMax[0]
    astMinMax[1] = astMinMax[1] - astMinMax[0]
    stlMinMax[1] = stlMinMax[1] - stlMinMax[0]
    blkMinMax[1] = blkMinMax[1] - blkMinMax[0]
    normalized_heuristic = []
    for player in averages:
        normalized_heuristic.append([
            (player['fgm'] / player['fga'] - fgMinMax[0]) / fgMinMax[1],
            (player['ftm'] / player['fta'] - ftMinMax[0]) / ftMinMax[1],
            (player['fg3m'] - fg3MinMax[0]) / fg3MinMax[1],
            (player['pts'] - ptsMinMax[0]) / ptsMinMax[1],
            (player['oreb'] - orebMinMax[0]) / orebMinMax[1],
            (player['dreb'] - drebMinMax[0]) / drebMinMax[1],
            (player['ast'] - astMinMax[0]) / astMinMax[1],
            (player['stl'] - stlMinMax[0]) / stlMinMax[1],
            (player['blk'] - blkMinMax[0]) / blkMinMax[1],
            player["player_id"],
            player["player_name"],
            player["season_id"]
        ])
    return normalized_heuristic

def create_fgft_value(averages):
    fgMinMax = [100000000, -1]
    ftMinMax = [100000000, -1]
    for player in averages:
        if player['fga'] != 0 and player['fgm']/player['fga'] > fgMinMax[1]:
            fgMinMax[1] = player['fgm']/player['fga']
        if player['fga'] != 0 and player['fgm']/player['fga'] < fgMinMax[0]:
            fgMinMax[0] = player['fgm']/player['fga']

        if player['fta'] != 0 and player['ftm']/player['fta'] > ftMinMax[1]:
            ftMinMax[1] = player['ftm']/player['fta']
        if player['fta'] != 0 and player['ftm']/player['fta'] < ftMinMax[0]:
            ftMinMax[0] = player['ftm']/player['fta']

def plot_normalized_averages6(normalized_averages):
    titles = ["fg%", "ft%", "3m", "pts", "oreb", "dreb", "ast", "stl", "blk", "player_id", "player_name", "season_id"]
    builds = {}
    for i in range(0,4):
        for j in range(i+1,5):
            for k in range(j+1, 6):
                for l in range(k+1,7):
                    for m in range(l+1, 8):
                        for n in range(m+1, 9):
                            x = []
                            gt4, gt5, gt6, gt7, total = 0, 0, 0, 0, 0
                            for average in normalized_averages:
                                total += 1
                                val = 10*(average[i]+average[j]+average[k]+average[l]+average[m]+average[n])/6
                                val = round(10 * val) / 10
                                if val >= 4:
                                    gt4 += 1
                                    if val >= 5:
                                        gt5 += 1
                                        if val < 6:
                                            x.append([average[10], val])
                                        if val >= 6:
                                            gt6 += 1
                                            if val >= 7:
                                                gt7 += 1
                                                #x.append(average[10])
                                #x.append(10*(average[i]+average[k]+average[j]+average[l]+average[m]+average[n])/6)
                            #plt.hist(x, 50, facecolor = 'blue')
                            #plt.xlabel("normalized value")
                            #plt.ylabel("Probability")
                            title=titles[i]+" "+titles[j]+" "+titles[k]+" "+titles[l]+" "+titles[m]+" "+titles[n]
                            #plt.title(title)
                            #plt.grid(True)
                            #plt.savefig(r"graphs of fantasy builds/6 cat builds/"+title+".png")
                            #plt.close("all")

                            if gt5 / total >= .14 and gt4 / total >= .4:
                                builds[title] = {"players": x, "values": [round(1000 * gt4 / total) / 10, round(1000 * gt5 / total) / 10, round(1000 * gt6 / total) / 10, round(1000 * gt7 / total) / 10]}
    return builds

def plot_normalized_averages7(normalized_averages):
    print()
    print("*******************************7*********************************")
    titles = ["fg%", "ft%", "3m", "pts", "oreb", "dreb", "ast", "stl", "blk", "player_id", "player_name", "season_id"]
    for i in range(0,3):
        for j in range(i+1,4):
            for k in range(j+1, 5):
                for l in range(k+1,6):
                    for m in range(l+1, 7):
                        for n in range(m+1, 8):
                            for o in range(n+1, 9):
                                x = []
                                gt4, gt5, gt6, gt7, total = 0, 0, 0, 0, 0
                                for average in normalized_averages:
                                    total += 1
                                    val = 10 * (average[i] + average[j] + average[k] + average[l] + average[m] + average[n] + average[o]) / 7
                                    val = round(10*val)/10
                                    if val >= 4:
                                        gt4 += 1
                                        if val >= 5:
                                            gt5 += 1
                                            if val < 6:
                                                x.append([average[10], val])
                                            if val >= 6:
                                                gt6 += 1
                                                if val >= 7:
                                                    gt7 += 1

                                    #x.append(10*(average[i]+average[j]+average[k]+average[l]+average[m]+average[n]+average[o])/7)
                                #3plt.hist(x, 50, facecolor = 'blue')
                                #plt.xlabel("normalized value")
                                #plt.ylabel("Probability")
                                title=titles[i]+" "+titles[j]+" "+titles[k]+" "+titles[l]+" "+titles[m]+" "+titles[n]+" "+titles[o]
                                #plt.title(title)
                                #plt.grid(True)
                                #plt.savefig(r"graphs of fantasy builds/7 cat builds/"+title+".png")
                                #plt.close("all")

                                if gt5 / total >= .12:
                                    print(title)
                                    print(x)
                                    print(round(1000* gt4 / total)/10, round(1000*gt5 / total)/10, round(1000*gt6 / total)/10, round(1000*gt7 / total)/10)
                                    print("-------------------------------------------------")

def test_builds():
    all_builds = {}
    for season in ["14-15.json", "15-16.json", "16-17.json", "17-18.json"]:
        # print()
        # print("*************"+season+"****************")
        averages = get_averages(season)
        normalized_averages = normalize_averages(averages)
        builds = plot_normalized_averages6(normalized_averages)
        for build in builds.keys():
            if build in all_builds.keys():
                all_builds[build].append(season)
            else:
                all_builds[build] = [season]

        # plot_normalized_averages7(normalized_averages)
    for build in all_builds:
        print(build, all_builds[build])

def main():
    averages = get_averages("17-18.json")
    for player in averages:
        print(averages)

if __name__ == "__main__":
    main()