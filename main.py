from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.circuit.library import DiagonalGate
import math
import random

def create_oracle(line_data):
    """
    Creates the 'bomb' oracle for a given line (row or column).

    This oracle marks the states corresponding to ship locations with a 
    negative phase (i.e., applies a Z gate).
    
    Args:
        line_data (list): A list of 0s (miss) and 1s (ship).
    
    Returns:
        qiskit.circuit.Gate: The oracle gate.
    """
    if not line_data:
        # Handle empty line data
        return DiagonalGate([1])
        
    n_qubits = math.ceil(math.log2(len(line_data)))
    if n_qubits == 0: # Happens if len(line_data) == 1
        n_qubits = 1
    
    # Create a diagonal matrix for the phase flip.
    # Start with all 1s (no phase flip).
    phases = [1] * (2**n_qubits)
    
    # Add -1 (phase flip) for each 'ship' location
    for i, has_ship in enumerate(line_data):
        if has_ship:
            if i < len(phases):
                phases[i] = -1
                
    return DiagonalGate(phases)
    


def quantum_scan_line(line_data, draw=False):
    """
    Performs a single "Interaction-Free" quantum scan on a line.
    
    This circuit uses H-Oracle-H (Grover's search) to detect the *presence*
    of a ship without needing to know *which* square it's in.
    
    - If the measurement is |00...0>, no ship is present (MISS).
    - If the measurement is anything else, a ship is present (DETECT).
    
    Args:
        line_data (list): A list of 0s (miss) and 1s (ship).
        
    Returns:
        str: "DETECT" or "MISS"
    """
    # Handle empty or single-item lines
    if not line_data:
        return "MISS" # Cannot scan an empty line
        
    # Determine number of qubits needed to represent the line
    n_qubits = math.ceil(math.log2(len(line_data)))
    if n_qubits == 0: # Happens if len(line_data) == 1
        n_qubits = 1

    # --- Build the Circuit ---
    qc = QuantumCircuit(n_qubits, n_qubits)
    
    # 1. Create superposition of all positions
    qc.h(range(n_qubits))
    
    # 2. Apply the "bomb" oracle
    oracle = create_oracle(line_data)
    qc.append(oracle, range(n_qubits))
    
    # 3. Apply interference
    qc.h(range(n_qubits))
    
    # 4. Measure
    qc.measure(range(n_qubits), range(n_qubits))
    
    if draw:
        print(qc.draw())
        return qc
    
    # --- Simulate ---
    # We use multiple shots for a more reliable probabilistic result.
    SHOTS = n_qubits + 1
    simulator = AerSimulator()
    t_qc = transpile(qc, simulator)
    result = simulator.run(t_qc, shots=SHOTS).result()
    counts = result.get_counts()
    
    # --- Interpret Result ---
    # The "MISS" state is '00...0'
    zero_state = '0' * n_qubits
    
    # Get the number of times we measured the "MISS" state
    miss_counts = counts.get(zero_state, 0)
    
    # If the number of "MISS" counts is less than the total shots,
    # it means we must have measured *something else* at least once.
    if miss_counts < SHOTS:
        # Measuring *any* other state is a "DETECT"
        return "DETECT"
    else:
        # Only if all 100 shots were '00...0' do we call it a "MISS"
        return "MISS"

# --- Game Logic ---

def create_board(size, ship_list):
    """Creates a simple game board."""
    board = [[0 for _ in range(size)] for _ in range(size)]
    for (r, c) in ship_list:
        if 0 <= r < size and 0 <= c < size:
            board[r][c] = 1
    return board, set(ship_list)

def print_board(board, title=""):
    """Helper function to print the board."""
    print(f"\n--- {title} ---")
    size = len(board)
    
    # Print column headers
    header = "  | " + " | ".join([str(i) for i in range(size)]) + " |"
    print(header)
    print(" " + " -" * (size * 2 + 1))
    
    # Print rows
    for i, row in enumerate(board):
        row_str = " | ".join(map(str, row))
        print(f"{i} | {row_str} |")
    print(" " + " -" * (size * 2 + 1))


def place_ships(size, ship_lengths):
    """
    Randomly places ships of given lengths onto a board of given size.
    
    Args:
        size (int): The width and height of the board.
        ship_lengths (list): A list of integers, where each is the length of a ship.
        
    Returns:
        set: A set of (row, col) tuples representing all ship coordinates.
    """
    ship_coords = set()
    max_retries = 100 # Avoid infinite loops

    for length in ship_lengths:
        placed = False
        for _ in range(max_retries):
            orientation = random.choice(['horizontal', 'vertical'])
            
            # Choose a random starting position
            if orientation == 'horizontal':
                r = random.randint(0, size - 1)
                c = random.randint(0, size - length)
            else: # vertical
                r = random.randint(0, size - length)
                c = random.randint(0, size - 1)
                
            # Check for overlap and bounds
            new_ship = set()
            valid_placement = True
            for i in range(length):
                if orientation == 'horizontal':
                    coord = (r, c + i)
                else:
                    coord = (r + i, c)
                
                # Check overlap
                if coord in ship_coords:
                    valid_placement = False
                    break
                new_ship.add(coord)
            
            if valid_placement:
                ship_coords.update(new_ship)
                placed = True
                break # Move to next ship
        
        if not placed:
            print(f"Warning: Could not place ship of length {length}. Board may be too full.")

    return ship_coords


def play_quantum_battleship(SIZE = 8, SHIP_LENGTHS = [4, 3, 3, 2]):
    """Main game simulation loop."""
    
    SHIP_COORDS = place_ships(SIZE, SHIP_LENGTHS)
    
    if not SHIP_COORDS:
        print("Error: No ships were placed. Exiting.")
        return
    
    hidden_board, ship_set = create_board(SIZE, SHIP_COORDS)
    
    # '?' = Unknown, 'O' = Miss, 'D' = Detected Line, 'X' = Confirmed Hit
    known_board = [['?' for _ in range(SIZE)] for _ in range(SIZE)]
    
    print("Welcome to Quantum Battleship!")
    print(f"Board size: {SIZE}x{SIZE}")
    print(f"Ships to find: {len(ship_set)} (from {len(SHIP_LENGTHS)} ships)")
    print_board(hidden_board, "HIDDEN BOARD (FOR DEBUG)")
    print_board(known_board, "YOUR RADAR VIEW")

    row_status = ['?'] * SIZE
    col_status = ['?'] * SIZE
    total_quantum_scans = 0

    # 2. Phase 1: Quantum Scanning
    print("\n--- Phase 1: Quantum Scanning ---")

    print("Using Quantum Circuit : ")
    quantum_scan_line(hidden_board[0], draw=True)
    
    # Scan Rows
    print("Scanning all rows...")
    for r in range(SIZE):
        row_data = hidden_board[r]
        row_status[r] = quantum_scan_line(row_data)
        total_quantum_scans += 1
        print(f"Row {r} scan result: {row_status[r]}")
        
        # Update known board with 'MISS' info
        if row_status[r] == "MISS":
            for c in range(SIZE):
                known_board[r][c] = 'O'
                
    # Scan Columns
    print("\nScanning all columns...")
    for c in range(SIZE):
        # Create column data
        col_data = [hidden_board[r][c] for r in range(SIZE)]
        col_status[c] = quantum_scan_line(col_data)
        total_quantum_scans += 1
        print(f"Col {c} scan result: {col_status[c]}")
        
        # Update known board with 'MISS' info
        if col_status[c] == "MISS":
            for r in range(SIZE):
                known_board[r][c] = 'O'
                
    print_board(known_board, "RADAR VIEW AFTER ALL SCANS")

    # 3. Phase 2: Classical Pinpointing (The "Hits")
    print("\n--- Phase 2: Classical Pinpointing --- ", end="")
    
    candidates = []
    for r in range(SIZE):
        for c in range(SIZE):
            # A candidate is any square that hasn't been ruled out
            # AND is at the intersection of a DETECTED row and column
            if (row_status[r] == "DETECT" and 
                col_status[c] == "DETECT" and 
                known_board[r][c] == '?'):
                
                candidates.append((r, c))
                known_board[r][c] = 'C' # Mark as Candidate

    print(f"Identified {len(candidates)} candidate(s) for classical probing.")
    print_board(known_board, "CANDIDATE VIEW")

    # This is the "E.V. Score"
    total_hits = 0
    ships_found = 0

    for (r, c) in candidates:
        print(f"Classically probing candidate at ({r}, {c})... ", end="")
        total_hits += 1 # This is a "HIT" in the E.V. score
        
        if (r, c) in ship_set:
            print("SUCCESSFUL HIT!")
            known_board[r][c] = 'X'
            ships_found += 1
        else:
            print("Final Miss.")
            known_board[r][c] = 'O'
            
    # 4. Final Report
    print("\n--- GAME OVER ---")
    print_board(known_board, "FINAL BOARD")
    
    print("--- STATISTICS ---")
    print(f"Total Quantum Scans: {total_quantum_scans}")
    print(f"Ships Found:         {ships_found} / {len(ship_set)}")
    print(f"Elitzur-Vaidman (E.V.) Score (Total 'Hits'): {total_hits / (SIZE * SIZE)}")

    if ships_found == len(ship_set):
        print("\nAll ships found! Your Quantum Radar was a success!")
    else:
        print("\nNot all ships found. The classical board may have changed!")
        
    print("\nClassical Comparison:")
    print(f"  - Quantum Strategy Hits: {total_hits}")
    print(f"  - Classical Brute Force (Worst Case): {SIZE * SIZE}")
    print(f"  - Classical Brute Force (Avg. for this board): ~{ (SIZE*SIZE) / 2 }")


play_quantum_battleship()

