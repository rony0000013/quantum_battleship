# Quantum Battleship

An innovative twist on the classic Battleship game that leverages quantum computing concepts to detect ships using quantum circuits and Grover's search algorithm.

## 🚀 Features

- **Quantum Scanning**: Uses quantum circuits to detect the presence of ships in rows and columns
- **Classical Pinpointing**: Combines quantum and classical approaches to locate ships efficiently
- **Interactive Gameplay**: Play against the computer with a text-based interface
- **Educational**: Learn about quantum computing concepts through gameplay

## 🛠️ Prerequisites

- Python 3.12+
- Qiskit
- Qiskit Aer
- Numpy

## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/quantum_battleship.git
   cd quantum_battleship
   ```

2. Install the required packages:
   ```bash
   uv sync
   ```

## 🎮 How to Play

1. Run the game:
   ```bash
   uv run main.py
   ```

2. The game has two phases:
   - **Quantum Scanning Phase**: The game automatically scans each row and column using quantum circuits
   - **Classical Pinpointing Phase**: The game reveals potential ship locations based on quantum scan results

3. The game will display two boards:
   - **Hidden Board**: Shows the actual ship locations (for debugging)
   - **Radar View**: Shows your current knowledge of the board

## 🎯 Game Rules

- The game is played on an 8x8 grid by default
- Ships of different lengths are randomly placed on the board
- Quantum scanning detects the presence of ships in rows/columns without revealing exact positions
- After scanning, the game reveals potential ship locations
- The game continues until all ships are found

## 🧠 How It Works

The game uses quantum circuits to implement an "interaction-free" measurement technique:

1. **Quantum Oracle**: Creates a phase-flip oracle that marks ship locations
2. **Grover's Search**: Uses H-Oracle-H (Hadamard-Oracle-Hadamard) to detect ship presence
3. **Measurement**: Interprets the quantum measurement results to determine if a ship is present in a row/column

## 📊 Example Output

```
Welcome to Quantum Battleship!
Board size: 8x8
Ships to find: 12 (from 4 ships)

--- Phase 1: Quantum Scanning ---
Scanning all rows...
Row 0 scan result: DETECT
Row 1 scan result: MISS
...
Scanning all columns...
Col 0 scan result: DETECT
...

--- Phase 2: Classical Pinpointing ---
Found potential ship at (0, 4)
...
```

## 📚 Learning Resources

- [Qiskit Documentation](https://qiskit.org/documentation/)
- [Quantum Computing Concepts](https://qiskit.org/learn/)
- [Grover's Algorithm](https://qiskit.org/textbook/ch-algorithms/grover.html)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Qiskit team for the amazing quantum computing framework
- All quantum computing educators and enthusiasts
