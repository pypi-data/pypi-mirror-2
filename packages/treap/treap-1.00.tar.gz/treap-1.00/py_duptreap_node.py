
# actually, it's a little faster with the standard random module than the lcgrng module; although random is a more time consuming algorithm, it's coded in C.
import random
#import lcgrng
random_module = random
#random_module = lcgrng

# FIXME: nice for debugging, bad for real life
#random_module.seed(0)

priority_size = 0x7fffffff

# this is all "hands off" to a client of the module
class _treap_node:
	
	
	
	
	

	def __init__(self):
		self.priority = long(random_module.random() * priority_size)
		self.left = None
		self.right = None

	def _check_tree_invariant(self):
		if self.left != None:
			assert self.key > self.left.key
			assert self.left._check_tree_invariant()
		if self.right != None:
			assert self.key <= self.right.key
			assert self.right._check_tree_invariant()
		return True

	def _check_heap_invariant(self):
		# I kinda thought it was supposed to be <, but clearly that won't work with random priorities
		if self.left != None:
			assert self.priority <= self.left.priority
			assert self.left._check_heap_invariant()
		if self.right != None:
			assert self.priority <= self.right.priority
			assert self.right._check_heap_invariant()
		return True

	def _check_invariants(self):
		assert self._check_tree_invariant()
		assert self._check_heap_invariant()
		return True

	def insert(self, node, key, value, priority):
		return self.pyx_insert(node, key, value, priority)

	def pyx_insert(self, node, key, value, priority):
		# We arbitrarily ditch duplicate values, but I believe we could just save them in a list.
		# We probably should have a series of classes via a class factory that sets class variables to
		# distinguish the priority max and whether we store duplicates.
		if node is None:
			# adding a node, increasing the treap length by 1
			node = _treap_node()
			if priority:
				node.priority = priority
			node.key = key
			node.value = value
			return (1, node)
		elif key < node.key:
			(length_delta, node.left) = self.pyx_insert(node.left, key, value, priority)
			if node.left.priority < node.priority:
				node = self.rotate_with_left_child(node)
			return (length_delta, node)
		elif key >= node.key:
			(length_delta, node.right) = self.pyx_insert(node.right, key, value, priority)
			if node.right.priority < node.priority:
				node = self.rotate_with_right_child(node)
			return (length_delta, node)
		

	def remove(self, node, key):
		return self.pyx_remove(node, key)

	def pyx_remove(self, node, key):
		found = False
		if node != None:
			if key < node.key:
				(found, node.left) = self.pyx_remove(node.left, key)
			elif key > node.key:
				(found, node.right) = self.pyx_remove(node.right, key)
			else:
				# Match found
				# these two tests for emptiness don't appear to be in http://users.cis.fiu.edu/~weiss/dsaajava/Code/DataStructures
				if node.left is None:
					return (True, node.right)
				if node.right is None:
					return (True, node.left)
				if node.left.priority < node.right.priority:
					node = self.rotate_with_left_child(node)
				else:
					node = self.rotate_with_right_child(node)

				# Continue on down
				if node != None:
					(found, node) = self.pyx_remove(node, key)
				else:
					# At a leaf
					node.left = None
		return (found, node)

	def remove_min(self, node):
		if not (node is None):
			if not (node.left is None):
				(node.left, result) = self.remove_min(node.left)
			else:
				# Minimum found
				return (node.right, (node.key, node.value))
		return (node, result)

	def remove_max(self, node):
		if not (node is None):
			if not (node.right is None):
				(node.right, result) = self.remove_max(node.right)
			else:
				# maximum found
				return (node.left, (node.key, node.value))
		return (node, result)

	def rotate_with_left_child(self, node):
		temp = node.left
		node.left = temp.right
		temp.right = node
		node = temp
		return node

	def rotate_with_right_child(self, node):
		temp = node.right
		node.right = temp.left
		temp.left = node
		node = temp
		return node

	def detailed_inorder_traversal(self, visit, depth=0, from_left=0):
		if self.left != None:
			self.left.detailed_inorder_traversal(visit, depth+1, from_left*2)
		visit(self, self.key, self.value, depth, from_left)
		if self.right != None:
			self.right.detailed_inorder_traversal(visit, depth+1, from_left*2+1)

	def inorder_traversal(self, visit):
		if self.left != None:
			self.left.inorder_traversal(visit)
		visit(self.key, self.value)
		if self.right != None:
			self.right.inorder_traversal(visit)

	def __str__(self):
		return '%s/%s/%s' % (self.key, self.priority, self.value)
		#return '%s/%s' % (self.key, self.value)

