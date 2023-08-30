# This is where you build your AI for the Chess game.

from joueur.base_ai import BaseAI

# <<-- Creer-Merge: imports -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
# you can add additional import(s) here

import random
import copy

# <<-- /Creer-Merge: imports -->>

class AI(BaseAI):
    """ The basic AI functions that are the same between games. """

    def get_name(self):
        """ This is the name you send to the server so your AI will control the player named this string.

        Returns
            str: The name of your Player.
        """
        # <<-- Creer-Merge: get-name -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        return "Tony Sax" # REPLACE THIS WITH YOUR TEAM NAME
        # <<-- /Creer-Merge: get-name -->>

    def start(self):
        """ This is called once the game starts and your AI knows its playerID and game. You can initialize your AI here.
        """
        # <<-- Creer-Merge: start -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # replace with your start logic

        self.Board = [["." for x in range(8)] for y in range(8)]
        for piece_num in range(len(self.game.pieces)):
            piece = self.game.pieces[piece_num]

        for r in range(8, 0, -1):
            for file_offset in range(0, 8):
                # start at a, with with file offset increasing the char
                f = chr(ord("a") + file_offset)
                current_piece = None
                for piece in self.game.pieces:
                    if piece.file == f and piece.rank == r:
                        # then we found the piece at (file, rank)
                        current_piece = piece
                        break

                code = "."  # default "no piece"
                if current_piece:
                    # the code will be the first character of their type
                    # e.g. 'Q' for "Queen"
                    code = current_piece.type[0]

                    if current_piece.type == "Knight":
                        # 'K' is for "King", we use 'N' for "Knights"
                        code = "N"

                    if current_piece.owner.id == "1":
                        # the second player (black) is lower case.
                        # Otherwise it's uppercase already
                        code = code.lower()
                # The x value (file) of the game board.
                abscissa = ord(f)-97
                # The y value (rank) of the game board.
                ordinate = r-1
                self.Board[ordinate][abscissa] = code

        # <<-- /Creer-Merge: start -->>

    def game_updated(self):
        """ This is called every time the game's state updates, so if you are tracking anything you can update it here.
        """
        # <<-- Creer-Merge: game-updated -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # replace with your game updated logic

        # Run the same code used to create the initial chess board again in order to update the current board.
        for r in range(8, 0, -1):
            for file_offset in range(0, 8):
                # start at a, with with file offset increasing the char
                f = chr(ord("a") + file_offset)
                current_piece = None
                for piece in self.game.pieces:
                    if piece.file == f and piece.rank == r:
                        # then we found the piece at (file, rank)
                        current_piece = piece
                        break

                code = "."  # default "no piece"
                if current_piece:
                    # the code will be the first character of their type
                    # e.g. 'Q' for "Queen"
                    code = current_piece.type[0]

                    if current_piece.type == "Knight":
                        # 'K' is for "King", we use 'N' for "Knights"
                        code = "N"

                    if current_piece.owner.id == "1":
                        # the second player (black) is lower case.
                        # Otherwise it's uppercase already
                        code = code.lower()
                # The x value (file) of the game board.
                abscissa = ord(f)-97
                # The y value (rank) of the game board.
                ordinate = r-1
                self.Board[ordinate][abscissa] = code

        # <<-- /Creer-Merge: game-updated -->>

    def end(self, won, reason):
        """ This is called when the game ends, you can clean up your data and dump files here if need be.

        Args:
            won (bool): True means you won, False means you lost.
            reason (str): The human readable string explaining why you won or lost.
        """
        # <<-- Creer-Merge: end -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # replace with your end logic

        # <<-- /Creer-Merge: end -->>
    def run_turn(self):
        """ This is called every time it is this AI.player's turn.

        Returns:
            bool: Represents if you want to end your turn. True means end your turn, False means to keep your turn going and re-call this function.
        """
        # <<-- Creer-Merge: runTurn -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # Put your game logic here for runTurn

        boolean_pieces_left = True
        list_of_pieces_used = []

        ##print("\n\nIt is now ", self.player.color, "'s turn.\n", sep="")


        # Print the board to the console
        print("\n")
        print("Player:", self.player.color)
        self.print_current_board()

        # No need to print this since we aren't looking at child nodes. Also its not as pretty.
        #self.print_my_board()

        # Print the opponent's last move to the console
        if len(self.game.moves) > 0:
            print("Opponent's Last Move: '" + self.game.moves[-1].san + "'")

        # Print how much time remaining this AI has to calculate moves
        #print("Time Remaining: " + str(self.player.time_remaining) + " ns")

        ###############
        # Starting code for ID-DL-MM
        ###############
        depth_limit_string = self.get_setting("depth_limit")
        depth_limit_int = int(depth_limit_string)
        # (* Initial call for maximizing player *)
        # minimax(origin, depth, TRUE)
        print("Running minimax")
        result_of_minimax = self.depth_limited_minimax(self.Board, depth_limit_int, True)
        print("Result of minimax", result_of_minimax)
        score_of_minimax = result_of_minimax[0]
        board_of_minimax = result_of_minimax[1]
        top_level_child = result_of_minimax[2]
        self.print_my_board(board_of_minimax)
        self.print_my_board(top_level_child)
        difference_list = self.difference_between_boards(top_level_child)
        if difference_list:
            from_space = difference_list[0]
            to_space = difference_list[1]
            to_file = to_space[0]
            to_rank = to_space[1]
            # Find the piece at the first difference.
            for piece in self.player.pieces:
                if piece.file == from_space[0] and piece.rank == from_space[1]:
                    print("piece.type", piece.type)
                    piece.move(to_file, to_rank, "Queen")


        return True
        # <<-- /Creer-Merge: runTurn -->>

    # <<-- Creer-Merge: functions -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
    # if you need additional functions for your AI you can add them here


    def print_current_board(self):
        """Prints the current board using pretty ASCII art
        Note: you can delete this function if you wish
        """

        # iterate through the range in reverse order
        for r in range(9, -2, -1):
            output = ""
            if r == 9 or r == 0:
                # then the top or bottom of the board
                output = "   +------------------------+"
            elif r == -1:
                # then show the ranks
                output = "     a  b  c  d  e  f  g  h"
            else:  # board
                output = " " + str(r) + " |"
                # fill in all the files with pieces at the current rank
                for file_offset in range(0, 8):
                    # start at a, with with file offset increasing the char
                    f = chr(ord("a") + file_offset)
                    current_piece = None
                    for piece in self.game.pieces:
                        if piece.file == f and piece.rank == r:
                            # then we found the piece at (file, rank)
                            current_piece = piece
                            break

                    code = "."  # default "no piece"
                    if current_piece:
                        # the code will be the first character of their type
                        # e.g. 'Q' for "Queen"
                        code = current_piece.type[0]

                        if current_piece.type == "Knight":
                            # 'K' is for "King", we use 'N' for "Knights"
                            code = "N"

                        if current_piece.owner.id == "1":
                            # the second player (black) is lower case.
                            # Otherwise it's uppercase already
                            code = code.lower()

                    output += " " + code + " "

                output += "|"
            print(output)

    # This prints out the Python list of lists that serves as my game board.
    # It prints out the board flipped across the x axis due to the way the python list of lists is ordered.
    # The coordinate (0, 0) is in the top left corner of the board.
    def print_my_board(self, Board):
        for y in reversed(Board):
          print(*y, sep=" ")

    # Returns a random piece on the board.
    def random_piece(self):
        random_piece = random.choice(self.game.pieces)
        return random_piece

    # Returns a random piece that I own.
    def my_random_piece(self):
        random_piece = random.choice(self.player.pieces)
        return random_piece

    def random_move(self):
        # Select a random piece from the pieces I own.
        random_piece = self.my_random_piece()
        random_file = chr(ord("a") + random.randrange(8))
        random_rank = random.randrange(8) + 1
        random_piece.move(random_file, random_rank)
        return

    # From the given Piece object and list of possible moves, makes a random move with the chess piece.
    # Returns nothing.
    def my_random_move(self, my_piece, list_of_spaces):
        random_moves_chosen = []
        boolean_has_possible_move = True

        '''
        # Print out all the possible moves for the chosen piece.
        for space in list_of_spaces:
            possible_space_file = space[0]
            possible_space_rank = space[1]
            if my_piece.type == "Pawn" and (possible_space_rank == 8 or possible_space_rank == 1):
                print(self.player.color, " ", my_piece.type, " from ", my_piece.file, my_piece.rank, " to ", possible_space_file, possible_space_rank, " promotion to Rook", sep="")
                print(self.player.color, " ", my_piece.type, " from ", my_piece.file, my_piece.rank, " to ", possible_space_file, possible_space_rank, " promotion to Knight", sep="")
                print(self.player.color, " ", my_piece.type, " from ", my_piece.file, my_piece.rank, " to ", possible_space_file, possible_space_rank, " promotion to Bishop", sep="")
                print(self.player.color, " ", my_piece.type, " from ", my_piece.file, my_piece.rank, " to ", possible_space_file, possible_space_rank, " promotion to Queen", sep="")
            else:
                print(self.player.color, " ", my_piece.type, " from ", my_piece.file, my_piece.rank, " to ", possible_space_file, possible_space_rank, sep="")
        '''

        # Pick the move
        random_move = random.choice(list_of_spaces)
        random_move_file = random_move[0]
        random_move_rank = random_move[1]
        random_moves_chosen.append(random_move)
        move_valid = self.check_if_move_valid(my_piece, random_move_file, random_move_rank)

        # Currently trying to make work.
        while move_valid == False:
            # This needs to be before we add a random_move to the random_move_chosen list.
            # If we have tried so many random moves that the same moves in list_of_spaces are in random_moves_chosen
            if sorted(random_moves_chosen) == sorted(list_of_spaces):
                print("You have randomly chosen all possible moves.")
                print("random_moves_chosen", random_moves_chosen)
                print("list_of_spaces", list_of_spaces)
                boolean_has_possible_move = False
                return boolean_has_possible_move
            # Re-pick the move because it was an invalid move.
            random_move = random.choice(list_of_spaces)
            random_move_file = random_move[0]
            random_move_rank = random_move[1]
            # Re-check if the move is valid
            move_valid = self.check_if_move_valid(my_piece, random_move_file, random_move_rank)
            if random_move not in random_moves_chosen:
                random_moves_chosen.append(random_move)


        print("Random Choice:")
        if my_piece.type == "Pawn" and (random_move_rank == 8 or random_move_rank == 1):
            # Pick out a random number 1,2,3, or 4 in order to choose a random promotion
            random_promotion_number = random.randint(1,4)
            print("random_promotion_number", random_promotion_number)
            if random_promotion_number == 1:
                print(self.player.color, " ", my_piece.type, " from ", my_piece.file, my_piece.rank, " to ", random_move_file, random_move_rank, " promotion to Rook\n", sep="")
                my_piece.move(random_move_file, random_move_rank, "Rook")
            if random_promotion_number == 2:
                print(self.player.color, " ", my_piece.type, " from ", my_piece.file, my_piece.rank, " to ", random_move_file, random_move_rank, " promotion to Knight\n", sep="")
                my_piece.move(random_move_file, random_move_rank, "Knight")
            if random_promotion_number == 3:
                print(self.player.color, " ", my_piece.type, " from ", my_piece.file, my_piece.rank, " to ", random_move_file, random_move_rank, " promotion to Bishop\n", sep="")
                my_piece.move(random_move_file, random_move_rank, "Bishop")
            if random_promotion_number == 4:
                print(self.player.color, " ", my_piece.type, " from ", my_piece.file, my_piece.rank, " to ", random_move_file, random_move_rank, " promotion to Queen\n", sep="")
                my_piece.move(random_move_file, random_move_rank, "Queen")
        else:
            print(self.player.color, " ", my_piece.type, " from ", my_piece.file, my_piece.rank, " to ", random_move_file, random_move_rank, "\n", sep="")
            my_piece.move(random_move_file, random_move_rank, "Queen")

        return boolean_has_possible_move
        
    # A function to check if a value is in bounds of the array.
    # Returns True if within the bounds of the list, otherwise returns False.
    def in_bounds(self, ordinate, abscissa):
        if ordinate >= 0 and ordinate <= 7:
            if abscissa >= 0 and abscissa <= 7:
                return True
            else:
                return False
        else:
            return False

    # A function to check if the proposed move is valid. It works by moving a piece on my own board and checking if the enemy's pieces can hit
    def check_if_move_valid(self, my_piece, file, rank):
        boolean_move_valid = False
        king_piece = None
        to_file_index = (ord(file)-96)-1
        to_rank_index = rank-1
        from_file_index = (ord(my_piece.file)-96)-1
        from_rank_index = my_piece.rank-1
        piece_letter = None
        possible_taken_piece_list = None
        space_moved_to_letter = None
        total_enemy_move_list = []
        engaged_space = True
        line_of_sight = False
        # Define the ally king
        for piece in self.player.pieces:
            if piece.type == "King":
                king_piece = piece

        # Assign the letter we want to place in that board slot based on what piece we are checking.
        # This can be made into its own function if need be.
        if my_piece.type == "Pawn":
            if my_piece.owner.color == "White":
                piece_letter = "P"
            elif my_piece.owner.color == "Black":
                piece_letter = "p"
        if my_piece.type == "Rook":
            if my_piece.owner.color == "White":
                piece_letter = "R"
            elif my_piece.owner.color == "Black":
                piece_letter = "r"
        if my_piece.type == "Knight":
            if my_piece.owner.color == "White":
                piece_letter = "N"
            elif my_piece.owner.color == "Black":
                piece_letter = "n"
        if my_piece.type == "Bishop":
            if my_piece.owner.color == "White":
                piece_letter = "B"
            elif my_piece.owner.color == "Black":
                piece_letter = "b"
        if my_piece.type == "Queen":
            if my_piece.owner.color == "White":
                piece_letter = "Q"
            elif my_piece.owner.color == "Black":
                piece_letter = "q"
        if my_piece.type == "King":
            if my_piece.owner.color == "White":
                piece_letter = "K"
            elif my_piece.owner.color == "Black":
                piece_letter = "k"

        # Make the move we want to test. If our check fails we should change this back later so we record the spot we changed first.
        space_moved_to_letter = self.Board[to_rank_index][to_file_index]
        self.Board[to_rank_index][to_file_index] = piece_letter
        self.Board[from_rank_index][from_file_index] = "."

        #self.print_my_board()

        # It is possible we took on of the enemy's pieces. Check the enemy's pieces to see if we moved our piece to where the enemy piece was located.
        # Then generate the list of the enemy's pieces without that possible_taken_piece_list.
        list_of_uncaptured_pieces = self.game.pieces
        list_of_current_players_pieces = self.player.pieces
        possible_taken_piece_list = [piece for piece in list_of_uncaptured_pieces if piece not in list_of_current_players_pieces and piece.file == file and piece.rank == rank]
        list_of_enemy_pieces = [piece for piece in list_of_uncaptured_pieces if piece not in list_of_current_players_pieces and piece not in possible_taken_piece_list]
        print("possible_taken_piece_list", possible_taken_piece_list)
        print("list of ally pieces", self.player.pieces)
        print("list_of_enemy_pieces", list_of_enemy_pieces)

        # Generate all the possible moves of the enemy's pieces, excluding spaces they can hit if the current player moves a piece. If the king is ANY of the move lists, then our choice of move was bad.
        for piece in list_of_enemy_pieces:
            if piece.type == "Pawn":
                # Use the pawn_engaged_space because the pawn may be able to attack pieces that move near its diagonals when it cant move to those spaces.
                enemy_pawn_engaged_list = self.pawn_engaged_space(piece)
                total_enemy_move_list = total_enemy_move_list + enemy_pawn_engaged_list
            if piece.type == "Rook":
                enemy_rook_move_list = self.rook_move_space(piece)
                if len(enemy_rook_move_list) > 0:
                    total_enemy_move_list = total_enemy_move_list + enemy_rook_move_list
            if piece.type == "Knight":
                enemy_knight_move_list = self.knight_move_space(piece)
                if len(enemy_knight_move_list) > 0:
                    total_enemy_move_list = total_enemy_move_list + enemy_knight_move_list
            if piece.type == "Bishop":
                enemy_bishop_move_list = self.bishop_move_space(piece)
                if len(enemy_bishop_move_list) > 0:
                    total_enemy_move_list = total_enemy_move_list + enemy_bishop_move_list
            if piece.type == "Queen":
                enemy_queen_move_list = self.queen_move_space(piece)
                if len(enemy_queen_move_list) > 0:
                    total_enemy_move_list = total_enemy_move_list + enemy_queen_move_list
            if piece.type == "King":
                enemy_king_move_list = self.king_move_space(piece)
                if len(enemy_king_move_list) > 0:
                    total_enemy_move_list = total_enemy_move_list + enemy_king_move_list

        print("king_piece", king_piece)
        # Check to see if any of the moves have the same file and rank as the ally player's king.
        print("total_enemy_move_list", total_enemy_move_list)
        for move in total_enemy_move_list:
            #print("enemy pieces moves", move)
            # If the enemy's pieces can still attack the king.
            if self.Board[move[1]-1][(ord(move[0])-96)-1] == "k" and my_piece.owner.color == "Black" or self.Board[move[1]-1][(ord(move[0])-96)-1] == "K" and my_piece.owner.color == "White":
                boolean_move_valid = False
                # Reset the pieces we moved earlier.
                self.Board[to_rank_index][to_file_index] = space_moved_to_letter
                self.Board[from_rank_index][from_file_index] = piece_letter
                # Must break from the loop because we don't need to check any more spaces and don't want to set boolean_move_valid to true.
                break
            else:
                boolean_move_valid = True

        return boolean_move_valid

    # A function to check if the proposed move is valid. It works by moving a piece on my own board and checking if the enemy's pieces can hit the king.
    # Parameters:   Board - The state of the board we want to check our move against.
    #               from_file - The file of the piece we want to move.
    #               from_rank - The rank of the piece we want to move.
    #               to_file - The file of the space we want to move to.
    #               to_rank - The rank of the space we want to move to.
    # Returns: True if a valid move. False otherwise.
    def check_if_space_to_move_valid(self, Board, from_file, from_rank, to_file, to_rank):
        #print("\nRunning check_if_space_to_move_valid()")
        boolean_move_valid = False
        king_piece = None
        king_file_index = None
        king_rank_index = None
        to_file_index = (ord(to_file)-96)-1
        to_rank_index = to_rank-1
        king_board_space = []
        from_file_index = (ord(from_file)-96)-1
        from_rank_index = from_rank-1
        piece_letter = None
        piece_color = None
        possible_taken_piece_list = None
        space_moved_to_letter = None
        enemy_possible_move_list = []

        # Assign the letter we want to place in that board slot based on what piece we are checking.
        piece_letter = Board[from_rank_index][from_file_index]

        # This needs to go before we check where the king is because it is also possible to move the king.
        # Make the move we want to test. If our check fails we should change this back later so we record the spot we changed first.
        space_moved_to_letter = Board[to_rank_index][to_file_index]
        Board[to_rank_index][to_file_index] = piece_letter
        Board[from_rank_index][from_file_index] = "."

        # Define the ally king
        # Check to see what team we are checking.
        piece_upper = piece_letter.isupper()
        for row in Board:
            for piece in row:
                # If the piece is White
                if piece_upper:
                    if piece == "K":
                        king_rank_index = Board.index(row)
                        king_file_index = row.index(piece)
                        king_board_space = self.index_to_board_space_list(king_rank_index, king_file_index)
                # The piece is Black
                else:
                    if piece == "k":
                        king_rank_index = Board.index(row)
                        king_file_index = row.index(piece)
                        king_board_space = self.index_to_board_space_list(king_rank_index, king_file_index)


        # It is possible we took one of the enemy's pieces. Check the enemy's pieces to see if we moved our piece to where the enemy piece was located.
        # Then generate the list of the enemy's pieces without that possible_taken_piece_list.
        possible_taken_piece_list = [space_moved_to_letter]

        # Generate all the possible moves of the enemy's pieces, excluding spaces they can hit if the current player moves a piece. 
        # If the king is ANY of the move lists, then our choice of move was bad.
        # Every move in this move list has four items, the first two are the from space, the last two the to space.
        enemy_possible_move_list = self.possible_move_list(Board, False)

        for piece in enemy_possible_move_list:
            piece_length = len(piece)
            for space in range(1, piece_length):
                enemy_possible_move = piece[space]
                #print("enemy_possible_move", enemy_possible_move)
                to_file = enemy_possible_move[0]
                to_rank = enemy_possible_move[1]
                if enemy_possible_move == king_board_space:
                    #print("boolean_move_valid = False")
                    boolean_move_valid = False
                    # Must break from the loop because we don't need to check any more spaces and don't want to set boolean_move_valid to true.
                    break
                else:
                    #print("boolean_move_valid = True")
                    boolean_move_valid = True
            if boolean_move_valid == False:
                break


        # Reset the pieces we moved earlier, because this function will only check if moves are possible, not make the move for us.
        Board[to_rank_index][to_file_index] = space_moved_to_letter
        Board[from_rank_index][from_file_index] = piece_letter


        #print("Exiting check_if_space_to_move_valid()\n")
        return boolean_move_valid

    # This function simply makes a move on my own board.
    # Parameters:   Board - The state of the board we want to check our move against.
    #               from_file - The file of the piece we want to move.
    #               from_rank - The rank of the piece we want to move.
    #               to_file - The file of the space we want to move to.
    #               to_rank - The rank of the space we want to move to.
    # Returns: The new board with changes to it.
    def make_move_on_my_board(self, Board, from_file, from_rank, to_file, to_rank):
        from_file_index = (ord(from_file)-96)-1
        from_rank_index = from_rank-1
        to_file_index = (ord(to_file)-96)-1
        to_rank_index = to_rank-1

        piece_letter = Board[from_rank_index][from_file_index]
        Board[to_rank_index][to_file_index] = piece_letter
        Board[from_rank_index][from_file_index] = "."
        return Board

    # The ordinate is the rank, which is the y value.
    # The abscissa is the file, which is the x value.
    # Returns a list item where the first value is the abscissa (file) and the second value is the ordinate (rank).
    def index_to_board_space_list(self, rank, file):
        # Convert the file's index position to a letter. Add 1 to get out of index and into range of board (1 to 8).
        # Add 96 to get value in ASCII.
        abscissa = chr(((file)+1)+96)
        # Conver the rank's index position to the actual rank.
        ordinate = rank+1

        board_space_list = [abscissa, ordinate]

        return board_space_list

    # Define the spaces a pawn can move, given the location of the pawn.
    # Takes in a Piece object as a parameter
    # Returns a list of all the possible spaces that the piece can move to.
    def pawn_move_space(self, Board, from_file_index, from_rank_index):
        pawn_rank_index = from_rank_index
        # Subtract 96 to get in range of 1-8 and subtract 1 to get within range of list.
        pawn_file_index = from_file_index
        pawn_rank = pawn_rank_index+1
        pawn_file = chr((pawn_file_index+96)+1)

        rank_in_front_index = None
        rank_2_in_front_index = None
        file_to_left_index = None
        file_to_left = None
        file_to_right_index = None
        file_to_right = None

        list_of_possible_spaces = []

        # Black and white pawns will have different directions to move.
        # Don't check for self.player.color because we may check Black's pawns on White's turn, or White's pawns on Black's turn.
        if Board[pawn_rank_index][pawn_file_index] == "P":
            # Initialize the rank_in_front_index values here because they will be different for black and white pawns.
            rank_in_front_index = pawn_rank_index + 1
            rank_2_in_front_index = pawn_rank_index + 2
            file_to_left_index = pawn_file_index - 1
            file_to_left = chr((file_to_left_index+96)+1)
            file_to_right_index = pawn_file_index + 1
            file_to_right = chr((file_to_right_index+96)+1)
        else: # The color player is "Black"
            # Initialize the rank_in_front_index values here because they will be different for black and white pawns.
            rank_in_front_index = pawn_rank_index - 1
            rank_2_in_front_index = pawn_rank_index - 2
            file_to_right_index = pawn_file_index + 1
            file_to_left_index = pawn_file_index - 1


        position_in_2_front_in_bounds = self.in_bounds(rank_2_in_front_index, pawn_file_index)
        position_in_front_in_bounds = self.in_bounds(rank_in_front_index, pawn_file_index)
        position_in_front_right_in_bounds = self.in_bounds(rank_in_front_index, file_to_right_index)
        position_in_front_left_in_bounds = self.in_bounds(rank_in_front_index, file_to_left_index)
        position_to_left_in_bounds = self.in_bounds(pawn_rank_index, file_to_left_index)
        position_to_right_in_bounds = self.in_bounds(pawn_rank_index, file_to_right_index)

        # Make sure we don't index out of the list.
        if position_in_front_in_bounds:
            # Check to see if moving forward at all is possible. The pawn can only move forward on empty spaces.
            if Board[rank_in_front_index][pawn_file_index] == ".":
                possible_space = self.index_to_board_space_list(rank_in_front_index, pawn_file_index)
                list_of_possible_spaces.append(possible_space)
                # Make sure we don't index off the list.
                if position_in_2_front_in_bounds:
                    # If the pawn can move forward,
                    #   check to see if it can move forward two spaces because it hasn't moved forward at all yet.
                    if Board[rank_2_in_front_index][pawn_file_index] == "." and (pawn_rank_index == 1 or pawn_rank_index == 6):
                        possible_space = self.index_to_board_space_list(rank_2_in_front_index, pawn_file_index)
                        list_of_possible_spaces.append(possible_space)
            


        # Check if capturing a piece is possible. It is possible to capture in either direction.
        if position_in_front_in_bounds and position_to_left_in_bounds:
            if (Board[pawn_rank_index][pawn_file_index].istitle() != Board[rank_in_front_index][file_to_left_index].istitle()) and Board[rank_in_front_index][file_to_left_index] != ".":
                possible_space = self.index_to_board_space_list(rank_in_front_index, file_to_left_index)
                list_of_possible_spaces.append(possible_space)
        if position_in_front_in_bounds and position_to_right_in_bounds:
            if (Board[pawn_rank_index][pawn_file_index].istitle() != Board[rank_in_front_index][file_to_right_index].istitle()) and Board[rank_in_front_index][file_to_right_index] != ".":
                possible_space = self.index_to_board_space_list(rank_in_front_index, file_to_right_index)
                list_of_possible_spaces.append(possible_space)



        # Check to see if "en passant" is possible.

        # If the list of moves is empty en passant is not possible.
        if self.game.moves:
            # Grab the last item in the list.
            last_move = self.game.moves[-1]
            if pawn_rank == 5 and self.player.color == "White":
                if self.in_bounds(pawn_rank_index, file_to_right_index):
                    if Board[pawn_rank_index][file_to_right_index] == "p":
                        # Check to see if the pawn moved from its starting position.
                        if (last_move.from_rank == pawn_rank+2) and (last_move.from_file == file_to_right) and (last_move.to_rank == pawn_rank) and (last_move.to_file == file_to_right):
                            possible_space = self.index_to_board_space_list(rank_in_front_index, file_to_right_index)
                            list_of_possible_spaces.append(possible_space)
                if self.in_bounds(pawn_rank_index, file_to_left_index):
                    if Board[pawn_rank_index][file_to_left_index] == "p":
                        # Check to see if the pawn moved from its starting position.
                        if (last_move.from_rank == pawn_rank+2) and (last_move.from_file == file_to_left) and (last_move.to_rank == pawn_rank) and (last_move.to_file == file_to_left):
                            possible_space = self.index_to_board_space_list(rank_in_front_index, file_to_left_index)
                            list_of_possible_spaces.append(possible_space)
            if pawn_rank == 4 and self.player.color == "Black":
                if self.in_bounds(pawn_rank_index, file_to_right_index):
                    if Board[pawn_rank_index][file_to_right_index] == "P":
                        # Check to see if the pawn moved from its starting position.
                        if (last_move.from_rank == pawn_rank-2) and (last_move.from_file == file_to_right) and (last_move.to_rank == pawn_rank) and (last_move.to_file == file_to_right):
                            possible_space = self.index_to_board_space_list(rank_in_front_index, file_to_right_index)
                            list_of_possible_spaces.append(possible_space)
                if self.in_bounds(pawn_rank_index, file_to_left_index):
                    if Board[pawn_rank_index][file_to_left_index] == "P":
                        # Check to see if the pawn moved from its starting position.
                        if (last_move.from_rank == pawn_rank-2) and (last_move.from_file == file_to_left) and (last_move.to_rank == pawn_rank) and (last_move.to_file == file_to_left):
                            possible_space = self.index_to_board_space_list(rank_in_front_index, file_to_left_index)
                            list_of_possible_spaces.append(possible_space)

        return list_of_possible_spaces

    # This function is primarily for the enemy_total_possible_move_list function in order to generate space that the enemy can attack.
    # Define the spaces a pawn can attack and move to (not en passant), given the location of the pawn.
    # Takes in a Piece object as a parameter
    # Returns a list of all the possible spaces that the piece can attack.
    def pawn_engaged_space(self, piece):
        pawn_rank = piece.rank
        pawn_file = piece.file
        pawn_rank_index = pawn_rank-1
        # Subtract 96 to get in range of 1-8 and subtract 1 to get within range of list.
        pawn_file_index = (ord(pawn_file)-96)-1

        rank_in_front_index = None
        file_to_left_index = None
        file_to_left = None
        file_to_right_index = None
        file_to_right = None

        list_of_engaged_spaces = []

        # Black and white pawns will have different directions to move.
        # Don't check for self.player.color because we may check Black's pawns on White's turn, or White's pawns on Black's turn.
        if self.Board[pawn_rank_index][pawn_file_index] == "P":
            # Initialize the rank_in_front_index values here because they will be different for black and white pawns.
            rank_in_front_index = pawn_rank_index + 1
            file_to_left_index = pawn_file_index - 1
            file_to_left = chr(file_to_left_index+96)
            file_to_right_index = pawn_file_index + 1
            file_to_right = chr(file_to_right_index+96)
        else: # The color player is "Black"
            # Initialize the rank_in_front_index values here because they will be different for black and white pawns.
            rank_in_front_index = pawn_rank_index - 1
            file_to_right_index = pawn_file_index + 1
            file_to_left_index = pawn_file_index - 1

        position_in_front_right_in_bounds = self.in_bounds(rank_in_front_index, file_to_right_index)
        position_in_front_left_in_bounds = self.in_bounds(rank_in_front_index, file_to_left_index)            

        # Check if capturing a piece is possible. It is possible to capture in either direction.
        if position_in_front_left_in_bounds:
                engaged_space = self.index_to_board_space_list(rank_in_front_index, file_to_left_index)
                list_of_engaged_spaces.append(engaged_space)
        if position_in_front_right_in_bounds:
                engaged_space = self.index_to_board_space_list(rank_in_front_index, file_to_right_index)
                list_of_engaged_spaces.append(engaged_space)

        return list_of_engaged_spaces

    # Define the spaces a rook can move, given the location of the rook.
    # Takes in a Piece object as a parameter
    # Returns a list of all the possible spaces that the piece can move to.
    def rook_move_space(self, Board, from_file_index, from_rank_index, engaged_space=False, line_of_sight=False, king_called=False):
        rook_rank_index = from_rank_index
        rook_file_index = from_file_index
        enemy_piece_count = 0

        max_spaces_up = 0
        max_spaces_down = 0
        max_spaces_left = 0
        max_spaces_right = 0

        list_of_possible_spaces = []
        list_of_engaged_spaces = []
        list_of_line_of_sight_space = []

        has_line_of_sight_to_king_blocked = False

        # Determine the spaces that be traveled upwards
        for space in range(rook_rank_index+1, 8):
            if Board[space][rook_file_index] == ".":
                max_spaces_up = max_spaces_up + 1
                possible_space = self.index_to_board_space_list(space, rook_file_index)
                list_of_possible_spaces.append(possible_space)
            # If the letter in the list of lists is the opposite case of the current rook, it is a piece that can be captured.
            # The loop must be broken from afterwards, because capturing a piece halts movement.
            elif (Board[space][rook_file_index].istitle() != Board[rook_rank_index][rook_file_index].istitle()):
                max_spaces_up = max_spaces_up + 1
                enemy_piece_count = enemy_piece_count + 1
                if engaged_space == False or (enemy_piece_count == 1 and king_called == True and (Board[space][rook_file_index] != "K" and Board[space][rook_file_index] != "k")):
                    possible_space = self.index_to_board_space_list(space, rook_file_index)
                    list_of_possible_spaces.append(possible_space)
                    break
                if engaged_space == True:
                    possible_space = self.index_to_board_space_list(space, rook_file_index)
                    list_of_possible_spaces.append(possible_space)
                    list_of_line_of_sight_space.append(possible_space)
                if enemy_piece_count == 2:
                    if (line_of_sight == True) and (Board[space][rook_file_index] == "k" or Board[space][rook_file_index] == "K"):
                        has_line_of_sight_to_king_blocked = True
                    break
            elif (Board[space][rook_file_index].istitle() == Board[rook_rank_index][rook_file_index].istitle()) and (engaged_space == True):
                max_spaces_up = max_spaces_up + 1
                possible_space = self.index_to_board_space_list(space, rook_file_index)
                list_of_possible_spaces.append(possible_space)
                break
            else:
                break

        # Reset what spaces are in 1 direction of the line of sight if we haven't encountered the king.
        if has_line_of_sight_to_king_blocked == False:
            list_of_line_of_sight_space = []
        # Reset the count per each direction.
        enemy_piece_count = 0
        # Determine the spaces that be traveled downwards
        for space in range(rook_rank_index-1, -1, -1):
            if Board[space][rook_file_index] == ".":
                max_spaces_down = max_spaces_down + 1
                possible_space = self.index_to_board_space_list(space, rook_file_index)
                list_of_possible_spaces.append(possible_space)
            # You have found the enemy!
            elif (Board[space][rook_file_index].istitle() != Board[rook_rank_index][rook_file_index].istitle()):
                max_spaces_down = max_spaces_down + 1
                enemy_piece_count = enemy_piece_count + 1
                if engaged_space == False or (enemy_piece_count == 1 and king_called == True and (Board[space][rook_file_index] != "K" and Board[space][rook_file_index] != "k")):
                    possible_space = self.index_to_board_space_list(space, rook_file_index)
                    list_of_possible_spaces.append(possible_space)
                    break
                if engaged_space == True:
                    possible_space = self.index_to_board_space_list(space, rook_file_index)
                    list_of_possible_spaces.append(possible_space)
                    list_of_line_of_sight_space.append(possible_space)
                if enemy_piece_count == 2:
                    if (line_of_sight == True) and (Board[space][rook_file_index] == "k" or Board[space][rook_file_index] == "K"):
                        has_line_of_sight_to_king_blocked = True
                    break
            elif (Board[space][rook_file_index].istitle() == Board[rook_rank_index][rook_file_index].istitle()) and (engaged_space == True):
                max_spaces_down = max_spaces_down + 1
                possible_space = self.index_to_board_space_list(space, rook_file_index)
                list_of_possible_spaces.append(possible_space)
                break
            else:
                break

        # Reset what spaces are in 1 direction of the line of sight if we haven't encountered the king.
        if has_line_of_sight_to_king_blocked == False:
            list_of_line_of_sight_space = []
        # Reset the count per each direction.
        enemy_piece_count = 0
        # Determine the spaces that be traveled left
        for space in range(rook_file_index-1, -1, -1):
            if Board[rook_rank_index][space] == ".":
                max_spaces_left = max_spaces_left + 1
                possible_space = self.index_to_board_space_list(rook_rank_index, space)
                list_of_possible_spaces.append(possible_space)
            # You have found the enemy!
            elif (Board[rook_rank_index][space].istitle() != Board[rook_rank_index][rook_file_index].istitle()):
                max_spaces_left = max_spaces_left + 1
                enemy_piece_count = enemy_piece_count + 1
                if engaged_space == False or (enemy_piece_count == 1 and king_called == True and (Board[rook_rank_index][space] != "K" and Board[rook_rank_index][space] != "k")):
                    possible_space = self.index_to_board_space_list(rook_rank_index, space)
                    list_of_possible_spaces.append(possible_space)
                    list_of_line_of_sight_space.append(possible_space)
                    break
                if engaged_space == True:
                    possible_space = self.index_to_board_space_list(rook_rank_index, space)
                    list_of_possible_spaces.append(possible_space)
                if enemy_piece_count == 2:
                    if (line_of_sight == True) and (Board[rook_rank_index][space] == "k" or Board[rook_rank_index][space] == "K"):
                        has_line_of_sight_to_king_blocked = True
                    break
            elif (Board[rook_rank_index][space].istitle() == Board[rook_rank_index][rook_file_index].istitle()) and (engaged_space == True):
                max_spaces_left = max_spaces_left + 1
                possible_space = self.index_to_board_space_list(rook_rank_index, space)
                list_of_possible_spaces.append(possible_space)
                break
            else:
                break

        # Reset what spaces are in 1 direction of the line of sight if we haven't encountered the king.
        if has_line_of_sight_to_king_blocked == False:
            list_of_line_of_sight_space = []
        # Reset the count per each direction.
        enemy_piece_count = 0
        # Determine the spaces that be traveled right
        for space in range(rook_file_index+1, 8):
            if Board[rook_rank_index][space] == ".":
                max_spaces_right = max_spaces_right + 1
                possible_space = self.index_to_board_space_list(rook_rank_index, space)
                list_of_possible_spaces.append(possible_space)
            # You have found the enemy!
            elif (Board[rook_rank_index][space].istitle() != Board[rook_rank_index][rook_file_index].istitle()):
                max_spaces_right = max_spaces_right + 1
                enemy_piece_count = enemy_piece_count + 1
                if engaged_space == False or (enemy_piece_count == 1 and king_called == True and (Board[rook_rank_index][space] != "K" and Board[rook_rank_index][space] != "k")):
                    possible_space = self.index_to_board_space_list(rook_rank_index, space)
                    list_of_possible_spaces.append(possible_space)
                    break
                if engaged_space == True:
                    possible_space = self.index_to_board_space_list(rook_rank_index, space)
                    list_of_possible_spaces.append(possible_space)
                    list_of_line_of_sight_space.append(possible_space)
                if enemy_piece_count == 2:
                    if (line_of_sight == True) and (Board[rook_rank_index][space] == "k" or Board[rook_rank_index][space] == "K"):
                        has_line_of_sight_to_king_blocked = True
                    break
            elif (Board[rook_rank_index][space].istitle() == Board[rook_rank_index][rook_file_index].istitle()) and (engaged_space == True):
                max_spaces_right = max_spaces_right + 1
                possible_space = self.index_to_board_space_list(rook_rank_index, space)
                list_of_possible_spaces.append(possible_space)
                break
            else:
                break

        return list_of_possible_spaces

    # Takes in a Piece object as a parameter
    # Returns a list of all the possible spaces that the piece can move to.
    def knight_move_space(self, Board, from_file_index, from_rank_index, engaged_space=False):
        knight_rank_index = from_rank_index
        knight_file_index = from_file_index

        list_of_possible_spaces = []

        position_one_in_bounds = self.in_bounds(knight_rank_index+2, knight_file_index+1)
        position_two_in_bounds = self.in_bounds(knight_rank_index+1, knight_file_index+2)
        position_three_in_bounds = self.in_bounds(knight_rank_index-1, knight_file_index+2)
        position_four_in_bounds = self.in_bounds(knight_rank_index-2, knight_file_index+1)
        position_five_in_bounds = self.in_bounds(knight_rank_index-2, knight_file_index-1)
        position_six_in_bounds = self.in_bounds(knight_rank_index-1, knight_file_index-2)
        position_seven_in_bounds = self.in_bounds(knight_rank_index+1, knight_file_index-2)
        position_eight_in_bounds = self.in_bounds(knight_rank_index+2, knight_file_index-1)

        position_knight = self.index_to_board_space_list(knight_rank_index, knight_file_index)
        position_one = self.index_to_board_space_list(knight_rank_index+2, knight_file_index+1)
        position_two = self.index_to_board_space_list(knight_rank_index+1, knight_file_index+2)
        position_three = self.index_to_board_space_list(knight_rank_index-1, knight_file_index+2)
        position_four = self.index_to_board_space_list(knight_rank_index-2, knight_file_index+1)
        position_five = self.index_to_board_space_list(knight_rank_index-2, knight_file_index-1)
        position_six = self.index_to_board_space_list(knight_rank_index-1, knight_file_index-2)
        position_seven = self.index_to_board_space_list(knight_rank_index+1, knight_file_index-2)
        position_eight = self.index_to_board_space_list(knight_rank_index+2, knight_file_index-1)

        position_knight_value = Board[knight_rank_index][knight_file_index]
        if position_one_in_bounds:
            position_one_value = Board[knight_rank_index+2][knight_file_index+1]
        else:
            position_one_value = None
        if position_two_in_bounds:
            position_two_value = Board[knight_rank_index+1][knight_file_index+2]
        else:
            position_two_value = None
        if position_three_in_bounds:
            position_three_value = Board[knight_rank_index-1][knight_file_index+2]
        else:
            position_three_value = None
        if position_four_in_bounds:
            position_four_value = Board[knight_rank_index-2][knight_file_index+1]
        else:
            position_four_value = None
        if position_five_in_bounds:
            position_five_value = Board[knight_rank_index-2][knight_file_index-1]
        else:
            position_five_value = None
        if position_six_in_bounds:
            position_six_value = Board[knight_rank_index-1][knight_file_index-2]
        else:
            position_six_value = None
        if position_seven_in_bounds:
            position_seven_value = Board[knight_rank_index+1][knight_file_index-2]
        else:
            position_seven_value = None
        if position_eight_in_bounds:
            position_eight_value = Board[knight_rank_index+2][knight_file_index-1]
        else:
            position_eight_value = None


        # If the possible space to move is empty, or the space has an opponent piece...
        if position_one_in_bounds:
            if (position_one_value == ".") or (position_knight_value.istitle() != position_one_value.istitle()):
                list_of_possible_spaces.append(position_one)
            elif (position_knight_value.istitle() == position_one_value.istitle()) and engaged_space == True:
                list_of_possible_spaces.append(position_one)
        if position_two_in_bounds:
            if (position_two_value == ".") or (position_knight_value.istitle() != position_two_value.istitle()):
                list_of_possible_spaces.append(position_two)
            elif (position_knight_value.istitle() == position_two_value.istitle()) and engaged_space == True:
                list_of_possible_spaces.append(position_two)
        if position_three_in_bounds:
            if (position_three_value == ".") or (position_knight_value.istitle() != position_three_value.istitle()):
                list_of_possible_spaces.append(position_three)
            elif (position_knight_value.istitle() == position_three_value.istitle()) and engaged_space == True:
                list_of_possible_spaces.append(position_three)
        if position_four_in_bounds:
            if (position_four_value == ".") or (position_knight_value.istitle() != position_four_value.istitle()):
                list_of_possible_spaces.append(position_four)
            elif (position_knight_value.istitle() == position_four_value.istitle()) and engaged_space == True:
                list_of_possible_spaces.append(position_four)
        if position_five_in_bounds:
            if (position_five_value == ".") or (position_knight_value.istitle() != position_five_value.istitle()):
                list_of_possible_spaces.append(position_five)
            elif (position_knight_value.istitle() == position_five_value.istitle()) and engaged_space == True:
                list_of_possible_spaces.append(position_five)
        if position_six_in_bounds:
            if (position_six_value == ".") or (position_knight_value.istitle() != position_six_value.istitle()):
                list_of_possible_spaces.append(position_six)
            elif (position_knight_value.istitle() == position_six_value.istitle()) and engaged_space == True:
                list_of_possible_spaces.append(position_six)
        if position_seven_in_bounds:
            if (position_seven_value == ".") or (position_knight_value.istitle() != position_seven_value.istitle()):
                list_of_possible_spaces.append(position_seven)
            elif (position_knight_value.istitle() == position_seven_value.istitle()) and engaged_space == True:
                list_of_possible_spaces.append(position_seven)
        if position_eight_in_bounds:
            if (position_eight_value == ".") or (position_knight_value.istitle() != position_eight_value.istitle()):
                list_of_possible_spaces.append(position_eight)
            elif (position_knight_value.istitle() == position_eight_value.istitle()) and engaged_space == True:
                list_of_possible_spaces.append(position_eight)


        return list_of_possible_spaces

    # Takes in a Piece object as a parameter
    # Returns a list of all the possible spaces that the piece can move to.
    def bishop_move_space(self, Board, from_file_index, from_rank_index, engaged_space=False, line_of_sight=False, king_called=False):
        bishop_rank_index = from_rank_index
        bishop_file_index = from_file_index

        max_spaces_up = 0
        max_spaces_down = 0
        max_spaces_left = 0
        max_spaces_right = 0

        enemy_piece_count = 0
        list_of_possible_spaces = []

        list_of_line_of_sight_space = []
        has_line_of_sight_to_king_blocked = False

        # Find the amount of spaces above the piece.
        for space in range(bishop_rank_index+1, 8):
            max_spaces_up = max_spaces_up + 1
        # Find the amount of spaces below the piece.
        for space in range(bishop_rank_index-1, -1, -1):
            max_spaces_down = max_spaces_down + 1
        # Find the amount of spaces to the left of the piece.
        for space in range(bishop_file_index-1, -1, -1):
            max_spaces_left = max_spaces_left + 1
        # Find the amount of spaces to the right of the piece.
        for space in range(bishop_file_index+1, 8):
            max_spaces_right = max_spaces_right + 1

        
        max_spaces_up_right = min(max_spaces_up, max_spaces_right)
        max_spaces_down_right = min(max_spaces_down, max_spaces_right)
        max_spaces_down_left = min(max_spaces_down, max_spaces_left)
        max_spaces_up_left = min(max_spaces_up, max_spaces_left)

        max_spaces_up_right_possible = 0
        max_spaces_down_right_possible = 0
        max_spaces_down_left_possible = 0
        max_spaces_up_left_possible = 0

        # Start range from 1 because we don't want to be checking against its own space.
        # Add plus one to the range of the for loops because the range is inclusive.
        for i in range(1, max_spaces_up_right+1):
            if Board[bishop_rank_index+i][bishop_file_index+i] == ".":
                max_spaces_up_right_possible = max_spaces_up_right_possible + 1
                possible_space = self.index_to_board_space_list(bishop_rank_index+i, bishop_file_index+i)
                list_of_possible_spaces.append(possible_space)
            # Same results, but a bishop must stop after capturing a piece.
            elif Board[bishop_rank_index][bishop_file_index].istitle() != Board[bishop_rank_index+i][bishop_file_index+i].istitle(): ####################################################################################
                max_spaces_up_right_possible = max_spaces_up_right_possible + 1
                enemy_piece_count = enemy_piece_count + 1
                if engaged_space == False or (enemy_piece_count == 1 and king_called == True and (Board[bishop_rank_index+i][bishop_file_index+i] != "K" and Board[bishop_rank_index+i][bishop_file_index+i] != "k")):
                    possible_space = self.index_to_board_space_list(bishop_rank_index+i, bishop_file_index+i)
                    list_of_possible_spaces.append(possible_space)
                    break
                if engaged_space == True:
                    possible_space = self.index_to_board_space_list(bishop_rank_index+i, bishop_file_index+i)
                    list_of_possible_spaces.append(possible_space)
                    list_of_line_of_sight_space.append(possible_space)
                if enemy_piece_count == 2:
                    if (line_of_sight == True) and (Board[bishop_rank_index+i][bishop_file_index+i] == "k" or Board[bishop_rank_index+i][bishop_file_index+i] == "K"):
                        has_line_of_sight_to_king_blocked = True
                    break
            elif Board[bishop_rank_index][bishop_file_index].istitle() == Board[bishop_rank_index+i][bishop_file_index+i].istitle() and (engaged_space == True):
                max_spaces_up_right_possible = max_spaces_up_right_possible + 1
                possible_space = self.index_to_board_space_list(bishop_rank_index+i, bishop_file_index+i)
                list_of_possible_spaces.append(possible_space)
                break
            # Check if the space is a piece you control.
            elif (Board[bishop_rank_index][bishop_file_index].istitle() == Board[bishop_rank_index+i][bishop_file_index+i].istitle()):
                # You cannot pass through your own pieces.
                break

        # Reset what spaces are in 1 direction of the line of sight if we haven't encountered the king.
        if has_line_of_sight_to_king_blocked == False:
            list_of_line_of_sight_space = []
        # Reset the count per each direction.
        enemy_piece_count = 0
        for i in range(1, max_spaces_down_right+1):
            if Board[bishop_rank_index-i][bishop_file_index+i] == ".":
                max_spaces_down_right_possible = max_spaces_down_right_possible + 1
                possible_space = self.index_to_board_space_list(bishop_rank_index-i, bishop_file_index+i)
                list_of_possible_spaces.append(possible_space)
            # Same results, but a bishop must stop after capturing a piece.
            elif Board[bishop_rank_index][bishop_file_index].istitle() != Board[bishop_rank_index-i][bishop_file_index+i].istitle():
                max_spaces_down_right_possible = max_spaces_down_right_possible + 1
                enemy_piece_count = enemy_piece_count + 1
                if engaged_space == False or (enemy_piece_count == 1 and king_called == True and (Board[bishop_rank_index-i][bishop_file_index+i] != "K" and Board[bishop_rank_index-i][bishop_file_index+i] != "k")):
                    possible_space = self.index_to_board_space_list(bishop_rank_index-i, bishop_file_index+i)
                    list_of_possible_spaces.append(possible_space)
                    break
                if engaged_space == True:
                    possible_space = self.index_to_board_space_list(bishop_rank_index-i, bishop_file_index+i)
                    list_of_possible_spaces.append(possible_space)
                    list_of_line_of_sight_space.append(possible_space)
                if enemy_piece_count == 2:
                    if (line_of_sight == True) and (Board[bishop_rank_index-i][bishop_file_index+i] == "k" or Board[bishop_rank_index-i][bishop_file_index+i] == "K"):
                        has_line_of_sight_to_king_blocked = True
                    break
            elif Board[bishop_rank_index][bishop_file_index].istitle() == Board[bishop_rank_index-i][bishop_file_index+i].istitle() and (engaged_space == True):
                max_spaces_down_right_possible = max_spaces_down_right_possible + 1
                possible_space = self.index_to_board_space_list(bishop_rank_index-i, bishop_file_index+i)
                list_of_possible_spaces.append(possible_space)
                break
            # Check if the space is a piece you control.
            elif (Board[bishop_rank_index][bishop_file_index].istitle() == Board[bishop_rank_index-i][bishop_file_index+i].istitle()):
                # You cannot pass through your own pieces.
                break

        # Reset what spaces are in 1 direction of the line of sight if we haven't encountered the king.
        if has_line_of_sight_to_king_blocked == False:
            list_of_line_of_sight_space = []                
        # Reset the count per each direction.
        enemy_piece_count = 0
        for i in range(1, max_spaces_down_left+1):
            if Board[bishop_rank_index-i][bishop_file_index-i] == ".":
                max_spaces_down_left_possible = max_spaces_down_left_possible + 1
                possible_space = self.index_to_board_space_list(bishop_rank_index-i, bishop_file_index-i)
                list_of_possible_spaces.append(possible_space)
            # Same results, but a bishop must stop after capturing a piece.
            elif Board[bishop_rank_index][bishop_file_index].istitle() != Board[bishop_rank_index-i][bishop_file_index-i].istitle():
                max_spaces_down_left_possible = max_spaces_down_left_possible + 1
                enemy_piece_count = enemy_piece_count + 1
                if engaged_space == False or (enemy_piece_count == 1 and king_called == True and (Board[bishop_rank_index-i][bishop_file_index-i] != "K" and Board[bishop_rank_index-i][bishop_file_index-i] != "k")):
                    possible_space = self.index_to_board_space_list(bishop_rank_index-i, bishop_file_index-i)
                    list_of_possible_spaces.append(possible_space)
                    break
                if engaged_space == True:
                    possible_space = self.index_to_board_space_list(bishop_rank_index-i, bishop_file_index-i)
                    list_of_possible_spaces.append(possible_space)
                    list_of_line_of_sight_space.append(possible_space)
                if enemy_piece_count == 2:
                    if (line_of_sight == True) and (Board[bishop_rank_index-i][bishop_file_index-i] == "k" or Board[bishop_rank_index-i][bishop_file_index-i] == "K"):
                        has_line_of_sight_to_king_blocked = True
                    break
            elif Board[bishop_rank_index][bishop_file_index].istitle() == Board[bishop_rank_index-i][bishop_file_index-i].istitle() and (engaged_space == True):
                max_spaces_down_left_possible = max_spaces_down_left_possible + 1
                possible_space = self.index_to_board_space_list(bishop_rank_index-i, bishop_file_index-i)
                list_of_possible_spaces.append(possible_space)
                break
            # Check if the space is a piece you control.
            elif (Board[bishop_rank_index][bishop_file_index].istitle() == Board[bishop_rank_index-i][bishop_file_index-i].istitle()):
                # You cannot pass through your own pieces.
                break

        # Reset what spaces are in 1 direction of the line of sight if we haven't encountered the king.
        if has_line_of_sight_to_king_blocked == False:
            list_of_line_of_sight_space = []                
        # Reset the count per each direction.
        enemy_piece_count = 0
        for i in range(1, max_spaces_up_left+1):
            if Board[bishop_rank_index+i][bishop_file_index-i] == ".":
                max_spaces_up_left_possible = max_spaces_up_left_possible + 1
                possible_space = self.index_to_board_space_list(bishop_rank_index+i, bishop_file_index-i)
                list_of_possible_spaces.append(possible_space)
            # Same results, but a bishop must stop after capturing a piece.
            elif Board[bishop_rank_index][bishop_file_index].istitle() != Board[bishop_rank_index+i][bishop_file_index-i].istitle():
                max_spaces_up_left_possible = max_spaces_up_left_possible + 1
                enemy_piece_count = enemy_piece_count + 1
                if engaged_space == False or (enemy_piece_count == 1 and king_called == True and (Board[bishop_rank_index+i][bishop_file_index-i] != "K" and Board[bishop_rank_index+i][bishop_file_index-i] != "k")):
                    possible_space = self.index_to_board_space_list(bishop_rank_index+i, bishop_file_index-i)
                    list_of_possible_spaces.append(possible_space)
                    list_of_line_of_sight_space.append(possible_space)
                    break
                if engaged_space == True:
                    possible_space = self.index_to_board_space_list(bishop_rank_index+i, bishop_file_index-i)
                    list_of_possible_spaces.append(possible_space)
                if enemy_piece_count == 2:
                    if (line_of_sight == True) and (Board[bishop_rank_index+i][bishop_file_index-i] == "k" or Board[bishop_rank_index+i][bishop_file_index-i] == "K"):
                        has_line_of_sight_to_king_blocked = True
                    break
            elif Board[bishop_rank_index][bishop_file_index].istitle() == Board[bishop_rank_index+i][bishop_file_index-i].istitle() and (engaged_space == True):
                max_spaces_up_left_possible = max_spaces_up_left_possible + 1
                possible_space = self.index_to_board_space_list(bishop_rank_index+i, bishop_file_index-i)
                list_of_possible_spaces.append(possible_space)
                break
            # Check if the space is a piece you control.
            elif (Board[bishop_rank_index][bishop_file_index].istitle() == Board[bishop_rank_index+i][bishop_file_index-i].istitle()):
                # You cannot pass through your own pieces.
                break



        return list_of_possible_spaces

    # Takes in a Piece object as a parameter
    # Returns a list of all the possible spaces that the piece can move to.
    def queen_move_space(self, Board, from_file_index, from_rank_index, engaged_space=False, line_of_sight=False, king_called=False):
        list_of_possible_spaces = []
        list_of_lateral_spaces = []
        list_of_diagonal_spaces = []

        # Calling these functions is currently uneccessary because the functions themselves check if the piece is a queen.
        # Passing in engaged space and line_of_sight should use the variable that was passed into queen.
        list_of_lateral_spaces = self.rook_move_space(Board, from_file_index, from_rank_index, engaged_space, line_of_sight, king_called)
        # Passing in engaged space and line_of_sight should use the variable that was passed into queen.
        list_of_diagonal_spaces = self.bishop_move_space(Board, from_file_index, from_rank_index, engaged_space, line_of_sight, king_called)

        if len(list_of_lateral_spaces) > 0 or len(list_of_diagonal_spaces) > 0:
            list_of_possible_spaces = list_of_lateral_spaces + list_of_diagonal_spaces

        return list_of_possible_spaces

    # Takes in a Piece object as a parameter
    # Takes in a boolean engaged_space parameter that determines if it should output spaces that the enemy engages.
    # Returns a list of all the possible spaces that the piece can move to.
    def king_move_space(self, Board, from_file_index, from_rank_index, engaged_space=False):
        king_rank_index = from_rank_index
        king_file_index = from_file_index
        king_rank = king_rank_index+1
        king_file = chr(((king_file_index)+1)+96)

        list_of_possible_spaces = []

        space_up_in_bounds = self.in_bounds(king_rank_index+1, king_file_index)
        space_up_right_in_bounds = self.in_bounds(king_rank_index+1, king_file_index+1)
        space_right_in_bounds = self.in_bounds(king_rank_index, king_file_index+1)
        space_down_right_in_bounds = self.in_bounds(king_rank_index-1, king_file_index+1)
        space_down_in_bounds = self.in_bounds(king_rank_index-1, king_file_index)
        space_down_left_in_bounds = self.in_bounds(king_rank_index-1, king_file_index-1)
        space_left_in_bounds = self.in_bounds(king_rank_index, king_file_index-1)
        space_up_left_in_bounds = self.in_bounds(king_rank_index+1, king_file_index-1)


        # Check to see if the spaces adjacent to the king are empty or contain an enemy piece.
        # This does not check if the King is in check.
        if(space_up_in_bounds):
            if Board[king_rank_index+1][king_file_index] == "." or (Board[king_rank_index][king_file_index].istitle() != Board[king_rank_index+1][king_file_index].istitle()):
                possible_space = self.index_to_board_space_list(king_rank_index+1, king_file_index)
                list_of_possible_spaces.append(possible_space)
            if engaged_space == True and (Board[king_rank_index][king_file_index].istitle() == Board[king_rank_index+1][king_file_index].istitle()):
                possible_space = self.index_to_board_space_list(king_rank_index+1, king_file_index)
                list_of_possible_spaces.append(possible_space)
        if(space_up_right_in_bounds):
            if Board[king_rank_index+1][king_file_index+1] == "." or (Board[king_rank_index][king_file_index].istitle() != Board[king_rank_index+1][king_file_index+1].istitle()):
                possible_space = self.index_to_board_space_list(king_rank_index+1, king_file_index+1)
                list_of_possible_spaces.append(possible_space)
            if engaged_space == True and (Board[king_rank_index][king_file_index].istitle() == Board[king_rank_index+1][king_file_index+1].istitle()):
                possible_space = self.index_to_board_space_list(king_rank_index+1, king_file_index+1)
                list_of_possible_spaces.append(possible_space)
        if(space_right_in_bounds):
            if Board[king_rank_index][king_file_index+1] == "." or (Board[king_rank_index][king_file_index].istitle() != Board[king_rank_index][king_file_index+1].istitle()):
                possible_space = self.index_to_board_space_list(king_rank_index, king_file_index+1)
                list_of_possible_spaces.append(possible_space)
            if engaged_space == True and (Board[king_rank_index][king_file_index].istitle() == Board[king_rank_index][king_file_index+1].istitle()):
                possible_space = self.index_to_board_space_list(king_rank_index, king_file_index+1)
                list_of_possible_spaces.append(possible_space)
        if(space_down_right_in_bounds):
            if Board[king_rank_index-1][king_file_index+1] == "." or (Board[king_rank_index][king_file_index].istitle() != Board[king_rank_index-1][king_file_index+1].istitle()):
                possible_space = self.index_to_board_space_list(king_rank_index-1, king_file_index+1)
                list_of_possible_spaces.append(possible_space)
            if engaged_space == True and (Board[king_rank_index][king_file_index].istitle() == Board[king_rank_index-1][king_file_index+1].istitle()):
                possible_space = self.index_to_board_space_list(king_rank_index-1, king_file_index+1)
                list_of_possible_spaces.append(possible_space)
        if(space_down_in_bounds):
            if Board[king_rank_index-1][king_file_index] == "." or (Board[king_rank_index][king_file_index].istitle() != Board[king_rank_index-1][king_file_index].istitle()):
                possible_space = self.index_to_board_space_list(king_rank_index-1, king_file_index)
                list_of_possible_spaces.append(possible_space)
            if engaged_space == True and (Board[king_rank_index][king_file_index].istitle() == Board[king_rank_index-1][king_file_index].istitle()):
                possible_space = self.index_to_board_space_list(king_rank_index-1, king_file_index)
                list_of_possible_spaces.append(possible_space)
        if(space_down_left_in_bounds):
            if Board[king_rank_index-1][king_file_index-1] == "." or (Board[king_rank_index][king_file_index].istitle() != Board[king_rank_index-1][king_file_index-1].istitle()):
                possible_space = self.index_to_board_space_list(king_rank_index-1, king_file_index-1)
                list_of_possible_spaces.append(possible_space)
            if engaged_space == True and (Board[king_rank_index][king_file_index].istitle() == Board[king_rank_index-1][king_file_index-1].istitle()):
                possible_space = self.index_to_board_space_list(king_rank_index-1, king_file_index-1)
                list_of_possible_spaces.append(possible_space)
        if(space_left_in_bounds):
            if Board[king_rank_index][king_file_index-1] == "." or (Board[king_rank_index][king_file_index].istitle() != Board[king_rank_index][king_file_index-1].istitle()):
                possible_space = self.index_to_board_space_list(king_rank_index, king_file_index-1)
                list_of_possible_spaces.append(possible_space)
            if engaged_space == True and (Board[king_rank_index][king_file_index].istitle() == Board[king_rank_index][king_file_index-1].istitle()):
                possible_space = self.index_to_board_space_list(king_rank_index, king_file_index-1)
                list_of_possible_spaces.append(possible_space)
        if(space_up_left_in_bounds):
            if Board[king_rank_index+1][king_file_index-1] == "." or (Board[king_rank_index][king_file_index].istitle() != Board[king_rank_index+1][king_file_index-1].istitle()):
                possible_space = self.index_to_board_space_list(king_rank_index+1, king_file_index-1)
                list_of_possible_spaces.append(possible_space)
            if engaged_space == True and (Board[king_rank_index][king_file_index].istitle() == Board[king_rank_index+1][king_file_index-1].istitle()):
                possible_space = self.index_to_board_space_list(king_rank_index+1, king_file_index-1)
                list_of_possible_spaces.append(possible_space)


        # Castling
        queenside_rook = None
        kingside_rook = None
        list_of_current_players_pieces = self.player.pieces
        for piece in list_of_current_players_pieces:
            if piece.type == "Rook":
                if piece.file == "a":
                    queenside_rook = piece
                elif piece.file == "f":
                    kingside_rook = piece


        # Castling Queenside
        # Is the king and rook on the player's first rank?
        if king_file == 1 and (queenside_rook.file == (king_file+3)):
            # Have the king or rook previously moved?
            if (piece.has_moved != True) and (queenside_rook.has_moved != True):
                # Are there any pieces between the king and rook?
                if (Board[king_rank_index][king_file_index-3] == ".") and (Board[king_rank_index][king_file_index-2]== ".") and (Board[king_rank_index][king_file_index-1] == "."):
                    # Is the king in check?
                    if self.player.in_check == False:
                        # Will the king pass through a square attacked by the enemy?
                        enemy_total_possible_move_list = self.enemy_total_possible_move_list()
                        queenside_castle_space_left = self.index_to_board_space_list(king_rank_index, king_file_index-3)
                        queenside_castle_space_middle = self.index_to_board_space_list(king_rank_index, king_file_index-2)
                        queenside_castle_space_right = self.index_to_board_space_list(king_rank_index, king_file_index-1)
                        if (queenside_castle_space_left not in enemy_total_possible_move_list) and (queenside_castle_space_middle not in enemy_total_possible_move_list) and (queenside_castle_space_right not in enemy_total_possible_move_list):
                            # You can now castle queenside.
                            list_of_possible_spaces.append(queenside_castle_space_middle)

        # Castling Kingside
        # Is the king and rook on the player's first rank?
        if king_file == 1 and (kingside_rook.file == (king_file-4)):
            # Have the king or rook previously moved?
            if (piece.has_moved != True) and (kingside_rook.has_moved != True):
                # Are there any pieces between the king and rook?
                if (Board[king_rank_index][king_file_index+2] == ".") and (Board[king_rank_index][king_file_index+1] == "."):
                    # Is the king in check?
                    if self.player.in_check == False:
                        # Will the king pass through a square attacked by the enemy?
                        enemy_total_possible_move_list = self.enemy_total_possible_move_list()
                        kingside_castle_space_left = self.index_to_board_space_list(king_rank_index, king_file_index+1)
                        kingside_castle_space_right = self.index_to_board_space_list(king_rank_index, king_file_index+2)
                        if (kingside_castle_space_left not in enemy_total_possible_move_list) and (kingside_castle_space_right not in enemy_total_possible_move_list):
                            # You can now castle kingside.
                            list_of_possible_spaces.append(kingside_castle_space_right)

        '''
        if engaged_space == True:
            return list_of_possible_spaces
        '''

        '''
        if engaged_space == False:
            king_called = True
            enemy_total_possible_move_list = self.enemy_total_possible_move_list(king_called)

            list_of_possible_spaces_not_engaged_by_enemy = [space for space in list_of_possible_spaces if space not in enemy_total_possible_move_list]

            return list_of_possible_spaces_not_engaged_by_enemy
        '''

        return list_of_possible_spaces

    # This function is for if the previous player's turn put the current player's king in check. It is not for making sure the current player's move keeps the king out of check.
    # This checks if a kings move will move it out of check.
    # Generate a list of all the possible moves that the enemy player can make.
    # Return that list.
    def enemy_total_possible_move_list(self, king_called=False):
        list_of_uncaptured_pieces = self.game.pieces
        list_of_current_players_pieces = self.player.pieces
        list_of_enemy_pieces = [piece for piece in list_of_uncaptured_pieces if piece not in list_of_current_players_pieces]
        total_enemy_move_list = []
        engaged_space = True
        line_of_sight = False

        for piece in list_of_enemy_pieces:
            if piece.type == "Pawn":
                # Use the pawn_engaged_space because the pawn may be able to attack pieces that move near its diagonals when it cant move to those spaces.
                enemy_pawn_engaged_list = self.pawn_engaged_space(piece)
                total_enemy_move_list = total_enemy_move_list + enemy_pawn_engaged_list
            if piece.type == "Rook":
                enemy_rook_move_list = self.rook_move_space(piece, engaged_space, line_of_sight, king_called)
                if len(enemy_rook_move_list) > 0:
                    total_enemy_move_list = total_enemy_move_list + enemy_rook_move_list
            if piece.type == "Knight":
                enemy_knight_move_list = self.knight_move_space(piece, engaged_space)
                if len(enemy_knight_move_list) > 0:
                    total_enemy_move_list = total_enemy_move_list + enemy_knight_move_list
            if piece.type == "Bishop":
                enemy_bishop_move_list = self.bishop_move_space(piece, engaged_space, line_of_sight, king_called)
                if len(enemy_bishop_move_list) > 0:
                    total_enemy_move_list = total_enemy_move_list + enemy_bishop_move_list
            if piece.type == "Queen":
                enemy_queen_move_list = self.queen_move_space(piece, engaged_space, line_of_sight, king_called)
                if len(enemy_queen_move_list) > 0:
                    total_enemy_move_list = total_enemy_move_list + enemy_queen_move_list
            if piece.type == "King":
                enemy_king_move_list = self.king_move_space(piece, engaged_space)
                if len(enemy_king_move_list) > 0:
                    total_enemy_move_list = total_enemy_move_list + enemy_king_move_list

        return total_enemy_move_list

    # A method to determine a score for only one player at certain board state based on the minimum value for each chess piece.
    # The only parameter is the board state, which should be a list of lists, containing strings.
    # Returns a integer value for the player it is called for.
    def generate_board_state_score(self, Board, player):

        board_state_score_white = 0
        board_state_score_black = 0

        # Generate the score for a board state.
        for row in Board:
            for piece in row:
                if piece == "P":
                    board_state_score_white = board_state_score_white + 1
                if piece == "p":
                    board_state_score_black = board_state_score_black + 1
                if piece == "R":
                    board_state_score_white = board_state_score_white + 5
                if piece == "r":
                    board_state_score_black = board_state_score_black + 5
                if piece == "N":
                    board_state_score_white = board_state_score_white + 3
                if piece == "n":
                    board_state_score_black = board_state_score_black + 3
                if piece == "B":
                    board_state_score_white = board_state_score_white + 3
                if piece == "b":
                    board_state_score_black = board_state_score_black + 3
                if piece == "Q":
                    board_state_score_white = board_state_score_white + 9
                if piece == "q":
                    board_state_score_black = board_state_score_black + 9
                # A king usually has an undefined value. 
                # Lets make it worth more than any piece in order to protect or atttack it as much as possible.
                if piece == "K":
                    board_state_score_white = board_state_score_white + 100
                if piece == "k":
                    board_state_score_black = board_state_score_black + 100

        if (self.player.color == "White" and player == False) or (self.player.color == "Black" and player == True):
            board_state_score_white = board_state_score_white - board_state_score_black
            return board_state_score_white
        if (self.player.color == "Black" and player == False) or (self.player.color == "White" and player == True):
            board_state_score_black = board_state_score_black - board_state_score_white
            return board_state_score_black

    # A method to determine a score for each player at certain board state based on the minimum value for each chess piece.
    # The only parameter is the board state, which should be a list of lists, containing strings.
    # Returns a list of two integer values, the first for white, the second for black.
    def generate_board_state_score_list(self, Board):

        board_state_score_white = 0
        board_state_score_black = 0
        board_state_score_total = [board_state_score_white, board_state_score_black]

        # Generate the score for a board state.
        for row in Board:
            for piece in row:
                if piece == "P":
                    board_state_score_white = board_state_score_white + 1
                if piece == "p":
                    board_state_score_black = board_state_score_black + 1
                if piece == "R":
                    board_state_score_white = board_state_score_white + 5
                if piece == "r":
                    board_state_score_black = board_state_score_black + 5
                if piece == "N":
                    board_state_score_white = board_state_score_white + 3
                if piece == "n":
                    board_state_score_black = board_state_score_black + 3
                if piece == "B":
                    board_state_score_white = board_state_score_white + 3
                if piece == "b":
                    board_state_score_black = board_state_score_black + 3
                if piece == "Q":
                    board_state_score_white = board_state_score_white + 9
                if piece == "q":
                    board_state_score_black = board_state_score_black + 9
                # A king will have an undefined value for this simple evaluation.
                if piece == "K":
                    board_state_score_white = board_state_score_white + 0
                if piece == "k":
                    board_state_score_black = board_state_score_black + 0

        # Reassign the values to the list because we have updated them.
        board_state_score_total = [board_state_score_white, board_state_score_black]

        return board_state_score_total

    # This function checks to see if the board state is a draw, but only because of insufficient materials.
    # The parameter is the board state to evaluate.
    # Returns a boolean value. True if there is a draw. False is there is not.
    def check_board_state_for_insufficient_materials(self, Board):
        #print("\nRunning check_board_state_draw.")
        boolean_draw = None
        total_piece_count = 0
        total_piece_list = []

        for piece in Board:
            if piece != ".":
                total_piece_count = total_piece_count + 1
                total_piece_list.append(piece)
            # There are always a sufficient amount of pieces to win a game with more than 3 pieces.
            # Rook, Queens, and Pawns do not count towards this type of draw.
            if total_piece_count > 3 or piece == "R" or piece == "r" or piece == "Q" or piece == "q" or piece == "P" or piece == "p":
                boolean_draw = False
                break
            # At this point the pieces must be (K vs. K, K vs. KB, or K vs. KN).
            else:
                boolean_draw = True

        #print("Exiting check_board_state_draw.")
        return boolean_draw

    # This function checks to see if the board state is a draw, but only because of threfoled repetition.
    # The parameter is the board state to evaluate.
    # Returns a boolean value. True if there is a draw. False is there is not.
    def check_board_state_for_threefold_repetition(self, Board):
        #print("\nRunning check_board_state_for_threefold_repetition()")
        boolean_draw = None

        repetition_count = 0

        list_of_past_moves = self.game.moves
        # Don't need to check if less than 7 moves have occurred
        # Move six will be the last move that occurred.
        if len(list_of_past_moves) > 6:
            move_zero = list_of_past_moves[-7]
            move_one = list_of_past_moves[-6]
            move_two = list_of_past_moves[-5]
            move_three = list_of_past_moves[-4]
            move_four = list_of_past_moves[-3]
            move_five = list_of_past_moves[-2]
            move_six = list_of_past_moves[-1]

            if move_zero.to_file == move_four.to_file and move_zero.to_rank == move_four.to_rank:
                repetition_count = repetition_count + 1
                if move_one.to_file == move_five.to_file and move_one.to_rank == move_five.to_rank:
                    repetition_count = repetition_count + 1
                    if move_two.to_file == move_six.to_file and move_two.to_rank == move_six.to_rank:
                        repetition_count = repetition_count + 1

            if repetition_count != 3:
                boolean_draw = False
            else:
                difference_list = self.difference_between_boards(Board)
                if difference_list:
                    to_space = difference_list[1]
                    difference_list_to_file = to_space[0]
                    difference_list_to_rank = to_space[1]
                    if move_three.to_file == difference_list_to_file and move_three.to_rank == difference_list_to_rank:
                        boolean_draw = True
        else:
            boolean_draw = False

        #print("Exiting check_board_state_for_threefold_repetition.\n")
        return boolean_draw

    # This function checks to see if the board state is a win-loss state (a king has been checkmated).
    # The parameter is the board state to evaluate.
    # Returns a boolean value. True if the game has been finished.
    def check_board_state_for_checkmate(self, Board):
        #print("\nRunning check_board_state_win_loss")
        boolean_checkmate = None
        whites_king_alive = False
        blacks_king_alive = False
        total_piece_list = []

        for row in Board:
            for piece in row:
                if piece == "K":
                    whites_king_alive = True
                if piece == "k":
                    blacks_king_alive = True

        if whites_king_alive == False or blacks_king_alive == False:
            boolean_checkmate = True
        else:
            boolean_checkmate = False

        return boolean_checkmate

    # Pseudocode from Wikipedia
    # This function runs the minimax algorithm, limited to a certain depth so it doesn't break the computer.
    # Parameters:   Board - the next Board state to test
    #               depth - the amount of depths to go until we reach the depth limit
    #               maximizing_player - a True/False value so we know if we need to maximize or minimize
    # Returns: An integer, the best value from the next layer of child nodes.
    # (* Initial call for maximizing player *)
    # minimax(origin, depth, TRUE)
    def depth_limited_minimax(self, Board, depth, maximizing_player):
        #print("\nRunning depth_limited_minimax()")
        board_state_checkmate = self.check_board_state_for_checkmate(Board)
        board_state_insufficient_draw = self.check_board_state_for_insufficient_materials(Board)
        board_state_threefold_draw = self.check_board_state_for_threefold_repetition(Board)
        best_value = None
        child_node_list = []

        if depth == 0 or board_state_checkmate or board_state_insufficient_draw or board_state_threefold_draw:
            print("\nboard_state_threefold_draw", board_state_threefold_draw)
            # The board_state_score ends up become the best value
            board_state_score = self.generate_board_state_score(Board, maximizing_player)
            # Threefold draw is not optimal. Take some points off the score.
            # This may cause trouble later.
            if board_state_threefold_draw:
                if maximizing_player == False:
                    board_state_score = board_state_score - 1
                elif maximizing_player == True:
                    board_state_score = board_state_score + 1
            print("Depth 0 board_state_score:", board_state_score)
            self.print_my_board(Board)
            # The board_node becomes the best_node
            board_node = Board
            # Create a list to return
            new_list = [board_state_score, board_node]
            #print("Exiting depth_limited_minimax()\n")
            return new_list

        child_node_list = self.generate_child_nodes(Board, maximizing_player)

        # If it is currently the maximizing player's turn...
        if maximizing_player == True:
            best_value = -1000
            for child in child_node_list:
                new_list = self.depth_limited_minimax(child, depth-1, False)
                new_value = new_list[0]
                print("maximizing best_value", best_value)
                print("maximizing new_value", new_value)
                if new_value > best_value:
                    best_node = new_list[1]
                    top_level_child = child
                best_value = max(best_value, new_value)

            #print("Max Best Value:", best_value)
            #print("Min Best Node:", best_node)
            best_list = [best_value, best_node, top_level_child]
            #print("Exiting depth_limited_minimax()\n")
            return best_list

        # Maximizing player == False, its the minimizing player's turn.
        else:
            best_value = 1000
            for child in child_node_list:
                new_list = self.depth_limited_minimax(child, depth-1, True)
                new_value = new_list[0]
                print("minimizing best_value", best_value)
                print("minimizing new_value", new_value)
                if new_value < best_value:
                    best_node = new_list[1]
                    top_level_child = child
                best_value = min(best_value, new_value)

            #print("Min Best Value:", best_value)
            #print("Min Best Node:", best_node)
            best_list = [best_value, best_node, top_level_child]
            #print("Exiting depth_limited_minimax()\n")
            return best_list

    # A function that defines all the possible moves for the current player.
    # It uses our own board so we can check future boards with it instead of just the board of the current turn.
    # Parameters:       Board - The board made of a list of lists.
    #                   Player - A True/False value to represent the current player or the enemy player.
    # Returns a list of all possible moves of the current player. Where each move is a list of 4 items, the first 2 items
    #   being the space we are moving from, the last 2 items being the space we are moving to.

    def possible_move_list(self, Board, player=True):
        #print("\nRunning possible_move_list()")
        piece_move_list = []
        total_move_list = []
        player_color = None
        from_file_index = None
        from_rank_index = None
        file_count = -1
        rank_count = -1

        if self.player.color == "White":
            player_color = "White"
        else:
            player_color = "Black"

        # Create the white player's possible move list.
        if (player_color == "White" and player == True) or (player_color == "Black" and player == False):
            # Reset rank_count before starting a new board just in case.
            rank_count = -1
            for row in Board:
                rank_count = rank_count + 1
                from_rank_index = rank_count
                # Reset count before starting a new row
                file_count = -1
                for piece_letter in row:
                    # Increment the count when there is another letter
                    file_count = file_count + 1
                    from_file_index = file_count
                    if piece_letter == "P":
                        to_move_list = self.pawn_move_space(Board, from_file_index, from_rank_index)
                        from_move_list = [self.index_to_board_space_list(from_rank_index, from_file_index)]
                        # Only append to the list if to_move_list is not empty
                        if to_move_list:
                            piece_move_list = [from_move_list + to_move_list]
                            total_move_list = total_move_list + piece_move_list
                    if piece_letter == "R":
                        to_move_list = self.rook_move_space(Board, from_file_index, from_rank_index)
                        from_move_list = [self.index_to_board_space_list(from_rank_index, from_file_index)]
                        if to_move_list:
                            piece_move_list = [from_move_list + to_move_list]
                            total_move_list = total_move_list + piece_move_list
                    if piece_letter == "N":
                        to_move_list = self.knight_move_space(Board, from_file_index, from_rank_index)
                        from_move_list = [self.index_to_board_space_list(from_rank_index, from_file_index)]
                        if to_move_list:
                            piece_move_list = [from_move_list + to_move_list]
                            total_move_list = total_move_list + piece_move_list
                    if piece_letter == "B":
                        to_move_list = self.bishop_move_space(Board, from_file_index, from_rank_index)
                        from_move_list = [self.index_to_board_space_list(from_rank_index, from_file_index)]
                        if to_move_list:
                            piece_move_list = [from_move_list + to_move_list]
                            total_move_list = total_move_list + piece_move_list
                    if piece_letter == "Q":
                        to_move_list = self.queen_move_space(Board, from_file_index, from_rank_index)
                        from_move_list = [self.index_to_board_space_list(from_rank_index, from_file_index)]
                        if to_move_list:
                            piece_move_list = [from_move_list + to_move_list]
                            total_move_list = total_move_list + piece_move_list
                    if piece_letter == "K":
                        to_move_list = self.king_move_space(Board, from_file_index, from_rank_index)
                        from_move_list = [self.index_to_board_space_list(from_rank_index, from_file_index)]
                        if to_move_list:
                            piece_move_list = [from_move_list + to_move_list]
                            total_move_list = total_move_list + piece_move_list
        # Create the black player's possible move list.
        elif (player_color == "Black" and player == True) or (player_color == "White" and player == False):
            # Reset rank_count before starting a new board just in case.
            rank_count = -1
            for row in Board:
                rank_count = rank_count + 1
                from_rank_index = rank_count
                # Reset count before starting a new row
                file_count = -1
                for piece in row:
                    # Increment the count when there is another letter
                    file_count = file_count + 1
                    from_file_index = file_count
                    if piece == "p":
                        to_move_list = self.pawn_move_space(Board, from_file_index, from_rank_index)
                        from_move_list = [self.index_to_board_space_list(from_rank_index, from_file_index)]
                        # Only append to the list if to_move_list is not empty
                        if to_move_list:
                            piece_move_list = [from_move_list + to_move_list]
                            total_move_list = total_move_list + piece_move_list
                    if piece == "r":
                        to_move_list = self.rook_move_space(Board, from_file_index, from_rank_index)
                        from_move_list = [self.index_to_board_space_list(from_rank_index, from_file_index)]
                        if to_move_list:
                            piece_move_list = [from_move_list + to_move_list]
                            total_move_list = total_move_list + piece_move_list
                    if piece == "n":
                        to_move_list = self.knight_move_space(Board, from_file_index, from_rank_index)
                        from_move_list = [self.index_to_board_space_list(from_rank_index, from_file_index)]
                        if to_move_list:
                            piece_move_list = [from_move_list + to_move_list]
                            total_move_list = total_move_list + piece_move_list
                    if piece == "b":
                        to_move_list = self.bishop_move_space(Board, from_file_index, from_rank_index)
                        from_move_list = [self.index_to_board_space_list(from_rank_index, from_file_index)]
                        if to_move_list:
                            piece_move_list = [from_move_list + to_move_list]
                            total_move_list = total_move_list + piece_move_list
                    if piece == "q":
                        to_move_list = self.queen_move_space(Board, from_file_index, from_rank_index)
                        from_move_list = [self.index_to_board_space_list(from_rank_index, from_file_index)]
                        if to_move_list:
                            piece_move_list = [from_move_list + to_move_list]
                            total_move_list = total_move_list + piece_move_list
                    if piece == "k":
                        to_move_list = self.king_move_space(Board, from_file_index, from_rank_index)
                        from_move_list = [self.index_to_board_space_list(from_rank_index, from_file_index)]
                        if to_move_list:
                            piece_move_list = [from_move_list + to_move_list]
                            total_move_list = total_move_list + piece_move_list

        #print("Exiting possible_move_list()\n")
        return total_move_list

    # A function that finds the piece object that has the same location as a letter in our own board.
    # Parameters:   file - the file index of the piece letter in my board
    #               rank - the rank index of the piece letter in my board
    # Returns: A piece object.
    def find_piece_object_at_index(self, file_index, rank_index):
        print("find_piece_object_at_index")

    # A function that generates all the possible child nodes for one player of a certain chess board state.
    # Parameters:   Board - The board made of a list of lists.
    # Returns: A list containing all the child nodes (Boards) of the Board given in the parameters.
    def generate_child_nodes(self, Board, player):
        print("\nRunning generate_child_nodes()")
        possible_move_list = []
        child_node_list = []
        from_file = None
        from_rank = None
        to_file = None
        to_rank = None
        valid_move = None
        player_color = None

        possible_move_list = self.possible_move_list(Board, player)
        #print("possible_move_list", possible_move_list)

        if (self.player.color == "White" and player == True) or (self.player.color == "Black" and player == False):
            player_color = "White"
        else:
            player_color = "Black"

        for piece in possible_move_list:
            piece_space = piece[0]
            from_file = piece_space[0]
            from_rank = piece_space[1]
            piece_length = len(piece)
            for space in range(1, piece_length):
                possible_move = piece[space]
                to_file = possible_move[0]
                to_rank = possible_move[1]
                valid_move = self.check_if_space_to_move_valid(Board, from_file, from_rank, to_file, to_rank)
                if valid_move:
                    new_board = copy.deepcopy(Board)
                    child_board = self.make_move_on_my_board(new_board, from_file, from_rank, to_file, to_rank)
                    #print(player_color, "Valid Move:")
                    #self.print_my_board(child_board)
                    child_node_list.append(child_board)

        print("Exiting generate_child_nodes()\n")
        return child_node_list

    # This function only works if the difference between the boards is only one move.
    # This function will output the two spaces that are different between the game board and my board.
    # Parameters:   Board - The list of lists to be passed to check against.
    # Returns:      A list of lists that contains the positions that are different
    def difference_between_boards(self, Board):
        #print("\nRunning difference_between_boards()")
        difference_list = []

        #self.print_my_board(self.Board)
        #self.print_my_board(Board)

        # Range goes to 8 because we don't include the last number
        for rank_index in range(0,8):
            for file_index in range(0,8):
                if self.Board[rank_index][file_index] != Board[rank_index][file_index]:
                    board_space_list = self.index_to_board_space_list(rank_index, file_index)
                    if Board[rank_index][file_index] == ".":
                        difference_list = [board_space_list] + difference_list 
                    else:
                        difference_list.append(board_space_list)

        #print("difference_list", difference_list)
        return difference_list
        #print("Exiting difference_between_boards()\n")

    # <<-- /Creer-Merge: functions -->>
