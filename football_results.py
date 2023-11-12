import csv

#Reading all the files to use later
with open("source_files/shootouts.csv") as shootouts_csv:
    shootouts = [row for row in csv.DictReader(shootouts_csv)]

with open("source_files/results.csv", encoding='utf-8') as results_csv:
    results = [row for row in csv.DictReader(results_csv)]

with open("source_files/goalscorers.csv", encoding='utf-8') as goalscorers_csv:
    goalscorers = [row for row in csv.DictReader(goalscorers_csv)]


# Calculating the percentage of games that have gone to penalty shootouts.
percentage_shootouts = len(shootouts)/len(results) * 100
#print(percentage_shootouts)   1.2% of international games have gone to a penalty shootout


# Funtion to add a winner column into the results dictionary obtained from results.csv
def winning_teams(dict):
    for i in range(len(dict)):
        row = dict[i]
        if row["home_score"] > row["away_score"]:
            dict[i].update({"winner": row["home_team"]})
        elif row["away_score"] > row["home_score"]:
            dict[i].update({"winner": row["away_team"]})
        else:
            dict[i].update({"winner": "Draw"})
    return dict
results_altered = winning_teams(results)
#print(results_altered)


# Function to find which countries have won the most penalty shootouts and most match wins
def most_wins(dictionary):
    wins = {}
    for row in dictionary:
        if row["winner"] in wins:
            wins[row["winner"]]+= 1
        else:
            wins[row["winner"]] = 1
    return wins

most_shootout_wins = most_wins(shootouts)
#print(most_shootout_wins)
most_match_wins = most_wins(results_altered)
#print(most_match_wins)


# Function to find the total games or shootouts per country
def games_or_shootouts_per_country(input):
    count= {}
    # Tallies total shootouts per country
    for row in input:
        if row["home_team"] in count:
            count[row["home_team"]]+= 1
        else:
            count[row["home_team"]] = 1

        if row["away_team"] in count:
            count[row["away_team"]]+= 1
        else:
            count[row["away_team"]] = 1
    return count

shootouts_per_country = games_or_shootouts_per_country(shootouts)
matches_per_country = games_or_shootouts_per_country(results)
#print(shootouts_per_country)
#print(matches_per_country)


# Function to find the shootout win percentage, based on the previously calculated number of wins and total shootouts.
def win_percentage(wins, total_amount):
    win_percentage = {}
    for country in wins:
        if country == "Draw":
            continue
        win_percentage[country] = wins[country]/total_amount[country]*100
    return win_percentage

shootout_win_percentage = win_percentage(most_shootout_wins, shootouts_per_country)
match_win_percentage = win_percentage(most_match_wins, matches_per_country)
#print(shootout_win_percentage)
#print(match_win_percentage)


# Function to find the top goalscorers
def top_goalscorer(goalscorers):
    top_goalscorers = {}
    for row in goalscorers:
        if row["scorer"] == "NA":
            continue
        elif row["scorer"] in top_goalscorers:
            top_goalscorers[row["scorer"]][1] += 1
        else:
            top_goalscorers.update({row["scorer"]: [row["team"], 1]})
    return top_goalscorers

top_goalscorers = top_goalscorer(goalscorers)
#print(top_goalscorers)


# A function that returns a ranked, ordered dictionary from an unordered one.
def ranking_inputs(unordered_input):
    ordered = dict(sorted(unordered_input.items(), key = lambda x:x[-1], reverse = True))
    input_ranked = {}
    rank = 1
    for item in ordered:
        input_ranked[rank] = [item, ordered[item]]
        rank += 1
    return input_ranked


# Function to flatten dictionaries that contain a list within a list to clean up the data e.g. top_goalscorers_ranked
# e.g A list [1, [2, 3]] will become [1, 2, 3]
def flatten_data(dictionary):
    def flatten(my_list):
        for i in range(len(my_list)):
            if my_list[i].__class__ != list:
                my_list[i] = [my_list[i]]
        return sum(my_list,[])
    for key,value in dictionary.items():
        dictionary[key] = flatten(value)
    return dictionary


# The match and shootout stats do not need the flatten_data function currently, but they are placed here for convenience in future use
ranked_shootout_win_percentage = ranking_inputs(shootout_win_percentage)
shootout_wins_ranked = ranking_inputs(most_shootout_wins)
#print(ranked_shootout_win_percentage)
#print(shootout_wins_ranked)

ranked_match_win_percentage = ranking_inputs(match_win_percentage)
match_wins_ranked = ranking_inputs(most_match_wins)
# print(ranked_match_win_percentage)
# print(match_wins_ranked)

top_goalscorers_ranked = flatten_data(ranking_inputs(top_goalscorers))
#print(top_goalscorers_ranked)


# A function to return the difficult to read dictionaries into a coherent csv file where each row represents an item
def readable_rankings(dictionary, file_name,  *headers):
    with open("findings/" + file_name, "w", newline = "", encoding = 'utf-8') as f:
        w = csv.writer(f, delimiter = ".")
        w.writerow(['rank', [*headers]])
        w.writerows(dictionary.items())
    

readable_rankings(shootout_wins_ranked, "shootout_wins_ranked.csv", "country", "wins")

readable_rankings(ranked_shootout_win_percentage, "shootout_win_percentage_ranked.csv", "country", "win_percentage")

readable_rankings(ranked_match_win_percentage, "match_win_percentage_ranked.csv", "country", "win_percentage")

readable_rankings(match_wins_ranked, "match_wins_ranked.csv", "country", "wins")

readable_rankings(top_goalscorers_ranked, "top_goalscorers_ranked.csv", "player", "country", "goals")

