from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class TicTacToeGame(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        self.rows = 4
        self.board = [""] * 9
        self.current_player = "X"
        
        # Board UI
        self.buttons = []
        for i in range(9):
            btn = Button(font_size=32)
            btn.bind(on_press=self.make_move)
            self.add_widget(btn)
            self.buttons.append(btn)
        
        # Status Label
        self.status_label = Label(text="Player X's turn", font_size=24, size_hint_y=0.2)
        self.add_widget(self.status_label)  # Add status label without colspan
    
    def make_move(self, instance):
        index = self.buttons.index(instance)
        if self.board[index] == "" and self.check_winner() is None:
            self.board[index] = self.current_player
            instance.text = self.current_player
            winner = self.check_winner()

            if winner:
                self.status_label.text = f"Player {winner} wins!"
                self.show_play_again_popup()
                return
            elif "" not in self.board:
                self.status_label.text = "It's a draw!"
                self.show_play_again_popup()
                return

            # Switch turn to AI or Player
            if self.current_player == "X":
                self.current_player = "O"
                self.status_label.text = "AI is thinking..."
                self.ai_move()
            else:
                self.current_player = "X"
                self.status_label.text = "Player X's turn"

    def ai_move(self):
        best_score = float("-inf")
        best_move = None
        for i in range(9):
            if self.board[i] == "":
                self.board[i] = "O"
                score = self.minimax(self.board, False)
                self.board[i] = ""
                if score > best_score:
                    best_score = score
                    best_move = i
        
        # Make the AI move
        if best_move is not None:
            self.board[best_move] = "O"
            self.buttons[best_move].text = "O"

        winner = self.check_winner()
        if winner:
            self.status_label.text = f"Player {winner} wins!"
            self.show_play_again_popup()
        elif "" not in self.board:
            self.status_label.text = "It's a draw!"
            self.show_play_again_popup()
        else:
            self.current_player = "X"
            self.status_label.text = "Player X's turn"

    def minimax(self, board, is_maximizing):
        winner = self.check_winner()
        if winner == "X":
            return -1
        elif winner == "O":
            return 1
        elif "" not in board:
            return 0
        
        if is_maximizing:
            best_score = float("-inf")
            for i in range(9):
                if board[i] == "":
                    board[i] = "O"
                    score = self.minimax(board, False)
                    board[i] = ""
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float("inf")
            for i in range(9):
                if board[i] == "":
                    board[i] = "X"
                    score = self.minimax(board, True)
                    board[i] = ""
                    best_score = min(score, best_score)
            return best_score

    def check_winner(self):
        # Define winning combinations
        win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]             # Diagonals
        ]
        for combo in win_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != "":
                return self.board[combo[0]]
        return None

    def show_play_again_popup(self):
        # Create the layout for the popup
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        play_again_button = Button(text="Play Again", on_press=self.reset_game)
        quit_button = Button(text="Quit", on_press=self.quit_game)
        
        popup_layout.add_widget(Label(text="Wanna play again? Type Y or N"))
        popup_layout.add_widget(play_again_button)
        popup_layout.add_widget(quit_button)

        # Create and open the popup
        self.popup = Popup(title="Game Over", content=popup_layout, size_hint=(0.5, 0.5))
        self.popup.open()

    def reset_game(self, instance):
        # Reset the game state and UI
        self.board = [""] * 9
        self.current_player = "X"
        self.status_label.text = "Player X's turn"
        for button in self.buttons:
            button.text = ""
        self.popup.dismiss()

    def quit_game(self, instance):
        # Close the app
        App.get_running_app().stop()
        self.popup.dismiss()

class TicTacToeApp(App):
    def build(self):
        return TicTacToeGame()

if __name__ == "__main__":
    TicTacToeApp().run()
