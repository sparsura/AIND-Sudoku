""" Initialize the global variables."""

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diag_units = [[r+c for r,c in zip(rows,cols)], [r+c for r,c in zip(rows,cols[::-1])]]
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

naked_twins_row = dict()
naked_twins_column = dict()
naked_twins_square = dict()
naked_twins_diag = dict()
