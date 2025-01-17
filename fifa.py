import csv
import math
from turtle import position


class Player:
	def __init__(self, sofifa_id, name, position, age, height, weight): 
		self.sofifa_id = sofifa_id 
		self.name = name
		self.position = position
		self.age = age
		self.height = height
		self.weight = weight
		self.rating_count = 0   # a contagem inicia como zero
		self.rating_avg = 0     # a média inicia como zero

	def incCount(self):
		# Incrementamos a contagem
		self.rating_count += 1
	
	def getSofifaID(self):
		return self.sofifa_id

	def setAverage(self, rating):
		# Multiplicamos a média anterior pela contagem anterior
		self.rating_avg = self.rating_avg*(self.rating_count-1)
		# Somamos a nova avaliação
		self.rating_avg += rating
		# Dividimos pela nova contagem e obtemos a média atualizada
		self.rating_avg = self.rating_avg/self.rating_count

	def __str__(self):
		return (str(self.sofifa_id) + " " + self.name + " " +  self.position + " " +  str(self.age) + " " +  str(self.height) + " " +  str(self.weight))


# Fields summary:
# 0 - sofifa_id
# 1 - long_name
# 2 - age
# 3 - player_positions

# ----------- players.csv ----------
# Total number of players:
NUM_PLAYERS = 18944
# Number of entries on Players hash table
NUM_ENTRIES_PLAYERS = 9497  # --> closest prime number to NUM_PLAYERS
# ----------- rating.csv -----------
# Total number of ratings:
NUM_RATINGS = 1048576 
# Number of entries on Ratings hash table
NUM_ENTRIES_RATINGS = 524287 # --> closest prime number to NUM_RATINGS
# ----------- tags.csv -----------



# Returns a hash table with NUM_ENTRIES_PLAYERS entries
def new_hash_table():
	hash_table = []
	for i in range(0, NUM_ENTRIES_PLAYERS):
		hash_table.append([])
	return hash_table



# Inserts a player in a hash table, according to its sofifa_id, and returns the hash table
def insert_hash(hash_table, a_player):
	hash_table[(a_player.getSofifaID())%NUM_ENTRIES_PLAYERS].append(a_player)
	return hash_table

# Opens the players.csv archive and inserts ... ---------> NOT FINISHED
def read_players_csv(hash_table):
	with open("players.csv", "r") as archive:
		line_count = 0
		csv_table = csv.reader(archive, delimiter=",")
		i=0
		for row in csv_table:
			if(i!=0):
				hash_table = insert_hash(hash_table, (Player(int(row[0]), row[1], row[2], int(row[3]), int(row[4]), int(row[5]))))
			i+=1
	return hash_table

# Opens the rating.csv archive and inserts ... ---------> NOT FINISHED
def read_rating_csv(hash_table):
	with open("rating.csv", "r") as archive:
		line_count = 0
		csv_table = csv.reader(archive, delimiter=",")
		i=0
		for row in csv_table:
			if(i!=0):
				hash_table = insert_hash(hash_table, (Player(int(row[0]), row[1], row[2], int(row[3]), int(row[4]), int(row[5]))))
			i+=1
	return hash_table

# Prints the statistic of the given hash table
def statistic_entries(hash_table):
	empty_entries = 0
	used_entries = 0
	longest = 0
	shortest = NUM_PLAYERS

	for entry in hash_table:
		if(entry == []):
			shortest = 0
			empty_entries += 1
		else:
			used_entries += 1
			if(len(entry)>longest):
				longest = len(entry)
	print(" ======== STATISTIC =========")
	print("Number of empty entries: " + str(empty_entries))
	print("Number of used entries: " + str(used_entries))
	print("USED/TOTAL = " + str(used_entries/NUM_ENTRIES_PLAYERS))
	print("Longest entries: " + str(longest))
	print("Shortest entries: " + str(shortest))

# ========    DEFINIÇÕES  =========
ALPHABET_SIZE = 30
# =================================

class User:
	def __init__(self, ID, ratings):
		self.ID = ID
		self.ratings = []
		self.ratings.append(ratings)
	def addRating(self, rating):
		self.ratings.append(rating)
	def getRatings(self):
		return self.ratings


# trie node

class TrieNode:
	def __init__(self, EndOfWord, letter):
		# EndOfWord is -1 if the letter does not represent the end of a word. Otherwise, its
		# value represents the sofifa_id of the player whose name is the word represented
		self.EndOfWord = EndOfWord 
		self.children = [None]*ALPHABET_SIZE
		self.letter = letter

	def getEndOfWord(self):
		return self.EndOfWord
	
	# Searches for a Player in the Trie Tree and returns:
	# - the sofifa_id of a Player if he was found
	def searchPrefix(self, word):
		# the node is where we search for the letter word[w] in node's children
		node = self
		size = len(word)        # the length of the word that we are searching for
		w = 0           # index for the word
		c = 0           # index for the children
		word=word.lower()
		while(w<size):           # outer loop --------> searchs for all letters
			# Checks if one the children has the letter searched:
			while(c<len(node.children)):
				if(node.children[c] is None):
					c+=1
				elif node.children[c].letter==word[w]:
					break
				else:
					c+=1
			# Checks if the it ran out of children and returns -1 if so 
			if(c==len(node.children)):
				return -1
			# If it didn't go out of children, it found the letter
			else:
				w += 1                          # will search for the next letter
				node = node.children[c]         # updates the node 
				c = 0                           # resets the first child
		return node   # Returns the sofifa_id if the letter is the end of a word or -1 if it is not

	def insertTrie(self, key, code):
		current=self
		for i in range(0,len(key)):
			l=key[i].lower()
			index=ord(l)-97
			if index<0 or index>26:	
				#No a-z characters ordered by frequency
				if index==-65: #' ' character
					index=28 
				elif index==-52: #'-' character
					index=27 
				elif index==-58: #"'" character
					index=28 
				elif index==-51: #'.' character
					index=26
				else:
					index=28 
			if(current.children[index] is None):
				if(i==len(key)):
					novo=TrieNode(code, l)
					current.children[index]=novo
				else:
					novo=TrieNode(-1, l)
					current.children[index]=novo
			if(i==len(key)-1):
				current.children[index].EndOfWord=code
			current=current.children[index]

	def printChildren(self, node, string):
		string=string+node.letter
		if node==None:
			return 
		total=len(node.children)
		for i in range(0, total-1):
			if node.children[i] is not None:
				self.printChildren(node.children[i], string)
		if node.EndOfWord!=-1:
			printPlayer(node.getEndOfWord())
		if node.children[total-1] is not None:
			self.printChildren(node.children[total-1], string)

root=TrieNode(-1," ")
root.insertTrie("Ana", 5)
root.insertTrie("astolfo", 10)
root.insertTrie("bia", 12)
root.printChildren(root,'')
root.searchPrefix("Ana")





# ===================================================================================
# ==============
# 
# 1 - Creates a hash table 
hash_table = new_hash_table()
# 2 - Opens the players.csv archive and inserts the players on the hash table
read_players_csv(hash_table)
# 3 - Prints the statistic of the hash table
statistic_entries(hash_table)
