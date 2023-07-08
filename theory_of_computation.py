from collections import deque
class NFA:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states
def epsilon_closure(nfa, states):
    closure = set(states)
    queue = deque(states)
    while queue:
        current_state = queue.popleft()
        if current_state in nfa.transitions and '$' in nfa.transitions[current_state]:
            epsilon_transitions = nfa.transitions[current_state]['$']
            for state in epsilon_transitions:
                if state not in closure:
                    closure.add(state)
                    queue.append(state)
    return frozenset(closure)
def move(nfa, states, symbol):
    moves = set()
    for state in states:
        if state in nfa.transitions and symbol in nfa.transitions[state]:
            moves.update(nfa.transitions[state][symbol])
    return frozenset(moves)
def nfa_to_dfa(nfa):
    dfa_states = []
    dfa_transitions = {}
    dfa_start_state = epsilon_closure(nfa, [nfa.start_state])
    dfa_accept_states = []
    unmarked_states = [dfa_start_state]
    while unmarked_states:
        current_state = unmarked_states.pop(0)
        dfa_states.append(current_state)
        if any(state in nfa.accept_states for state in current_state):
            dfa_accept_states.append(current_state)
        for symbol in nfa.alphabet:
            next_state = epsilon_closure(nfa, move(nfa, current_state, symbol))
            if next_state not in dfa_states:
                unmarked_states.append(next_state)
            if current_state not in dfa_transitions:
                dfa_transitions[current_state] = {}
            if symbol not in dfa_transitions[current_state]:
                dfa_transitions[current_state][symbol] = next_state
    return NFA(dfa_states, nfa.alphabet, dfa_transitions, dfa_start_state, dfa_accept_states)
def change_format_of_DFA(dfa):
    temp = set()
    for i in range(len(dfa.states)):
        temp.add(dfa.states[i])
    dfa.states = temp
    temp1 = set()
    for i in range(len(dfa.accept_states)):
        temp1.add(dfa.accept_states[i])
    dfa.accept_states = temp1
    return dfa
def accept_string(dfa, input_string):
    current_state = dfa.start_state
    for symbol in input_string:
        if current_state not in dfa.transitions or symbol not in dfa.transitions[current_state]:
            return False
        current_state = dfa.transitions[current_state][symbol]
    if current_state in dfa.accept_states:
        return True
    return False
def get_nfa():
    nfa = NFA(
        states=set(),
        alphabet=set(),
        transitions=dict(),
        start_state=str(),
        accept_states=set()
    )
    temp = input()
    q = temp.split(' ')[0]
    s = temp.split(' ')[1]
    a = temp.split(' ')[2]
    m = temp.split(' ')[3]
    global n
    n = int(temp.split(' ')[4])
    for i in range(int(q)):
        nfa.states.add('q' + str(i))
    for i in range(int(s)):
        temp = input()
        nfa.alphabet.add(str(temp))
    temp = input()
    nfa.start_state = 'q' + str(temp)
    for i in range(int(a)):
        temp = input()
        nfa.accept_states.add('q' + str(temp))
    for i in range(int(m)):
        temp = input().split(' ')
        if str('q' + str(temp[0])) not in nfa.transitions.keys():
            nfa.transitions['q' + str(temp[0])] = dict()
            x = nfa.transitions['q' + str(temp[0])]
            x[str(temp[1])] = set()
            x[str(temp[1])].add(str('q' + str(temp[2])))
        else:
            x = nfa.transitions['q' + str(temp[0])]
            if str(temp[1]) in x.keys():
                x[str(temp[1])].add(str('q' + str(temp[2])))
            if str(temp[1]) not in x.keys():
                x[str(temp[1])] = set()
                x[str(temp[1])].add(str('q' + str(temp[2])))
    return nfa
#----------------------start program----------------------
strings_List = list()
nfa = get_nfa()
for i in range(n):
    strings_List.append(str(input()))
print("DFA states:", nfa.states)
print("DFA alphabet:", nfa.alphabet)
print("DFA transitions:", nfa.transitions)
print("DFA start state:", nfa.start_state)
print("DFA accept states:", nfa.accept_states)
print("---------------------------------------")
dfa0 = nfa_to_dfa(nfa)
print("DFA states:", dfa0.states)
print("DFA alphabet:", dfa0.alphabet)
print("DFA transitions:", dfa0.transitions)
print("DFA start state:", dfa0.start_state)
print("DFA accept states:", dfa0.accept_states)
print("---------------------------------------")
#----------------------end of part 1----------------------
dfa = change_format_of_DFA(dfa0)
print("DFA states:", dfa0.states)
print("DFA alphabet:", dfa0.alphabet)
print("DFA transitions:", dfa0.transitions)
print("DFA start state:", dfa0.start_state)
print("DFA accept states:", dfa0.accept_states)
print("---------------------------------------")
for i in range(len(strings_List)):
    input_string = strings_List[i]
    # if input_string == '$':
    #     print("YES")
    #     continue
    result = accept_string(dfa, input_string)
    if result:
        print("YES")
    else:
        print("NO")
# #----------------------end of part 2----------------------
"""
5 2 1 6 2
a
b
0
4
0 a 1
1 a 0
0 b 4
0 a 2
2 a 3
3 b 0
aaa
aab
"""
"""
NO
YES
YES
YES
NO
YES
NO

"""

"""
7 2 2 10 7
a
b
0
1
5
0 a 0
0 $ 1
0 $ 4
1 a 2
2 b 3
3 b 1
4 b 4
4 $ 5
5 b 6
6 a 5
$
aaa
aaab
abb
abbab
abbaba
abbc
"""