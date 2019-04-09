## SteamReviewManager ##

W I P

- - -

- Can download reviews of games and classify them (by genres?)
  - [x] Downloads Gameinfo.
  - [x] Donwloads Reviews of the specified games in a specific language.
  - [x] Tracks the downloads in a Summary of the game reviews
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

Data Sample:

```javascript
{
    'recommendationid': 'numString',
    'author': {
        'steamid': 'numString',
        'num_games_owned': number,
        'num_reviews': number,
        'playtime_forever': number,
        'playtime_last_two_weeks': number,
        'last_played': number
    },
    'language': 'String',
    'review': 'LongString',
    'timestamp_created': number,
    'timestamp_updated': number,
    'voted_up': Boolean,
    'votes_up': number,
    'votes_funny': number,
    'weighted_vote_score': number,
    'comment_count': number,
    'steam_purchase': Boolean,
    'received_for_free': Boolean,
    'written_during_early_access': Boolean
}
```

Choose:

- [ ] SVM binary labeled learning
- [ ] Summarizing
- [ ] Review ranking by review and user attributes
> playedTime + reviewLikes + userScore + oldnessOfReview + reviewFunnyLikesRatio
- [ ] Extract the justification on why the users thing something is good or bad 
> Graphics, Gameplay, Controls, BusinessModel ...



