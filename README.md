

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
[![Demandez moi n'importe quoi !](https://img.shields.io/badge/Demandez%20moi-n'%20importe%20quoi-1abc9c.svg)](https://GitHub.com/Naereen/ama.fr)
# CS-50 AI

 :wave: In this repository, you will be following my progress through the course. I got the idea of doing it a few days ago so this is why there are some folders that were already created.

## Week 0 : Search

###  Degrees : [:book:](https://cs50.harvard.edu/ai/2020/projects/0/degrees/)
I was provided with two folders one containing a set of a large data sets and another for small data sets. The goal is to find the `shortest_path` from the `source`'s id to the `target`'s id. I go on to implement this by defining a `starting_node`, `visited` (empty list) , `queue` list with the `starting_node` as the first element and the `shortest_path` being an empty list. Then in the while loop, we first check the neighbours of the first node in the lights of finding a relation to the `target` . If nothing is found, the neighbours become nodes that aren't explored yet and they get added to the queue to be explored. Keeping track of the length of the shortest path to get to the target and the nodes that already been visited in `visited`.
### Tic-Tac-Toe : [:book:](https://cs50.harvard.edu/ai/2020/projects/0/tictactoe/)
In this project, the Minimax algorithm used, goes over all the future actions possible calculating the `min_value` or the `max_value` based on the AI's position. The algorithm chooses the **highest** or **lowest** scores relatively.
The higher (or lower) the score the more win outcomes possible derive from the move.

## Week 1 : Knowledge
### Knights : [:book:](https://cs50.harvard.edu/ai/2020/projects/1/knights/)

Given a way to express logical sentences, I was asked to solve four puzzles given.

### Minesweeper : [:book:](https://cs50.harvard.edu/ai/2020/projects/1/minesweeper/)

In this project, we had to write an AI agent that can gather knowledge about the minesweeper board and automatically select cells that are known to be safe.  

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

## Week 4: Learning
### Shopping : [:book:](https://cs50.harvard.edu/ai/2020/projects/4/shopping/)
We are given a csv file that contains data about around 12000 users. With this data I should use the K neighbor classifier to be able to predict whether a user will make a purchase or not.

In the `load_data` function, we read the csv file row by row, forming the evidence list and the label list.

`train_model` : given the lists of evidence and labels that we formed in the previous function, we had to train the model with k = 1 and then return the trained model.


In the last function (`evaluate`), the predictions that the model has made were given as well as their true labels. So going over the data given, I compared the labels to the predictions and added counters to keep track of :
- The true positive labels that were identified (`true_positive_count`)
- The true negative labels that were identified (`true_negative_count`)
- The total number of positives (`total_positives`)
- The total number of negatives (`total_negatives`)

Then using these variables, I calculated the `sensitivity` and `specificity`.

### Nim : [:book:](https://cs50.harvard.edu/ai/2020/projects/4/nim/)
Two files were given, one that has the classes for which I have to implement the methods (`nim.py`). The other being the file that handles the gameplay (`play.py`).

The first function to implement is the `get_q_value` in the `NimAI` class. All this function does, is check if there's a `q` value for the given 'state' and 'action' if not return 0.

Using the formula :
$$Q(s, a) \leftarrow Q(s, a) + \alpha \times (NVE - OVE)$$
- `NVM` being the New Value Estimate
- `OVE` being the Old Value Estimate

The q value gets updated in the `update_q_value` function.

In the last function to implement (`choose_action`) :
- In the case where epsilon is `True` :
  - I set two choices either a random move or the best move in the goal of either exploring or exploiting.
  - Based on the epsilon value as a weight for the `random.choices()` the AI takes the next action (either choses randomly from the list of actions or chooses based on the highest `q` value).

- In the case where epsilon is `False` :
  - I go over the possible actions in the current state. Checking if they have a `q` value or not (if they don't their `q` value will be considered 0).
  - Comparing their values until it finds the one with the highest `q` value.
  - Otherwise, it will just choose the last one on the list of actions.


  Playing against the AI, it does take smart moves but with a little bit of cleverness it can be defeated.

## Week 5 : Neural Networks
### Traffic : [:book:](https://cs50.harvard.edu/ai/2020/projects/5/traffic/)
For this project, a README is required in which I should go over my experimentation process. ([📄](/traffic/README.md))

## Week 6 : Langage
### Parser : [:book:](https://cs50.harvard.edu/ai/2020/projects/6/parser/)
We are asked to determine the structure of a sentence using context-free grammar. We are supplied with a `TERMINAL` set of symbols and our main task will be to create `NONTERMINALS` that are general enough to generate the sentences provided in the `/sentences` folder. Keeping in my that we should avoid **over-generation** as well as **under-generation**. 
The first task, is to implement a function that will accept a sentence as a string and we should return the words in that sentence to lowecase in a list. Which was pretty simple, all I had to do was in the help of the `nltk.tokenize.word_tokenize(sentence.lower())` split the sentence into tokens and then filter the tokens that weren't words.
