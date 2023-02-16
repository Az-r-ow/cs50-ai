import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | NP VP CP | NP
PP -> P NP | P
CP -> Conj NP VP | Conj VP NP
NP -> Det N Adv | Det N PP | Det Adj N | Det N | Adj N | N
VP -> Adv V NP | V Adv CP | V PP | V | V NP | V PP 
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    tokenized_sentence = nltk.tokenize.word_tokenize(sentence.lower())
    for word in tokenized_sentence:
        if not word.isalpha():
            tokenized_sentence.remove(word)

    return tokenized_sentence

    
def np_chunk(tree, nps = []):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    nps = []
    
    for position in tree.treepositions():
        # Skip if the element is a value
        if type(tree[position]) is str:
            continue
        else:
            if tree[position].label() == "NP":    
                hasNP = False
                for leaf in tree[position]:
                    if leaf.label() == "NP":
                        hasNP = True
                        break
                if not hasNP:
                    nps.append(tree[position])
    return nps          
                    

if __name__ == "__main__":
    main()
