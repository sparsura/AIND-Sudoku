import logging
from initvars import *

assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def init_naked_twins():
    """Initialize all naked_twins diectionaries.
    """

    global naked_twins_row
    global naked_twins_column
    global naked_twins_square
    global naked_twins_diag

    # Initialize row/column/square/diag dictionaries
    naked_twins_row = dict()
    naked_twins_column = dict()
    naked_twins_square = dict()
    naked_twins_diag = dict()

def find_naked_twins(values):
    """Find all instances of naked twins.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    """

    # For boxes with exactly 2 digits, look for (and store) naked twins among row/column/square/diag peers
    for box in boxes:
        if len(values[box]) == 2:
            # Scan row peers for a possible naked twin
            for rp in rpeers[box]:
                if values[box] == values[rp]:
                    naked_twins_row[box] = rp
                    break
            # Scan column peers for a possible naked twin
            for cp in cpeers[box]:
                if values[box] == values[cp]:
                    naked_twins_column[box] = cp
                    break
            # Scan square peers for a possible naked twin
            for sp in speers[box]:
                if values[box] == values[sp]:
                    naked_twins_square[box] = sp
                    break
            # Scan diagonal peers for a possible naked twin
            for dp in dpeers[box]:
                if values[box] == values[dp]:
                    naked_twins_diag[box] = dp
                    break

def eliminate_naked_twins_in_peers(values):
    """Eliminate all instances of naked twins in peers.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    """

    # For each box that has a naked twin, remove the 2 digits in all row/column/square/diag peers (excluding the naked twin)
    for box in boxes:
        if box in naked_twins_row:
            # Check each peer for the 2 digits contained in the box
            for digit in values[box]:
                for rp in rpeers[box]:
                    # Remove the digit from the peer unless its the naked twin of the box
                    if rp != naked_twins_row[box]:
                        values[rp] = values[rp].replace(digit,'')
        if box in naked_twins_column:
            # Check each peer for the 2 digits contained in the box
            for digit in values[box]:
                for cp in cpeers[box]:
                    # Remove the digit from the peer unless its the naked twin of the box
                    if cp != naked_twins_column[box]:
                        values[cp] = values[cp].replace(digit,'')
        if box in naked_twins_square:
            # Check each peer for the 2 digits contained in the box
            for digit in values[box]:
                for sp in speers[box]:
                    # Remove the digit from the peer unless its the naked twin of the box
                    if sp != naked_twins_square[box]:
                        values[sp] = values[sp].replace(digit,'')
        if box in naked_twins_diag:
            # Check each peer for the 2 digits contained in the box
            for digit in values[box]:
                for dp in dpeers[box]:
                    # Remove the digit from the peer unless its the naked twin of the box
                    if dp != naked_twins_diag[box]:
                        values[dp] = values[dp].replace(digit,'')


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Initialize all naked_twins dictionaries
    init_naked_twins()

    # Find all instances of naked twins
    find_naked_twins(values)

    # Eliminate the naked twins as possibilities for their peers
    eliminate_naked_twins_in_peers(values)

    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """

    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """

    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print

def eliminate(values):
    """
    Go through all the boxes, and whenever there is a box with a value, eliminate this value from the values of all its peers.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """

    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """

    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """

    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)

        # Invoke the naked_twins strategy
        values = naked_twins(values)

        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    """Using depth-first search and propagation, try all possible values.
    """

    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

    # Convert the string to a properly initialized dictionary
    values = grid_values(grid)

    # Invoke the search method which alternates between the three techniques and DFS to solve the puzzle
    values = search(values)

    # Update the assignments list to test visualization
    # Do this before changing all assignments in the program to use assign_value instead of directly updating boxes
    # This is not working - I see a blank window - known issue as per the forums
    for k,v in values.items():
        values = assign_value(values,k,v)
    return values


if __name__ == '__main__':

    # Set logging level to ERROR
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)

    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    # Log error if the length of the sudoku grid is not 81
    len_dsg = len(diag_sudoku_grid)
    if len_dsg != 81:
        logger.error('ERROR: %s length is %d.  It should be 81.' % ("diag_sudoku_grid", len_dsg))
        exit()

    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
