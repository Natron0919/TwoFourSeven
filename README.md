# TwoFourSeven
Python Package to scrape recruiting data from 247Sports website

Able to scrape transfer portal page as well.

## Installation:
pip install twofourseven <br>

## Classes:
<strong>Recruit</strong> <br>
  getClass(team, year) - Returns df of the recruiting class of a given team from the given year. (does NOT include transfers) <br>
  getAllTime(team) - Returns df of top recruits for a team for recent history. <br>
  getFBPlayerData(year) - Returns df of top 2000 fb recruits for a given year. <br>
  getBBPlayerData(year) - Returns df of top 2000 (or less depending on how many are ranked) bb recruits for a given year. <br>
  getDraft(year) - Returns df of the NFL draft from a given year <br>
<br>
<strong>TransferPortal</strong> <br>
  getFootballData(year) - Returns df of everyone who entered the transferportal for a given year for football <br>
  getBasketballData(year) - Returns df of everyone who entered the transferportal for a given year for basketball <br>
  
