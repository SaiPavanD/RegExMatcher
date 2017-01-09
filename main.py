class count():
	"""Class for maintaining a counter"""
	def __init__(self):
		self.count = 0

	def get_count(self):
		self.count+=1
		return self.count-1

class prod():
	"""Class for maintaining productions of cfg"""
	def __init__(self,lhs,rhs):
		self.lhs = lhs
		self.rhs = rhs

class cfg_reg():
	"""Class for maintaining cfg of valid reg ex"""
	def __init__(self):
		#init with the productions required
		self.prod1 = []		#list of prods of type A -> BC
		self. prod2 = []	#prof of prods of type A -> a
		
		self.prod1.append(prod('S','AB'))
		self.prod1.append(prod('B','DC'))
		self.prod1.append(prod('D','SE'))
		self.prod1.append(prod('D','SF'))
		self.prod1.append(prod('D','SG'))
		self.prod1.append(prod('E','HS'))
		self.prod1.append(prod('G','IS'))

		self.prod2.append(prod('A','('))
		self.prod2.append(prod('C',')'))
		self.prod2.append(prod('H','+'))
		self.prod2.append(prod('F','*'))
		self.prod2.append(prod('I','.'))
		for i in 'qwertyuiopasdfghjklzxcvbnm':
			self.prod2.append(prod('S',i))

class nfa():
	"""Class maintaining NFA"""
	def __init__(self):
		self.s = None
		self.f = None
		self.delta = {}

class reg_ex():
	"""Class for maintaining and checking for valid reg ex"""
	def __init__(self,s):
		self.count = count()
		self.re = s
		self.cyk()
		

	def cyk(self):
		n = len(self.re)
		grammar = cfg_reg()
		t = []
		for i in range(n + 1):
			t.append([])
			for j in range(n + 1):
				t[i].append([])

		for i in range(n):
			for p in grammar.prod2:
				if p.rhs == self.re[i:i+1]:
					t[i][i+1].append(p.lhs)

		for m in range(2,n + 1):
			for i in range(n - m + 1):
				for j in range(i+1,i+m):
					for p in grammar.prod1:
						if p.rhs[0] in t[i][j] and p.rhs[1] in t[j][i+m]:
							t[i][i+m].append(p.lhs)

		if 'S' in t[0][n]:
			self.valid = True
			self.make_nfa()
		else:
			self.valid = False

	def base(self,a):
		n1 = nfa()
		i = self.count.get_count()
		j = self.count.get_count()
		n1.s = i
		n1.f = j
		n1.delta[(i,a)] = [j]
		return n1

	def concat(self,n1,n2):
		n3 = nfa()
		n3.s = n1.s
		n3.f = n2.f
		for i in n1.delta:
			n3.delta[i] = n1.delta[i]
		for i in n2.delta:
			n3.delta[i] = n2.delta[i]
		n3.delta[(n1.f,'')] = [n2.s]
		return n3

	def union(self,n1,n2):
		n3 = nfa()
		i = self.count.get_count()
		j = self.count.get_count()
		n3.s = i
		n3.f = j
		for k in n1.delta:
			n3.delta[k] = n1.delta[k]
		for k in n2.delta:
			n3.delta[k] = n2.delta[k]
		n3.delta[(i,'')] = [n1.s,n2.s]
		n3.delta[(n1.f,'')] = [j]
		n3.delta[(n2.f,'')] = [j]
		return n3

	def star(self,n1):
		n2 = nfa()
		i = self.count.get_count()
		j = self.count.get_count()
		n2.s = i
		n2.f = j
		for k in n1.delta:
			n2.delta[k] = n1.delta[k]
		for k in n2.delta:
			n2.delta[k] = n2.delta[k]
		n2.delta[(i,'')] = [n1.s,j]
		n2.delta[(n1.f,'')] = [j,n1.s]
		return n2

	def make_nfa(self):
		paren_stack = []
		alpha_stack = []
		symbol_stack = []
		for i in self.re:
			if i is '(':
				paren_stack.append(i)
			elif i is '*' or i is '+' or i is '.':
				symbol_stack.append(i)
			elif i in 'qwertyuiopasdfghjklzxcvbnm':
				n = self.base(i)
				alpha_stack.append(n)
			elif i is ')':
				if symbol_stack[-1] is '*':
					temp = alpha_stack.pop()
					temp2 = self.star(temp)
					alpha_stack.append(temp2)
				elif symbol_stack[-1] is '+':
					temp = alpha_stack.pop()
					temp1 = alpha_stack.pop()
					temp2 = self.union(temp1,temp)
					alpha_stack.append(temp2)
				elif symbol_stack[-1] is '.':
					temp = alpha_stack.pop()
					temp1 = alpha_stack.pop()
					temp2 = self.concat(temp1,temp)
					alpha_stack.append(temp2)
				paren_stack.pop()
				symbol_stack.pop()
		self.nfa = alpha_stack[0]			

	def is_accepted(self,s):
		curr = [self.nfa.s]
		for i in s:
			e_s = self.e_trans(curr)
			temp = []
			for j in e_s:
				if (j,i) in self.nfa.delta:
					for k in self.nfa.delta[(j,i)]:
						temp.append(k)
			curr = []
			for j in temp:
				curr.append(j)
		e_s = self.e_trans(curr)
		for i in e_s:
			curr.append(i)
		if self.nfa.f in curr:
			return 'Yes'
		else:
			return 'No'
	
	def e_trans(self,l):
		r = []
		temp = []
		for i in l:
			temp.append(i)
			r.append(i)
		while len(temp)!=0:
			temp1 = []
			for i in temp:
				if (i,'') in self.nfa.delta:
					for j in self.nfa.delta[(i,'')]:
						if j not in r:
							temp1.append(j)
							r.append(j)
			temp = []
			for i in temp1:
				temp.append(i)
		return r

regex = str(raw_input())

re = reg_ex(regex)
l = []

if re.valid:
	t = int(raw_input())
	for i in range(0,t):
		l.append(str(raw_input()))
	for i in l:
		print re.is_accepted(i)
	
else:
	print "Wrong Expression"
