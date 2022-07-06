#!/usr/bin/python3

###################################################################################################################################################################################
#
# author: Jan Hammer, xhamme00@stud.fit.vutbr.cz; hammerjan@email.cz
#
###################################################################################################################################################################################
#
###################################################################################################################################################################################

import sys, math

import copy
from netbench.pattern_match.b_dfa import b_dfa

###################################################################################################################################################################################
#######################################       SETTING CONSTANTS                      ##############################################################################################
###################################################################################################################################################################################

MAX_CL_LEN = 5



###################################################################################################################################################################################
#######################################       GLOBAL CONSTANTS & VARIABLES           ##############################################################################################
###################################################################################################################################################################################

DEBUG = False

INT32_MAX = 2 ** 32

###################################################################################################################################################################################
#######################################      FUNCTIONS    #########################################################################################################################
################################0###################################################################################################################################################

#def hashf(CLW, size):

    #instr = CLW.CL[0] + str(CLW.root)
    #h = 0
    #for c in instr:
        #h = 37 * h + ord(c)
        #if h >= INT32_MAX:
            #h -= INT32_MAX
    #return int((h + CLW.disc) % size)

def hashf(CLW, size, parent = None):

    if parent == None:
        in_str = CLW.CL[0] + str(CLW.state.parent_state.final_index) + str(CLW.fin_state[0])
    else:
        in_str = CLW.CL[0] + str(parent) + str(CLW.fin_state[0])

    h = 0

    for c in in_str:
        h = 37 * h + ord(c)
        if h >= INT32_MAX:
            h -= INT32_MAX

    return int((h + CLW.disc) % size)


###################################################################################################################################################################################
# so far not used
#
def remove_duplicates(lst):

    lst.sort()
    length = len(lst)
    i = 0

    while i < length - 1:
        if lst[i] == lst[i + 1]:
            lst.pop(i)
            length -= 1
        else:
            i += 1

###################################################################################################################################################################################
#######################################       CLASSES             #################################################################################################################
###################################################################################################################################################################################


#######################################       CLASS CCL           #################################################################################################################
#
# representation of a content label
#
class cCL:

    def __init__(self, state):
        self.CL = []            #
        self.root = -1          # the root of the corresponding default transition tree
        self.fin_state = []     # string marking the finishing states
        self.disc = 0           # discriminators
        self.length = 0         # length of the CL without repeating characters: len('aabcb') == len ('abc') == 3
        self.state = state

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def __str__(self):
        if len(self.CL) == 0:
            return "%s,%d" % ('', self.root) #@@@
        else:
            x = list(self.CL[0])
            for i in range(0, len(x)):
                if ord(x[i]) <= 4:
                    x[i] = chr(ord(x[i]) + 97)
                else:
                    x[i] = chr(ord(x[i]) + 61)

            return ''.join(x)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def __repr__(self):
        if len(self.CL) == 0:
            return "%s,%d" % ('', self.root)
        else:
            return "%s,%d" % (repr(self.CL[0]), self.root)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def printOut(self):
        if len(self.CL) == 0:
            return "%s,%d" % ('', self.root)
        else:
            x = list(self.CL[0])
            for i in range(0, len(x)):
                if ord(x[i]) <= 4:
                    x[i] = chr(ord(x[i]) + 97)
                else:
                    x[i] = chr(ord(x[i]) + 61)

            print (''.join(x), "(%d)" % self.disc)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def __len__(self):
        return self.length

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def get_size(self):
        size = 0
        for cl in self.CL:
            size += len(cl)
        if size > 2:
            return 2
        else:
            return 1

#######################################       CLASS CTREE         #################################################################################################################
#
# representation of a spanning tree
#
class cTree:

    def __init__(self):
        self.root = None    # will point to a cNode (root of a tree)
        self.weight = 0     # wight of the tree

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def find(self, state):
        if self.root == None:
            return False
        return self.root.find(state)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def get_diameter_from_state(self, from_state):
        if self.root == None:
            return False

        tmp_state = self.root.find(from_state)
        if tmp_state == False:
            return False
        else:
            return tmp_state.get_diameter()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def get_diameter(self):
        if self.root == None:
            return 0

        return self.root.get_diameter()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def print_tree(self):
        if self.root != None:
            self.root.print_tree()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def establish_parents(self):
        self.root.establish_parents()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def add_edge(self, n1, n2, weight = 0):
        if self.root == None:
            self.root = cNode(n1)
        self.root.add_edge(n1, n2)
        self.weight += weight

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def tree_to_list(self):
        if self.root == None:
            return []
        return self.root.tree_to_list()


#######################################       CLASS CNODE         #################################################################################################################
#
# a node of a cTree
#

class cNode:
    def __init__(self, state_num):
        self.state_num = state_num      # state id
        self.others = []                # list of all neighboring states including the parent
        self.parent = None

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# finds a specific cNode, recursive
# uses parameter 'prev' to recognise the parent in the recursive call

    def find(self, state, prev = None):
        if self.state_num == state:
            return self

        for next in self.others:
            if next.state_num == prev:
                continue
            tmp = next.find(state, self.state_num)
            if tmp != False:
                return tmp
        return False

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# get tree diameter from the cNode, recursive
# uses parameter 'prev' to recognise the parent in the recursive call

    def get_diameter(self, prev = None):
        max_depth = 0
        for next in self.others:
            if next.state_num == prev:
                continue
            tmp = next.get_diameter(self.state_num)
            if tmp + 1 > max_depth:
                max_depth = tmp + 1
        return max_depth

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# prints all the tree nodes, recursive
# uses parameter 'prev' to recognise the parent in the recursive call

    def print_tree(self, prev = None):
        print (self, ' ---> ', self.others) #, '    parent: ', self.parent
        for next in self.others:
            if next.state_num != prev:
                next.print_tree(self.state_num)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def establish_parents(self, prev = None):
        self.parent = prev
        for next in self.others:
            if next != prev:
                next.establish_parents(self)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# finds the node n1 and attach n2 to it, recursive
# uses parameter 'prev' to recognise the parent in the recursive call

    def add_edge(self, n1, n2, prev = None):
        if self.state_num == n1:
            # found n1, attach n2 to it
            tmp = cNode(n2)
            self.others.append(tmp)
            tmp.others.append(self)
            return True

        for next in self.others:
            # look for n1 in all subtrees, not in the parent
            if next.state_num == prev:
                continue
            if next.add_edge(n1, n2, self.state_num):
                return True
        return False

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# listifies the tree nodes, recursive
# uses parameter 'prev' to recognise the parent in the recursive call

    def tree_to_list(self, prev = None):
        tmp = [self.state_num]
        for next in self.others:
            if next.state_num != prev:
                tmp += next.tree_to_list(self.state_num)
        return tmp

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def __str__(self):
        return "%d" % self.state_num

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def __repr__(self):
        return "%d" % self.state_num

#######################################       CLASS CSRG_EDGE     #################################################################################################################
#
# an edge of the SRG - space reduction graph
#

class cSRG_edge:
    def __init__(self, state1, state2, value = 0):
        self.state1 = state1        # vertex 1
        self.state2 = state2        # vertex 2
        self.value = value          # value of the edge

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def get_indegree(self):
        return self.state1.indegree + self.state2.indegree

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def __str__(self):
        return "S%d S%d: %d  (%d)" % (self.state1.num, self.state2.num, self.value, self.get_indegree())

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def __repr__(self):
        return "S%d S%d: %d" % (self.state1.num, self.state2.num, self.value)

#######################################       CLASS CSTATE     ####################################################################################################################
#
# state of a CDDFA
#

class cState:
    def __init__(self, num):
        self.num = num         # state number
        self.indegree = 0       # indegree - number of trensitions of the original DFA leading to the state
        self.tree = None        # tree of the spanning forest that the state belongs to
        self.CLW = cCL(self)        # content label wrapper
        self.CLs = {}           # content labels of neigboring states that I can go to
        self.final_index = 0
        self.group_index = 0
        self.size = 0
        self.CL_size_in = 0
        self.CL_size_out = 0
        self.parent_state = None

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    #def get_parent(self):
        #if self.is_root():
            #return None
        #return self.tree.find(self.num).parent

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def is_root(self):
        return self.tree == None or self.tree.root.state_num == self.num

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def get_size(self):
        size = 0
        for cl in self.CLs:
            size += self.CLs[cl].get_size()
        return size

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def get_distance_to_root(self):
        return len(self.CLW.CL)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def __str__(self):
        return "S%d" % (self.num  +1) #@@@

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def __repr__(self):
        return "S%d" % (self.num + 1)

###################################################################################################################################################################################
#######################################       CLASS CDDFA      ####################################################################################################################
###################################################################################################################################################################################
#
# content addressed delayed deterministic finite automaton
#

class cddfa(b_dfa):

    def __init__(self):
        b_dfa.__init__(self)

        self.states = []
        self.final_states = set()
        self.starting_state = None
        self.alphabet = []
        self.transitions = []

        self.roots = 0
        self.non_roots = 0

        self.states_sorted = []
        self.state_offsets = []

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def set_transition(self, from_state, symbol, to_state):
        self.transitions[len(self.alphabet) * from_state + symbol] = to_state

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def get_transition(self, from_state, symbol):
        return self.transitions[len(self.alphabet) * from_state + symbol]

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def print_transitions(self):
        for state in range(0, len(self.states)):
            for symb in range(0, len(self.alphabet)):
                print ("S%d --%c--> S%d" % (state + 1, symb, self.get_transition(state, symb) + 1))

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# space reduction graph is a list of all the edges between every pair of states
# the value of the edge is the number of common transitions that go from the two states to a same destination
#
    def _create_space_reduction_graph(self):

        space_reduct_graph = []

        # first count the indegree (transitions leading to) for every state
        for t in self.transitions:
            self.states[t].indegree += 1

        # for every two states count the number of transition (ie. the value) with the same destination
        for i in range(0, len(self.states)):
            for j in range(i + 1, len(self.states)):

                srg_edge = 0
                for s in range(0, len(self.alphabet)):
                    if self.get_transition(i, s) == self.get_transition(j, s):
                        srg_edge += 1
                # add the adge to the space reduction graph list
                if srg_edge >= len(self.alphabet) - MAX_CL_LEN:
                    space_reduct_graph.append(cSRG_edge(self.states[i], self.states[j], srg_edge))


        #sort the SRG according to ...
        space_reduct_graph.sort(key = lambda srg_edge: srg_edge.get_indegree(), reverse = True)   #... indegrees (secondary)
        space_reduct_graph.sort(key = lambda srg_edge: srg_edge.value, reverse = True)   #    the edge value (primary)

        return space_reduct_graph

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# creates spannig forest - a collection (list) of trees created from the SRG
#

    def _create_spanning_forest(self, space_reduct_graph):

        spanning_forest = []
        # proceed from the highest value edge to the lowest
        for srg_edge in space_reduct_graph:

            # if state1 and state2 aren't in any tree create new tree and insert the edge 'state1 -> state2'
            if srg_edge.state1.tree == None and srg_edge.state2.tree == None:
                srg_edge.state1.tree = srg_edge.state2.tree = cTree()
                srg_edge.state1.tree.add_edge(srg_edge.state1.num, srg_edge.state2.num, srg_edge.value)
                spanning_forest.append(srg_edge.state1.tree)

            # if both state are in a tree (same one or different) can't do anything
            elif srg_edge.state1.tree != None and srg_edge.state2.tree != None:
                pass

            # if only the state1 is in a tree then add the edge 'state1 -> state2' but only if max tree diameter is not exceeded, otherwise can't do anything
            elif srg_edge.state1.tree != None:
                if srg_edge.state1.tree.get_diameter_from_state(srg_edge.state1.num) <= 1:
                    srg_edge.state1.tree.add_edge(srg_edge.state1.num, srg_edge.state2.num, srg_edge.value)
                    srg_edge.state1.tree.root = srg_edge.state1.tree.find(srg_edge.state1.num)
                    srg_edge.state2.tree = srg_edge.state1.tree

            # only state2 is in a tree, add 'edge state2 -> state1' but check diameter
            else:
                if srg_edge.state2.tree.get_diameter_from_state(srg_edge.state2.num) <= 1:
                    srg_edge.state2.tree.add_edge(srg_edge.state2.num, srg_edge.state1.num, srg_edge.value)
                    srg_edge.state2.tree.root = srg_edge.state2.tree.find(srg_edge.state2.num)
                    srg_edge.state1.tree = srg_edge.state2.tree

        return spanning_forest

 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def _spanning_forest_reduction(self, spanning_forest, space_reduct_graph):

        total_weight = 0
        next_reduction_cycle = True

        SRG_dict = {}
        for edge in space_reduct_graph:
            SRG_dict[edge.state1.num, edge.state2.num] = edge.value

        for tree in spanning_forest:
            total_weight += tree.weight

        # iterate over the spanning forest until no change has been done
        while next_reduction_cycle:
            new_total_weight = total_weight
            spanning_forest.sort(key = lambda tree: tree.weight, reverse = True)
            next_reduction_cycle = False

            # iterate over individual trees in spanning forest
            # using a while loop, cause some trees may get removed during the iteration
            idx = 0
            spanning_forest_len = len(spanning_forest)
            while idx < spanning_forest_len:

                # get next tree
                dissolved_tree = spanning_forest[idx]

                new_edges = []
                new_total_weight -= dissolved_tree.weight

                # for every vertex of the dissolved tree, look for the highest rated edge to another tree's root
                for vertex in dissolved_tree.tree_to_list():

                    # find the edge with highest value
                    max_edge_val = 0
                    tree_to_connect = None

                    for new_tree in spanning_forest:
                        if dissolved_tree == new_tree:
                            continue

                        # every edge is only once in the dictionary and we don't know in which order - check both
                        if (vertex, new_tree.root.state_num) in SRG_dict:
                            tmp_val = SRG_dict[vertex, new_tree.root.state_num]
                        elif (new_tree.root.state_num, vertex) in SRG_dict:
                            tmp_val = SRG_dict[new_tree.root.state_num, vertex]
                        else:
                            continue

                        # collect the max value, also remember to which tree it leads
                        if tmp_val > max_edge_val:
                            max_edge_val = tmp_val
                            tree_to_connect = new_tree

                    new_total_weight += max_edge_val
                    new_edges.append((tree_to_connect, vertex, max_edge_val))

                # if the new weight is greater, save the changes
                if new_total_weight > total_weight:
                    # remove the old tree
                    spanning_forest.pop(idx)
                    spanning_forest_len -= 1

                    # add the new branches from the list to their respective trees
                    for edge in new_edges:
                        edge[0].add_edge(edge[0].root.state_num, edge[1], edge[2])
                        self.states[edge[1]].tree = edge[0]

                    total_weight = new_total_weight

                    # also mark that there will be another reduction cycle
                    next_reduction_cycle = True
                    break
                else:
                    idx += 1

        for tree in spanning_forest:
            tree.establish_parents()


 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def _generate_content_labels(self):

        root_index = 0

        for state in self.states:
            if state.is_root():
                self.roots += 1
                state.final_index = root_index
                root_index += 1

        for state in self.states:
            state.CLW.root = self.states[state.tree.root.state_num].final_index
            if not state.is_root():
                self.non_roots += 1
                state.CLW.CL.append('')
                for symbol in self.alphabet:
                    if self.get_transition(state.num, symbol) != self.get_transition(state.tree.root.state_num, symbol):
                        state.CLW.CL[0] += chr(symbol)

                state.CLW.length = len(state.CLW.CL[0])

            if state.num in self.final_states:
                state.CLW.fin_state = [1]
            else:
                state.CLW.fin_state = [0]

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def _reattach_state(self, state, dest_state):

        # state will contain the CL of its ancestor...
        state.CLW.CL = dest_state.CLW.CL[:]

        # and before that all the records of transitions that are different from the ancestor
        tmpCL = ''
        for symbol in self.alphabet:
            if self.get_transition(state.num, symbol) != self.get_transition(dest_state.num, symbol):
                tmpCL += chr(symbol)
        state.CLW.CL[0:0] = tmpCL

        # the root state is the same
        state.CLW.root = dest_state.CLW.root
        state.CLW.length = len(state.CLW.CL[0])

        state.CLW.fin_state = state.CLW.fin_state[0:1] + dest_state.CLW.fin_state[:]

        state.tree = dest_state.tree

        node = state.tree.find(state.num)
        dest_node = dest_state.tree.find(state.num)

        # @@@ is it necessary to re-generate CL_size_in/out ???

        # adjust others, parent
        node.others.remove(node.parent)
        node.parent = dest_node
        node.others.append(dest_node)

        for elem in node.others:
            if elem != node.parent:
                self.reattach_state(self.states[elem.state_num], self.states[elem.parent.state_num])

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def _spanning_forest_optimization(self):

        # count ingoing and outgoing CL sizes
        for state in self.states:
            for cl in state.CLs:
                tmp_size = state.CLs[cl].get_size()
                state.CL_size_out += tmp_size
                self.states[self.get_transition(state.num, cl)].CL_size_in += tmp_size

        next_opt_cycle = True

        while next_opt_cycle:
            # sort accordingly
            next_opt_cycle = False
            states = sorted(self.states, key = lambda s: s.CL_size_out - s.CL_size_in, reverse = True)

            for state in states:
                min_size = len(self.alphabet) + 1
                best_candidate = None

                for ancestor_candidate in self.states:
                    if state != ancestor_candidate or ancestor_candidate.get_distance_to_root() == 1:
                        size = 0
                        for symbol in self.alphabet:
                            if self.get_transition(state.num, symbol) != self.get_transition(ancestor_candidate.num, symbol):
                                size += 1
                        tmp_size = ancestor_candidate.CLW.get_size() + size + 1
                        if tmp_size < min_size:
                            min_size = tmp_size
                            best_candidate = ancestor_candidate

                if min_size < state.CLW.get_size():
                    print ('HIT!!! for state', state, ' the best root state is', best_candidate, 'with new CL size of', min_size)
                    # re-generate state's CL
                    self._reattach_state(state, best_candidate)
                    next_opt_cycle = True

        #for state in self.states:
            #print state, " out:", state.CL_size_out, " in:", state.CL_size_in


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def _assign_content_labels(self):

        for state in self.states:
            if state.is_root():
                # get all of the CLs
                for symbol in self.alphabet:
                    state_idx = self.get_transition(state.num, symbol)
                    state.CLs[symbol] = self.states[state_idx].CLW
            else:
                # get the CLs for those transitions that differ from the tree root
                for symbol in self.alphabet:
                    if self.get_transition(state.num, symbol) != self.get_transition(state.tree.root.state_num, symbol):
                        state_idx = self.get_transition(state.num, symbol)
                        state.CLs[symbol] = self.states[state_idx].CLW

        for state in self.states:
            for key in state.CLs:
                state.size += state.CLs[key].get_size()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def _get_next_candidate_label_by_permuting(self, CLW):

        CL = list(CLW.CL[0])

        hit = -1
        for i in range(len(CL) - 1, 0, -1):
            if CL[i] > CL[i - 1]:
                hit = i - 1
                break
        if hit == -1:
            return None

        idx_of_min = hit + 1

        for i in range(hit + 1, len(CL)):
            if CL[i] < CL[idx_of_min] and CL[i] > CL[hit]:
                idx_of_min = i

        CL[hit], CL[idx_of_min] = CL[idx_of_min], CL[hit]
        CL = CL[:hit + 1] + sorted(CL[hit + 1:])

        CLW.CL[0] = ''.join(CL)
        return CLW

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def _get_next_candidate_label_by_padding(self, CLW, size):

        CL = list(CLW.CL[0])
        d = {}

        for c in CL:
            if c in d:
                d[c] += 1
            else:
                d[c] = 1

        numlst = []

        keys = sorted(d)
        for e in keys:
            numlst.append(d[e])

        hit  = -1
        for i in range(len(numlst) - 2, -1, -1):
            if numlst[i] > 1:
                hit = i
                break
        try:
            if hit == -1:
                if size > len(CL):
                    numlst[0] = numlst[-1] + 1
                    if len(numlst) > 1:
                        numlst[-1] = 1
                else:
                    return None
            else:
                numlst[hit] -= 1
                numlst[hit + 1] += 1
                for i in range(hit + 2, len(numlst)):
                    if numlst[i] > 1:
                        numlst[hit + 1] += numlst[i] - 1
                        numlst[i] = 1
        except:
            print ('EXCEPTION: got CL:', CLW.CL[0], '   size:', size, 'len:', len(CLW.CL[0]))
            sys.exit(1)

        CL = []
        for i in range(0, len(numlst)):
            for j in range(0, numlst[i]):
                CL.append(keys[i])

        CLW.CL[0] = ''.join(CL)
        return CLW


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def _get_next_candidate_label_by_discriminator(self, CLW, dis_bits):

        if CLW.disc + 1 >= 2**dis_bits:
            return None
        else:
            self._get_basic_form_of_CL(CLW)
            CLW.disc += 1
            return CLW


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def _get_next_candidate_label(self, CLW, disc_bits):

        tmp = self._get_next_candidate_label_by_permuting(CLW)

        if tmp == None:
            tmp = self._get_next_candidate_label_by_padding(CLW, 5)

        if tmp == None:
            tmp = self._get_next_candidate_label_by_discriminator(CLW, disc_bits)

        return tmp

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def _get_basic_form_of_CL(self, CLW):

        CL_lst = sorted(CLW.CL[0])

        i = 0
        length = len(CL_lst)
        while i < length - 1:
            if CL_lst[i] == CL_lst[i + 1]:
                CL_lst.pop(i + 1)
                length -= 1
            else:
                i += 1

        CLW.CL[0] = ''.join(CL_lst)
        return CLW

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def _try_next_hash(self, CLW, htable, gen, dis_bits):

        if gen:
            tmpCLW = self._get_next_candidate_label(CLW, dis_bits)
            if tmpCLW == None:
                return False
            else:
                CLW = tmpCLW

        while htable[hashf(CLW, len(htable))] == 1:
            tmpCLW = self._get_next_candidate_label(CLW, dis_bits)
            if tmpCLW == None:
                return False
            else:
                CLW = tmpCLW

        htable[hashf(CLW, len(htable))] = 1
        return True

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def _prepare_hashing_for_group(self, CLWs):

        i = 0
        dis_bits = 1   # @@@ later start with 0 and increment?
        htable = [0] * len(CLWs)
        gen = False

        for CLW in CLWs:
            self._get_basic_form_of_CL(CLW)

        while i < len(CLWs):
            #for j in range(0, i):
                #print CLWs[j], '-', hashf(CLWs[j], len(htable))

            if i < 0:
                print ("NO MATCHING FOUND")
                print (htable)
                sys.exit(1)

            if self._try_next_hash(CLWs[i], htable, gen, dis_bits):
                i += 1
                gen = False
            else:
                # clean up
                self._get_basic_form_of_CL(CLWs[i])
                CLWs[i].disc = 0

                i -= 1
                gen = True

        return htable

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def _prepare_hashing_for_group_2(self, CLWs):

        disc_bits = 1
        ht_size = len(CLWs)
        hash_values = []    # list of lists of hash values for every CL
        CL_candidates = []

        for i in range(0, ht_size):
            print (i, "-", CLWs[i], "-", hashf(CLWs[i], ht_size))

        # first for every content label generate the list of candidate hash values
        for CLW in CLWs:
            CLW_hash_values = []   # list of hash values for current CL
            tmp_cand = []
            tmp = CLW
            while (tmp != None):

                hv = hashf(tmp, ht_size)
                if hv not in CLW_hash_values:
                    tmp_cand.append(copy.deepcopy(tmp))
                    CLW_hash_values.append(hv)
                tmp = self._get_next_candidate_label(tmp, disc_bits)
                #tmp.printOut()

            #remove_duplicates(CLW_hash_values)
            hash_values.append(CLW_hash_values)
            CL_candidates.append(tmp_cand)

        print ('HASH_VALUES')
        print (hash_values)
        print ()


        ht_space = [0] * ht_size        # indicates which indexes are taken
        cur_indexes = [-1] * ht_size    # which CL from hash_values list are now active
        i = 0

        while i >= 0 and i < ht_size:
            cur_indexes[i] += 1
            if cur_indexes[i] >= len(hash_values[i]):
                cur_indexes[i] = -1
                i -= 1
            elif ht_space[hash_values[i][cur_indexes[i]]] == 0:
                ht_space[hash_values[i][cur_indexes[i]]] = 1
                i += 1

        if i < 0:
            print ('NO HASHING FOUND')

        for i in range(0, ht_size):
            CLWs[i].CL = CL_candidates[i][cur_indexes[i]].CL
            CLWs[i].disc = CL_candidates[i][cur_indexes[i]].disc

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def _prepare_hashing(self):

        for state in self.states:
            if not state.is_root():
                state.parent_state = self.states[state.tree.find(state.num).parent.state_num]

        CL_groups = {}

        for state in self.states:
            if state.is_root():
                print ('state', state.num + 1, 'will not be hashed - it\'s root')
                state.group_index = 0
                continue

            elif state.size == 0:
                print ('state', state.num + 1, 'will not be hashed - zero length')
                state.group_index = 1000
                continue

            elif state.size in CL_groups:
                CL_groups[state.size].append(state.CLW)
                state.group_index = state.size
                print ('adding state', state.num + 1, 'to group', state.size)

            else:
                CL_groups[state.size] = [state.CLW]
                state.group_index = state.size
                print ('adding state', state.num + 1, 'to group', state.size)

        for group in CL_groups:
            #generate list of results for the group
            self._prepare_hashing_for_group(CL_groups[group])

        for state in self.states:
            if not state.is_root() and state.size > 0:
                state.final_index = hashf(state.CLW, len(CL_groups[state.size]))

        start_state_num = self.states[self.starting_state].num

        self.states.sort(key = lambda state: state.final_index)
        self.states.sort(key = lambda state: state.group_index)

        self.state_offsets.append(self.roots)

        for i in range(1, max(CL_groups) + 1):
            if i in CL_groups:
                self.state_offsets.append(len(CL_groups[i]) + self.state_offsets[-1])
            else:
                self.state_offsets.append(self.state_offsets[-1])

        print ('GROUP OFFSETS:')
        print (self.state_offsets)

        for i in range(0, len(self.states)):
            if self.states[i].num == start_state_num:
                self.starting_state = i
                break


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def _reduce_root_alphabet(self):

        common_transitions = {}

        for state in self.states:
            if state.is_root():
                next_states = {}
                common_trans = None
                common_trans_value = 0

                for symbol in self.alphabet:
                    dst = self.get_transition(state.num, symbol)
                    if dst in next_states:
                        next_states[dst] += 1
                    else:
                        next_states[dst] = 1

                    if next_states[dst] > common_trans_value:
                        common_trans_value = next_states[dst]
                        common_trans = dst

                common_transitions[state.num] = dst

        root_alphabet = []
        for state in self.states:
            if state.is_root():
                for symbol in self.alphabet:
                    if self.get_transition(state.num, symbol) != common_transitions[state.num] and symbol not in root_alphabet:
                        root_alphabet.append(symbol)
        print ('ROOT ALPHABET:')
        print (sorted(root_alphabet))

        return root_alphabet

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def _reduce_non_root_alphabet(self):

        non_root_alphabet = []

        for state in self.states:
            if not state.is_root():
                for key in state.CLs:
                    if key not in non_root_alphabet:
                        non_root_alphabet.append(key)

        print ('NON-ROOT ALPHABET:')
        print (sorted(non_root_alphabet))
        return non_root_alphabet

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def _optimize_content_labels(self):

        r_alphabet = self._reduce_root_alphabet()
        nr_alphabet = self._reduce_non_root_alphabet()

        for symbol in nr_alphabet:
            if symbol not in r_alphabet:
                r_alphabet.append(symbol)

        print ("REDUCED ALPHABET:")
        print (r_alphabet)
        bits_for_symbol = int(math.ceil(math.log(len(r_alphabet), 2)))
        bits_for_root = int(math.ceil(math.log(self.roots, 2)))

        print ("BITS FOR SYMBOL:", bits_for_symbol)
        print ("BITS FOR ROOT:", bits_for_root)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def _make_cddfa(self):

        if DEBUG:
            print ('STATES:')
            for state in self.states:
                print (state, ' -  ',)

            print ('\nTRANSITIONS (len = %d):' % len(self.transitions))
            print (self.transitions)

            print ('SYMBOLS:')
            print (self.alphabet)

            print ('STRARING STATE:')
            print (self.starting_state)

            print ('FINISHING STATES:')
            print (self.final_states)


        #space_reduct_graph = self._create_space_reduction_graph()

        #if DEBUG:
            #print '\n#############################################################################################'
            #print 'SRG:'
            #for srg_edge in space_reduct_graph:
                #print srg_edge
            #print '\n\n'

        #spanning_forest = self._create_spanning_forest(space_reduct_graph)
        #if DEBUG:
            #print '#############################################################################################'
            #print 'SPANNING FOREST:'
            #for tree in spanning_forest:
                #tree.print_tree()
                #print ''
            #print ''

        #self._spanning_forest_reduction(spanning_forest, space_reduct_graph)

        #if DEBUG:
            #print '#############################################################################################'
            #print 'REDUCED SPANNING FOREST:'
            #for tree in spanning_forest:
                #tree.print_tree()
                #print ''
            #print ''

        #for state in self.states:
            #print "state %d -> tree root %d" % (state.num, state.tree.root.state_num)


        #################################################
        #################################################
        #################################################
        t = cTree()
        t.add_edge(0, 1)
        t.add_edge(0, 2)
        t.add_edge(0, 3)
        for state in self.states:
            state.tree = t


        #################################################
        #################################################
        #################################################

        self._generate_content_labels()

        if DEBUG:
            print ('#############################################################################################')
            print ('CONTENT LABELS:')
            for state in self.states:
                if state.is_root():
                    print ('%s: %s' % (state , 'ROOT'))
                else:
                    print ('%s: %s' % (state, state.CLW))
            print ('\n')

        self._assign_content_labels()

        if DEBUG:
            print ('#############################################################################################')
            print ('ASSIGNED CONTENT LABELS:')
            for state in self.states:
                print (state)
                for cl in state.CLs:
                    print (' -', cl, ':', state.CLs[cl])
            print ('\n')


        self._spanning_forest_optimization()    # @@@ must find a way how to test this !!!

        self._optimize_content_labels()

        #htable = self._prepare_hashing()


        if DEBUG:
            print ('#############################################################################################')
            print ('CONTENT LABELS AFTER HASHING:')
            for state in self.states:
                if state.is_root():
                    print ('%s: %s (group index = %d, final index = %d)' % (state , 'ROOT', state.group_index, state.final_index))
                else:
                    print ('%s: %s (group index = %d, final index = %d)' % (state, state.CLW, state.group_index, state.final_index))
            print ('\n')
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def load(self, filepath):
        f = open(filepath, 'r')

        # read the list of states
        for s in f.readline().split():
            self.states.append(cState(int(s) -1))   # @@@!
        self.states.sort(key = lambda state: state.num)

        # read the lst of final states
        for fs in f.readline().split():
            self.final_states.add(int(fs))

        # read the startin state number
        self.starting_state = int(f.readline())

        # read the alphabet
        for s in f.readline().split():
            self.alphabet.append(int(s) - 1)   # @@@!
        self.alphabet.sort()

        # read and parse the transitions
        state_prev = state_next = stat = 0
        symbol = '0'

        self.transitions = [None] * (len(self.alphabet) * len(self.states))

        for t in f.readline().split():
            if stat == 0:
                state_prev = int(t) - 1   # @@@!
                stat = 1
            elif stat == 1:
                symbol = int(t)- 1   # @@@!
                stat = 2
            elif stat == 2:
                state_next = int(t) - 1  # @@@!
                self.set_transition(state_prev, symbol, state_next)
                stat = 0

        f.close()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def run(self, input_string):



        #print 'STATES (state num, final index, group index):'
        #for state in self.states:
            #print state.num + 1, " - ", state.final_index, " - ", state.group_index

        #print 'state 1:', hashf(self.states[2].CLW, 3), hashf(self.states[2].CLW, 3, 0)
        #print 'state 7:', hashf(self.states[3].CLW, 3), hashf(self.states[3].CLW, 3, 0)
        #print 'state 5:', hashf(self.states[4].CLW, 3), hashf(self.states[4].CLW, 3, 1)

        #print 'state 9:', hashf(self.states[5].CLW, 2) ,hashf(self.states[5].CLW, 2, 1)
        #print 'state 6:', hashf(self.states[6].CLW, 2), hashf(self.states[6].CLW, 2, 0)

        #print 'state 4:', hashf(self.states[7].CLW, 1), hashf(self.states[7].CLW, 1, 0)

        cur_state = self.states[self.starting_state]

        print ('\n\n\nRUN..............\n')
        #print 'offsets:', self.state_offsets


        for i in range(0, len(input_string)):
            print ('step', i + 1, ' - current state =', cur_state,)

            cur_symbol = input_string[i]
            if i + 1 >= len(input_string):
                next_symbol = -1
                print ('   current symbol =', ord(cur_symbol), '    next symbol =', -1)
            else:
                next_symbol = input_string[i + 1]
                print ('   current symbol =', ord(cur_symbol), '    next symbol =', ord(next_symbol))


            if i == 0 and ord(cur_symbol) not in cur_state.CLs:
                curCL = cur_state.CLW
            else:
                curCL = cur_state.CLs[ord(cur_symbol)]

            if next_symbol == -1:
                return curCL.fin_state[0] == 1

            symbol_in = -1
            for j in range(0, len(curCL.CL)):
                if next_symbol in curCL.CL[j]:
                    symbol_in = j
                    break

            if symbol_in == -1:
                cur_state = self.states[curCL.root]
            else:
                cur_root = curCL.root
                j = len(curCL.CL) - 1
                while j >= symbol_in:
                    s = curCL.state.get_size()
                    #print 'SIZE =', s
                    #o = cur_root
                    #print 'R', o
                    cur_root = hashf(curCL, self.state_offsets[s] - self.state_offsets[s - 1], cur_root) + self.state_offsets[s - 1]


                    #print 'CL: ', curCL, '-', curCL.state.get_size()
                    #print 'current root index', cur_root, "(", hashf(curCL, self.state_offsets[s] - self.state_offsets[s - 1], o), "+ ", self.state_offsets[s - 1], ")"


                    j -= 1
                cur_state = self.states[cur_root]

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def compute(self):
        # 1. if necessary, determinise and minimise
        # 2. read nfa data into cddfa data
        # 3. call _make_cddfa

        #print 'STATES:'
        #print self._automaton.states
        #print '-----------------------------------'

        #print 'SYMBOLS'
        #print self._automaton.alphabet
        #print '-----------------------------------'

        #print 'TRANSITIONS'
        #print self._automaton.transitions
        #print '-----------------------------------'

        # read states
        for state in self._automaton.states:
            self.states.append(cState(state))
        self.states.sort(key = lambda state: state.num)

        # read alphabet
        for symbol in self._automaton.alphabet:
            self.alphabet.append(symbol)
        self.alphabet.sort()

        # read starting state
        self.starting_state = self._automaton.start

        # read final statess
        for state in self._automaton.final:
            self.final_states.add(state)

        # read transitions
        self.transitions = [self.starting_state] * (len(self.alphabet) * len(self.states))

        for transition in self._automaton.transitions:
            self.set_transition(transition[0], transition[1], transition[2])

        self._make_cddfa()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def SaveToFile(self, FileName):

        fout = open(FileName, 'w')

        #<NUMBER_OF_ROOT_STATES> <NUMBER_OF_NON_ROOT_STATES> <NUMBER_OF_SYMBOLS> <SIZE_OF_CL> <CLS_IN_NON_ROOT_STATE>
        fout.write("%d %d %d %d %d\n" % (self.roots, self.non_roots, len(self.alphabet), 8, 5))

        if DEBUG:
            print ('#############################################################################################')
            print ('OUTPUT:')

        for state in self.states:
            if state.is_root():
                if DEBUG:
                    print ('------------------------------------ R' + str(state.num + 1))
                for symbol in self.alphabet:
                    fout.write("%s,%d %s %d\n" % (state.CLs[symbol].CL, state.CLs[symbol].root, state.CLs[symbol].fin_state, state.CLs[symbol].disc))
                    if DEBUG:
                        print ("%s,%d %s %d" % (state.CLs[symbol].CL, state.CLs[symbol].root, state.CLs[symbol].fin_state, state.CLs[symbol].disc))

        for state in self.states:
            if not state.is_root():
                if DEBUG:
                    print ('------------------------------------ ' + str(state.num + 1))
                states = 0
                for key in sorted(state.CLs):
                    fout.write("%s,%d %s %d\n" % (state.CLs[key].CL, state.CLs[key].root, state.CLs[key].fin_state, state.CLs[key].disc))
                    states += 1
                    if DEBUG:
                        print ("%d:  %s,%d %s %d" % (key, state.CLs[key].CL, state.CLs[key].root, state.CLs[key].fin_state, state.CLs[key].disc))

        fout.close()

###################################################################################################################################################################################

#DEBUG=1

#my_cddfa = cddfa()
#my_cddfa.load('input')
#my_cddfa._make_cddfa()
#            'dddabaccdd' = '\x03\x03\x03\x00\x01\x00\x02\x02\x03\x03'
#accepted = my_cddfa.run('\x03\x03\x03\x00\x01\x00\x02\x02\x03\x03')

#print 'RESULT:', accepted
#my_cddfa.SaveToFile('my_cddfa')

