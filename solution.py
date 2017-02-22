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

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins


    # Create row/column/square/diag dictionaries to store naked twins for each box
    naked_twins_row = dict()
    naked_twins_column = dict()
    naked_twins_square = dict()
    naked_twins_diag = dict()

    # For boxes with exactly 2 digits, look for (and store) naked twins among row/column/square/diag peers
    for box in boxes:
        if len(values[box]) == 2:
            for rp in rpeers[box]:
                if values[box] == values[rp]:
                    naked_twins_row[box] = rp
                    break
            for cp in cpeers[box]:
                if values[box] == values[cp]:
                    naked_twins_column[box] = cp
                    break
            for sp in speers[box]:
                if values[box] == values[sp]:
                    naked_twins_square[box] = sp
                    break
            for dp in dpeers[box]:
                if values[box] == values[dp]:
                    naked_twins_diag[box] = dp
                    break


    # Eliminate the naked twins as possibilities for their peers


    # For each box that has a naked twin, remove the 2 digits in all row/column/square/diag peers (excluding the naked twin)
    for box in boxes:
        if box in naked_twins_row:
            for digit in values[box]:
                for rp in rpeers[box]:
                    if rp != naked_twins_row[box]:
                        values[rp] = values[rp].replace(digit,'')
        if box in naked_twins_column:
            for digit in values[box]:
                for cp in cpeers[box]:
                    if cp != naked_twins_column[box]:
                        values[cp] = values[cp].replace(digit,'')
        if box in naked_twins_square:
            for digit in values[box]:
                for sp in speers[box]:
                    if sp != naked_twins_square[box]:
                        values[sp] = values[sp].replace(digit,'')
        if box in naked_twins_diag:
            for digit in values[box]:
                for dp in dpeers[box]:
                    if dp != naked_twins_diag[box]:
                        values[dp] = values[dp].replace(digit,'')

    return values

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

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
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values):
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
    "Using depth-first search and propagation, try all possible values."
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

# Define some of the global variables that are used in the methods

rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diag_units = [[rows[i]+cols[i] for i in range(len(rows))], [rows[-i-1]+cols[i] for i in range(len(rows))]]
unitlist = row_units + column_units + square_units + diag_units

runits = dict((s, [u for u in row_units if s in u]) for s in boxes)
rpeers = dict((s, set(sum(runits[s],[]))-set([s])) for s in boxes)
cunits = dict((s, [u for u in column_units if s in u]) for s in boxes)
cpeers = dict((s, set(sum(cunits[s],[]))-set([s])) for s in boxes)
sunits = dict((s, [u for u in square_units if s in u]) for s in boxes)
speers = dict((s, set(sum(sunits[s],[]))-set([s])) for s in boxes)
dunits = dict((s, [u for u in diag_units if s in u]) for s in boxes)
dpeers = dict((s, set(sum(dunits[s],[]))-set([s])) for s in boxes)
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
