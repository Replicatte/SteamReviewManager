## SteamReviewManager ##

W I P

- - -

- Can download reviews of games and classify them (by genres?)
  - [x] Crawls different applications of Steam 
  - [x] Gets the summary of the review values maybe with multiple languages (if the game is also in spanish also get spanish reviews)
  - [x] Starts downloading reviews (most popular games first?)
  - [x] Saves the application reviews of the same kind in the same file (by genres?/language)
  
- Can load the reviews of determined file for making an simple analysis
  - [ ] Loads the file
  - [ ] Evaluation
  - [ ] Data providing
  
- Provides web responses FLASK
  - [ ] Learn flask
  - [ ] Make a server for downloading the reviews and providing the data


### Downloader requierements ###

You need a MongoDB to place the data.

### How does(should atm) the downloader work? ###

The downloaderPlanner executes and downloads all the posible games, afterwards it starts with the reviews in the specified language.
Gonna take a while for it to finish.

### Data evaluation. ###

- [ ] SVM binary labeled learning
- [ ] Summarizing
- [ ] Review ranking by review and user attributes

> playedTime + reviewLikes + userScore + oldnessOfReview + reviewFunnyLikesRatio

```json
{
    'recommendationid': '49207914',
    'author': {
        'steamid': '76561198077842371',
        'num_games_owned': 21,
        'num_reviews': 4,
        'playtime_forever': 881,
        'playtime_last_two_weeks': 0,
        'last_played': 1545929761
    },
    'language': 'english',
    'review': 'Quite frankly, dont buy this.  Worst game out there currently, seriously.  The positive reviews is definetly staff or friends of staff working at the company.  This is a disaster!!!!  Everyone I knew quit, and no one is online anymore.  At least Ark has a community',
    'timestamp_created': 1551005549,
    'timestamp_updated': 1551005549,
    'voted_up': False,
    'votes_up': 0,
    'votes_funny': 0,
    'weighted_vote_score': 0,
    'comment_count': 0,
    'steam_purchase': True,
    'received_for_free': False,
    'written_during_early_access': True
}
```
