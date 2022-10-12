import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """

        # Going over the variables
        # Removing the values that are not consistent with the variable's unary constraints
        for variable in self.domains:
            variable_domains = self.domains[variable].copy()

            # Going over the values of each variable
            for value in variable_domains:
                # Making sure that every value in its domain has the same number of letters as the variable's length
                if not variable.length == len(value):
                    # Remove the value
                    self.domains[variable].remove(value)
        return

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # Get the overlaps between the two variables
        overlaps = self.crossword.overlaps[x, y]
        if not overlaps:
            return False

        # Keep track of the values removed
        revisions = 0

        x_domains = self.domains[x].copy()
        y_domains = self.domains[y].copy()

        # Go over each value of x to see if it's
        for value in x_domains:
            for value_y in y_domains:
                if value[overlaps[0]] == value_y[overlaps[1]]:
                    break
            else:
                self.domains[x].remove(value)
                revisions += 1

        return True if revisions else False # Return false if no revisions were made to x

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        queue = list()

        if not arcs:
            # Get all the arcs in the problem
            # Go over each variable in the problem and get the list of neighbors
            # Each arc will consist of the variable and its neighbors
            for variable in self.crossword.variables:
                variable_neighbors = self.crossword.neighbors(variable)
                for neighbor in variable_neighbors:
                    queue.append((variable, neighbor))
        else:
            queue = arcs

        # Revising each arc in the queue
        while len(queue):
            x, y = queue.pop(0) # Dequeueing
            if self.revise(x, y):
                if not len(self.domains[x]):
                    return False
                for z in self.crossword.neighbors(x):
                    if z == y :
                        continue # Skip the current neighbor
                    queue.append((z, x)) # Enqueueing
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # Check if all the variables are in the dict
        check_all_variables = all(item in assignment for item in self.crossword.variables)

        if not check_all_variables:
            return False

        # Check if all the variables have a value assigned to them
        for value in assignment.values():
            if not isinstance(value, str):
                return False

        # All the tests has passed, assignment over
        return True
    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        # list that will keep track of values for duplicates
        unique_values = []

        for variable in assignment:
            value = assignment[variable]
            # Values are the correct length
            if not len(value) == variable.length:
                return False
            # Check that values are distinct
            if value in unique_values:
                return False
            unique_values.append(value)
            # No conflicts between the variables
            # Go over each value get its neighbors and compare the letters in which they intersect
            for neighbor in self.crossword.neighbors(variable):
                # Get the overlap
                i, j = self.crossword.overlaps[variable, neighbor]
                # Check if the characters are the same
                # TODO:  the neighbor might not be in the assignment
                # if the neighbor is in the assignment and the two letters don't match then return False
                if neighbor in assignment:
                    if not value[i] == assignment[neighbor][j]:
                        return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        var_dict = dict()

        # Going over the values for the var
        for value in self.domains[var]:
            if value in assignment.values():
                continue
            # get the neighbors of the var to see how many values it rules out
            for neighbor in self.crossword.neighbors(var):
                if value in self.domains[neighbor]:
                    if value in var_dict.keys():
                        var_dict[value] += 1
                    else:
                        var_dict[value] = 1

        # converting to list of tuples for sorting
        var_heuristic_list = [(k, v) for k, v in var_dict.items()]

        # Sorting the list
        var_heuristic_list.sort(key=lambda item: item[1])

        ordered_domain_values = []

        for item in var_heuristic_list:
            ordered_domain_values.append(item[0])

        return ordered_domain_values

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        variable_domains_length = []

        for variable in self.domains:
            if variable in assignment:
                continue
            variable_domains_length.append({"variable": variable, "domain_length": len(self.domains[variable])})

        # Sort the list by domain length
        sorted_list = sorted(variable_domains_length, key= lambda x : x["domain_length"])

        return sorted_list[0]["variable"]


    # The inference function that will be used in the backtrack algo
    def inference(self, assignment, x):

        # The queue that will be given to the ac3 algo
        queue = list()

        # Get the neighbors
        for y in self.crossword.neighbors(x):
            queue.append((y, x))

        # enforce arc consistency
        if self.ac3(queue):
            inferences = dict()
            for var in self.domains:
                if len(self.domains[var]) == 1 and not var in assignment:
                    inferences[var] = list(self.domains[var])[0]
            return inferences if len(inferences) else False
        # Return fail if no changes were made to the domain
        return False


    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # Assigment complete
        if self.assignment_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)

        for value in self.domains[var]:
            if self.consistent(assignment):
                assignment[var] = value
                inferences = self.inference(assignment, var)
                if not inferences == False:
                    for inference in inferences:
                        assignment[inference] = inferences[inference]
                result = self.backtrack(assignment)
                if not result == None:
                    return result
                del assignment[var]
                if not inferences == False:
                    for inference in inferences:
                        del assignment[inference]
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
