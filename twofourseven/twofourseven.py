import requests
import pandas as pd
import csv
from lxml import html
import numpy as np
import re
import time

class Recruit:

    def __init__(self):
        self.session = requests.Session()

    def getClass(self, year, team): # Return DataFrame of a teams recruiting class from a specific year
        self.year = year
        self.team = str(team)
        self.team = self.team.replace(' ', '-')
        self.team = self.team.lower()

        res = self.session.get('https://247sports.com/college/' + self.team + '/Season/' + str(self.year) + '-Football/Commits/', headers = {'User-Agent': 'Mozilla/5.0'})
        res.raise_for_status()
        site = html.fromstring(res.content)

        players = site.xpath("//div[@class='recruit']/a/text()")
        pos = site.xpath("//li[@class='ri-page__list-item']/div/div[@class='position']/text()")
        metrics = site.xpath("//li[@class='ri-page__list-item']/div/div[@class='metrics']/text()")
        ht = [x.split('/')[0].strip() for x in metrics]
        wt = [x.split('/')[1].strip() for x in metrics]
        hometown = site.xpath("//div[@class='recruit']/span/text()")
        hometown = [x.strip() for x in hometown if x.strip()]
        score = site.xpath("//div[@class='rating']/div/span[@class='score']/text()")
        nat_rank = site.xpath("//a[@class='natrank']/text()")
        pos_rank = site.xpath("//a[@class='posrank']/text()")
        st_rank = site.xpath("//a[@class='sttrank']/text()")

        di = {
        'Player' : players, 
        'POS' : pos,
        'HT' : ht,
        'WT' : wt,
        'Hometown': hometown,
        'Rating' : score,
        'National_Rank' : nat_rank,
        'Position_Rank' : pos_rank,
        'State_Rank' : st_rank
        }

        df = pd.DataFrame(di)
        df.insert(0, 'Year', year)


        return df

    def getAllTime(self, team): # Return DataFrame of a teams all time greatest recruits
        self.team = str(team)
        self.team = self.team.replace(' ', '-')
        self.team = self.team.lower()

        res = self.session.get('https://247sports.com/college/' + self.team + '/Sport/Football/AllTimeRecruits/', headers = {'User-Agent': 'Mozilla/5.0'})
        res.raise_for_status()
        site = html.fromstring(res.content)

        players = site.xpath("//div[@class='recruit']/a/text()")
        pos = site.xpath("//li[@class='ri-page__list-item']/div/div[@class='position']/text()")
        metrics = site.xpath("//li[@class='ri-page__list-item']/div/div[@class='metrics']/text()")
        ht = [x.split('/')[0].strip() for x in metrics]
        wt = [x.split('/')[1].strip() for x in metrics]
        hometown = site.xpath("//div[@class='recruit']/span[1]/text()")
        hometown = [x.strip() for x in hometown if x.strip()]
        score = site.xpath("//div[@class='rating']/div/span[@class='score']/text()")
        nat_rank = site.xpath("//a[@class='natrank']/text()")
        pos_rank = site.xpath("//a[@class='posrank']/text()")
        st_rank = site.xpath("//a[@class='sttrank']/text()")
        clas = site.xpath("//div[@class='recruit']/span[2]/text()")
        clas = [x.split('Class of ')[1] for x in clas]

        di = {
        'Player' : players, 
        'POS' : pos,
        'HT' : ht,
        'WT' : wt,
        'Class' : clas,
        'Hometown': hometown,
        'Rating' : score,
        'National_Rank' : nat_rank,
        'Position_Rank' : pos_rank,
        'State_Rank' : st_rank
        }

        df = pd.DataFrame(di)

        return df


    def getFBPlayerData(self, year):
        player_id = []
        players = []
        pos = []
        ht = []
        wt = []
        hs = []
        city = []
        state = []
        score = []
        nat_rank = []
        pos_rank = []
        st_rank = []
        team = []
        pattern = "college/(.*?)/"

        for i in range(40):
            res = requests.get('https://247sports.com/Season/' + str(year) + '-Football/CompositeRecruitRankings/?ViewPath=~%2FViews%2FSkyNet%2FPlayerSportRanking%2F_SimpleSetForSeason.ascx&InstitutionGroup=HighSchool&Page=' + str(i + 1) + '', headers = {'User-Agent': 'Mozilla/5.0'})
            site = html.fromstring(res.content)

            status_list = site.xpath("//div[@class='status']")


            ids = site.xpath("//div[@class='recruit']/a[1]/@href")
            player_id.extend([re.search("([^-]+$)", x).group(1) for x in ids])
            players.extend(site.xpath("//div[@class='recruit']/a[1]/text()"))
            pos.extend(site.xpath("//li[@class='rankings-page__list-item']/div/div[@class='position']/text()"))
            metrics = site.xpath("//li[@class='rankings-page__list-item']/div/div[@class='metrics']/text()")
            ht.extend([x.split('/')[0].strip() for x in metrics])
            wt.extend([x.split('/')[1].strip() for x in metrics])
            hometown_err = site.xpath("//div[@class='recruit']/span/text()")
            
            hs_err = [x.split('(')[0] for x in hometown_err]
            hs.extend(x.strip() for x in hs_err)
            citystate = [x.split('(')[1] for x in hometown_err]
            city.extend([x.split(',')[0] for x in citystate])
            state_err = []
            for x in citystate:
                try:
                    state_err.append(x.split(',')[1])
                except:
                    state_err.append('NULL')

            state_err = [x.replace(')', '') for x in state_err]
            state.extend([x.strip() for x in state_err])

            score.extend(site.xpath("//div[@class='rating']/div/span[@class='score']/text()"))
            nat_rank.extend(site.xpath("//a[@class='natrank']/text()"))
            pos_rank.extend(site.xpath("//a[@class='posrank']/text()"))
            st_rank.extend(site.xpath("//a[@class='sttrank']/text()"))

            for x in status_list:
                try:
                    url = x.xpath("a[1]/@href")
                    url = url[0]
                    if re.search(pattern, url):
                        substring = re.search(pattern, url).group(1)
                        substring = substring.replace('-', ' ')
                        team.append(substring)
                    else:
                        raise ValueError('Not Committed Yet')
                except:
                    team.append('NULL')

            time.sleep(2)

        di = {
        'ID' : player_id,
        'Player' : players, 
        'POS' : pos,
        'HT' : ht,
        'WT' : wt,
        'High School' : hs,
        'City' : city,
        'State' : state,
        'Rating' : score,
        'National_Rank' : nat_rank,
        'Position_Rank' : pos_rank,
        'State_Rank' : st_rank,
        'Team' : team
        }

        df = pd.DataFrame(di)
        df.insert(0, 'Year', year)


        return df

    def getBBPlayerData(self, year):
        player_id = []
        players = []
        pos = []
        ht = []
        wt = []
        hs = []
        city = []
        state = []
        score = []
        nat_rank = []
        pos_rank = []
        st_rank = []

        team = []
        pattern = "college/(.*?)/"

        for i in range(20):
            res = requests.get('https://247sports.com/Season/' + str(year) + '-Basketball/CompositeRecruitRankings/?ViewPath=~%2FViews%2FSkyNet%2FPlayerSportRanking%2F_SimpleSetForSeason.ascx&InstitutionGroup=HighSchool&Page=' + str(i + 1) + '', headers = {'User-Agent': 'Mozilla/5.0'})
            site = html.fromstring(res.content)

            status_list = site.xpath("//div[@class='status']")


            ids = site.xpath("//div[@class='recruit']/a[1]/@href")
            player_id.extend([re.search("([^-]+$)", x).group(1) for x in ids])
            players.extend(site.xpath("//div[@class='recruit']/a[1]/text()"))
            pos.extend(site.xpath("//li[@class='rankings-page__list-item']/div/div[@class='position']/text()"))
            metrics = site.xpath("//li[@class='rankings-page__list-item']/div/div[@class='metrics']/text()")
            ht.extend([x.split('/')[0].strip() for x in metrics])
            wt.extend([x.split('/')[1].strip() for x in metrics])
            hometown_err = site.xpath("//div[@class='recruit']/span/text()")
            
            hs_err = [x.split('(')[0] for x in hometown_err]
            hs.extend(x.strip() for x in hs_err)
            citystate = [x.split('(')[1] for x in hometown_err]
            city.extend([x.split(',')[0] for x in citystate])
            state_err = []
            for x in citystate:
                try:
                    state_err.append(x.split(',')[1])
                except:
                    state_err.append('NULL')

            state_err = [x.replace(')', '') for x in state_err]
            state.extend([x.strip() for x in state_err])

            score.extend(site.xpath("//div[@class='rating']/div/span[@class='score']/text()"))
            nat_rank.extend(site.xpath("//a[@class='natrank']/text()"))
            pos_rank.extend(site.xpath("//a[@class='posrank']/text()"))
            st_rank.extend(site.xpath("//a[@class='sttrank']/text()"))

            for x in status_list:
                try:
                    url = x.xpath("a[1]/@href")
                    url = url[0]
                    if re.search(pattern, url):
                        substring = re.search(pattern, url).group(1)
                        substring = substring.replace('-', ' ')
                        team.append(substring)
                    else:
                        raise ValueError('Not Committed Yet')
                except:
                    team.append('NULL')

            time.sleep(2)

        di = {
        'ID' : player_id,
        'Player' : players, 
        'POS' : pos,
        'HT' : ht,
        'WT' : wt,
        'High School' : hs,
        'City' : city,
        'State' : state,
        'Rating' : score,
        'National_Rank' : nat_rank,
        'Position_Rank' : pos_rank,
        'State_Rank' : st_rank,
        'Team' : team
        }

        df = pd.DataFrame(di)
        df.insert(0, 'Year', year)


        return df

    def getDraft(self, year):
        player_id = []
        player = []
        position = []
        rd_pick = []
        draft_pick = []
        rd = []
        rating = []
        team = []
        
        for i in range(7):
            res = requests.get('https://247sports.com/League/NFL/DraftPicks/?year=' + str(year) + '&round=' + str(i+1) + '&mock=0', headers = {'User-Agent': 'Mozilla/5.0'})
            site = html.fromstring(res.content)


            draft_list = (site.xpath("//ul[@class='content-list draft-list league']/li[not(@class)]"))

            for x in draft_list:
                if str(x.xpath("p[@class='analysis-txt']/text()")) != "['Forfeited Pick']":
                    ids = x.xpath("div[@class='list-data left']/div[@class='name']/a[1]/@href")
                    player_id.append([re.search("([^-]+$)", y).group(1) for y in ids])
                    player.append(x.xpath("div[@class='list-data left']/div[@class='name']/a[1]/text()"))
                    try:
                        position.append(x.xpath("div[@class='list-data left']/ul[@class='metrics-list']/li[1]/text()"))
                    except:
                        position.append('NULL')
                        continue

                    rd.append(str(i+1))
                    rd_pick.append(x.xpath("div[@class='pick left']/span[1]/text()"))
                    draft_pick.append(x.xpath("div[@class='pick left']/span[2]/text()"))
                    rating.append(x.xpath("div[@class='list-data left']/div[@class='rating']/span[@class='score']/text()"))
                    team.append(x.xpath("div[@class='team left']/a[2]/text()"))

        player_id = [''.join(x) for x in player_id] # Turn all entries into strings instead of one length lists
        player = [''.join(x) for x in player] # Turn all entries into strings instead of one length lists
        position = [''.join(x) for x in position] # Turn all entries into strings instead of one length lists
        rd_pick = [''.join(x) for x in rd_pick] # Turn all entries into strings instead of one length lists
        draft_pick = [''.join(x) for x in draft_pick] # Turn all entries into strings instead of one length lists
        rating = [''.join(x) for x in rating] # Turn all entries into strings instead of one length lists
        team = [''.join(x) for x in team] # Turn all entries into strings instead of one length lists

        di = {
            'ID' : player_id,
            'Player' : player,
            'POS' : position,
            'Team' : team,
            'Rating' : rating,
            'Round' : rd,
            'RD_pick' : rd_pick,
            'Draft_pick' : draft_pick
        }

        df = pd.DataFrame(di)
        df['POS'] = df['POS'].replace('', 'NULL')
        df.insert(0, 'Year', year)
        return df

class TransferPortal:

    def __init__(self):
        self.session = requests.Session()
        self.fbcollegedf = pd.read_csv('https://raw.githubusercontent.com/Natron0919/twofourseven/main/Data/fbcolleges.csv')
        self.bbcollegedf = pd.read_csv('https://raw.githubusercontent.com/Natron0919/twofourseven/main/Data/bbcolleges.csv')


    def getFootballData(self, year):
        
        self.year = year
        # Get html from site for appropriate year. 
        res = requests.get('https://247sports.com/Season/' + str(year) + '-Football/TransferPortal/', headers={'User-Agent': 'Mozilla/5.0'})
        res.raise_for_status()
        site = html.fromstring(res.content)

        # Return lists of player names, position, and rating from HS
        players = site.xpath("//div[@class='player']/a/text()")
        positions = site.xpath("//div[@class='position']/text()")
        scores = site.xpath("//span[child::span[text()='(HS)']]/text()")

        # Get Player specific ID
        ids = site.xpath("//div[@class='player']/a[1]/@href")
        ids = [re.search("([^-]+$)", x).group(1) for x in ids]


        # Return initial team and new team for each player
        player_list = site.xpath("//li[@class='portal-list_itm']")
        team1 = [] # Empty list for original team
        team2 = [] # Empty list for new team
        pattern = "college/(.*?)/"

        for x in player_list: # For-loop to get all players original team
            try:
                url = x.xpath("div[contains(@class, 'transfer-institution')]/a[1]/@href")
                url = url[0]

                if re.search(pattern, url):
                    substring = re.search(pattern, url).group(1)
                    substring = substring.replace('-', ' ')
                    team1.append(substring)
                else:
                    raise ValueError('No Original Team')
            except:
                team1.append('NULL')
        for x in player_list: # For-loop to get all players new team
            try:
                url = x.xpath("div[contains(@class, 'transfer-institution')]/a[2]/@href")
                url = url[0]
                if re.search(pattern, url):
                    substring = re.search(pattern, url).group(1)
                    substring = substring.replace('-', ' ')
                    team2.append(substring)
                else:
                    raise ValueError('No Original Team')
            except:
                team2.append('NULL')

        # team1 = [''.join(x) for x in team1] # Turn all entries into strings instead of one length lists
        # team1 = [x.lower() for x in team1]
        # team2 = [''.join(x) for x in team2] # Turn all entries into strings instead of one length lists
        # team2 = [x.lower() for x in team2]

        # Create dictionary from all lists
        di = {'ID' : ids, 'Player' : players, 'POS' : positions, 'Rating' : scores, 'Team_Old' : team1, 'Team_New' : team2}

        # Turn dictionary into DataFrame
        df = pd.DataFrame(di)
        df['Player'] = df['Player'].astype(str)
        df['POS'] = df['POS'].astype(str)
        df['Rating'] = df['Rating'].str.strip()
        df = df.replace('N/A', 'NULL')
        df.insert(0, 'Year', year)
        df['Team_Old'] = df['Team_Old'].replace(r'^\s*$', 'NULL', regex = True)
        df['Team_New'] = df['Team_New'].replace(r'^\s*$', 'NULL', regex = True)

        df = pd.merge(df, self.fbcollegedf, left_on = ['Team_Old'], right_on = ['Team'], how = 'left')
        df = df.drop(columns = {'Team'})
        df = pd.merge(df, self.fbcollegedf, left_on = ['Team_New'], right_on = ['Team'], how = 'left', suffixes = ['_Old', '_New'])
        df = df.drop(columns = {'Team'})
        df = df.replace(np.nan, 'NULL')
        df['ID'] = df['ID'].str.replace('/', '')

        return df







    def getBasketballData(self, year):
        
        self.year = year
        # Get html from site for appropriate year. 
        res = requests.get('https://247sports.com/Season/' + str(year) + '-Basketball/TransferPortal/', headers={'User-Agent': 'Mozilla/5.0'})
        res.raise_for_status()
        site = html.fromstring(res.content)

        # Return lists of player names, position, and rating from HS
        players = site.xpath("//div[@class='player']/a/text()")
        positions = site.xpath("//div[@class='position']/text()")
        scores = site.xpath("//span[child::span[text()='(HS)']]/text()")

        # Get Player specific ID
        ids = site.xpath("//div[@class='player']/a[1]/@href")
        ids = [re.search("([^-]+$)", x).group(1) for x in ids]

        # Return initial team and new team for each player
        player_list = site.xpath("//li[@class='portal-list_itm']")
        team1 = [] # Empty list for original team
        team2 = [] # Empty list for new team
        pattern = "college/(.*?)/"

        for x in player_list: # For-loop to get all players original team
            try:
                url = x.xpath("div[contains(@class, 'transfer-institution')]/a[1]/@href")
                url = url[0]
                if re.search(pattern, url):
                    substring = re.search(pattern, url).group(1)
                    substring = substring.replace('-', ' ')
                    team1.append(substring)
                else:
                    raise ValueError('No Original Team')
            except:
                team1.append('NULL')

        for x in player_list: # For-loop to get all players new team
            try:
                url = x.xpath("div[contains(@class, 'transfer-institution')]/a[2]/@href")
                url = url[0]
                if re.search(pattern, url):
                    substring = re.search(pattern, url).group(1)
                    substring = substring.replace('-', ' ')
                    team2.append(substring)
                else:
                    raise ValueError('No New Team')
            except:
                team2.append('NULL')

        # team1 = [''.join(x) for x in team1] # Turn all entries into strings instead of one length lists
        # team1 = [x.lower() for x in team1]
        # team2 = [''.join(x) for x in team2] # Turn all entries into strings instead of one length lists
        # team2 = [x.lower() for x in team2]

        # Create dictionary from all lists
        di = {'ID' : ids, 'Player' : players, 'POS' : positions, 'Rating' : scores, 'Team_Old' : team1, 'Team_New' : team2}

        # Turn dictionary into DataFrame
        df = pd.DataFrame(di)
        df['Player'] = df['Player'].astype(str)
        df['POS'] = df['POS'].astype(str)
        df['Rating'] = df['Rating'].str.strip()
        df = df.replace('N/A', 'NULL')
        df.insert(0, 'Year', year)
        df['Team_Old'] = df['Team_Old'].replace(r'^\s*$', 'NULL', regex = True)
        df['Team_New'] = df['Team_New'].replace(r'^\s*$', 'NULL', regex = True)

        df = pd.merge(df, self.bbcollegedf, left_on = ['Team_Old'], right_on = ['Team'], how = 'left')
        df = df.drop(columns = {'Team'})
        df = pd.merge(df, self.bbcollegedf, left_on = ['Team_New'], right_on = ['Team'], how = 'left', suffixes = ['_Old', '_New'])
        df = df.drop(columns = {'Team'})
        df = df.replace(np.nan, 'NULL')
        df['ID'] = df['ID'].str.replace('/', '')

        return df