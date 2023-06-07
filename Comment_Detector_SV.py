
n_Comment = 0  #Total number of comments
n_Line = 0 #Total number of lines

def comment_lines_in_SV(filename):
    comment_lines = []  #List to add the number of comment lines
    global n_Comment, n_Line
    mls = 0  #Multi-line Comments Start Line 
    mle = 0	 #Multi-line Comments End Line
    with open(filename, encoding="utf8") as file:  #SystemVerilog is a UTF8 encoded file
        lines = file.readlines()
        for i, line in enumerate(lines, start=1):
            line = line.strip()
            n_Line += 1
            if line.rfind('//') != -1:
                n_Comment += 1
                comment_lines.append(i)
            elif line.rfind('/*') != -1:
                mls= i
                print(mls)
            elif line.rfind('*/') != -1:
                mle = i
                print(mle)
                for x in range(mls,mle+1):
                    n_Comment += 1
                    comment_lines.append(x)

    return comment_lines


filename = 'aes_core.sv'  #Specify the SystemVerilog Source File Here
comment_lines = comment_lines_in_SV(filename)
print(f"Total Number of Lines = {n_Line}")
print(f"Total Number of Comements = {n_Comment}")
print(f"Comment lines in {filename}: {comment_lines}")
