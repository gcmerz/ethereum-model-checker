# translate opcodes.py
# translates opcodes in to CSP# language
# input: a file containing a list of newline seperated opcodes
# output: a CSP# prorgram representation in the file newfile.csp

import argparse
from collections import OrderedDict as odict
from collections import deque

def generate_jump_proc(program_len):
	# we have to handle jumps within CSP# to avoid executing 
	# the EVM code in python (a nightmare!)
	# in order to do this, we create a process called JUMP_PROC
	# which takes in as an argument the most recent item on the CSP# stack
	# it only jumps to the process labeled with that number by guarding the 
	# processes
	jump_str = 'JUMP_PROC(JUMP_ARG) ='
	for i in xrange(program_len - 1):
		jump_str += '[JUMP_ARG ==' + str(i) + ']P' + str(i) + '() []\n'
	jump_str += '[JUMP_ARG ==' + str(i + 1) + ']P' + str(i + 1) + '();'
	return jump_str

def add_command(program_str, command, program_ctr):
	# add a command to our program
	program_str['P' + str(program_ctr) + '()'] = command + '; P' + str(program_ctr + 1) + '();'
	program_ctr += 1
	return program_str, program_ctr

def handle_push(line, program_str, program_ctr):
	# handle push commands (need to parse the arguments)
	args = line.split(' ')
	push_arg = args[1]
	push_arg = int(push_arg, 16)
	command = 'PUSH(' + str(push_arg) + ')'
	program_str, program_ctr = add_command(program_str, command, program_ctr)
	return program_str, program_ctr

def handle_dupswap(line, program_str, program_ctr, command_arg):
	# handle dups + swaps
	dupswap_num = line[len(command_arg):]
	command = command_arg + '(' + dupswap_num + ')'
	program_str, program_ctr = add_command(program_str,command, program_ctr)
	return program_str, program_ctr

def handle_jump(line, program_str, program_ctr):
	# jumpdest has no effect on program state + right now we don't track valid jump
	# destinations (whoops)
	if 'JUMDEST' in line:
		return
	else:
		# can't use regular "add_command" here b/c would cause off by one error in program counter
		if 'JUMPI' in line:
			new_command = '[stack[stack_pos - 2] == 1]JUMP_PROC(stack[stack_pos - 1]) [] P' + str(program_ctr + 1) + '();'
			program_str['P' + str(program_ctr) + '()'] = new_command
			program_ctr += 1
		else:
			new_command = 'JUMP_PROC(stack[stack_pos - 1]);'
			program_str['P' + str(program_ctr) + '()'] = new_command
			program_ctr += 1
	return program_str, program_ctr



if __name__ == '__main__':

	# argument parsing
	parser = argparse.ArgumentParser(description="Translate Ethereum Opcodes to CSP# for Model Checking")
	parser.add_argument('opcode_file', metavar = 'f', type=str, 
		help = 'a file containing ethereum opcodes as formatted on etherscan')
	args = vars(parser.parse_args())
	
	# check if we parsed correctly + try to open the file
	if 'opcode_file' in args:
		try:
			program_str = odict()
			program_ctr = 0
			with open(args['opcode_file']) as f:
				for line in f:
					line = line.strip()
					if 'PUSH' in line:
						program_str, program_ctr = handle_push(line, program_str, program_ctr)
					elif 'SWAP' in line:
						program_str, program_ctr = handle_dupswap(line, program_str, program_ctr, 'SWAP')
					elif 'DUP' in line:
						program_str, program_ctr = handle_dupswap(line, program_str, program_ctr, 'DUP')
					elif 'JUMP' in line:
						program_str, program_ctr = handle_jump(line, program_str, program_ctr)
					else:
						command = line + "()"
						program_str, program_ctr = add_command(program_str, command, program_ctr)
			with open("newfile.csp", "w") as f:
				for k,v in program_str.iteritems():
					f.write(k + '=' + v + '\n')
				fstr = generate_jump_proc(program_ctr)
				f.write(fstr)
		except:
			print "ERROR"




