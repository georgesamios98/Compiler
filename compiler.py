####   Gia na trexei to programma tha prepei sto terminal na dothei h entolh python lexsynt.py testfile.min h python3 lexsynt.py testfile.min
####   Paradidoume epishs 2 arxeia gia elegxo ena arxeio testfile.min pou prepei na pernaei compiler xwris error
####   kai ena arxeio testfile1.min pou prepei na yparxei error kathos dn kleinei mia agkylh '}'
import string
import sys
import copy

##########LEKTIKOS ANALYTHS##########
fpos=0
line=1
pos=0

def lex():
	filename = sys.argv[1]
	#print(filename)
	fp = open(filename, 'r')
	#states
	state0 = 0		#arxikh katastash
	state1 = 1		#katastash gia anagnwristika
	state2 = 2		#katastash gia arithmitikh stathera
	state3 = 3		#katastash gia <
	state4 = 4		#katastash gia >
	state5 = 5		#katastash gia :
	state6 = 6		#katastash gia sxolia //
	state7 = 7		#katastash gia telos sxolion //
	state8 = 8		#katastash gia sxolia /*
	state9 = 9		#katastash gia sxolia */
	state10 = 10	#katastash gia - ws (- h gia arnhtiko arithmo)
	OK = -1			#katastash OK
	error = -2		#katastash gia errors
	EOF = -3		#katastash gia end-of-file

	#tokens to return
	tokens = []
	keywords = ['program', 'declare', 'if', 'else', 'while','doublewhile','loop', 'exit', 'forcase',
					'incase','when','default', 'not', 'and', 'or', 'function','procedure', 'call',
					'return', 'in', 'inout', 'input','print']

	global fpos
	global line
	global pos
	lexeme = ''
	fp.seek(fpos)
	state=state0
	while(state!=OK and state!=error and state!=EOF ):
		char = fp.read(1)
		pos += 1
		#state0
		if(state==state0):
			if(char == ''):
				state=EOF
			#paramenoume oso erxetai leukos xaraktiras
			elif (char == ' '):
				state = state0
			elif (char == '\t'):
				pos+=4	#proxwrav 4 thesis
			elif(char=='\n'):
				line+=1		#allazw grammh
				pos=0
			#an erthei gramma pame stin katastasi 1
			elif(char in string.ascii_letters):
				state=state1
			#an erthei arithmos pame stin katastasi 2
			elif(char in string.digits):
				state=state2
			elif(char=='<'):
				state=state3
			elif(char=='>'):
				state=state4
			elif(char==':'):
				state=state5
			elif(char=='+'):
				state = OK
				lexeme =char
				tokens += [lexeme] +[3]
			elif(char=='-'):
				state = state10
			elif(char=='*'):
				state = OK
				lexeme = char
				tokens += [lexeme] +[5]
			elif(char=='/'):
				state = state6
			elif(char==','):
				state = OK
				lexeme = char
				tokens += [lexeme] +[7]
			elif(char==';'):
				state = OK
				lexeme = char
				tokens += [lexeme] +[8]
			elif(char=='{'):
				state = OK
				lexeme = char
				tokens += [lexeme] +[9]
			elif(char=='}'):
				state = OK
				lexeme = char
				tokens += [lexeme] +[10]
			elif(char=='('):
				state = OK
				lexeme = char
				tokens += [lexeme] +[11]
			elif(char==')'):
				state = OK
				lexeme = char
				tokens += [lexeme] +[12]
			elif(char=='['):
				state = OK
				lexeme = char
				tokens += [lexeme] +[13]
			elif(char==']'):
				state = OK
				lexeme = char
				tokens += [lexeme] +[14]
			elif(char=='='):
				state = OK
				lexeme = char
				tokens += [lexeme] +[15]
			else:
					state=error
					print('error: Unknown character= %s' % char)
					print('Line(pos) > %d(%d)' % (line, pos))
		#state10 for '-'
		if(state==state10):
			lexeme+=char
			char = fp.read(1)
			if(char in string.digits):
				state = state2
			else:
				state=OK
				tokens += [lexeme]+[4]
				fp.seek(fp.tell()-1)
				pos-=1
		#state1
		if(state==state1):
			if(char in string.ascii_letters or char in string.digits):
				lexeme+=char
			else:
				if(len(lexeme)<=30):
					state=OK
					fp.seek(fp.tell()-1)
					pos-=1
					if(lexeme in keywords):
						tokens += [lexeme]+[keywords.index(lexeme)+25]
					else:
						tokens += [lexeme]+[1]
				else:
					state = error
					print('error: Invalid name,(length of %s > 30)  ' % lexeme)
					print('Line(pos) > %d(%d)' % (line,pos))
		#state2
		if(state == state2):
			if(char in string.digits):
				lexeme+=char
			else:
				pos-=1
				if(int(lexeme)>32767):
					state = error
					print('error: Number:(%s) > 32767  ' % lexeme)
					print('Line(pos) > %d(%d)' % (line, pos))
				elif(int(lexeme)<-32767):
					state = error
					print('error: Number:(%s) < -32767  ' % lexeme)
					print('Line(pos) > %d(%d)' % (line, pos))
				else:
					state=OK
					tokens += [lexeme]+[2]
					fp.seek(fp.tell()-1)
		#state3
		if(state == state3):
			lexeme+=char	#lexeme='<'
			char = fp.read(1)	#diavazoume ena char parakato
			if(char == '='):
				state = OK
				lexeme+=char
				pos+=1
				tokens += [lexeme]+[16]
			elif(char == '>'):
				state = OK
				lexeme+=char
				pos+=1
				tokens += [lexeme]+[17]
			else:
				state = OK
				tokens += [lexeme]+[18]
				fp.seek(fp.tell()-1)
		#state4
		if(state == state4):
			lexeme+=char	#lexeme='>'
			char = fp.read(1)	#diavazoume ena char parakato
			if(char == '='):
				state = OK
				lexeme+=char
				pos+=1
				tokens += [lexeme]+[19]
			else:
				state = OK
				tokens += [lexeme]+[20]
				fp.seek(fp.tell()-1)
		#state5
		if(state == state5):
			lexeme+=char	#lexeme=':'
			char = fp.read(1)	#diavazoume ena char parakato
			if(char == '='):
				state = OK
				lexeme+=char
				pos+=1
				tokens += [lexeme]+[21]
			else:
				state = OK
				tokens += [lexeme]+[22]
				fp.seek(fp.tell()-1)
		#state6
		if(state == state6):
			char = fp.read(1)	#diavazoume ena char parakato
			if(char == '/'):
				pos+=1
				state=state7
				char = fp.read(1)
				pos+=1
			elif(char == '*'):
				pos+=1
				state = state8
				char = fp.read(1)
				pos+=1
			else:
				state = OK
				tokens += [lexeme]+[24]
				fp.seek(fp.tell()-1)
		#state7
		if(state == state7):
			if(char != '\n'):
				state=state7
			else:
				state=state0
				line+=1
		#state8
		if(state == state8):
			if(char == '*'):
				state=state9
			elif(char == '\n'):
				line+=1
			elif(char == ''):
				state=error
				print('error: Unclosed comments' )
				print('Line(pos) > %d(%d)' % (line, pos))
			else:
				state = state8
		#state9
		if(state == state9):
			char = fp.read(1)
			pos+=1
			if(char == '/'):
				state = state0
			else:
				state = state8
				fp.seek(fp.tell()-1)
		#error
		if(state == error):
			tokens += ['error']+[-2]
		#EOF
		if(state == EOF):
			tokens = ['EOF']+[-3]

	fpos = fp.tell()
	fp.close()
	#print (tokens[0],",",tokens[1])
	return tokens




##################################################
##################################################
############  SYNTAKTIKOS ANALYTIS  ##############
##################################################
##################################################


#lista opou apothikevo oles tis metavlites p ginontai declare
#tin xrisimopoio ston isodinamo kodika
global declarationList
declarationList=[]

def SyntaktikosAnalyths():
	global tokens
	global flag
	global tempcounter
	tempcounter=0
	flag=False
	tokens=lex()
	#<program> ::= program id { <block> }
	def program():
		global tokens
		if(tokens[0]=='program'):
			tokens=lex()
			if(tokens[1]==1):
				pName=tokens[0]
				#print("name=%s"%pName)
				tokens=lex()
				if(tokens[0]=='{'):
					tokens=lex()
					block(pName,True)
					if(tokens[0]=='}'):
						tokens=lex()
						#genQuad("halt",pName,"_","_")
						#print("%s"%x)
						return
					else:
						print("error: Missing right brackets '}' ")
						print('Line(pos) > %d(%d)' % (line, pos))
						exit(1)
				else:
					print("error: Missing open brackets '{' ")
					print('Line(pos) > %d(%d)' % (line, pos))
					exit(1)
			else:
				print("error: program name expected")
				print('Line(pos) > %d(%d)' % (line, pos))
				exit(1)
		else:
			print("error: The keyword program was expected")
			print('Line(pos) > %d(%d)' % (line, pos))
			exit(1)
		return

	#<block> ::= <declarations> <subprograms> <statements>
	def block(bName,isMainProgram):
		global tokens,argumentsList
		add_scope(bName,isMainProgram)
		if(not isMainProgram):
			for a in argumentsList:
				offset = get_offset()
				e = Entity()
				e.name=a.name
				e.type = "par"
				e.par.parMode = a.parMode
				e.par.offset = offset
				add_entities(e)
		genQuad("begin_block",bName,"_","_")
		if(not isMainProgram):
			get_startQuad()
		#print("%s"%x)
		declarations()
		subprograms()
		statements()
		if(isMainProgram==True):
			genQuad("halt",bName,"_","_")
		else:
			get_frameLength()
		genQuad("end_block",bName,"_","_")
			#print("%s"%x)
		return

	#<declarations> ::= (declare <varlist>;)*
	def declarations():
		global declarationList
		global tokens
		while(tokens[0]=='declare'):
			declarationList.append("int ")
			tokens=lex()
			varlist()
			if(tokens[0]==';'):
				declarationList.append("; \n\t")
				tokens=lex()
			else:
				print("error: Expected ';' ")
				print('Line(pos) > %d(%d)' % (line, pos))
				exit(1)
		return

	#<varlist> ::= e | id ( , id )*
	def varlist():
		global declarationList
		global tokens
		if(tokens[1]==1):
			###### code #####
			declarationList.append(tokens[0])
			entity = Entity()
			entity.name = tokens[0]
			entity.var.offset = get_offset()
			entity.type = "var"
			add_entities(entity)
			tokens=lex()
			while(tokens[0]==','):
				declarationList.append(tokens[0])
				tokens=lex()
				if(tokens[1]==1):
					###### code ######
					declarationList.append(tokens[0])
					entity = Entity()
					entity.name = tokens[0]
					entity.var.offset = get_offset()
					entity.type = "var"
					add_entities(entity)
					tokens=lex()
				else:
					print("error: Expected variable before %s in declarations",tokens[0])
					print('Line(pos) > %d(%d)' % (line, pos))
					exit(1)
		return

	#<subprograms> ::= (<subprogram>)*
	def subprograms():
		global tokens
		while(tokens[0]=='function' or tokens[0]=='procedure'):
			subprogram()
		return
	#<subprogram> ::= function id <funcbody> | procedure id <funcbody>
	def subprogram():
		global tokens
		if(tokens[0]=='function'):
			tokens=lex()
			if(tokens[1]==1):
				funcname=tokens[0]
				entity = Entity()
				entity.name = funcname
				entity.funcProc.type = "func"
				entity.type = "funcproc"
				add_entities(entity)
				tokens=lex()
				funcbody(funcname)
			else:
				print("error: function name was expected")
				print('Line(pos) > %d(%d)' % (line, pos))
				exit(1)
		elif(tokens[0]=='procedure'):
			tokens=lex()
			if(tokens[1]==1):
				procName=tokens[0]
				entity = Entity()
				entity.name = procName
				entity.funcProc.type = "proc"
				entity.type = "funcproc"
				add_entities(entity)
				tokens=lex()
				funcbody(procName)
			else:
				print("error: procedure name was expected")
				print('Line(pos) > %d(%d)' % (line, pos))
				exit(1)
		return

	#<funcbody> ::= <formalpars> { <block> }
	def funcbody(name):
		global tokens
		formalpars()
		if(tokens[0]=='{'):
			tokens=lex()
			block(name,False)
			if(tokens[0]=='}'):
				tokens=lex()
				return
			else:
				print("error: Missing right brackets '}' ")
				print('Line(pos) > %d(%d)' % (line, pos))
				exit(1)
		else:
			print("error: Missing open brackets '{' ")
			print('Line(pos) > %d(%d)' % (line, pos))
			exit(1)
		return

	#<formalpars> ::= ( <formalparlist> )
	def  formalpars():
		global tokens
		if(tokens[0]=='('):
			tokens=lex()
			formalparlist()
			if(tokens[0]==')'):
				tokens=lex()
				return
			else:
				print("error: Missing right parentheses ')' ")
				print('Line(pos) > %d(%d)' % (line, pos))
				exit(1)
		else:
			print("error: Missing open parentheses '(' ")
			print('Line(pos) > %d(%d)' % (line, pos))
			exit(1)
		return

	#<formalparlist> ::= <formalparitem> ( , <formalparitem> )* | e
	def formalparlist():
		global tokens
		if(tokens[0]=="in" or tokens[0]=="inout"):
			formalparitem()
			while(tokens[0]==','):
				tokens=lex()
				formalparitem()
		return

	#<formalparitem> ::= in id | inout id
	def formalparitem():
		global tokens
		if(tokens[0]=='in'):
			tokens=lex()
			if(tokens[1]==1):
				argument = Argument()
				argument.name = tokens[0]
				argument.parMode = "cv"
				add_args(argument)
				tokens=lex()
				return
			else:
				print("error: Expected variable name after 'in' ")
				print('Line(pos) > %d(%d)' % (line, pos))
				exit(1)
		elif(tokens[0]=='inout'):
			tokens=lex()
			if(tokens[1]==1):
				argument = Argument()
				argument.name = tokens[0]
				argument.parMode = "ref"
				add_args(argument)
				tokens=lex()
				return
			else:
				print("error: Expected variable name after 'inout' ")
				print('Line(pos) > %d(%d)' % (line, pos))
				exit(1)
		return

	#<statements> ::= <statement> | { <statement> ( ; <statement> )* }
	def statements():
		global tokens
		if(tokens[0]=='{'):
			tokens=lex()
			statement()
			while(tokens[0]==';'):
				tokens=lex()
				statement()
			if(tokens[0]=='}'):
				tokens=lex()
				return
			else:
				print("error: Missing close brackets '}' ")
				print('Line(pos) > %d(%d)' % (line, pos))
				exit(1)
		else:
			statement()
		return

	#<statement> ::= <assignment-stat> |
	#					<if-stat> |
	#					<while-stat> |
	#					<doublewhile-stat> |
	#					<loop-stat> |
	#					<exit-stat> |
	#					<forcase-stat> |
	#					<incase-stat> |
	#					<call-stat> |
	#					<return-stat> |
	#					<input-stat> |
	#					<print-stat>
	def statement():
		global tokens
		if(tokens[1]==1):
			assignmentstat()	#otan mpw tha exw dei id
		elif(tokens[1]==27):
			ifstat()
		elif(tokens[1]==29):
			whilestat()
		elif(tokens[1]==30):
			doublewhilestat()
		elif(tokens[1]==31):
			loopstat()
		elif(tokens[1]==32):
			exitstat()
		elif(tokens[1]==33):
			forcasestat()
		elif(tokens[1]==34):
			incasestat()
		elif(tokens[1]==42):
			callstat()
		elif(tokens[1]==43):
			returnstat()
		elif(tokens[1]==45):
			inputstat()
		elif(tokens[1]==47):
			printstat()
		return

	#<assignment-stat> ::= id := <expression>
	def assignmentstat():
		global tokens
		global flag
		global tempcounter
		id=tokens[0]
		tokens=lex()
		if(tokens[0]==':='):
			tokens=lex()
			x=expression()
			if(flag==True):
				genQuad(":=","T_"+str(tempcounter),"_",id)
				flag=False
			else:
				genQuad(":=",x,"_",id)
		else:
			print("error: Expected ':=' ")
			print('Line(pos) > %d(%d)' % (line, pos))
			exit(1)
		return

	#<if-stat> ::= if (<condition>) then <statements> <elsepart>
	def ifstat():
		global tokens
		tokens=lex()
		if(tokens[0]=='('):
			tokens=lex()
			cond=condition()
			if(tokens[0]==')'):
				tokens=lex()
				if(tokens[0]=='then'):
					tokens=lex()
					##{P1}
					backPatch(cond[0],nextQuad())
					statements()
					#{P2}
					if_list = makeList(nextQuad())
					genQuad("JUMP","_","_","_")
					backPatch(cond[1],nextQuad())
					elsepart()
					#{P3}
					backPatch(if_list,nextQuad())
			else:
				print("error: Missing close parentheses ')' ")
				print('Line(pos) > %d(%d)' % (line, pos))
				exit(1)
		else:
			print("error: Missing open parentheses '(' ")
			print('Line(pos) > %d(%d)' % (line, pos))
			exit(1)
		if_true = cond[0]
		if_false = cond[1]
		return if_true,if_false

	#<elsepart> ::= e | else <statements>
	def elsepart():
		global tokens
		if(tokens[0]=='else'):
			tokens=lex()
			statements()
		return

	#<while-stat> ::= while (<condition>) <statements>
	def whilestat():
		global tokens
		tokens=lex()
		if(tokens[0]=='('):
			tokens=lex()
			next_j = nextQuad()
			cond = condition()
			if(tokens[0]==')'):
				backPatch(cond[0],nextQuad())
				tokens=lex()
				statements()
				genQuad("JUMP","_","_",next_j)
				backPatch(cond[1],nextQuad())
			else:
				print("error: Expected ')' after condition while-stat")
				print('Line(pos) > %d(%d)' % (line, pos))
				exit(1)
		else:
			print("error: Expected '(' after while-stat")
			print('Line(pos) > %d(%d)' % (line, pos))
			exit(1)
		while_true = cond[0]
		while_false=cond[1]
		return while_true,while_false

	#<doublewhile-stat> ::= doublewhile (<condition>) <statements> else <statements>
	def doublewhilestat():
		global tokens
		tokens=lex()
		if(tokens[0]=='('):
			tokens=lex()
			condition()
			if(tokens[0]==')'):
				tokens=lex()
				statements()
				if(tokens[0]=='else'):
					elsepart()
					return
				else:
					print("error: Expected 'else-condition' after condition doublewhile-stat")
					print('Line(pos) > %d(%d)' % (line, pos))
					exit(1)
			else:
				print("error: Expected ')' after condition doublewhile-stat")
				print('Line(pos) > %d(%d)' % (line, pos))
				exit(1)
		else:
			print("error: Expected '(' after condition doublewhile-stat")
			print('Line(pos) > %d(%d)' % (line, pos))
			exit(1)
		return

	#<loop-stat> ::= loop <statements>
	def loopstat():
		global tokens
		tokens=lex()
		statements()
		return

	#<exit-stat> ::= exit
	def exitstat():
		global tokens
		tokens=lex()
		return

	#<forcase-stat> ::= forcase ( when (<condition>) : <statements> )* default: <statements>
	def forcasestat():
		global tokens
		tokens=lex()
		while(tokens[0]=='when'):
			tokens=lex()
			if(tokens[0]=='('):
				tokens=lex()
				next_i = nextQuad()
				cond = condition()
				if(tokens[0]==')'):
					backPatch(cond[0],nextQuad())
					tokens=lex()
					if(tokens[0]==':'):
						tokens=lex()
						statements()
						genQuad("JUMP","_","_",next_i)
						backPatch(cond[1],nextQuad())
					else:
						print("error: Expected ':' after condition forcase-stat")
						print('Line(pos) > %d(%d)' % (line, pos))
						exit(1)
				else:
					print("error: Expected ')' after condition forcase-stat")
					print('Line(pos) > %d(%d)' % (line, pos))
					exit(1)
			else:
				print("error: Expected '(' after condition forcase-stat")
				print('Line(pos) > %d(%d)' % (line, pos))
				exit(1)
		if(tokens[0]=='default'):
			tokens=lex()
			if(tokens[0]==':'):
				tokens=lex()
				statements()
		return

	#<incase-stat> ::= incase ( when (<condition>) : <statements> )*
	def incasestat():
		global tokens
		tokens=lex()
		while(tokens[0]=='when'):
			tokens=lex()
			if(tokens[0]=='('):
				tokens=lex()
				condition()
				if(tokens[0]==')'):
					tokens=lex()
					if(tokens[0]==':'):
						tokens=lex()
						statements()
					else:
						print("error: Expected ':' after condition incase-stat")
						print('Line(pos) > %d(%d)' % (line, pos))
						exit(1)
				else:
					print("error: Expected ')' after condition incase-stat")
					print('Line(pos) > %d(%d)' % (line, pos))
					exit(1)
			else:
				print("error: Expected ':' after condition incase-stat")
				print('Line(pos) > %d(%d)' % (line, pos))
				exit(1)
		return

	#<call-stat> ::= call id(<actualpars>)
	def callstat():
		global tokens
		tokens=lex()
		if(tokens[1]==1):
			tokens=lex()
			name = tokens[0]
			actualpars(name,False)
			return
		else:
			print("error: Expected 'id' after call-stat")
			print('Line(pos) > %d(%d)' % (line, pos))
			exit(1)
		return

	#<return-stat> ::= return <expression>
	def returnstat():
		global tokens
		tokens=lex()
		exp = expression()
		genQuad("retv",exp,"_","_")
		return

	#<input-stat> ::= input (id)
	def inputstat():
		global tokens
		tokens=lex()
		if(tokens[0]=='('):
			tokens=lex()
			if(tokens[1]==1):
				tokens=lex()
				if(tokens[0]==')'):
					tokens=lex()
					return
				else:
					print("error: Expected ')' after input-stat")
					print('Line(pos) > %d(%d)' % (line, pos))
					exit(1)
			else:
				print("error: Expected 'id' after input-stat")
				print('Line(pos) > %d(%d)' % (line, pos))
				exit(1)
		else:
			print("error: Expected '(' after input-stat")
			print('Line(pos) > %d(%d)' % (line, pos))
			exit(1)
		return

	#<print-stat> ::= print (<expression>)
	def printstat():
		global tokens
		tokens=lex()
		if(tokens[0]=='('):
			tokens=lex()
			exp=expression()
			if(tokens[0]==')'):
				tokens=lex()
				genQuad('out',exp,'_','_')
			else:
				print("error: Expected ')' after print-stat")
				print('Line(pos) > %d(%d)' % (line, pos))
				exit(1)
		else:
			print("error: Expected '(' after print-stat")
			print('Line(pos) > %d(%d)' % (line, pos))
			exit(1)
		return

	#<actualpars> ::= ( <actualparlist> )
	def actualpars(name,isfuction):
		global tokens
		if(tokens[0]=='('):
			tokens=lex()
			actualparlist()
			if(tokens[0]==')'):
				tokens=lex()
				if(isfuction==True):	#An einai function tote prepei na kanw return
					x=newTemp()
					genQuad("par",x,"RET","_")
					genQuad("call",name,"_","_")
				else:
					genQuad("call",name,"_","_")
				return
			else:
				print("error: Expected ')' actualpars")
				print('Line(pos) > %d(%d)' % (line, pos))
				exit(1)
		else:
			print("error: Expected '(' actualpars")
			print('Line(pos) > %d(%d)' % (line, pos))
			exit(1)
		return

	#<actualparlist> ::= <actualparitem> ( , <actualparitem> )* | e
	def actualparlist():
		global tokens
		if(tokens[0]=="in" or tokens[0]=="inout"):
			actualparitem()
			while(tokens[0]==','):
				tokens=lex()
				actualparitem()
		return

	#<actualparitem> ::= in <expression> | inout id
	def actualparitem():
		global tokens
		if(tokens[0]=='in'):
			tokens=lex()
			var=expression()
			genQuad("par",var,"CV","_")
		elif(tokens[0]=='inout'):
			tokens=lex()
			if(tokens[1]==1):
				var=tokens[0]
				genQuad("par",var,"REF","_")
				tokens=lex()
				return
			else:
				print("error: Expected name of variable after 'inout' ")
				print('Line(pos) > %d(%d)' % (line, pos))
				exit(1)
		return

	#<condition> ::= <boolterm> {P1} (or {P2} <boolterm> {P3})*
	def condition():
		global tokens
		condTrue=[]
		condFalse=[]
		b1=boolterm()
		#gia to {P1}
		condTrue=b1[0]
		condFalse=b1[1]
		while(tokens[0]=='or'):
			tokens=lex()
			#gia to {P2}
			backPatch(condFalse,nextQuad())
			b2=boolterm()
			#gia to {P3}
			condTrue=mergeList(condTrue,b2[0])
			condFalse=b2[1]
		return condTrue,condFalse

	#<boolterm> ::= <boolfactor> {P1} (and {P2} <boolfactor> {P3})*
	def boolterm():
		global tokens
		bTermTrue=[]
		bTermFalse=[]
		b1=boolfactor()
		#{P1}
		bTermTrue=b1[0]
		bTermFalse=b1[1]
		while(tokens[0]=='and'):
			tokens=lex()
			#gia to {P2}
			backPatch(bTermTrue,nextQuad())
			b2=boolfactor()
			#gia to {P3}
			bTermFalse=mergeList(bTermFalse,b2[1])##b2[0]
			bTermTrue=b2[0]
		return bTermTrue,bTermFalse

	#<boolfactor> ::= not [<condition>] | [<condition>] | <expression> <relational-oper> <expression>
	def boolfactor():
		global tokens
		bfactorTrue=[]
		bfactorFalse=[]
		if(tokens[0]=='not'):
			tokens=lex()
			if(tokens[0]=='['):
				tokens=lex()
				cond=condition()
				if(tokens[0]==']'):
					tokens=lex()
					bfactorTrue=cond[1]##0
					bfactorFalse=cond[0]##1
					#return bfactorTrue,bfactorFalse
				else:
					print("error: Expected ']' after condition")
					print('Line(pos) > %d(%d)' % (line, pos))
					exit(1)
			else:
				print("error: Expected '[' after condition")
				print('Line(pos) > %d(%d)' % (line, pos))
				exit(1)
		elif(tokens[0]=='['):
			tokens=lex()
			cond=condition()
			if(tokens[0]==']'):
				tokens=lex()
				#{P1}
				bfactorTrue=cond[0]##1
				bfactorFalse=cond[1]##0
				#return bfactorTrue,bfactorFalse
			else:
				print("error: Expected ']' after condition")
				print('Line(pos) > %d(%d)' % (line, pos))
				exit(1)
		else:
			exp1=expression()
			relop=relationaloper()
			exp2=expression()
			bfactorTrue=makeList(nextQuad())
			genQuad(relop,exp1,exp2,"_")
			bfactorFalse=makeList(nextQuad())
			genQuad("JUMP","_","_","_")
		return bfactorTrue,bfactorFalse

	#<expression> ::= <optional-sign> <term> ( <add-oper> <term>)*
	def expression():
		global tokens
		optionalsign()
		#vazw thn prwth metavlhth se mia var1
		var1=term()
		while(tokens[0]=='+' or tokens[0]=='-'):
			#vazw thn prajh se metavlhth oper
			oper=addoper()
			#vazw thn epomenh metavlhth se mia var2
			var2=term()
			#se prosorini metavlhth temp1 tha perasw t apotelesma
			temp=newTemp()
			genQuad(oper,var1,var2,temp)
			var1=temp
		x=var1
		return x

	#<term> ::= <factor> (<mul-oper> <factor>)*
	def term():
		global tokens
		#vazw thn prwth metavlhth se mia var1
		var1=factor()
		while(tokens[0]=='*' or tokens[0]=='/'):
			#vazw thn prajh se metavlhth oper
			oper=muloper()
			#vazw thn epomenh metavlhth se mia var2
			var2=factor()
			#se prosorini metavlhth temp1 tha perasw t apotelesma
			temp=newTemp()
			genQuad(oper,var1,var2,temp)
			var1=temp
		x=var1
		return x

	#<factor> ::= constant | (<expression>) | id <idtail>
	def factor():
		global tokens
		if(tokens[1]==2):
			num=tokens[0]
			tokens=lex()
			return num
		elif(tokens[0]=='('):
			tokens=lex()
			x=expression()
			if(tokens[0]==')'):
				num=x
				tokens=lex()
				#return x
			else:
				print("error: Expected ')' after expression")
				print('Line(pos) > %d(%d)' % (line, pos))
				exit(1)
		elif(tokens[1]==1):
			num=tokens[0]
			tokens=lex()
			idtail(num)
			#return num
		else:
			print("error: Expected 'constant' or '(expression)' or 'id'")
			print('Line(pos) > %d(%d)' % (line, pos))
			exit(1)
		return num

	#<idtail> ::= e | <actualpars>
	def idtail(name):
		global tokens
		global flag
		if(tokens[0]=='('):
			flag=True
			actualpars(name,flag)
			return

	#<relational-oper> ::= = | <= | >= | > | < | <>
	def relationaloper():
		global tokens
		if(tokens[0]=='='):
			relop=tokens[0]
			tokens=lex()
		elif(tokens[0]=='<='):
			relop=tokens[0]
			tokens=lex()
		elif(tokens[0]=='>='):
			relop=tokens[0]
			tokens=lex()
		elif(tokens[0]=='>'):
			relop=tokens[0]
			tokens=lex()
		elif(tokens[0]=='<'):
			relop=tokens[0]
			tokens=lex()
		elif(tokens[0]=='<>'):
			relop=tokens[0]
			tokens=lex()
		else:
			print("error: Expected '=' or '<=' or '>=' or '>' or '<' or '<>'")
			print('Line(pos) > %d(%d)' % (line, pos))
			exit(1)
		return relop

	#<add-oper> ::= + | -
	def addoper():
		global tokens
		if(tokens[0]=='+' or tokens[0]=='-'):
			oper=tokens[0]
			tokens=lex()
		return oper

	#<mul-oper> ::= * | /
	def muloper():
		global tokens
		if(tokens[0]=='*' or tokens[0]=='/'):
			oper=tokens[0]
			tokens=lex()
		return oper

	#<optional-sign> ::= e | <add-oper>
	def optionalsign():
		global tokens
		if(tokens[0]=='+' or tokens[0]=='-'):
			addoper()
			return

	program()

############################################################
############################################################
###########	  SYNARTHSEIS ENDIAMESOY KWDIKAS   #############
############################################################
############################################################

global lista_tetradon
global lista_etiketon
global quadcounter
lista_tetradon=[]
quadcounter=100

def nextQuad():
		# o metritis tetradon esto oti ksekinaei apo to 100,stin epomeni tha ginei 101
		global quadcounter
		return quadcounter

def genQuad(op,x,y,z):
	global quadcounter,lista_tetradon
	list=[]
	list+=[nextQuad()] + [op] + [x] + [y] + [z]
	quadcounter+=1
	lista_tetradon.append(list)
	return list

def newTemp():
	#i proti temporary metavliti tha legetai T_1 ,i deuteri T_2 ktl
	global tempcounter
	tempcounter+=1
	tempName = 'T_' + str(tempcounter)
	entity = Entity()
	entity.name = tempName
	entity.type = "temp"
	entity.temp.offset = get_offset()
	add_entities(entity)
	return tempName

def emptyList():
	return []

def makeList(x):
	list=[x]
	return list

def mergeList(l1,l2):
	return l1 + l2

def backPatch(list,z):
	global lista_tetradon
	for pointer in list:
		for i,quad in enumerate(lista_tetradon):
			if(pointer==quad[0] and quad[4]=="_"):
				lista_tetradon[i][4]=z
	return

def endiamesosFile():
	global lista_tetradon
	f = open("endiamesos.int", "w")
	for list in lista_tetradon:
		f.write(str(list[0])+":  ")
		f.write(str(list[1])+" , ")
		f.write(str(list[2])+" , ")
		f.write(str(list[3])+" , ")
		f.write(str(list[4]))
		f.write("\n")
	f.close

def isodinamoFile():
	global lista_tetradon
	global tempcounter
	global declarationList
	f = open("isodinamos.c", "w")
	f.write("#include <stdio.h> \n\n")
	f.write("int main(){ \n\t")
	if(len(declarationList)!=0):
		for x in range(len(declarationList)):
			f.write(declarationList[x])
	if(tempcounter>0):
		f.write("int ")
		for temp in range(1,tempcounter+1):
			f.write('T_' + str(temp))
			if(temp!=tempcounter):
				f.write(",")
			else:
				f.write("; \n\n\t")
	for i,tetrada in enumerate(lista_tetradon):
		if(tetrada[1] == "begin_block"):
			f.write("label_"+str(i+100)+": \n\t")
		elif(tetrada[1] == ":="):
			f.write("label_"+str(i+100)+": "+ tetrada[4]+" = "+tetrada[2]+";\n\t")
		elif(tetrada[1] == "+"):
			f.write("label_"+str(i+100)+": "+ tetrada[4]+" = "+tetrada[2]+"+"+tetrada[3]+";\n\t")
		elif(tetrada[1] == "-"):
			f.write("label_"+str(i+100)+": "+ tetrada[4]+" = "+tetrada[2]+"-"+tetrada[3]+";\n\t")
		elif(tetrada[1] == "*"):
			f.write("label_"+str(i+100)+": "+ tetrada[4]+" = "+tetrada[2]+"*"+tetrada[3]+";\n\t")
		elif(tetrada[1] == "/"):
			f.write("label_"+str(i+100)+": "+ tetrada[4]+" = "+tetrada[2]+"/"+tetrada[3]+";\n\t")
		elif(tetrada[1] == "<"):
			f.write("label_"+str(i+100)+": if("+tetrada[2]+"<"+tetrada[3]+") goto label_"+str(tetrada[4])+";\n\t")
		elif(tetrada[1] == ">"):
			f.write("label_"+str(i+100)+": if("+tetrada[2]+">"+tetrada[3]+") goto label_"+str(tetrada[4])+";\n\t")
		elif(tetrada[1] == "<="):
			f.write("label_"+str(i+100)+": if("+tetrada[2]+"<="+tetrada[3]+") goto label_"+str(tetrada[4])+";\n\t")
		elif(tetrada[1] == ">="):
			f.write("label_"+str(i+100)+": if("+tetrada[2]+">="+tetrada[3]+") goto label_"+str(tetrada[4])+";\n\t")
		elif(tetrada[1] == "="):
			f.write("label_"+str(i+100)+": if("+tetrada[2]+"=="+tetrada[3]+") goto label_"+str(tetrada[4])+";\n\t")
		elif(tetrada[1] == "<>"):
			f.write("label_"+str(i+100)+": if("+tetrada[2]+"!="+tetrada[3]+") goto label_"+str(tetrada[4])+";\n\t")
		elif(tetrada[1] == "JUMP"):
			f.write("label_"+str(i+100)+": goto label_"+str(tetrada[4])+";\n\t")
		elif(tetrada[1] == "out"):
			f.write("label_"+str(i+100)+": "+"printf(\"%d\\n\", "+tetrada[2]+"); \n\t")
		elif(tetrada[1] == "inp"):
			f.write("label_"+str(i+100)+": "+"scanf(\"%d\\n\", "+tetrada[2]+"); \n\t")
		elif(tetrada[1] == "halt"):
			f.write("label_"+str(i+100)+": {}\n\t")
	f.write("\n}")
	f.close()

############################################################
############################################################
#############  SYNARTHSEIS PINAKA SYMBOLWN   ###############
############################################################
############################################################

class Entity():
	def __init__(self):
		self.name = ""
		self.type = ""
		self.var = self.Var(self.name)
		self.funcProc = self.FuncProc(self.name)
		self.const = self.Const(self.name)
		self.par = self.Par(self.name)
		self.temp = self.Temp(self.name)


	class Var():
		def __init__(self,name):
			self.name = name
			self.type = "int"
			self.offset = 0
	class FuncProc():
		def __init__(self,name):
			self.name = name
			self.type = ""
			self.startQuad = 0
			self.arguments = argumentsList
			self.frameLength = 0
	class Const():
		def __init__(self,name):
			self.name = name
			self.value = ""
	class Par():
		def __init__(self,name):
			self.name = name
			self.parMode = ""
			self.offset = 0
	class Temp():
		def __init__(self,name):
			self.name = name
			self.offset = 0


class Scope():
	def __init__(self):
		self.name = ""
		self.entities = entitiesList
		self.nestingLevel = 0
		self.periklionta = scopesList

class Argument():
	def __init__(self):
		self.name = ""
		self.parMode = ""
		self.type = "int"

argumentsList = []
entitiesList = []
scopesList = []

scope = Scope()
scopesList.append(scope)

def add_args(arg):
	global argumentsList
	global entitiesList
	argumentsList.append(arg)
	entitiesList[len(entitiesList)-1].funcProc.arguments.append(arg)

def add_entities(entity):
	global argumentsList
	global entitiesList
	global scopesList
	entitiesList.append(entity)
	scopesList[len(scopesList)-1].entities.append(entity)
	argumentsList = []

def add_scope(name,isMainScope):
	global scope
	global entitiesList
	global scopesList
	scope.name = name
	newScope = Scope()
	if(isMainScope == False):
		newScope.periklionta.append(scope)
	scope = newScope
	scope.entities = []
	entitiesList = []
	if(len(scope.periklionta)==0):
		scope.nestingLevel = 0
	else:
		scope.nestingLevel = scope.periklionta[-1].nestingLevel + 1

def delete_scope():
	global scopesList
	if(len(scopesList)>0):
		scopesList.pop()

def get_offset():
	global scopesList
	offset = 12
	if(len(scopesList[len(scopesList)-1].entities) != 0):
		for entity in scopesList[len(scopesList)-1].entities:
			offset += 4
	return offset

def get_startQuad():
	global scopesList
	for entity in scopesList[-1].periklionta[-2].entities:
		if(entity.name == scopesList[-1].periklionta[-1].name):
			entity.funcProc.startQuad = nextQuad()

def get_frameLength():
	for entity in scopesList[-1].periklionta[-2].entities:
		if(entity.name == scopesList[-1].periklionta[-1].name):
			entity.funcProc.frameLength = get_offset()

def pinakasSymvolon_file():
	global argumentsList
	global entitiesList
	global scopesList
	f = open("pinakas_symvolon.sym", "w")
	for s in scopesList:
		f.write("\nScope: "+s.name + "\tnestingLevel: "+str(s.nestingLevel) + "\n")
		for e in s.entities:
			if(e.type == "var"):
				f.write("\tEntity: "+e.name + "\toffset: "+str(e.var.offset)+ "\n")
			elif(e.type == "par"):
				f.write("\tEntity: "+e.name + "\toffset: "+str(e.par.offset)+ "\n")
			elif(e.type == "temp"):
				f.write("\tEntity: "+e.name + "\toffset: "+str(e.temp.offset)+ "\n")
			elif(e.type == "funcproc"):
				if(e.funcProc.type == "func"):
					f.write("\tEntity: "+e.name + "\tFunction"+"\tframeLength: "+str(e.funcProc.frameLength)+ "\n")
					for a in e.funcProc.arguments:
						f.write("\t\tArgument: "+a.name+ "\tMode: "+ a.parMode+ "\n")
				elif(e.funcProc.type == "proc"):
					f.write("\tEntity: "+e.name + "\tProcedure"+"\tframeLength: "+str(e.funcProc.frameLength)+ "\n")
					for a in e.funcProc.arguments:
						f.write("\t\tArgument: "+a.name+ "\tMode: "+ a.parMode+ "\n")




#########################################################################


def mips():
	global lista_tetradon
	mipsFile = open('mipsFile.asm','w')
	for i in range(0,len(lista_tetradon)):
		mipsFile.write("L" + str(lista_tetradon[i][0]) + ":")
		if(lista_tetradon[i][1] == "begin_block"):
			mipsFile.write("\tsw $ra,-0($sp)\n")
		if(lista_tetradon[i][1] == ":="):
			loadvr(lista_tetradon[i][2],1,mipsFile)
			storerv(1,lista_tetradon[i][4],mipsFile)
		if(lista_tetradon[i][1] == "+"):
			loadvr(lista_tetradon[i][2],1,mipsFile)
			loadvr(lista_tetradon[i][3],2,mipsFile)
			mipsFile.write("\tadd $t1,$t1,$t2\n")
			storerv(1,lista_tetradon[i][4],mipsFile)
		if(lista_tetradon[i][1] == "-"):
			loadvr(lista_tetradon[i][2],1,mipsFile)
			loadvr(lista_tetradon[i][3],2,mipsFile)
			mipsFile.write("\tsub $t1,$t1,$t2\n")
			storerv(1,lista_tetradon[i][4],mipsFile)
		if(lista_tetradon[i][1] == "*"):
			loadvr(lista_tetradon[i][2],1,mipsFile)
			loadvr(lista_tetradon[i][3],2,mipsFile)
			mipsFile.write("\tmul $t1,$t1,$t2\n")
			storerv(1,lista_tetradon[i][4],mipsFile)
		if(lista_tetradon[i][1] == "/"):
			loadvr(lista_tetradon[i][2],1,mipsFile)
			loadvr(lista_tetradon[i][3],2,mipsFile)
			mipsFile.write("\tdiv $t1,$t1,$t2\n")
			storerv(1,lista_tetradon[i][4],mipsFile)
		if(lista_tetradon[i][1] == "out"):
			mipsFile.write("\tli $v0,1\n")
			loadvr(lista_tetradon[i][2],0,mipsFile)
			mipsFile.write("\tadd $a0,$zero,$t0"+"\n")
			mipsFile.write("\tsyscall\n")
		if(lista_tetradon[i][1] == "JUMP"):
			mipsFile.write("\tj L"+str(lista_tetradon[i][4])+"\n")
		if(lista_tetradon[i][1] == "<"):
			loadvr(lista_tetradon[i][2],1,mipsFile)
			loadvr(lista_tetradon[i][3],2,mipsFile)
			mipsFile.write("\tblt $t1,$t2,L"+str(lista_tetradon[i][4])+"\n")
		if(lista_tetradon[i][1] == ">"):
			loadvr(lista_tetradon[i][2],1,mipsFile)
			loadvr(lista_tetradon[i][3],2,mipsFile)
			mipsFile.write("\tbgt $t1,$t2,L"+str(lista_tetradon[i][4])+"\n")
		if(lista_tetradon[i][1] == "="):
			loadvr(lista_tetradon[i][2],1,mipsFile)
			loadvr(lista_tetradon[i][3],2,mipsFile)
			mipsFile.write("\tbeq $t1,$t2,L"+str(lista_tetradon[i][4])+"\n")
		if(lista_tetradon[i][1] == "<="):
			loadvr(lista_tetradon[i][2],1,mipsFile)
			loadvr(lista_tetradon[i][3],2,mipsFile)
			mipsFile.write("\tble $t1,$t2,L"+str(lista_tetradon[i][4])+"\n")
		if(lista_tetradon[i][1] == ">="):
			loadvr(lista_tetradon[i][2],1,mipsFile)
			loadvr(lista_tetradon[i][3],2,mipsFile)
			mipsFile.write("\tbge $t1,$t2,L"+str(lista_tetradon[i][4])+"\n")
		if(lista_tetradon[i][1] == "<>"):
			loadvr(lista_tetradon[i][2],1,mipsFile)
			loadvr(lista_tetradon[i][3],2,mipsFile)
			mipsFile.write("\tbne $t1,$t2,L"+str(lista_tetradon[i][4])+"\n")
		if(lista_tetradon[i][1] == 'end_block' or lista_tetradon[i][1] == 'halt'):
			mipsFile.write("\tlw $ra,-0($sp) \n \tjr $ra\n")



def gnvlcode(v):
	mipsFile.write("\tlw $t0"+","+"-4($sp)\n")
	mipsFile.write("\tlw $t0"+","+"-4($t0)\n")
	for e in scopesList[0].entities:
		if(v == e.name and e.type == "var"):
			mipsFile.write("\tadd $t0,$t0"+","+str(-e.var.offset)+"\n")

def loadvr(v,r,mipsFile):

	ti = "$t"+str(r)
	#mipsFile = open("mipsFile.asm","w")
	if(v.isdigit()):
		mipsFile.write("\tli " + ti + "," + v+"\n")
	for e in scopesList[0].entities:
		if(v == e.name and e.type == "var"):
			mipsFile.write("\tlw "+ti+","+str(-e.var.offset)+"($s0)\n")
	'''
	for e in scopesList[-1].entities:
		if(v == e.name and e.type == "var"):
			mipsFile.write("\tlw "+ti+","+str(-e.var.offset)+"($sp)\n")
		if(v == e.name and e.type == "par" and e.par.parMode == 'cv'):
			mipsFile.write("\tlw "+ti+","+str(-e.par.offset)+"($sp)\n")
		if(v == e.name and e.type == "par" and e.par.parMode == 'ref'):
			mipsFile.write("\tlw $t0"+","+str(-e.par.offset)+"($sp)\n")
			mipsFile.write("\tlw "+ti+","+"($t0)\n")
		if(v == e.name and e.type == "temp"):
			mipsFile.write("\tlw "+ti+","+str(-e.temp.offset)+"($sp)\n")
	'''
def storerv(r,v,mipsFile):

	ti = "$t"+str(r)
	#mipsFile = open("mipsFile.asm","w")
	for e in scopesList[0].entities:
		if(v == e.name and e.type == "var"):
			mipsFile.write("\tsw "+ti+","+str(-e.var.offset)+"($s0)\n")
'''
		if(v == e.name and e.type == "par" and e.par.parMode == 'cv'):
			mipsFile.write("\tsw "+ti+","+str(-e.par.offset)+"($sp)\n")
		if(v == e.name and e.type == "temp"):
			mipsFile.write("\tsw "+ti+","+str(-e.temp.offset)+"($sp)\n")
		if(v == e.name and e.type == "par" and e.par.parMode == 'ref'):
			mipsFile.write("\tlw $t0"+","+str(-e.par.offset)+"($sp)\n")
			mipsFile.write("\tsw "+ti+","+"($t0)\n")
'''

SyntaktikosAnalyths()
print("%s"%lista_tetradon)
endiamesosFile()
isodinamoFile()
pinakasSymvolon_file()
mips()