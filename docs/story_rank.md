# Ranking algorithm for stories

Rank = (P-1) / (T+2)^G

where,

P = points of an item (and -1 is to negate submitters vote)

T = time since submission (in hours)

G = Gravity, defaults to 1.8 (this value comes from hackernews see reference link below.)

[Reference](https://medium.com/hacking-and-gonzo/how-hacker-news-ranking-algorithm-works-1d9b0cf2c08d)