
# CS-50 AI

 :wave: In this repository, you will be following my progress through the course. I got the idea of doing it a few days ago so this is why there are some folders that were already created.

## Week 0 : Search

###  Degrees : [:book:](https://cs50.harvard.edu/ai/2020/projects/0/degrees/)

### Tic-Tac-Toe : [:book:](https://cs50.harvard.edu/ai/2020/projects/0/tictactoe/)
In this project, the Minimax algorithm used, goes over all the future actions possible calculating the `min_value` or the `max_value` based on the AI's position. The algorithm chooses the **highest** or **lowest** scores relatively.
The higher (or lower) the score the more win outcomes possible derive from the move.

## Week 1 : Knowledge
### Knights : [:book:](https://cs50.harvard.edu/ai/2020/projects/1/knights/)

### Minesweeper : [:book:](https://cs50.harvard.edu/ai/2020/projects/1/minesweeper/)

## Week 2 : Uncertainty
### PageRank : [:book:](https://cs50.harvard.edu/ai/2020/projects/2/pagerank/)
For this one, I implemented a `crawl()` function that parses a directory of HTML pages and checks for links to other pages using a regex that I created. This function will return a `dict` where each `key` is a page and their values are a list of all the other pages in the corpus that are linked to by the page.

Afterwards, I was told to define a `transition_model()` function. This function returns the probability of distribution over which page to visit next.
The `transition_model()` accepts as arguments, `corpus`, `page` the page that the random surfer is currently at and the `damping_factor` being the damping factor which our case is a constant representing the damping factor used to calculate the probabilities.

Then, I was asked to implement two **pagerank** algorithms :

 - `sample_pagerank`
 - `iterative_pagerank`

In both algorithm, I start by initialising a starting a starting rank. In the `sample_pagerank` I start with 0 and in the `iterative_pagerank` I start with a starting rank being :
$$startingRank = 1 / N$$
Then, in the `sample_pagerank` I just randomly jump from page to page (with the help of the `random.choices()` function to calculate their probabilities based on the previous results.
For the `iterative_pagerank`, I use a while loop that keeps running until the count variable is equal to the number of pages in the corpus. In the while loop the given formula will be used to calculate the pageranks.
$$PR_{(p)}=\frac{1 - d}{N}+ d\sum_{i}^{}\frac{PR_{(i)}}{NumLinks_{(i)}}$$
`d` Being the damping factor.
`NumLinks(i)` Being the number of links on the current page.
`N` Being the number of pages in the corpus. 
