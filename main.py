import json
ast = open('nerv.json')   #To open the json file
data = json.load(ast)
print(type(data))
data1 = data['members']

def input_ports():     #Input ports identification function
  for val in data1:
     if "Instance" == val['kind']:
        val1 = val['body']
        for key in val1['members']:
            if "Port" == key['kind'] and "In" == key['direction']:
                 print(key['name'])


print("The following are the Input Ports:")
input_ports()

def output_ports():      #Output ports identification function
  for val in data1:
     if "Instance" == val['kind']:
        val1 = val['body']
        for key in val1['members']:
            if "Port" == key['kind'] and "Out" == key['direction']:
                 print(key['name'])


print("The following are the Output Ports:")
output_ports()

def module_name(kind):      #This function for detecting the module name.
    for keyval in data['members']:
        if kind == keyval['kind']:
            return keyval['name']

if module_name("Instance") != "":

    print("The Module Name is:", module_name("Instance"))
else:
    print("No Module Name has been found!")



ast.close()