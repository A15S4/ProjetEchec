
class StatsAction:

    @staticmethod
    def calculate_piece_percentages(data):
        total_pieces = data.total
        percentages = {
            'king': "{:.0f}%".format((data.king / total_pieces) * 100) if total_pieces > 0 else "0%",
            'queen': "{:.0f}%".format((data.queen / total_pieces) * 100) if total_pieces > 0 else "0%",
            'rook': "{:.0f}%".format((data.rook / total_pieces) * 100) if total_pieces > 0 else "0%",
            'pawn': "{:.0f}%".format((data.pawn / total_pieces) * 100) if total_pieces > 0 else "0%",
            'knight': "{:.0f}%".format((data.knight / total_pieces) * 100) if total_pieces > 0 else "0%",
            'bishop': "{:.0f}%".format((data.bishop / total_pieces) * 100) if total_pieces > 0 else "0%",
        }
        return percentages
    

    @staticmethod
    def format_game_time(game_time_total):
        hours = game_time_total // 3600
        remaining_seconds = game_time_total % 3600
        minutes = remaining_seconds // 60
        seconds = remaining_seconds % 60 
        formatted_time = "{:02d}h {:02d}m {:02d}s".format(hours, minutes, seconds)
        return formatted_time
    
    @staticmethod
    def calculate_win_percentage(data):
        total_games = data.total_win + data.total_loss + data.total_draw
        win_percentage = "{:.0f}%".format(100 * (data.total_win / total_games)) if total_games > 0 else "0%"
        return win_percentage
    
    