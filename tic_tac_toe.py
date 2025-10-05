import time
import copy

class TicTacToe:
    def __init__(self):
        # Initialize empty board 1
        self.grid = []
        for i in range(3):
            row = []
            for j in range(3):
                row.append(' ')
            self.grid.append(row)
        
        self.call_count = 0
        self.ai_time_total = 0.0
        self.chosen_algo = None
        
    def start_new_game(self):
        """Start a fresh game"""
        for i in range(3):
            for j in range(3):
                self.grid[i][j] = ' '
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
        """Validate if move is legal"""
        if row < 0 or row > 2:
            return False
        if col < 0 or col > 2:
            return False
        if self.grid[row][col] != ' ':
            return False
        return True
    
    def place_symbol(self, row, col, symbol):
        """Put symbol on board if valid"""
        if self.check_valid_position(row, col):
            self.grid[row][col] = symbol
            return True
        else:
            return False
    
    def game_status(self):
        """Figure out if someone won or it's a tie"""
        # Check all rows
        for i in range(3):
            if (self.grid[i][0] == self.grid[i][1] == self.grid[i][2]) and self.grid[i][0] != ' ':
                return self.grid[i][0]
        
        # Check all columns  
        for j in range(3):
            if (self.grid[0][j] == self.grid[1][j] == self.grid[2][j]) and self.grid[0][j] != ' ':
                return self.grid[0][j]
        
        # Check main diagonal
        if (self.grid[0][0] == self.grid[1][1] == self.grid[2][2]) and self.grid[0][0] != ' ':
            return self.grid[0][0]
            
        # Check other diagonal
        if (self.grid[0][2] == self.grid[1][1] == self.grid[2][0]) and self.grid[0][2] != ' ':
            return self.grid[0][2]
        
        # Check if board full
        spaces_left = 0
        for i in range(3):
            for j in range(3):
                if self.grid[i][j] == ' ':
                    spaces_left += 1
        
        if spaces_left == 0:
            return 'Draw'
        
        return None  # Game still going
    
    def find_empty_spots(self):
        """Find all available moves"""
        empty_list = []
        for i in range(3):
            for j in range(3):
                if self.grid[i][j] == ' ':
                    empty_list.append((i, j))
        return empty_list
    
    def score_position(self):
        """Score current board state"""
        result = self.game_status()
        if result == 'O':  # AI victory
            return 10
        elif result == 'X':  # Human victory  
            return -10
        else:
            return 0
    
    def minimax_search(self, board, depth, maximizing_player):
        """Classic minimax implementation"""
        self.call_count += 1
        
        # Save current state
        old_grid = self.grid
        self.grid = board
        
        current_score = self.score_position()
        status = self.game_status()
        
        # Restore state
        self.grid = old_grid
        
        # Terminal cases
        if status == 'O':
            return 10 - depth
        elif status == 'X':
            return -10 + depth  
        elif status == 'Draw':
            return 0
        
        if maximizing_player:
            max_eval = float('-inf')
            # Try all possible moves
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
            min_eval = float('inf')
            # Try all possible moves
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
        """Minimax with alpha beta cuts"""
        self.call_count += 1
        
        # Save current state
        old_grid = self.grid
        self.grid = board
        
        current_score = self.score_position()
        status = self.game_status()
        
        # Restore state  
        self.grid = old_grid
        
        # Base cases
        if status == 'O':
            return 10 - depth
        elif status == 'X':
            return -10 + depth
        elif status == 'Draw':
            return 0
        
        if maximizing_player:
            max_eval = float('-inf')
            # Check all moves
            for row in range(3):
                for col in range(3):
                    if board[row][col] == ' ':
                        new_board = copy.deepcopy(board)
                        new_board[row][col] = 'O'
                        eval_score = self.alpha_beta_search(new_board, depth + 1, alpha, beta, False)
                        max_eval = max(max_eval, eval_score)
                        alpha = max(alpha, eval_score)
                        if beta <= alpha:
                            break  # Prune remaining branches
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            # Check all moves
            for row in range(3):
                for col in range(3):
                    if board[row][col] == ' ':
                        new_board = copy.deepcopy(board)
                        new_board[row][col] = 'X'
                        eval_score = self.alpha_beta_search(new_board, depth + 1, alpha, beta, True)
                        min_eval = min(min_eval, eval_score)
                        beta = min(beta, eval_score)
                        if beta <= alpha:
                            break  # Prune
                if beta <= alpha:
                    break
            return min_eval
    
    def calculate_best_move(self):
        """Find optimal move using selected algorithm"""
        best_position = None
        best_value = float('-inf')
        
        start = time.time()
        
        available_moves = self.find_empty_spots()
        
        for move in available_moves:
            row, col = move
            test_board = copy.deepcopy(self.grid)
            test_board[row][col] = 'O'
            
            calls_before = self.call_count
            
            if self.chosen_algo == 'minimax':
                move_value = self.minimax_search(test_board, 0, False)
            else:
                move_value = self.alpha_beta_search(test_board, 0, float('-inf'), float('inf'), False)
            
            if move_value > best_value:
                best_value = move_value
                best_position = move
        
        end = time.time()
        elapsed = (end - start) * 1000
        self.ai_time_total += elapsed
        
        return best_position
    
    def get_player_input(self):
        """Get valid move from human player"""
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
        """Main game execution"""
        print("=== Tic Tac Toe vs AI ===")
        print("You play as X, computer plays as O")
        print("Enter moves as: row col (using 0, 1, 2)")
        
        # Let user pick algorithm
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
        
        self.print_board()
        
        # Game loop
        while True:
            # Human turn
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
        
        # Show final results
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

# Main execution
def main():
    print("Tic-Tac-Toe AI Assignment Test Runner")
    
    game_results = []
    
    for game_num in range(1, 4):
        print(f"\n{'*'*50}")
        print(f"STARTING GAME {game_num}")
        print(f"{'*'*50}")
        
        ttt = TicTacToe()
        outcome = ttt.run_game()
        
        # Store results for summary
        game_results.append({
            'number': game_num,
            'algorithm': ttt.chosen_algo,
            'winner': outcome,
            'calls': ttt.call_count,
            'time_ms': ttt.ai_time_total
        })
        
        if game_num < 3:
            input(f"\nPress Enter to start Game {game_num + 1}...")
    
    # Final summary table
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