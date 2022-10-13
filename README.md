
[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
[![Demandez moi n'importe quoi !](https://img.shields.io/badge/Demandez%20moi-n'%20importe%20quoi-1abc9c.svg)](https://GitHub.com/Naereen/ama.fr)
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

### Heredity : [:book:](https://cs50.harvard.edu/ai/2020/projects/2/heredity/)
I found this assignment to be one of the easiest, it was pretty straightforward and I passed all the tests in the first go.
Going over each person individually in the people list, I set a few conditions to be able to calculate the probabilities checking if a person, is a `parent` or `child` .
Then the following dictionary helps me in getting the relative probabilities of passing the genes by the number of genes :
```
prob_parent_give_gene = {
                0: 0.01,
                1: 0.49,
                2: 0.99
            }
 ```
 Next in the `if else if` chain, I calculate the the person's probabilities of having the gene based on the number of genes in the parents. After it's calculated, I add them to the people probabilities to finally return the **joint probability** being the product of all the elements in `people_probabilities`.
## Week 3 : Optimisation
### Crossword : [:book:](https://cs50.harvard.edu/ai/2020/projects/3/crossword/)
This was a long one but a fun one to make. The feeling I got after seeing the table displaying the right words is indescribable.
I was a given a list of words in `.txt` files and structures for the tables that were parsed by the `crossword.py` script given, turning them into a `Crossword` and a `Variable` classes. Which are used to be able to solve the crossword.
It consisted of implementing the `ac3` algorithm and basically going over the given word possibilities singling out the ones that were not consistent with the contraints and keeping the ones that were.
To speed things up I implement the **least constraining value heuristic** (which was suggested but not required). Using this heuristic, I ordered the values in the domain of `var` (being the variable that we're currently on) starting with the one rules out the fewest values amongst the neighbours of `var`.
