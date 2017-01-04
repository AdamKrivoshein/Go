import pygame
pygame.init()

wood = pygame.transform.scale(pygame.image.load('C:\Python\Board2.png'), (1000, 1000))
clear = pygame.transform.scale(pygame.image.load('C:\Python\Clear.png'), (47, 47))
BStone = pygame.transform.scale(pygame.image.load('C:\Python\BStone.png'), (47, 47))
WStone = pygame.transform.scale(pygame.image.load('C:\Python\WStone.png'), (47, 47))
board = [['']*19, ['']*19, ['']*19, ['']*19, ['']*19, ['']*19, ['']*19, ['']*19, ['']*19, ['']*19, ['']*19, ['']*19, ['']*19, ['']*19, ['']*19, ['']*19, ['']*19, ['']*19, ['']*19]

class stone:
	liberties = 4
	
	def __init__(self, state, i, j):
		self.state = state
		self.groupID = 0
		self.x = i
		self.y = j
		
	def stoneRect(i, j):
		return (51*i + 17), (51*j + 20), 47, 47
	
	def draw(self, x, y, state, gameDisplay):
		if state == "Empty":
			gameDisplay.blit(clear, (x, y))
		if state == "Black":
			gameDisplay.blit(BStone, (x, y))
		if state == "White":
			gameDisplay.blit(WStone, (x, y))
			
	def notSurrounded(self, i, j, board, turn):
		self.liberties = 4
		if i == (len(board) - 1):
			self.liberties -= 1
		elif board[i + 1][j].state != "Empty":
			self.liberties -= 1
		if i == 0:
			self.liberties -= 1
		elif board[i - 1][j].state != "Empty":
			self.liberties -= 1
		if j == (len(board) - 1):
			self.liberties -= 1
		elif board[i][j + 1].state != "Empty":
			self.liberties -= 1
		if j == 0:
			self.liberties -= 1
		elif board[i][j - 1].state != "Empty":
			self.liberties -= 1
		print("Liberties: " + str(self.liberties))
		if self.liberties > 0:
			return True
		if self.liberties < 1:
			self.liberties = 4
			return False
			
	def kill(self, i, j, board, turn):		#FIX edge liberties crashing
		killed = False
		if board[(i + 1)][j].groupID == 0:
			if i < (len(board) - 1):
				if board[(i + 1)][j].notSurrounded((i + 1), j, board, turn) == False:
					killed = True
		else:
			print("GroupID != 0!!!")
			if board[board[(i + 1)][j].groupID[0]][board[(i + 1)][j].groupID[1]].notSurrounded((i + 1), j, board, turn) == False:
				print("Groupd is Dead!")
				#board[(i + 1)][j].captured((i + 1), j, board)
				board[board[(i + 1)][j].groupID[0]][board[(i + 1)][j].groupID[1]].captured((i + 1), j, board)
				killed = True
		if i > 0:
			if board[(i - 1)][j].notSurrounded((i - 1), j, board, turn) == False:
				killed = True
		if j < (len(board) - 1):
			if board[i][(j + 1)].notSurrounded(i, (j + 1), board, turn) == False:
				killed = True
		if j > 0:
			if board[i][(j - 1)].notSurrounded(i, (j - 1), board, turn) == False:
				killed = True
		print("Bacon" + str(killed))
		return killed

	def captured(self, i, j, board):		#Don't need this anymore
		print(board[i][j].groupID[0])
		print(board[i][j].groupID[1])
		board[board[i][j].groupID[0]][board[i][j].groupID[1]].captured(i, j, board)
		
	def seekGroup(self, i, j, x, y, turn, timeline):
		if board[x][y].state == turn:
			if board[x][y].groupID == 0:
				board[i][j] = group(turn, [i, j], [[i, j], [(x), (y)]])	#Need to add check if connects groups		#Need to add liberty check of group
				board[x][y].groupID = [i, j]
				return True
			else:
				board[i][j].groupID = board[x][y].groupID
				board[board[i][j].groupID[0]][board[i][j].groupID[1]].members.append([i, j])	#board[i][j] = board[x][y].members.append([i, j])	#Doesn't work. Adjacent stone might not be keystone. Must search for keystone
				return True
	
	def joinGroup(self, i, j, board, turn, timeline):
		peers = []
		sortedPeers = []
		if board[(i + 1)][j].state == turn:			#FIX checking past edges
			peers.append(board[(i + 1)][j].groupID)
		if board[(i - 1)][j].state == turn:
			peers.append(board[(i - 1)][j].groupID)
		if board[i][(j + 1)].state == turn:
			peers.append(board[i][(j + 1)].groupID)
		if board[i][(j - 1)].state == turn:
			peers.append(board[i][(j - 1)].groupID)
		for k in peers:
			if k not in sortedPeers:
				sortedPeers.append(k)
		print(sortedPeers)
		if len(sortedPeers) == 1:
			if i < (len(board) - 1):
				if self.seekGroup(i, j, (i + 1), j, turn, timeline) == True:
					return True
			if i > 0:
				if self.seekGroup(i, j, (i - 1), j, turn, timeline) == True:
					return True
			if j < (len(board) - 1):
				if self.seekGroup(i, j, i, (j + 1), turn, timeline) == True:
					return True
			if j > 0:
				if self.seekGroup(i, j, i, (j - 1), turn, timeline) == True:
					return True
		elif len(sortedPeers) > 1:
			board[i][j].groupID = sortedPeers[0]
			board[sortedPeers[0][0]][sortedPeers[0][1]].members.append([i, j])
			for l in range(len(sortedPeers)):
				if l > 0:
					for m in range(len(board[sortedPeers[l][0]][sortedPeers[l][1]].members)):
						board[sortedPeers[0][0]][sortedPeers[0][1]].members.append(board[sortedPeers[l][0]][sortedPeers[l][1]].members[m])
			for n in range(len(sortedPeers)):		#Sets all other group keystones = to a stone type
				if n != 0:
					board[sortedPeers[n][0]][sortedPeers[n][1]] = stone(turn, sortedPeers[n][0], sortedPeers[n][1])
			for o in range(len(board[sortedPeers[0][0]][sortedPeers[0][1]].members)):		#Sets group ID of all the new group members
				board[board[sortedPeers[0][0]][sortedPeers[0][1]].members[o][0]][board[sortedPeers[0][0]][sortedPeers[0][1]].members[o][1]].groupID = sortedPeers[0]
			print("Members" + str(board[sortedPeers[0][0]][sortedPeers[0][1]].members))
				#board[sortedPeers[0]].members.append each board[sortedPeers].members. Set all but sortedPeers[0] = to regular stone
				#board[each sortedPeers].members add board.sortedPeers[0] members
		#if board[i][j - 1].state == turn:
		#	if board[i][j - 1].groupID == 0:
		#		board[i][j] = group(turn, timeline, ([i, j], [i, (j - 1)]))	#Need to add check if connects groups		#Need to add liberty check of group
		#		board[i][j - 1].groupID = timeline
		#		return True
		#	else:
		#		board[i][j] = group(turn, board[i][j - 1].groupID, ([i, j], [i, (j - 1)]))
		#		return True

	def valid(self, i, j, board, turn, timeline):
		if board[i][j].state == "Empty":
			board[i][j].state = turn
			#print(board[i][j].kill(i, j, board, turn))
			#print(board[i][j].notSurrounded(i, j, board, turn))
			if board[i][j].kill(i, j, board, turn) == True or board[i][j].notSurrounded(i, j, board, turn) == True or board[i][j].joinGroup(i, j, board, turn, timeline) == True:		#Freaks out trying to check a group stone
				board[i][j].joinGroup(i, j, board, turn, timeline)
				if i < (len(board) - 1):
					if board[i + 1][j].notSurrounded((i + 1), j, board, turn) == False and board[i + 1][j].groupID == 0:
						board[i + 1][j].state = "Empty"
				if i > 0:
					if board[i - 1][j].notSurrounded((i - 1), j, board, turn) == False and board[i - 1][j].groupID == 0:
						board[i - 1][j].state = "Empty"
				if j < (len(board) - 1):
					if board[i][j + 1].notSurrounded(i, (j + 1), board, turn) == False and board[i][j + 1].groupID == 0:
						board[i][j + 1].state = "Empty"
				if j > 0:
					if board[i][j - 1].notSurrounded(i, (j - 1), board, turn) == False and board[i][j - 1].groupID == 0:
						board[i][j - 1].state = "Empty"
				#board[i][j].joinGroup(i, j, board, turn, timeline)
				return True
			else:
				board[i][j].state = "Empty"
				return False
		else:
			#board[i][j].state = "Empty"
			return False
				
class group:
	def __init__(self, state, groupID, members):
		self.state = state
		self.groupID = groupID
		self.members = members
		
	def valid(self, i, j, board, turn, empty):
		return False
	
	def captured(self, i, j, board):
		for k in range(len(board[self.groupID[0]][self.groupID[1]].members)):
			#board[board[self.groupID[0]][self.groupID[1]].members[k][0]][board[self.groupID[0]][self.groupID[1]].members[k][1]].groupID = 0
			x = self.groupID[0]
			y = self.groupID[1]
			print(self.members[k][0])
			print(self.members[k][1])
			if self.members[k][0] != self.groupID[0] or self.members[k][1] != self.groupID[1]:
				board[self.members[k][0]][self.members[k][1]].state = "Empty"
			if self.members[k][0] != self.groupID[0] or self.members[k][1] != self.groupID[1]:
				board[self.members[k][0]][self.members[k][1]].groupID = 0
			#board[board[self.groupID[0]][self.groupID[1]].members[k][0]][board[self.groupID[0]][self.groupID[1]].members[k][1]].state = "Empty"
			#board[self.groupID[0]][self.groupID[1]] = stone("Empty", i, j)
			#Need to set group keystone groupID = to 0
			board[x][y] = stone("Empty", i, j)
			
	def addStone(self, stone):
		self.members.append(stone)
		
	def libertyList(self, member):	#FIX off edge liberties
		liberties = []
		#print(member[0], member[1])
		if board[(member[0] + 1)][member[1]].state == "Empty":
			liberties.append([(member[0] + 1), member[1]])
		if board[(member[0] - 1)][member[1]].state == "Empty":
			liberties.append([(member[0] - 1), member[1]])
		if board[member[0]][(member[1] + 1)].state == "Empty":
			liberties.append([member[0], (member[1] + 1)])
		if board[member[0]][(member[1] - 1)].state == "Empty":
			liberties.append([member[0], (member[1] - 1)])
		#print(liberties)
		return(liberties)
	
	def notSurrounded(self, i, j, board, turn):		#FIX off edge liberties
		totalLiberties = []
		for i in range(len(self.members)):		#i = number of group members
			for j in range(len(self.libertyList(self.members[i]))):		#j = number of coords recieved from liberty list
				add = True
				for k in range(len(totalLiberties)):	#k = number of pre-existing liberty coords
					if self.libertyList(self.members[i])[j] == totalLiberties[k]:
						add = False
				if add == True:
					totalLiberties.append(self.libertyList(self.members[i])[j])
		print(totalLiberties)
		if len(totalLiberties) > 0:
			return True
		else:
			#Kill self
			return False

	def draw(self, x, y, state, gameDisplay):
		if state == "Empty":
			gameDisplay.blit(clear, (x, y))
		if state == "Black":
			gameDisplay.blit(BStone, (x, y))
		if state == "White":
			gameDisplay.blit(WStone, (x, y))
		
def Draw_Board(board, gameDisplay):
	for i in range(19):
		for j in range(19):
			board[i][j].draw((51*i + 17), (51*j + 20), board[i][j].state, gameDisplay)

def main():
	display_width = 1000
	display_height = 1000
	black = (0, 0, 0)
	white = (255, 255, 255)

	gameDisplay = pygame.display.set_mode((display_width, display_height))
	pygame.display.set_caption('Go')
	clock = pygame.time.Clock();
	
	#board = [['']*19, ['']*19, ['']*19, ['']*19, ['']*19, ['']*19, ['']*19, ['']*19, ['']*19, ['']*19, ['']*19, ['']*19, ['']*19, ['']*19, ['']*19, ['']*19, ['']*19, ['']*19, ['']*19]
	boardg = [['']*19, ['']*19, ['']*19, ['']*19, ['']*19, ['']*19, ['']*19, ['']*19, ['']*19, ['']*19, ['']*19, ['']*19, ['']*19, ['']*19, ['']*19, ['']*19, ['']*19, ['']*19, ['']*19]
	x = True
	turn = "Black"
	timeline = 0
	moves = []
	for i in range(19):
		for j in range(19):
			board[i][j] = stone("Empty", i, j)
			boardg[i][j] = stone("Empty", i, j)

	while x == True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				x = False
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				pos = event.pos
				for i in range(19):
					for j in range(19):
						if pygame.Rect(stone.stoneRect(i, j)).collidepoint(pos):
							if board[i][j].valid(i, j, board, turn, timeline) == True:
								#if board[i + 1][j].notSurrounded((i + 1), j, board, turn) == False:
								#	board[i + 1][j].state = 0
								board[i][j].state = turn
								#moves.append([i, j, turn])
								#print(moves)
								timeline += 1
								print("Move: " + str(timeline))
								#if timeline == 5 or timeline == 8:
									#board = boardg
								#if timeline >= 3:
									#boardg[moves[timeline - 3][0]][moves[timeline - 3][1]].state = moves[timeline - 3][2]
								if turn == "Black":
									turn = "White"
								else:
									turn = "Black"
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
				pos = event.pos
				for i in range(19):
					for j in range(19):
						if pygame.Rect(stone.stoneRect(i, j)).collidepoint(pos):
							print(board[i][j].state + " - " + str(board[i][j].groupID))
							if board[i][j].groupID != 0:
								#print("Members: " + str(board[i][j].members))
								print(board[i][j].notSurrounded(i, j, board, turn))

		gameDisplay.fill(white)
		gameDisplay.blit(wood, (0, 0))
		Draw_Board(board, gameDisplay)
		
		pygame.display.update()
		clock.tick(10)

main()
pygame.quit()
quit()