import json

ast = open('nerv.json')   #To open the json file
data = json.load(ast)
ast.close()
data1 = data['members']

def input_ports():     #Input ports identification function
  for val in data1:
     if "Instance" == val['kind']:
        val1 = val['body']
        for key in val1['members']:
            if "Port" == key['kind'] and "In" == key['direction']:
                 print(key['name'])




def always_block():      #Always, AlwaysFF and AlwaysComb block identification and counting function
    n_ab_ff = 0
    n_ab_comb = 0
    n_ab = 0
    for val in data1:
        if "Instance" == val['kind']:
            val1 = val['body']
            for key in val1['members']:
                if "ProceduralBlock" == key['kind'] and "AlwaysFF" == key['procedureKind']:
                    n_ab_ff += 1
                elif "ProceduralBlock" == key['kind'] and "AlwaysComb" == key['procedureKind']:
                    n_ab_comb += 1
                elif "ProceduralBlock" == key['kind'] and "Always" == key['procedureKind']:
                    n_ab += 1
    print("Total Number of AlwaysFF Blocks: ")
    print(n_ab_ff)
    print("Total Number of AlwaysComb Blocks: ")
    print(n_ab_comb)
    print("Total Number of Always Blocks: ")
    print(n_ab)




def output_ports():      #Output ports identification function
  for val in data1:
     if "Instance" == val['kind']:
        val1 = val['body']
        for key in val1['members']:
            if "Port" == key['kind'] and "Out" == key['direction']:
                 print(key['name'])


def module_name(kind):      #This function for detecting the module name.
    for keyval in data['members']:
        if kind == keyval['kind']:
            return keyval['name']




def main():
    print("The Module Name is:", module_name("Instance"))
    print("\n")
    print("The following are the Input Ports:")
    input_ports()
    print("\n")
    print("The following are the Output Ports:")
    output_ports()
    print("\n")
    always_block()


main()