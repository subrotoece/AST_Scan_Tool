import json
ast = open('i2c_core.json')   #To open the json file
data = json.load(ast)
ast.close()

n_ab_ff = 0
n_ab_comb = 0
n_ab = 0
n_case = 0
n_d_case = 0
error_d_case = 0
n_assign = 0
n_if_block = 0


def always_block(json_data, key):
    global n_ab
    global n_ab_ff
    global n_ab_comb
    if isinstance(json_data, dict):
        for k, v in json_data.items():
            if k == key:
                if v == "Always":
                    n_ab +=1
                elif v == "AlwaysFF":
                    n_ab_ff +=1
                elif v == "AlwaysComb":
                    n_ab_comb +=1

            else:
                always_block(v, key)
    elif isinstance(json_data, list):
        for item in json_data:
            always_block(item, key)


def case_block(json_data, key, value):
    global n_case
    if isinstance(json_data, dict):
        for k, v in json_data.items():
            if k == key and v == value:
                n_case +=1

            else:
                case_block(v, key, value)
    elif isinstance(json_data, list):
        for item in json_data:
            case_block(item, key, value)


def dcase_block(json_data, key):
    global n_d_case
    global error_d_case
    if isinstance(json_data, dict):
        for k, v in json_data.items():
            if k == key:
                n_d_case += 1

                for n, m in v.items():
                    if n == "kind" and m == "Empty":
                        error_d_case += 1
                        #n_d_case += 1
                    #elif n == "kind" and m == "ExpressionStatement":
                        
            else:
                dcase_block(v, key)
    elif isinstance(json_data, list):
        for item in json_data:
            dcase_block(item, key)
            
            
            
def assignment_statement(json_data, key):
    global n_assign

    if isinstance(json_data, dict):
        for k, v in json_data.items():
            if k == key:
                if v == "Assignment":
                    n_assign += 1


            else:
                assignment_statement(v, key)
    elif isinstance(json_data, list):
        for item in json_data:
            assignment_statement(item, key)
            
            
def if_block(json_data, key):
    global n_if_block

    if isinstance(json_data, dict):
        for k, v in json_data.items():
            if k == key:
                if v == "Conditional":
                    n_if_block += 1


            else:
                if_block(v, key)
    elif isinstance(json_data, list):
        for item in json_data:
            if_block(item, key)
            
            

if_block(data, "kind")
print("Total Number of If-Else Block: ")
print(n_if_block)
assignment_statement(data, "kind")
print("Total Number of Assignment Statement: ")
print(n_assign)
always_block(data, "procedureKind")
print("Total Number of AlwaysFF Blocks: ")
print(n_ab_ff)
print("Total Number of AlwaysComb Blocks: ")
print(n_ab_comb)
print("Total Number of Always Blocks: ")
print(n_ab)
case_block(data, "kind", "Case")
dcase_block(data, "defaultCase")
print("------------------------------------------------")
print("Total Number of Case Blocks: ")
print(n_case)
if(n_case>n_d_case) or error_d_case>0:
    missing_d_case = n_case - n_d_case
    print("_____________________WARNING____________________")
    if missing_d_case >0:
        print("Default Case missing in "+str(missing_d_case)+" Case Block/Blocks")
    elif error_d_case>0:
        print("Default Case is empty in "+str(error_d_case)+" Case Block/Blocks")