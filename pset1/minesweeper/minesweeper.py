import itertools
import random
import copy

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
        If count is equal to count of cells in the sentence, all the mines in the sentence are mines.
        """
        if self.count == len(self.cells):
            return self.cells
        else:
            return set()


    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        If count is 0, all the mines in the sentence are safe.
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
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


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

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

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


       
    # 1) mark the cell as a move that has been made
        self.moves_made.add(cell)

    # 2) mark the cell as safe
        self.mark_safe(cell)
        
    # 3) add a new sentence to the AI's knowledge base, based on the value of `cell` and `count`
        neighbours = []
        for i in range(3):
            for j in range(3):

                x = cell[0]-1+i
                y = cell[1]-1+j

                # Find any neigbouring cell, that's on the board

                cellItself = (i == 1 and j == 1)
                xInArea = 0 <= x < self.height
                yInArea = 0 <= y < self.width

                if xInArea and yInArea and not(cellItself):
                    if (x, y) in self.mines:
                        count -= 1
                    elif (x, y) not in self.safes:
                        neighbours.append((x, y))

        # Add the new sentence to the KB
        self.knowledge.append(Sentence(neighbours, count))

        
    # 4) mark any additional cells as safe or as mines 
    #       if it can be concluded based on the AI's knowledge base
        

        # Make a copy of our knowledge, because we're going to edit our knowledge while iterating
        IterateKnowledge = copy.deepcopy(self.knowledge)

        # Iterate the current knowledge to look for new found mines and safes
        for sentence in IterateKnowledge:
            mines = sentence.known_mines()
            safes = sentence.known_safes()
            if(safes):
                self.safes = self.safes.union(safes)
            if(mines):
                self.mines = self.mines.union(mines)
        
    # 5) add any new sentences to the AI's knowledge base
    #       if they can be inferred from existing knowledge


        # Make a copy of our knowledge, because we're going to edit our knowledge while iterating
        IterateKnowledge = copy.deepcopy(self.knowledge)

        # Iterate through our KB to compare every sentence with our new sentence "sentence2"
        for sentence1 in IterateKnowledge:
            sentence2 = Sentence(neighbours, count)

            # Compare both sentences and look if we can derive new knowledge from them.
            if sentence2.cells and sentence1.cells != sentence2.cells:
                if sentence1.cells.issubset(sentence2.cells):

                    CELL = sentence2.cells-sentence1.cells
                    COUNT = sentence2.count-sentence1.count
                    NEW_SENTENCE = Sentence( CELL , COUNT )

                    self.knowledge.append(NEW_SENTENCE)

                if sentence2.cells.issubset(sentence1.cells):

                    CELL = sentence1.cells-sentence2.cells
                    COUNT = sentence1.count-sentence2.count
                    NEW_SENTENCE =Sentence( CELL , COUNT )

                    self.knowledge.append(NEW_SENTENCE)

        # Make a copy of our knowledge, because we're going to edit our knowledge while iterating
        IterateKnowledge = copy.deepcopy(self.knowledge)

        # Remove empty sentences from our KB
        for sentence in IterateKnowledge:
            if sentence.cells == set():
                self.knowledge.remove(sentence)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
       
        for safe in self.safes:
            if safe not in self.moves_made:
                print(safe)
                return safe
        return None
        

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        
        possibleMoves = []
        for i in range(self.height):
            for j in range(self.width):
                cell = (i, j)
                UniqueMove = cell not in self.moves_made
                NotAMine = cell not in self.mines

                if UniqueMove and NotAMine:
                    return cell

        if possibleMoves != []:
            move = possibleMoves[random.randrange(len(possibleMoves))]
            print (move)
            return move
        else:
            return None

        
