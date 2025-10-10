import time
import copy

class TicTacToe:
    """
    Task:
    - Maintaining 3x3 grid
    - Validating and executing moves
    - Detecting terminal states (win/draw/ongoing)
    - Compute AI moves using either Minimax or Alpha-Beta
    - Tracking diagnostics: call_count and ai_time_total
    """
    def __init__(self):
        """
        initializing empty 3x3 board, diagnostic counters, and algorithm selection type.

        Attributes:
        - grid: 3x3 list of ' ', 'X', or 'O'
        - call_count: number of recursive AI invocations done so far
        - ai_time_total: cumulative AI computation time in ms for the current game
        - chosen_algo: 'minimax' or 'alpha_beta'
        """
        
        # Build empty grid (rows of spaces). A space represents an empty cell.
        self.grid = []
        for i in range(3):
            row = []
            for j in range(3):
                row.append(' ')
            self.grid.append(row)
        
        # Diagnostics counter and algorithm
        self.call_count = 0
        self.ai_time_total = 0.0
        self.chosen_algo = None
        
    def start_new_game(self):
        """Start a fresh game"""
        
        #clear all cells to spaces
        for i in range(3):
            for j in range(3):
                self.grid[i][j] = ' '
        
        #reset diagnostics between each game        
        self.call_count = 0
        self.ai_time_total = 0.0
        
    def print_board(self):
        """Print current game state"""
        print("\nBoard Status:")
        print("  0   1   2")
        for row_idx in range(3):
            line = str(row_idx) + " "
            for col_idx in range(3):
                line += self.grid[row_idx][col_idx]
                if col_idx < 2:
                    line += " | "
            print(line)
            if row_idx < 2:
                print("  ---------")
        print()
        
    def check_valid_position(self, row, col):
        """
        Validate if move is legal
        Return True if (row, col) is inside the 3x3 grid and the cell is empty.
        Guards against out-of-bounds or overpositioning occupied cells.
        """
        
        #check bounds first, then emptiness check
        if row < 0 or row > 2:
            return False
        if col < 0 or col > 2:
            return False
        if self.grid[row][col] != ' ':
            return False
        return True
    
    def place_symbol(self, row, col, symbol):
        """
        Place 'X' or 'O' at (row, col) if valid; return True on success, else False.
        Confirms legality to check_valid_position to avoid duplication.
        """
        
        if self.check_valid_position(row, col):
            self.grid[row][col] = symbol
            return True
        else:
            return False
    
    def game_status(self):
        """
        Return the game outcome if ended, else None.
        - 'X' if X has any 3-in-a-row/column/diagonal
        - 'O' if O has any 3-in-a-row/column/diagonal
        - 'Draw' if board full and no winner
        - None if game still in progress

        Checks: rows, columns and both diagonals, then board completeness.
        """
        
        # check all rows
        for i in range(3):
            if (self.grid[i][0] == self.grid[i][1] == self.grid[i][2]) and self.grid[i][0] != ' ':
                return self.grid[i][0]
        
        # check all columns  
        for j in range(3):
            if (self.grid[0][j] == self.grid[1][j] == self.grid[2][j]) and self.grid[0][j] != ' ':
                return self.grid[0][j]
        
        # check main diagonal
        if (self.grid[0][0] == self.grid[1][1] == self.grid[2][2]) and self.grid[0][0] != ' ':
            return self.grid[0][0]
            
        # check other diagonal
        if (self.grid[0][2] == self.grid[1][1] == self.grid[2][0]) and self.grid[0][2] != ' ':
            return self.grid[0][2]
        
        # check if the board is full
        spaces_left = 0
        for i in range(3):
            for j in range(3):
                if self.grid[i][j] == ' ':
                    spaces_left += 1
        
        if spaces_left == 0:
            return 'Draw'
        
        return None  # game still ongoing
    
    def find_empty_spots(self):
        """
        Finds all available moves
        Return list of all coordinates (row, col) where grid cell is empty.
        Used by the AI to iterate legal successor states.
        """
        
        empty_list = []
        for i in range(3):
            for j in range(3):
                if self.grid[i][j] == ' ':
                    empty_list.append((i, j))
        return empty_list
    
    def score_position(self):
        """
        Heuristic for only terminal nodes as follows:
        - +10 if 'O' (AI) wins
        - -10 if 'X' (human) wins
        - 0 for draw or non-terminal node
        Note: The depth-adjusted scores are done by the search functions.
        """
        
        result = self.game_status()
        if result == 'O':  # AI wins!
            return 10
        elif result == 'X':  # Human wins!  
            return -10
        else:
            return 0
    
    def minimax_search(self, board, depth, maximizing_player):
        """
        Minimax over Tic-Tac-Toe state space.

        Parameters:
        - board: 3x3 list of lists representing the states simulated
        - depth: current recursion depth ( for preferring faster wins and slower losses)
        - maximizing_player: True when choosing move for AI ('O'), False for User ('X')

        Returns:
        - scalar value with respect to AI ('O'):
          for terminal:
            'O' win: 10 - depth
            'X' win: -10 + depth
            'Draw': 0
          for non-terminal: best achievable value via recursive minimax.

        Notes:
        - self.grid is temporarily replaced with `board` to reuse helpers
          (game_status/score_position), then restored to avoid side effects.
        - Uses deepcopy to generate child states safely.
        """
        
        # count this recursive call for diagnostics
        self.call_count += 1
        
        # save current state
        # temporarily redirects the helpers to inspect this simulated board
        old_grid = self.grid
        self.grid = board
        
        current_score = self.score_position()
        status = self.game_status()
        
        # restore original board immediately after querying
        self.grid = old_grid
        
        # terminal cases (depth-sensitive preferring faster outcomes)
        if status == 'O':
            return 10 - depth   # prefer quicker wins
        elif status == 'X':
            return -10 + depth  # prefer slower losses
        elif status == 'Draw':
            return 0
        
        if maximizing_player:
            # AI turn: chooses move that maximizes the value
            max_eval = float('-inf')
            # try all possible moves
            for row in range(3):
                for col in range(3):
                    if board[row][col] == ' ':
                        # Make move
                        new_board = copy.deepcopy(board)
                        new_board[row][col] = 'O'
                        # Recursive call
                        eval_score = self.minimax_search(new_board, depth + 1, False)
                        max_eval = max(max_eval, eval_score)
            return max_eval
        else:
            # opponent turn to minimize the AI's utility
            min_eval = float('inf')
            # try all possible moves
            for row in range(3):
                for col in range(3):
                    if board[row][col] == ' ':
                        # Make move
                        new_board = copy.deepcopy(board)
                        new_board[row][col] = 'X'
                        # Recursive call
                        eval_score = self.minimax_search(new_board, depth + 1, True)
                        min_eval = min(min_eval, eval_score)
            return min_eval
    
    def alpha_beta_search(self, board, depth, alpha, beta, maximizing_player):
        """
        Minimax with Alpha-Beta pruning.

        Parameters:
        - board: current simulated state
        - depth: recursion depth for tie-breaking
        - alpha: lower bound
        - beta: upper bound
        - maximizing_player: True for AI ('O') and False for User ('X')

        Returns:
        - same scoring convention as minimax_search.

        Pruning:
        - When alpha >= beta, remaining sibling nodes cannot influence the ancestor's choice and are pruned.
        """
        
        # track recursion count
        self.call_count += 1
        
        # evaluate terminal condition on this node using helper methods
        old_grid = self.grid
        self.grid = board
        
        current_score = self.score_position()
        status = self.game_status()
        
        # restore the state  
        self.grid = old_grid
        
        # base cases
        if status == 'O':
            return 10 - depth
        elif status == 'X':
            return -10 + depth
        elif status == 'Draw':
            return 0
        
        if maximizing_player:
            max_eval = float('-inf')
            # check all moves for AI ('O')
            for row in range(3):
                for col in range(3):
                    if board[row][col] == ' ':
                        new_board = copy.deepcopy(board)
                        new_board[row][col] = 'O'
                        eval_score = self.alpha_beta_search(new_board, depth + 1, alpha, beta, False)
                        max_eval = max(max_eval, eval_score)
                        alpha = max(alpha, eval_score)
                        if beta <= alpha:
                            break  # prune remaining branches
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            # check all moves for User ('X')
            for row in range(3):
                for col in range(3):
                    if board[row][col] == ' ':
                        new_board = copy.deepcopy(board)
                        new_board[row][col] = 'X'
                        eval_score = self.alpha_beta_search(new_board, depth + 1, alpha, beta, True)
                        min_eval = min(min_eval, eval_score)
                        beta = min(beta, eval_score)
                        if beta <= alpha:
                            break  # prune
                if beta <= alpha:
                    break
            return min_eval
    
    def calculate_best_move(self):
        """
        Find all legal moves for 'O' from the current real grid,
        evaluate each by one-ply expansion plus search, and choose the
        move with the highest result value.
        """
        
        best_position = None
        best_value = float('-inf')
        
        # start timing AI computation for this decision
        start = time.time()
        
        # precompute legal moves once to avoid repeated scanning
        available_moves = self.find_empty_spots()
        
        for move in available_moves:
            row, col = move
            
            # simulate placing 'O' and evaluate the resulting position
            test_board = copy.deepcopy(self.grid)
            test_board[row][col] = 'O'
            
            calls_before = self.call_count
            
            # select the search method based on user choice
            if self.chosen_algo == 'minimax':
                move_value = self.minimax_search(test_board, 0, False)
            else:
                move_value = self.alpha_beta_search(test_board, 0, float('-inf'), float('inf'), False)
            
            # track the best-scoring move so far
            if move_value > best_value:
                best_value = move_value
                best_position = move
        
        # stop timing and add to total AI time (ms)
        end = time.time()
        elapsed = (end - start) * 1000
        self.ai_time_total += elapsed
        
        return best_position
    
    def get_player_input(self):
        """
        Prompt the user for a legal (row, col) pair:
        - Accepts two integers separated by space in the range [0,2]
        - Re-prompts on invalid input (non-integer, out-of-bounds, or occupied)
        Returns a valid (row, col) tuple.
        """
        
        while True:
            try:
                user_input = input("Your move (row col): ").strip()
                parts = user_input.split()
                
                if len(parts) != 2:
                    print("Please enter row and column separated by space")
                    continue
                
                row = int(parts[0])
                col = int(parts[1])
                
                if row < 0 or row > 2 or col < 0 or col > 2:
                    print("Numbers must be 0, 1, or 2")
                    continue
                    
                if self.grid[row][col] != ' ':
                    print("That spot is taken, try another")
                    continue
                    
                return row, col
                
            except ValueError:
                print("Please enter valid numbers")
                continue
    
    def run_game(self):
        """
        Perform one full human-vs-AI game:
        1) Prompting AI algorithm selection
        2) Alternate turns: human 'X' then AI 'O'
        3) After each move, check for terminal status and stop if reached
        4) Print the final result and each game statistics

        Returns:
        - 'X' if human wins
        - 'O' if AI wins
        - 'Draw' otherwise
        """
        
        print("=== Tic Tac Toe vs AI ===")
        print("You play as X, computer plays as O")
        print("Enter moves as: row col (using 0, 1, 2)")
        
        # let the user pick algorithm
        while True:
            print("\nChoose AI algorithm:")
            print("1 - Minimax")
            print("2 - Alpha Beta Pruning")
            choice = input("Enter 1 or 2: ").strip()
            
            if choice == '1':
                self.chosen_algo = 'minimax'
                print("Using Minimax algorithm")
                break
            elif choice == '2':
                self.chosen_algo = 'alpha_beta'  
                print("Using Alpha-Beta Pruning")
                break
            else:
                print("Invalid choice, try again")
        
        # show the initial empty board
        self.print_board()
        
        # game loop
        while True:
            # human turn
            print("Your turn:")
            player_row, player_col = self.get_player_input()
            self.place_symbol(player_row, player_col, 'X')
            self.print_board()
            
            result = self.game_status()
            if result is not None:
                break
            
            # AI turn
            print("AI is calculating move...")
            ai_move = self.calculate_best_move()
            if ai_move:
                ai_row, ai_col = ai_move
                self.place_symbol(ai_row, ai_col, 'O')
                print(f"AI chose position ({ai_row}, {ai_col})")
                self.print_board()
                
                result = self.game_status()
                if result is not None:
                    break
        
        # show final results
        print("\n" + "="*40)
        print("GAME FINISHED")
        print("="*40)
        
        if result == 'X':
            print("You won! Great job!")
        elif result == 'O':
            print("AI wins this round")
        else:
            print("It's a tie game")
        
        print(f"\nStatistics:")
        algo_name = "Minimax" if self.chosen_algo == 'minimax' else "Alpha-Beta Pruning"
        print(f"Algorithm: {algo_name}")
        print(f"AI thinking time: {self.ai_time_total:.2f} milliseconds")
        print(f"Function calls made: {self.call_count}")
        
        return result

# main
def main():
    """
    Main function for running three sequential games and printing a summary table.
    For each game:
    - Create a new TicTacToe instance
    - Run a full game
    - Record algorithm used, winner, call_count, and AI time
    After all games, print results.
    """
    
    print("Tic-Tac-Toe AI Assignment Test Runner")
    
    game_results = []
    
    for game_num in range(1, 4):
        print(f"\n{'*'*50}")
        print(f"STARTING GAME {game_num}")
        print(f"{'*'*50}")
        
        ttt = TicTacToe()
        outcome = ttt.run_game()
        
        # store results for summary
        game_results.append({
            'number': game_num,
            'algorithm': ttt.chosen_algo,
            'winner': outcome,
            'calls': ttt.call_count,
            'time_ms': ttt.ai_time_total
        })
        
        if game_num < 3:
            input(f"\nPress Enter to start Game {game_num + 1}...")
    
    # final summary table
    print(f"\n{'='*70}")
    print("ASSIGNMENT RESULTS SUMMARY")  
    print(f"{'='*70}")
    print(f"{'Game':<6} {'Algorithm':<18} {'Winner':<10} {'Calls':<8} {'Time(ms)':<10}")
    print("-" * 70)
    
    for result in game_results:
        algo_display = "Minimax" if result['algorithm'] == 'minimax' else "Alpha-Beta"
        winner_display = result['winner']
        if winner_display == 'X':
            winner_display = 'Human'
        elif winner_display == 'O':
            winner_display = 'AI'
            
        print(f"{result['number']:<6} {algo_display:<18} {winner_display:<10} {result['calls']:<8} {result['time_ms']:<10.2f}")
    

if __name__ == "__main__":

    main()
