import numpy as np
from random import choice
import time

move_counter = 0

class Block:
	"""Represents one specific block."""

	def __init__(self, size, position):
		self.size = int(size)
		self.position = position
		self.block_on_top = False

class Tower:
	"""Represents one specific tower. The number of blocks in it and the visualization array.
	Offers methods that have to do with one specific tower."""

	def __init__(self, position, total_blocks):

		#Position of the tower ((left, center, right) = (1, 2, 3))
		self.pos = position
		self.total_block_number = total_blocks
		self.blocks_in_tower = 0
		self.block_object_list = []
		for i in range(total_blocks):
			self.block_object_list.append(0)

		#Create a visualization array for the tower
		self.block_visual_array = np.zeros((total_blocks, 1)).astype(np.int32)


	def fill_tower(self, number_of_blocks):
		"""Fills in a tower with the specified number of blocks so the game can be initialized."""

		#Fill a tower to start the game
		block_visual_list = [] 	#temporary list of the positions to be later passed on to an array
		for block_size in range(1, self.total_block_number + 1):
			block = Block(block_size, [block_size - 1, self.pos])
			self.block_object_list[block_size - 1] = block
			block_visual_list.append(block.size)
			self.blocks_in_tower += 1

		self.block_visual_array[:, 0] = block_visual_list
		self.update_block_on_top_flag()

	def check_if_empty(self):
		"""Checks if the tower is empty. Returns bool."""

		if self.blocks_in_tower == 0:
			return True
		else:
			return False


	def get_block_list(self):
		"""Returns the visalisation array for the tower"""

		return self.block_visual_array


	def check_for_block(self, size):
		"""Checks to see if the block of a specific size is in the tower. Returns bool."""

		for block in self.block_object_list:
			if type(block) == int:
				continue
			else:
				if block.size == size:
					return True
		return False


	def add_block(self, block):
		"""Adds a block on the top of the stack of the tower and updates the relevant attributes 
		and array. Checks if the move is legal. Modifies the tower and returns True if so. 
		If move invalid, returns False and prints out an appropriate message."""

		global move_counter

		#Check if the size of the block is within the range of the game.
		assert block.size <= self.total_block_number, "Size is out of bounds of this game instance."

		#Check if the tower is empty. If so, add the block on the bottom.
		if self.check_if_empty() == True:
			self.block_object_list[-1] = block
			self.block_visual_array[-1] = block.size
			block.position[0] = self.block_object_list.index(block)
			block.position[1] = self.pos
			self.blocks_in_tower += 1
			self.update_block_on_top_flag()
			move_counter += 1
			return True

		#Find the top of the tower and add the block if its size is smaller than the top block
		#of the tower. Returns False if the size is larger.
		for i in range(self.total_block_number):
			if type(self.block_object_list[i]) == int:
				continue
			else:
				if block.size < self.block_object_list[i].size:
					self.block_object_list[i-1] = block
					self.block_visual_array[i-1, 0] = block.size
					block.position[0] = self.block_object_list.index(block)
					self.blocks_in_tower += 1
					self.update_block_on_top_flag()
					move_counter += 1
					return True
				else:
					# print("That is not a valid move.")
					return False

	def remove_block(self):
		"""Removes the top block of the tower. Updates the relevant attribute and visual array."""

		if self.blocks_in_tower == 0:
			# print("This tower is empty.")
			return False

		for i in range(self.total_block_number):
			if type(self.block_object_list[i]) == int:  #This specific patters appear multiple times
				continue								#since the list will contain 0 (an integer)
			else:										#if there is no block object in that position.
				block_to_return = self.block_object_list[i]
				self.block_object_list[i] = 0
				self.block_visual_array[i, 0] = 0
				self.blocks_in_tower -= 1
				self.update_block_on_top_flag()
				return block_to_return

	def get_block_position(self, size):
		"""Returns the position of the block with a specific size"""
		for i in range(self.total_block_number):
			if type(self.block_object_list[i]) == int:
				continue
			elif self.block_object_list[i].size != size:
				continue
			elif self.block_object_list[i].size == size:
				return i

	def update_block_on_top_flag(self):
		"""Finds the block on top and updates its flag that it is the top block."""

		if self.check_if_empty() == True:
			return None
		else:
			for block in self.block_object_list:
				if type(block) == int:
					continue
				else:
					block.block_on_top = True
					posit = self.get_block_position(block.size)
					if posit == self.total_block_number - 1:
						break
					else:
						for bl in self.block_object_list[posit + 1:]:
							bl.block_on_top = False
					break

	def top_block_size(self):
		"""Returns the size of the top block of the tower."""

		for block in block_object_list:
			if type(block) == int:
				continue
			else:
				if block.block_on_top == True:
					return block.size

	def get_top_block(self):
		"""Returns the object of the top block of the tower."""

		for block in self.block_object_list:
			if type(block) == int:
				continue
			else:
				if block.block_on_top == True:
					return block


	#Unused tower methods

	# def tower_complete(self, size):
	# 	block_sizelist = []
	# 	try:
	# 		for block in self.block_object_list:
	# 			block_size_list.append(block.size)
	# 		if block_size_list == list(range(1, size + 1)):
	# 			return True
	# 	except AttributeError:
	# 		return False



class Game:
	"""A game instance. Takes in the number of blocks we want to play with.
	Sets up the game by filling the left-most tower according to the number given. 
	Offers method that have to do with more than one towers."""

	def __init__(self, number_of_blocks):
		"""Initialize the game by creating three towers, a list of the objects, and a complete 
		visual array for the visualization of the game."""

		#Create the tower instances
		self.number_of_blocks = number_of_blocks
		self.left = Tower(1, number_of_blocks)
		self.center = Tower(2, number_of_blocks)
		self.right = Tower(3, number_of_blocks)

		#Create a list of the objects
		self.tower_object_list = [self.left, self.center, self.right]
		self.tower_position_list = [1, 2, 3]
		self.tower_names_list = ['left', 'center', 'right']

		#Fills in the left-hand tower
		self.left.fill_tower(number_of_blocks)

		#Creates the visualization array.
		self.visual_array = np.zeros((self.number_of_blocks, 3)).astype(np.int32)
		self.visual_array[:, 0] = self.left.block_visual_array[:, 0]
		self.visual_array[:, 1] = self.center.block_visual_array[:, 0]
		self.visual_array[:, 2] = self.right.block_visual_array[:, 0]


	def print_visual_array(self):
		"""Prints the visualization array."""

		print(self.visual_array)


	def update_visual_array(self):
		"""Updates the visualization array."""

		self.visual_array[:, 0] = self.left.block_visual_array[:, 0]
		self.visual_array[:, 1] = self.center.block_visual_array[:, 0]
		self.visual_array[:, 2] = self.right.block_visual_array[:, 0]


	def move_block(self, from_, to):
		"""Moves a block from one tower to another"""

		#Create variables for the towers chosen to remove from and to add to.
		tower_to_move_from = self.tower_object_list[self.tower_position_list.index(from_)]
		tower_to_move_to = self.tower_object_list[self.tower_position_list.index(to)]

		# print(f"\nChecking {self.tower_names_list[from_ - 1]} tower.")
		# time.sleep(0.5)

		#Create variable for the block to move
		block_to_move = tower_to_move_from.remove_block()

		#Check if the move is valid or not. Carry on with the move if so. Return block to 
		#original tower if not.
		if block_to_move == False:  #Check if the tower is empty.
			return False
		else:
			# string_to_print = f"Attempting to move block {block_to_move.size} from {self.tower_names_list[from_ - 1]}"
			# string_to_print += f" to {self.tower_names_list[to - 1]}."
			# print(string_to_print)
			# time.sleep(0.5)
			if tower_to_move_to.add_block(block_to_move) == True:
				# print("Success!")
				# time.sleep(0.5)
				self.update_visual_array()
				# self.print_visual_array()
				# time.sleep(0.5)
				return True
			else:
				tower_to_move_from.add_block(block_to_move)
				# print(f"Returning block to {self.tower_names_list[from_ - 1]} tower.")
				return False

	def find_block(self, size):
		"""Searches for the block of the specified size and retunrs the object of the tower
		that contains it."""
		
		for tower in self.tower_object_list:
			if tower.check_for_block(size) == True:
				return tower

	def move_block_x_to(self, number, to):
		"""Takes in the size of the block you want to move (int) and the tower position to move it
		to (int). Executes the move and reconstructs the new tower with the chosen block as the base. 
		If the block is covered by other blocks, it calls itself recursively for the block directly
		above."""

		tower_list = self.tower_object_list[:]

		tower_to = tower_list.pop(self.tower_position_list.index(to))

		tower_from = self.find_block(number)
		tower_list.remove(tower_from)

		third_tower = tower_list[0]

		if number == 1 or tower_from.get_top_block().size == number:
			self.move_block(tower_from.pos, tower_to.pos)
		else:
			self.move_block_x_to(number-1, third_tower.pos)
			self.move_block(tower_from.pos, tower_to.pos)
			self.move_block_x_to(number-1, tower_to.pos)

	#Unused game methods

	# def choose_empty_tower(self):

	# 	empty_towers = []
	# 	for tower in self.tower_object_list:
	# 		if tower.check_if_empty() == True:
	# 			empty_towers.append(tower)
	# 	if len(empty_towers) == 1:
	# 		return empty_towers[0]
	# 	elif len(empty_towers) == 2:
	# 		return choice(empty_towers)
	# 	else:
	# 		return None


#Initialize the game
game_1 = Game(10)
game_1.print_visual_array()
print("\n")

#Solve the game - If you want it to go slower, explaining what it does in the process, 
#uncomment all the sleep and print commands in the tower.move_block() method.
game_1.move_block_x_to(10, 3)
game_1.print_visual_array()
print(move_counter)