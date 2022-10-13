import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if self.count == len(self.cells):
            return self.cells
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # Remove that cell from the sentence
        # Reduce the number of mine counts by one
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
        return


    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)
        return


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)
            self.mines.add(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)
            self.safes.add(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # Marking the cell as a move
        self.moves_made.add(cell)
        # Marking the cell as safe
        self.safes.add(cell)

        # Updating the sentences that contain the cell
        for sentence in self.knowledge:
            if cell in sentence.cells:
                sentence.cells.remove(cell)

        neighbors = [(-1,-1), (-1,0), (-1,1), (0,1), (1,1), (1,0), (1,-1), (0,-1)]
        cells = set()
        # Creating a new sentence with the cells neighbors
        for x, y in neighbors:
            if (cell[0] + x >= 0 and cell[0] + x < self.height) and (cell[1] + y >= 0 and cell[1] + y < self.width):
                neighbor_cell = (cell[0] + x, cell[1] + y)
                # Check if the cell has
                if not neighbor_cell in self.moves_made:
                    cells.add(neighbor_cell)
                    # If the count of the cell is 0 ulitmately all the cells around it are safe
                    if count == 0:
                        self.safes.add(neighbor_cell)

        # Add this new sentence to the knowledge base
        sentence = Sentence(cells, count)
        self.knowledge.append(sentence)

        # New sentences that have been inferred
        new_sentences = []

        # Checking the sentences
        for sentence in self.knowledge:
            # If a cell in a sentence can be marked as a mine
            if len(sentence.known_mines()) != 0:
                mines = set()
                for mine in sentence.known_mines():
                    mines.add(mine)
                for mine in mines:
                    sentence.mark_mine(mine)

            # If a cell in a sentence can be marked as safe
            if len(sentence.known_safes()) != 0:
                safes = set()
                for safe in sentence.known_safes():
                    safes.add(safe)
                for safe in safes:
                    sentence.mark_safe(safe)

            # If new sentences can be inferred
            for i in range(len(self.knowledge)):
                if sentence.cells == self.knowledge[i].cells:
                    # Skip the senctence itself
                    continue
                # Sentence is subset of another sentence
                if sentence.cells.issubset(self.knowledge[i].cells) and len(sentence.cells) != 0:
                    # Create a new sentence from the unique values
                    cells = self.knowledge[i].cells - sentence.cells
                    count = self.knowledge[i].count - sentence.count
                    new_sentence = Sentence(cells, count)
                    if new_sentence in self.knowledge:
                        continue
                    new_sentences.append(new_sentence)

        # Adding the new sentences that has been inferred to the knowledge base
        for sentence in new_sentences:
            self.knowledge.append(sentence)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # If there's known safe cells return one of them that hasn't been made
        if len(self.safes) != 0:
            for cell in self.safes:
                if not cell in self.moves_made:
                    return cell
        return None


    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        cells = []
        # Creating a list of all the cells in the board excluding :
        # The cells that has been checked
        # The cells that are mines
        for row in range(self.height):
            for col in range(self.width):
                cell = (row, col)
                # Make sure the cell has not already been checked and that it's not a mine
                if cell not in self.moves_made and cell not in self.mines:
                    cells.append(cell)
        if len(cells) != 0:
            return random.choice(cells)
        else:
            return None
