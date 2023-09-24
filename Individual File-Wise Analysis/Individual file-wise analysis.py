import csv
import re
import os
import statistics
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

iteration = 0
#Function to find the most frequent item from a list.
#We used this function to find out the most common comment length by word count
def most_frequent(List):
    return max(set(List), key = List.count)



#The following function detects the comments, code, comments length in words, remove empty line from the code, etc.
def comment_lines_in_SV(filename):
    n_comment = 0  #Total number of comments
    n_line = 0 #Total number of lines
    n_io = 0 #Number of Input/Output
    n_is = 0 #Number of Internal Signals
    n_code = 0 #Total number of code line
    n_inline_comment = 0 #Total number of inline comments
    n_section_comment = 0 #Total number of sectioncomments
    n_copyright_comment = 0 #Total number of copyright comments
    comment_density = 0.0 #The ratio of total comment lines and code lines in the project
    len_comments = [] #Length of comments by word
    n_file = 0 #Total number of Verilog/SystemVerilog files in the directory
    n_if_else = 0 #Total number of if-else blocks in the project
    n_always = 0 #Total number of always blocks in the project
    n_always_ff = 0 #Total number of always_ff blocks in the project
    n_always_comb = 0 #Total number of always_comb blocks in the project
    n_case = 0 #Total number of case blocks in the project
    n_code_comment_match = 0 #Total number of code comment keyword matching in the project
    module_start_number = 0   #variable to count the first line number after copyright comments
    count = 0 #To count comma in I/O declaration line, specially for verilog
    data = []
    global iteration
    with open(filename, encoding="utf8") as file:  #SystemVerilog is a UTF8 encoded file
        lines = file.readlines()
        
        for i, line in enumerate(lines, start=1):
            line = line.strip()
            if line.startswith("//"):  #To find the comment at the beginning of the Verilog/SV file
                n_copyright_comment += 1
            elif line.startswith("module"): #To detect the end of copyright comment
                module_start_number = i
                break
        
        for i, line in enumerate(lines, start= 1):
            line = line.strip()
            
            if i >= module_start_number: #To identify other comment except copyright comment
                if line.rfind('//') != -1 and not line.startswith("//--" or "////"):
                    
                    n_comment += 1
                    extra_t, comments_t = line.split('//', 1)  # Split the line at the first occurrence of '//', to separate the comment part from the code. 
                    comments_t = comments_t.strip()
                    words = re.findall(r'\w+', comments_t.lower()) #Word identification in the comment
                    number_words = len(words) #Word count in the line
                    if number_words > 0:
                        len_comments.append(number_words) #Adding the counter value to len_comments list
                    
                    if line.startswith('//'):
                        n_section_comment += 1  #Section comment counting
                    else:
                        n_inline_comment += 1 #Inline comment counting
                        
        for i, line in enumerate(lines, start= 1): #To remove empty line from the code to identify the exact number of code lines 
            line = line.strip()
            if line:
                n_line += 1 #Total number of lines counting except the empty line
        
        for i, line in enumerate(lines, start=1):
            line = line.strip()
            if line.startswith("if (") or line.startswith("if("):  #To find the if_else blocks in Verilog/SV file
                n_if_else += 1
            elif line.startswith("always @(") or line.startswith("always @ ("): #To find the always blocks in Verilog file
                n_always += 1
            elif line.startswith("always_ff @(") or line.startswith("always_ff @ ("): #To find the always_ff blocks in SystemVerilog file
                n_always_ff += 1
            elif line.startswith("always_comb"): #To find the always_comb blocks in SystemVerilog file
                n_always_comb += 1 
            elif line.startswith("case (") or line.startswith("case(") or line.startswith("unique case(") or line.startswith("unique case (") : #To find the case blocks in Verilog/SystemVerilog file
                n_case += 1
            
            
            
        for i, line in enumerate(lines, start=1):
            line = line.strip()
            if line.startswith("input") or line.startswith("output"):
                count= 0
                if line.endswith(';'):
                    for char in line:
                        if char == ',':
                            count += 1
                    n_io += (count+1)
                elif line.endswith(','):
                    n_io += 1
                
            elif 'input' in line and not line.startswith('input'):
                if not line.startswith('//'):
                    n_io += 1
                elif line.startswith(','):
                    n_io += 1
            elif 'output' in line and not line.startswith('output'):
                if not line.startswith('//'):
                    n_io += 1
                elif line.startswith(','):
                    n_io += 1
            elif line.startswith("logic") or line.startswith("reg") or line.startswith("wire"):
                count= 0
                for char in line:
                    if char == ',':
                        count += 1
                n_is += (count+1) 
        
        
                
        data.append((filename, n_line, n_io, n_is, n_comment, n_code, n_copyright_comment, n_section_comment, n_inline_comment, n_if_else, n_always, n_always_ff, n_always_comb, n_case))
        if iteration == 0:        
            final_csv(final_csv_path, data)
        else:
            final_csv2(final_csv_path, data)



            
            
            
#Export analysis results to a CSV file
def final_csv(file_path, results):


        with open(file_path, "a", newline="") as file: #To create CSV file
            writer = csv.writer(file)
            writer.writerow(['File', 'Total Lines', 'Total IO', 'Total IS', 'Total Comment', 'Total Code', 'Copyright Comment', 'Functional Comment', 'In-line Comment', 'If_Else', 'Always', 'Always_FF', 'Always_Comb', 'Case']) #Columns heading
            writer.writerows(results) #Data updating to CSV from results
            file.close()
            #print(f"CSV file '{csv_file_name}' created.") #A confirmation message that CSV generated successfully
            
            
#Export analysis results to a CSV file
def final_csv2(file_path, results):


        with open(file_path, "a", newline="") as file: #To create CSV file
            writer = csv.writer(file)
            #writer.writerow(['Total Lines', 'Total Comment', 'Total Code', 'Copyright Comment', 'Functional Comment', 'In-line Comment', 'If_Else', 'Always', 'Always_FF', 'Always_Comb', 'Case']) #Columns heading
            writer.writerows(results) #Data updating to CSV from results
            file.close()
            #print(f"CSV file '{csv_file_name}' created.") #A confirmation message that CSV generated successfully
            

#To analyze the verilog/SV files. This function will call all the required function we created before
def analyze_comments(directory):
    global iteration
    
    # Iterate through all Python files in the directory
    for root, _, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith(".sv") or file_name.endswith(".v"): #To find all the verilog/SV files in the directory
                file_path = os.path.join(root, file_name) #To ad the file name to the path
                comment_lines_in_SV(file_path) #comment_lines_in_SV function is called here
                iteration += 1

                

    
                


#To get the Directory path of a Project
path = input(r"Enter the Project Path Here: ")
final_csv_path = r'C:\Users\Subroto\Desktop\Code_Comment Analysis Report\Latest Analysis\Peripherals\Result.csv' #CSV File Path, change the directory after the r
analyze_comments(path) #analyze_comments function is called here



