import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """

    evidence = list()
    labels = list()

    with open(filename) as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader, None) # Skipping the headers
        for row in csvreader:
            e = list()

            # Administrative as an int
            e.append(int(row[0]))

            # Administrative_Duration as a float
            e.append(float(row[1]))

            # Informational as an integer
            e.append(int(row[2]))

            # Informational_Duration as an float
            e.append(float(row[3]))

            # ProductRelated as an integer
            e.append(int(row[4]))

            # ProductRelated_Duration as a float
            e.append(float(row[5]))

            #BounceRates as a float
            e.append(float(row[6]))

            # ExitRates as a float
            e.append(float(row[7]))

            #PageValues, a floating point number
            e.append(float(row[8]))

            # - SpecialDay, a floating point number
            e.append(float(row[9]))

            # - Month, an index from 0 (January) to 11 (December)
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

            e.append(months.index(row[10]))

            # - OperatingSystems, an integer
            e.append(int(row[11]))

            # - Browser, an integer
            e.append(int(row[12]))

            # - Region, an integer
            e.append(int(row[13]))

            # - TrafficType, an integer
            e.append(int(row[14]))

            # - VisitorType, an integer 0 (not returning) or 1 (returning)
            e.append(1 if row[15].lower() == "returning_visitor" else 0)

            # - Weekend, an integer 0 (if false) or 1 (if true)
            e.append(0 if row[16] == "FALSE" else 1)

            # Add the row to the evidence list
            evidence.append(e)

            labels.append(1 if row[17] == "TRUE" else 0)

    return (evidence, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    neigh = KNeighborsClassifier(n_neighbors=1) # k = 1

    return neigh.fit(evidence, labels)


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    true_positive_count, true_negative_count = 0, 0
    total_positives, total_negatives = 0, 0

    for i in range(len(labels)):
        if labels[i] == predictions[i] and labels[i] == 1:
            true_positive_count += 1
            total_positives += 1
        elif labels[i] == predictions[i] and labels[i] == 0:
            true_negative_count += 1
            total_negatives += 1
        elif labels[i] == 1:
            total_positives += 1
        elif labels[i] == 0:
            total_negatives += 1

    sensitivity = true_positive_count / total_positives
    specificity = true_negative_count / total_negatives

    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
