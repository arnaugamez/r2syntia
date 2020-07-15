import sys
import r2pipe

from z3 import simplify
from syntia.mcts.game import Game, Variable
from syntia.mcts.grammar import Grammar
from syntia.mcts.mcts import *
from syntia.utils.paralleliser import Paralleliser
from syntia.mcts.utils import *


# Open pipe with radare2 shell session
r2 = r2pipe.open()


# Define global constants
BITSIZE = int(sys.argv[1])
MAX_UNSIGNED = 2 ** BITSIZE
STRT = sys.argv[2]
FINI = sys.argv[3]
VARS_IN = [sys.argv[i] for i in range(4, len(sys.argv)-1)]
NUM_OF_VARIABLES = len(VARS_IN)
VAR_OUT = sys.argv[-1]

NUM_IO_PAIRS = 50
VERBOSITY = 2 # 0, 1, 2


# Print general information
if VERBOSITY > 0:
    print ("[*] General information")
    print ("---")
    print ("Bit size: " + str(BITSIZE))
    print ("Start at offset: " + STRT)
    print ("Finish at offset: " + FINI)
    print ("Inputs: " + ', '.join(VARS_IN))
    print ("Output: " + VAR_OUT)
    print ("===\n")


# Create I/O mapping to store I/O pairs
in_out_map = {}


# Initialize ESIL VM state and VM stack.
r2.cmd("aeim")


# Generate I/O pairs with ESIL emulation
print ("[*] Generate I/O pairs")

if VERBOSITY > 0:
    print ("---")

INPUTS = get_random_inputs(NUM_OF_VARIABLES, NUM_IO_PAIRS)
for i in range(NUM_IO_PAIRS):
    in_vect = tuple(INPUTS[i])

    r2.cmd("s " + STRT)
    r2.cmd("aeim")

    for j in range(NUM_OF_VARIABLES):
        var = VARS_IN[j]

        # Memory location
        if var[0] == '[': r2.cmd("ae " + str(in_vect[j]) + ",`?v " + var[1:-1] + "`,=[]")
        
        # Register
        else: r2.cmd("aer " + var + "=" + str(in_vect[j]))

    r2.cmd("aesu " + FINI)

    # Memory location output
    if VAR_OUT[0] == '[':
        in_out_map[in_vect] = int(r2.cmd("pf N8 @ " + VAR_OUT[1:-1] + "~[1]")[:-1])
    
    # Register output
    else:
        in_out_map[in_vect] = int(r2.cmd("aer " + VAR_OUT)[:-1], 16)

    if VERBOSITY > 0:
        print ("#{:02d}".format(i+1)+" |", in_vect, "->", in_out_map[in_vect])

if VERBOSITY > 0:
    print ("===\n")


# Create list of variables with size
variables = []
for var_index in range(NUM_OF_VARIABLES):
    v = Variable(VARS_IN[var_index], BITSIZE)
    variables.append(v)


# Generate context-free grammar and obtain its information
print ("[*] Create Context-free grammar")

grammar = Grammar(variables, bitsize=BITSIZE)
gd = grammar.dump()
terminals = gd['terminals']
terminals += [get_operator_symbol(op) for op in gd['op2']]
terminals += [get_operator_symbol(op) for op in gd['op1']]
non_terminals = gd['non_terminals']
rules = []
for sz in grammar.bit_sizes: rules += gd['u{}_rules'.format(sz)]


# Print context-free grammar information
if VERBOSITY > 0:
    print ("---")
    print ("Non-terminals (variables): { " + ', '.join(non_terminals) + " }")
    print ("Terminals: { " + ", ".join(terminals) + " }")
    print ("Production rules (RPN):")


    # This is super hacky; just to display prettier info about the grammar
    for r in rules:
        infix = ""
        rs = r.split(" ")
        if rs[0] in map(str, grammar.bit_sizes):
            infix = "\t≡ {:12} {}".format(rpn_to_infix(r), "[infix]")
            rs[-1] = get_operator_symbol(rs[-1])
            rs = rs[1:]
            r = ' '.join(rs)

        print ("{:>5} -> {:10} {:10}".format("u" + str(BITSIZE), r, infix))

    print ("Start variable: " + "u{}".format(BITSIZE)) # From game's initial move
    print ("===\n")


# Define the I/O oracle
def oracle(args):
    return in_out_map[tuple(args)]


# Main synthesis task
def synthesise(command, result, index):
    ret = ""

    max_iter = command[0]
    uct_scalar = command[1]
    game = command[2]
    oracle = command[3]
    synthesis_inputs = command[4]

    mc = MCTS(game, oracle, synthesis_inputs, uct_scalar=uct_scalar)
    mc.verbosity_level = VERBOSITY
    s = State(game, BITSIZE)

    mc.search(s, max_iter, max_time=120) # Timeout at 120 seconds

    if mc.final_expression:
        if VERBOSITY > 0:
            print("===\n")

        print("[*] Final expression found (w/ reward: 1.0)\n---")
        ret = rpn_to_infix(mc.final_expression)
        print("{} ({} iterations)".format(rpn_to_infix(mc.final_expression), mc.current_iter))
        try:
            print("{} (simplified)".format(simplify(game.to_z3(mc.final_expression))))
        except:
            pass

    result[index] = ret


# Create game and required variables for synthesis
game = Game(grammar, variables, bitsize=BITSIZE)
max_iter = 50000
uct_scalar = 1.5
task_groups = []
workers = []
commands = []

for index in range(4):
    task_group = "TG"
    task_groups.append(task_group)

    synthesis_inputs = [list(k) for k in in_out_map]
    command = [max_iter, uct_scalar, game, oracle, synthesis_inputs]

    workers.append(synthesise)
    commands.append(command)

number_of_tasks = len(commands)


# Start main synthesis
print ("[*] Start main synthesis")

if VERBOSITY > 0:
    print ("---")

paralleliser = Paralleliser(commands, workers, number_of_tasks, task_groups)
start_time = time()
paralleliser.execute()
end_time = time()

print("===\n")
print("[*] Synthesis finished in {} seconds".format(end_time - start_time))