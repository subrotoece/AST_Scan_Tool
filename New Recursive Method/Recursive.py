import json
import sys

# approach
# 1. get output ports
#   1a. add to adj list
#   1b. add to queue
# 2. for each node in queue
#   2a. search for assignment where lhs contains node
#   2b. add rhs of assignment to adj list[node]
#   2c. add nodes from rhs to queue
#   2b. add siblings of node, if any, to adj list
#   2c. add rhs of assignment to adj list[sibling]
#   2d. add siblings, if any, to queue


def addToGraph(assignment, node, nets):
    if 'symbol' in node.keys() and node['symbol'] in nets.keys():
        nets[node['symbol']].append(assignment)

def checkNetDeps(ast, node, nets):
    # check if we have found a potential dependency
    if 'kind' in node.keys() and node['kind'] == 'NamedValue':
        addToGraph(ast, node, nets)
    
    # traverse recursively
    if 'right' in node.keys():
        checkNetDeps(ast, node['right'], nets)
    if 'left' in node.keys():
        checkNetDeps(ast, node['left'], nets)            
    if 'operand' in node.keys():
        checkNetDeps(ast, node['operand'], nets)
        
# BFS algorithm to traverse tree
def parseAST(ast, nets):
    pretty(ast)
    print('*' * 10)
    
    
    # check kind
    if 'kind' in ast.keys():
        # add nets to graph
        if ast['kind'] == 'Net' or ast['kind'] == 'Variable':
            nets[str(ast['addr']) + " " + ast['name']] = []
        
        # add assignments as dependecies
        elif ast['kind'] == "Assignment":
            checkNetDeps(ast['left'], ast['right'], nets)
    
    # recursive traversal
    if 'members' in ast.keys():
        for member in ast['members']:
            parseAST(member, nets)    
    if 'list' in ast.keys():
        for member in ast['list']:
            parseAST(member, nets)
    if 'body' in ast.keys():
        parseAST(ast['body'], nets)
    if 'expr' in ast.keys():
        parseAST(ast['expr'], nets)
    if 'assignment' in ast.keys():
        parseAST(ast['assignment'], nets)
    if 'stmt' in ast.keys():
        parseAST(ast['stmt'], nets)
            
def pretty(d, indent=0):
    for key, value in d.items():
        print('\t' * indent + str(key))
        if isinstance(value, dict):
            pretty(value, indent+1)
        else:
            print('\t' * (indent+1) + str(value))
         
def main():
    # open ast json file
    # TODO: update to ArgParser
    f = open('ast.json')
    ast = json.load(f)
    f.close()
    
    # redirect to file for dev/debug
    orig_stdout = sys.stdout
    f = open('out.json', 'w')
    sys.stdout = f
    nets = {}
    # pretty(ast)
    parseAST(ast, nets)
    print(nets)
    # for net in nets:
    #     print(net)
    #     print('*' * 10)
    sys.stdout = orig_stdout
    f.close()
    
if __name__=="__main__":
    main()
    
#f.close()
