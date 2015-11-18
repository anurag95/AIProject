import sys
import random
import signal

#Timer handler, helper function

class TimedOutExc(Exception):
        pass

def handler(signum, frame):
    #print 'Signal handler called with signal', signum
    raise TimedOutExc()


class Manual_player:
	def __init__(self):
		pass
	def move(self, temp_board, old_move, flag):
		print 'Enter your move: <format:row column> (you\'re playing with', flag + ")"	
		mvp = raw_input()
		mvp = mvp.split()
		return (int(mvp[0]), int(mvp[1]))
		

def moves_allowed(temp_board, old_move, flag):
	for_corner = [0,2,3,5,6,8]

	#List of permitted blocks, based on old move.
	blocks_allowed  = []

	if old_move[0] in for_corner and old_move[1] in for_corner:
		## we will have 3 representative blocks, to choose from

		if old_move[0] % 3 == 0 and old_move[1] % 3 == 0:
			## top left 3 blocks are allowed
			blocks_allowed = [0, 1, 3]
		elif old_move[0] % 3 == 0 and old_move[1] in [2, 5, 8]:
			## top right 3 blocks are allowed
			blocks_allowed = [1,2,5]
		elif old_move[0] in [2,5, 8] and old_move[1] % 3 == 0:
			## bottom left 3 blocks are allowed
			blocks_allowed  = [3,6,7]
		elif old_move[0] in [2,5,8] and old_move[1] in [2,5,8]:
			### bottom right 3 blocks are allowed
			blocks_allowed = [5,7,8]
		else:
			print "SOMETHING REALLY WEIRD HAPPENED!"
			sys.exit(1)
	else:
	#### we will have only 1 block to choose from (or maybe NONE of them, which calls for a free move)
		if old_move[0] % 3 == 0 and old_move[1] in [1,4,7]:
			## upper-center block
			blocks_allowed = [1]

		elif old_move[0] in [1,4,7] and old_move[1] % 3 == 0:
			## middle-left block
			blocks_allowed = [3]

		elif old_move[0] in [2,5,8] and old_move[1] in [1,4,7]:
			## lower-center block
			blocks_allowed = [7]

		elif old_move[0] in [1,4,7] and old_move[1] in [2,5,8]:
			## middle-right block
			blocks_allowed = [5]
		elif old_move[0] in [1,4,7] and old_move[1] in [1,4,7]:
			blocks_allowed = [4]

	# We get all the empty cells in allowed blocks. If they're all full, we get all the empty cells in the entire board.
	cells = []  # it will be list of tuples
	
	#Iterate over possible blocks and get empty cells
	for idb in blocks_allowed:
		id1 = idb/3
		id2 = idb%3
		for i in range(id1*3,id1*3+3):
			for j in range(id2*3,id2*3+3):
				if temp_board[i][j] == '-':
					cells.append((i,j))

	# If all the possible blocks are full, you can move anywhere
	if cells == []:
		for i in range(9):
			for j in range(9):
				if temp_board[i][j] == '-':
					cells.append((i,j))	
	return cells


class Player:

	def __init__(self):
		pass


	def alpha_beta_pruning(self, temp_board, old_move, alpha, beta, flag, depth):
		flag = int(flag)
		sym = ''
		if(flag):
			sym = 'o'
		else:
			sym = 'x'

		cells = moves_allowed(temp_board, old_move, flag)

		if(depth == 5):
			return [old_move[0],old_move[1],0]
		if depth%2 == 0:
			maxv = [-1, -1 , -10000]
			for i in cells:
				a, b = i

				temp_board[a][b] = sym
				val = self.alpha_beta_pruning(temp_board, (a,b), alpha, beta, (flag+1)%2, depth+1)

				if( val[2] > maxv[2]):
					maxv[0] = a
					maxv[1] = b
					maxv[2] = val[2]

				alpha = max(alpha, maxv[2])
				temp_board[a][b] = '-'

				if(beta <= alpha):
					break
			return maxv

		else:
			minv = [-1, -1 , 10000]
			for i in cells:
				a, b = i
				temp_board[a][b] = sym

				val = self.alpha_beta_pruning(temp_board, (a,b), alpha, beta, (flag+1)%2, depth+1)

				if( val[2] <= minv[2]):
					minv[0] = a
					minv[1] = b
					minv[2] = val[2]

				beta = min(beta, minv[2])
				temp_board[a][b] = '-'

				if(beta < alpha):
					break
			return minv

	def move(self,temp_board,old_move,flag):

		if(flag == 'o'):
			turn = 1
		else:
			turn = 0
	# We get all the empty cells in allowed blocks. If they're all full, we get all the empty cells in the entire board.
		cell = self.alpha_beta_pruning(temp_board, old_move, -10000, 10000, turn, 0)
		cell = cell[0:2]
		cell = (cell[0],cell[1])
		return cell

#Initializes the game
def get_init_board_and_blockstatus():
	board = []
	for i in range(9):
		row = ['-']*9
		board.append(row)
	
	block_stat = ['-']*9
	return board, block_stat

# Checks if player has messed with the board. Don't mess with the board that is passed to your move function. 
def verification_fails_board(board_game, temp_board_state):
	return board_game == temp_board_state	

# Checks if player has messed with the block. Don't mess with the block array that is passed to your move function. 
def verification_fails_block(block_stat, temp_block_stat):
	return block_stat == temp_block_stat	

#Gets empty cells from the list of possible blocks. Hence gets valid moves. 
def get_empty_out_of(gameb, blal):
	cells = []  # it will be list of tuples
	#Iterate over possible blocks and get empty cells
	for idb in blal:
		id1 = idb/3
		id2 = idb%3
		for i in range(id1*3,id1*3+3):
			for j in range(id2*3,id2*3+3):
				if gameb[i][j] == '-':
					cells.append((i,j))

	# If all the possible blocks are full, you can move anywhere
	if cells == []:
		for i in range(9):
			for j in range(9):
				if gameb[i][j] == '-':
					cells.append((i,j))	
		
	return cells
		
# Note that even if someone has won a block, it is not abandoned. But then, there's no point winning it again!
# Returns True if move is valid
def check_valid_move(game_board, current_move, old_move):

	# first we need to check whether current_move is tuple of not
	# old_move is guaranteed to be correct
	if type(current_move) is not tuple:
		return False
	
	if len(current_move) != 2:
		return False

	a = current_move[0]
	b = current_move[1]	

	if type(a) is not int or type(b) is not int:
		return False
	if a < 0 or a > 8 or b < 0 or b > 8:
		return False

	#Special case at start of game, any move is okay!
	if old_move[0] == -1 and old_move[1] == -1:
		return True


	for_corner = [0,2,3,5,6,8]

	#List of permitted blocks, based on old move.
	blocks_allowed  = []

	if old_move[0] in for_corner and old_move[1] in for_corner:
		## we will have 3 representative blocks, to choose from

		if old_move[0] % 3 == 0 and old_move[1] % 3 == 0:
			## top left 3 blocks are allowed
			blocks_allowed = [0, 1, 3]
		elif old_move[0] % 3 == 0 and old_move[1] in [2, 5, 8]:
			## top right 3 blocks are allowed
			blocks_allowed = [1,2,5]
		elif old_move[0] in [2,5, 8] and old_move[1] % 3 == 0:
			## bottom left 3 blocks are allowed
			blocks_allowed  = [3,6,7]
		elif old_move[0] in [2,5,8] and old_move[1] in [2,5,8]:
			### bottom right 3 blocks are allowed
			blocks_allowed = [5,7,8]

		else:
			print "SOMETHING REALLY WEIRD HAPPENED!"
			sys.exit(1)

	else:
		#### we will have only 1 block to choose from (or maybe NONE of them, which calls for a free move)
		if old_move[0] % 3 == 0 and old_move[1] in [1,4,7]:
			## upper-center block
			blocks_allowed = [1]
	
		elif old_move[0] in [1,4,7] and old_move[1] % 3 == 0:
			## middle-left block
			blocks_allowed = [3]
		
		elif old_move[0] in [2,5,8] and old_move[1] in [1,4,7]:
			## lower-center block
			blocks_allowed = [7]

		elif old_move[0] in [1,4,7] and old_move[1] in [2,5,8]:
			## middle-right block
			blocks_allowed = [5]

		elif old_move[0] in [1,4,7] and old_move[1] in [1,4,7]:
			blocks_allowed = [4]


	# We get all the empty cells in allowed blocks. If they're all full, we get all the empty cells in the entire board.
	cells = get_empty_out_of(game_board, blocks_allowed)

	#Checks if you made a valid move. 
	if current_move in cells:
		return True
	else:
		return False

def update_lists(game_board, block_stat, move_ret, fl):
	#move_ret has the move to be made, so we modify the game_board, and then check if we need to modify block_stat
	game_board[move_ret[0]][move_ret[1]] = fl


	#print "@@@@@@@@@@@@@@@@@"
	#print block_stat

	block_no = (move_ret[0]/3)*3 + move_ret[1]/3	
	id1 = block_no/3
	id2 = block_no%3
	mg = 0
	mflg = 0
	if block_stat[block_no] == '-':

		### now for diagonals
		## D1
		# ^
		#   ^
		#     ^
		if game_board[id1*3][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3+2][id2*3+2] and game_board[id1*3+1][id2*3+1] != '-':
			mflg=1
			mg=1
			#print "SEG: D1 found"

		## D2
		#     ^
		#   ^
		# ^
		############ MODIFICATION HERE, in second condition -> gb[id1*3][id2*3+2]
		# if game_board[id1*3+2][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3+2][id2*3] and game_board[id1*3+1][id2*3+1] != '-':
		if game_board[id1*3+2][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3][id2*3 + 2] and game_board[id1*3+1][id2*3+1] != '-':
			mflg=1
			mg=1
			#print "SEG: D2 found"

		### col-wise
		if mflg != 1:
                    for i in range(id2*3,id2*3+3):
                        #### MODIFICATION HERE, [i] was missing previously
                        # if game_board[id1*3]==game_board[id1*3+1] and game_board[id1*3+1] == game_board[id1*3+2] and game_board[id1*3] != '-':
                        if game_board[id1*3][i]==game_board[id1*3+1][i] and game_board[id1*3+1][i] == game_board[id1*3+2][i] and game_board[id1*3][i] != '-':
                                mflg = 1
				#print "SEG: Col found"
                                break

                ### row-wise
		if mflg != 1:
                    for i in range(id1*3,id1*3+3):
                        ### MODIFICATION HERE, [i] was missing previously
                        #if game_board[id2*3]==game_board[id2*3+1] and game_board[id2*3+1] == game_board[id2*3+2] and game_board[id2*3] != '-':
                        if game_board[i][id2*3]==game_board[i][id2*3+1] and game_board[i][id2*3+1] == game_board[i][id2*3+2] and game_board[i][id2*3] != '-':
                                mflg = 1
				#print "SEG: Row found"
                                break

	
	if mflg == 1:
		block_stat[block_no] = fl

	#print 
	#print block_stat
	#print "@@@@@@@@@@@@@@@@@@@@@@@"	
	return mg

#Check win
def terminal_state_reached(game_board, block_stat,point1,point2):
	### we are now concerned only with block_stat
	bs = block_stat
	## Row win
	if (bs[0] == bs[1] and bs[1] == bs[2] and bs[1]!='-') or (bs[3]!='-' and bs[3] == bs[4] and bs[4] == bs[5]) or (bs[6]!='-' and bs[6] == bs[7] and bs[7] == bs[8]):
		print block_stat
		return True, 'W'
	## Col win
	elif (bs[0] == bs[3] and bs[3] == bs[6] and bs[0]!='-') or (bs[1] == bs[4] and bs[4] == bs[7] and bs[4]!='-') or (bs[2] == bs[5] and bs[5] == bs[8] and bs[5]!='-'):
		print block_stat
		return True, 'W'
	## Diag win
	elif (bs[0] == bs[4] and bs[4] == bs[8] and bs[0]!='-') or (bs[2] == bs[4] and bs[4] == bs[6] and bs[2]!='-'):
		print block_stat
		return True, 'W'
	else:
		smfl = 0
		for i in range(9):
			for j in range(9):
				if game_board[i][j] == '-':
					smfl = 1
					break
		if smfl == 1:
			return False, 'Continue'
		
		else:
			##### check of number of DIAGONALs


			if point1>point2:
				return True, 'P1'
			elif point2>point1:
				return True, 'P2'
			else:
				return True, 'D'	


def decide_winner_and_get_message(player,status, message):
	if status == 'P1':
		return ('P1', 'MORE DIAGONALS')
	elif status == 'P2':
		return ('P2', 'MORE DIAGONALS')
	elif player == 'P1' and status == 'L':
		return ('P2',message)
	elif player == 'P1' and status == 'W':
		return ('P1',message)
	elif player == 'P2' and status == 'L':
		return ('P1',message)
	elif player == 'P2' and status == 'W':
		return ('P2',message)
	else:
		return ('NONE','DRAW')
	return


def print_lists(gb, bs):
	print '=========== Game Board ==========='
	for i in range(9):
		if i > 0 and i % 3 == 0:
			print
		for j in range(9):
			if j > 0 and j % 3 == 0:
				print " " + gb[i][j],
			else:
				print gb[i][j],

		print
	print "=================================="

	print "=========== Block Status ========="
	for i in range(0, 9, 3):
		print bs[i] + " " + bs[i+1] + " " + bs[i+2] 
	print "=================================="
	print
	

def simulate(obj1,obj2):
	
	# game board is a 9x9 list, block_stat is a 1D list of 9 elements
	game_board, block_stat = get_init_board_and_blockstatus()

	#########
	# deciding player1 / player2 after a coin toss
	pl = [obj1, obj2] 

	### basically, player with flag 'x' will start the game
	pl_fl = ['x', 'o']

	old_move = (-1, -1) ### for the first move

	WINNER = ''
	MESSAGE = ''
	TIMEALLOWED = 60


	### These points will not keep track of the total points of both the players.
	### Instead, these variables will keep track of only the blocks won by DIAGONALS, and these points will be used only in cases of DRAW....
	draw_pts=[0,0]
	turn=0
	#### printing
	print_lists(game_board, block_stat)
	cur_player = ''
	
	while(1):
		###################################### 
		########### firstly pl1 will move
		###################################### 
		
		## just for checking that the player1 does not modify the contents of the 2 lists
		if turn == 0:
			cur_player = 'P1'
		else:
			cur_player = 'P2'
		
		temp_board_state = game_board[:]
		temp_block_stat = block_stat[:]
	
		signal.signal(signal.SIGALRM, handler)
		signal.alarm(TIMEALLOWED)
		# Player1 to complete in TIMEALLOWED secs. 
		try:
			ret_move_pl = pl[turn].move(temp_board_state, old_move, pl_fl[turn])
		except TimedOutExc as e:
			WINNER, MESSAGE = decide_winner_and_get_message(cur_player, 'L',   'TIMED OUT')
			break
			### MODIFICATION!!
		signal.alarm(0)
	
		#### check if both lists are the same!!
		if not (verification_fails_board(game_board, temp_board_state) and verification_fails_block(block_stat, temp_block_stat)):
			##player1 loses - he modified something
			WINNER, MESSAGE = decide_winner_and_get_message(cur_player, 'L',   'MODIFIED CONTENTS OF LISTS')
			break
		
		### now check if the returned move is valid
		if not check_valid_move(game_board, ret_move_pl, old_move):
			## player1 loses - he made the wrong move.
			WINNER, MESSAGE = decide_winner_and_get_message(cur_player, 'L',   'MADE AN INVALID MOVE')
			break
			

		print cur_player, " made the move:", ret_move_pl, 'with', pl_fl[turn]
		######## So if the move is valid, we update the 'game_board' and 'block_stat' lists with move of pl1
		draw_pts[turn] += update_lists(game_board, block_stat, ret_move_pl, pl_fl[turn])

		### now check if the last move resulted in a terminal state
		gamestatus, mesg =  terminal_state_reached(game_board, block_stat,draw_pts[0],draw_pts[1])
		if gamestatus == True:
			print_lists(game_board, block_stat)
			WINNER, MESSAGE = decide_winner_and_get_message(cur_player, mesg,  'COMPLETE')	
			break

		
		old_move = ret_move_pl
		print_lists(game_board, block_stat)
		turn = turn^1		

	######### THESE ARE NOT THE TOTAL points, these are just the diagonal points, (refer to the part before the while(1) loop
	####### These will be used only in cases of DRAW
	print 'DRAW points of P1', draw_pts[0]		
	print 'DRAW points of P2', draw_pts[1]

	
	print WINNER
	print MESSAGE
#	return WINNER, MESSAGE, p1_pt2, p2_pt2

if __name__ == '__main__':
	## get game playing objects

	if len(sys.argv) != 2:
		print 'Usage: python simulator.py <option>'
		print '<option> can be 1 => Random player vs. Random player'
		print '                2 => Human vs. Random Player'
		print '                3 => Human vs. Human'
		sys.exit(1)
 
	obj1 = ''
	obj2 = ''
	option = sys.argv[1]
	if option == '1':
		obj1 = Player()
		obj2 = Player()

	elif option == '2':
		obj1 = Player()
		obj2 = Manual_player()
	elif option == '3':
		obj1 = Manual_player()
		obj2 = Manual_player()


	#########
	# deciding player1 / player2 after a coin toss
	num = random.uniform(0,1)
	print num
	interchange = 0
	if num > 0.5:
		interchange = 1
		simulate(obj2, obj1)
	else:
		simulate(obj1, obj2)
