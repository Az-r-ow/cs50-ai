import os
import random
import re
import sys

import pdb

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    pages_probabilities = {}
    num_links = len(corpus[page])

    # Page has no outgoing links
    if not num_links:
        # Calculate the probability
        equal_probability = 1 / len(corpus)
        for p in corpus:
            pages_probabilities[p] = equal_probability
        return pages_probabilities

    # Page has outgoing links
    # Get the probability for each page
    probability = damping_factor / len(corpus[page])

    # Get the probability of choosing randomly among all pages
    remainder = (1 - damping_factor) / len(corpus)

    # Assigning the probabilities
    for p in corpus :
        pages_probabilities[p] = remainder + probability if p in corpus[page] else remainder
    
    return pages_probabilities


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    results = {}

    # Initializing the current results to 0
    for page in corpus :
        results[page] = 0
        
    # first randomly choose a page
    page = random.choice(list(corpus.keys()))
    results[page] = 1 

    for g in range(1, n):
        p_dist = transition_model(corpus, page, damping_factor)
        # based on the old distribution get a new page
        page = random.choices(list(p_dist.keys()), list(p_dist.values()), k=1)[0]
        results[page] += 1
        
    # Normalize the results
    for page in results:
        results[page] /= n
    
    return results 


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    N = len(corpus)

    # 1 / N
    starting_rank = 1 / N

    # Assigning each page the starting_rank
    page_ranks = {}

    for page in corpus :
        page_ranks[page] = starting_rank

    run = True

    while run:
        count = 0
        for page in corpus:
            page_rank = (1 - damping_factor) / N
            sigma = 0
            for i in corpus:
                if page in corpus[i]:
                    num_links = len(corpus[i])
                    sigma = sigma + page_ranks[i] / num_links
            sigma = damping_factor * sigma
            page_rank += sigma
            if abs(page_rank - page_ranks[page]) < 0.00001:
                count += 1
            # If the difference is less than the threshold
            # Assign the new page_rank
            page_ranks[page] = page_rank
            if count == N:
                run = False
                break

    return page_ranks

if __name__ == "__main__":
    main()
