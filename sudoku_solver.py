import re

def cross(A, B):
    return [a + b for a in A for b in B]

digits = '123456789'
rows = 'ABCDEFGHI'
cols = digits
squares = cross(rows, cols)

# Create units (rows, columns, and boxes)
unitlist = ([cross(rows, c) for c in cols] +
            [cross(r, cols) for r in rows] +
            [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])

# Create units and peers dictionaries
units = dict((s, [u for u in unitlist if s in u]) for s in squares)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in squares)

def parse_grid(grid):
    """Convert grid to a dict of possible values, {square: digits}, or return False if a contradiction is detected."""
    # Initialize values with all digits
    values = dict((s, digits) for s in squares)
    # Assign values from the grid to the values dict
    for s, d in grid_values(grid).items():
        if d in digits:
            if not assign(values, s, d):
                return False  # Contradiction detected
    return values

def grid_values(grid):
    """Convert grid string into a dict of {square: char} with '0' or '.' for empties."""
    chars = [c for c in grid if c in digits or c in '0.']
    assert len(chars) == 81, "Input grid must be a string of length 81 (digits, dots, or zeros)."
    return dict(zip(squares, chars))

def assign(values, s, d):
    """Eliminate all other values (except d) from values[s] and propagate.
    Return values, or False if a contradiction is detected."""
    other_values = values[s].replace(d, '')
    if all(eliminate(values, s, d2) for d2 in other_values):
        return values
    else:
        return False  # Contradiction detected

def eliminate(values, s, d):
    """Eliminate d from values[s]; propagate when values or places <= 1.
    Return values, or False if a contradiction is detected."""
    if d not in values[s]:
        return values  # Already eliminated
    values[s] = values[s].replace(d, '')
    # If a square is reduced to zero digits, contradiction
    if len(values[s]) == 0:
        return False
    # If a square is reduced to one digit, eliminate it from peers
    elif len(values[s]) == 1:
        d2 = values[s]
        if not all(eliminate(values, s2, d2) for s2 in peers[s]):
            return False
    # If a unit is reduced to only one place for a digit, assign it there
    for u in units[s]:
        dplaces = [s2 for s2 in u if d in values[s2]]
        if len(dplaces) == 0:
            return False  # Contradiction: no place for this digit
        elif len(dplaces) == 1:
            if not assign(values, dplaces[0], d):
                return False
    return values

def reduce_puzzle(values):
    """Iteratively apply eliminate and only choice strategies."""
    stalled = False
    while not stalled:
        # Keep track of solved boxes before reduction
        solved_values_before = len([s for s in squares if len(values[s]) == 1])
        # Apply the eliminate strategy
        values = eliminate_strategy(values)
        if values is False:
            return False  # Contradiction detected
        # Apply the only choice strategy
        values = only_choice(values)
        if values is False:
            return False  # Contradiction detected
        # Keep track of solved boxes after reduction
        solved_values_after = len([s for s in squares if len(values[s]) == 1])
        # Check if any progress was made
        stalled = solved_values_before == solved_values_after
        # If a box has no possible values, return False
        if any(len(values[s]) == 0 for s in squares):
            return False
    return values

def eliminate_strategy(values):
    """Apply the eliminate strategy."""
    solved_values = [s for s in squares if len(values[s]) == 1]
    for s in solved_values:
        d = values[s]
        for s2 in peers[s]:
            if d in values[s2]:
                values[s2] = values[s2].replace(d, '')
                if len(values[s2]) == 0:
                    return False  # Contradiction detected
    return values

def only_choice(values):
    """Apply the only choice strategy."""
    for unit in unitlist:
        for d in digits:
            dplaces = [s for s in unit if d in values[s]]
            if len(dplaces) == 0:
                return False  # Contradiction detected
            elif len(dplaces) == 1:
                if len(values[dplaces[0]]) > 1:
                    if not assign(values, dplaces[0], d):
                        return False
    return values

def search(values):
    """Using depth-first search and constraint propagation."""
    # First, reduce the puzzle
    values = reduce_puzzle(values)
    if values is False:
        return False  # Failed earlier
    if all(len(values[s]) == 1 for s in squares):
        return values  # Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n, s = min((len(values[s]), s) for s in squares if len(values[s]) > 1)
    # Try each possible value recursively
    for d in values[s]:
        new_values = values.copy()
        new_values[s] = d
        attempt = search(new_values)
        if attempt:
            return attempt
    return False

def solve(grid):
    """Solve the Sudoku puzzle."""
    values = parse_grid(grid)
    if values is False:
        print("Puzzle is invalid.")
        return False
    solution = search(values)
    if solution:
        return solution
    else:
        print("Puzzle is unsolvable.")
        return False

def validate_sudoku(grid):
    """Validate the input grid string."""
    if not re.match(r'^[0-9.]{81}$', grid):
        return False
    return True

def display(values):
    """Display the Sudoku grid."""
    width = 1 + max(len(values[s]) for s in squares)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF':
            print(line)
    print()

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    if validate_sudoku(diag_sudoku_grid):
        solution = solve(diag_sudoku_grid)
        if solution:
            display(solution)
    else:
        print("Invalid Sudoku puzzle input.")
