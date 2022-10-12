import csv
import itertools
import sys
import math

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """

    people_probabilities = [] # The values of the set will be multiplied altogether in the end
    for person in people:
        number_genes = 1 if person in one_gene else 2 if person in two_genes else 0 # 0, 1 or 2
        has_trait = True if person in have_trait else False # True or False
        person_probability = 0

        # Person is a parent :
        if not people[person]['mother'] or not people[person]['father']:
            # Get the probabilities from the PROBS
            person_probability = PROBS["gene"][number_genes] * PROBS["trait"][number_genes][has_trait]
            # Add it to the probabilities list
            people_probabilities.append(person_probability)
            continue
        # Person is child
        else :
            # Child's parents
            father = people[person]['father']
            mother = people[person]['mother']

            father_number_genes = 1 if father in one_gene else 2 if father in two_genes else 0
            mother_number_genes = 1 if mother in one_gene else 2 if mother in two_genes else 0

            # The probabilities of passing the gene by number of genes
            prob_parent_give_gene = {
                0: 0.01,
                1: 0.49,
                2: 0.99
            }

            # To get the probability of a child who has 0 genes
            # There's only one scenario, none of the parents will give the gene
            if number_genes == 0:
                person_probability = (1 - prob_parent_give_gene[father_number_genes]) * (1 - prob_parent_give_gene[mother_number_genes])
            # In the case of a gene there's two scenarios :
            # The father giving the gene or the mother giving the gene
            elif number_genes == 1:
                # If the father is giving the gene :
                person_probability = prob_parent_give_gene[father_number_genes] * (1 - prob_parent_give_gene[mother_number_genes])

                # If the mother is giving the gene :
                person_probability += (1 - prob_parent_give_gene[father_number_genes]) * prob_parent_give_gene[mother_number_genes]
            # In the case of two genes there's only one scenario
            # Both parents giving one gene
            else :
                person_probability = prob_parent_give_gene[father_number_genes] * prob_parent_give_gene[mother_number_genes]

            person_probability = person_probability * PROBS["trait"][number_genes][has_trait]
            people_probabilities.append(person_probability)
            continue

    return math.prod(people_probabilities)


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """

    # For each person
    for person in probabilities:
        number_genes = 1 if person in one_gene else 2 if person in two_genes else 0 # 0, 1 or 2
        has_trait = True if person in have_trait else False # True or False
        probabilities[person]["gene"][number_genes] += p
        probabilities[person]["trait"][has_trait] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        for distribution in probabilities[person]:
            # Get the total value to be able to get the proportions
            sigma = sum(probabilities[person][distribution].values())
            # Go over each value to change it based on its proportion
            for value in probabilities[person][distribution]:
                probabilities[person][distribution][value] = probabilities[person][distribution][value] / sigma


if __name__ == "__main__":
    main()
