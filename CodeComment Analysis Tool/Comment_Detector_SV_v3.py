import csv
import re
import os
import statistics
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

n_comment = 0  #Total number of comments
n_line = 0 #Total number of lines
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
data = []
#Function to find the most frequent item from a list.
#We used this function to find out the most common comment length by word count
def most_frequent(List):
    return max(set(List), key = List.count)



#The following function detects the comments, code, comments length in words, remove empty line from the code, etc.
def comment_lines_in_SV(filename):
    global n_comment, n_line, n_inline_comment, n_section_comment, n_copyright_comment, n_if_else, n_always, n_always_ff, n_always_comb, n_case
    global len_comments
    module_start_number = 0   #variable to count the first line number after copyright comments
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

#This function splits the whole comment line and code line to corresponding words and finds the matching words between code and comment
def find_matching_words(code, comments):
    global n_code_comment_match
    matching_words = [] #List of matching words
    for code_line_number, code_line in code:
        for comment_line_number, comment_line in comments:
            #This is the range of searching for matching word, the wrods from a comment line will be used to find matching from the same line of code to next fve lines onwards
            if code_line_number in range(comment_line_number , comment_line_number+5): 
                code_words = re.findall(r'[a-zA-Z]+', code_line.lower())
                comment_words = re.findall(r'\w+', comment_line.lower())
                matching = set(code_words) & set(comment_words) #To match the the words from code line and comment line
                if matching:
                    n_code_comment_match += 1
                    matching_words.append((code_line_number, comment_line_number, code_line, comment_line, matching)) #matching_words list updating
    return matching_words #Return the matching_words list upon calling

#This function finds the relation between code and comment and returns the relations list upon calling
def find_relation(matching_words):
    relations = []
    for code_line_number, comment_line_number, code_line, comment_line, matching in matching_words:
        if code_line_number < comment_line_number:
            relation = 'Code line comes before Comment line'  #if code line is related with a comment next to the code line
        elif code_line_number > comment_line_number:
            relation = 'Code line comes after Comment line'  #When comment line is related to next code line/lines
        else:
            relation = 'Code line and Comment line are on the same line' #When inline code and comment are related
        relations.append((code_line_number, comment_line_number, code_line, comment_line, matching, relation))
    return relations

#This function identifies the code and comments along with their line numbers and returns the code, comments and line numbers upon calling
def read_code_and_comments(file_path):
    code = [] #The list of code line and line number
    comments = [] #The list of comment line and line number
    with open(file_path, encoding="utf-8") as file: #To open the verilog/SV file which encoded in UTF8
        lines = file.readlines()
        for line_number, line in enumerate(lines, start=1): 
            if '//' in line and not line.startswith('//'): #To find the inline comment
                code_t, comments_t = line.split('//', 1)  # Split the line at the first occurrence of '//' to code and comment
                code_t = code_t.strip()
                comments_t = comments_t.strip()
                comments.append((line_number, comments_t)) #Append the comments list with comment line and line number

                code.append((line_number, code_t)) #Append the code list with code line and line number
                
            elif line.startswith('//'): #To find regular comments except inline comments
                comments.append((line_number, line.strip())) #Append the comments list with comment line and line number
            else: #To find the code line
                code.append((line_number, line.strip())) #Append the code list with code line and line number
    return code, comments #Return code, comments list upon call

#Export analysis results to a CSV file
def export_to_csv(file_path, results):
    #for file_name in os.listdir(file_path):
    if file_path.endswith(".sv") or file_path.endswith(".v"): #To find all the verilog/SV files in the directory
        csv_file_name = os.path.splitext(file_path)[0] + ".csv" #To set the CSV file with the same name of Verilog/SV file
        csv_file_path = os.path.join(file_path, csv_file_name) #To set the CSV file path

        with open(csv_file_path, "w", newline="") as file: #To create CSV file
            writer = csv.writer(file)
            writer.writerow(['Line Number', 'Code Line', 'Comment Line', 'Matching Words', 'Relation']) #Columns heading
            writer.writerows(results) #Data updating to CSV from results

            print(f"CSV file '{csv_file_name}' created.") #A confirmation message that CSV generated successfully
            
            
            
            
            
            
#Export analysis results to a CSV file
def final_csv(file_path, results):


        with open(file_path, "a", newline="") as file: #To create CSV file
            writer = csv.writer(file)
            #writer.writerow(['Number of Files', 'Total Lines', 'Total Comment', 'Total Code', 'Copyright Comment', 'Functional Comment', 'In-line Comment', 'Comment Density', 'Frequent Length',
            #'Min Length', 'Max Length', 'Mean Length', 'Median Length', 'If_Else', 'Always', 'Always_FF', 'Always_Comb', 'Case', 'Total Match']) #Columns heading
            writer.writerows(results) #Data updating to CSV from results
            file.close()
            #print(f"CSV file '{csv_file_name}' created.") #A confirmation message that CSV generated successfully
            

#To analyze the verilog/SV files. This function will call all the required function we created before
def analyze_comments(directory):
    global n_file
    
    # Iterate through all Python files in the directory
    for root, _, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith(".sv") or file_name.endswith(".v"): #To find all the verilog/SV files in the directory
                n_file += 1 #Updating the number of file
                file_path = os.path.join(root, file_name) #To ad the file name to the path
                code, comments = read_code_and_comments(file_path) # read_code_and_comments function is called here
                matching_words = find_matching_words(code, comments) #find_matching_words function is called here
                relations = find_relation(matching_words) #find_relation function is called here
                comment_lines_in_SV(file_path) #comment_lines_in_SV function is called here

                

    
                


#To get the Directory path of a Project
path = input(r"Enter the Project Path Here: ")
final_csv_path = r'C:\Users\Subroto\Desktop\Code_Comment Analysis Report\phase2\new_csv.csv' #Final CSV path, change according to your preference after the r
analyze_comments(path) #analyze_comments function is called here

n_code = n_line - (n_copyright_comment +  n_comment)      #To find total number of code line
comment_density = n_comment/n_code #To calculate the comment_density
data.append((n_file, n_line, n_comment, n_code, n_copyright_comment, n_section_comment, n_inline_comment, comment_density, most_frequent(len_comments), min(len_comments), max(len_comments), statistics.mean(len_comments), statistics.median(len_comments),
                             n_if_else, n_always, n_always_ff, n_always_comb, n_case, n_code_comment_match))
                
final_csv(final_csv_path, data)
pdf_filename = "Reports.pdf" #defined the pdf name
pdf_file_path = os.path.join(path, pdf_filename) #defined the pdf saving directory
c = canvas.Canvas(pdf_file_path, pagesize=letter) #Canvus setup

# Set the font and font size
c.setFont("Helvetica", 12)

# Write the various variable value to the PDF, we need to convert every value to string
c.drawString(50, 770, "Code-Comments Analysis Report")
c.drawString(50, 760, "-------------------------------------------------------------")
c.drawString(50, 730, "Total Number of Verilog/SV files in the directory: " +str(n_file))
c.drawString(50, 710, "Total Number of Lines (except empty line): " +str(n_line))
c.drawString(50, 690, "Total Number of Comment Lines: " +str(n_comment))
c.drawString(50, 670, "Total Number of Code Lines: " +str(n_code))
c.drawString(50, 650, "Total Number of Copyright Comment: " +str(n_copyright_comment))
c.drawString(50, 630, "Total Number of Functional Comment: " +str(n_section_comment))
c.drawString(50, 610, "Total Number of In-Line Comment: " +str(n_inline_comment))
c.drawString(50, 550, "Comment Density: " +str(comment_density))
c.drawString(50, 530, "Most Frequent Comment Length by Words: " +str(most_frequent(len_comments)))
c.drawString(50, 510, "Minimum Comment Length by Words: " +str(min(len_comments)))
c.drawString(50, 490, "Maximum Comment Length by Words: " +str(max(len_comments)))
c.drawString(50, 470, "Mean of Comment Length by Words: " +str(statistics.mean(len_comments)))
c.drawString(50, 450, "Median of Comment Length by Words: " +str(statistics.median(len_comments)))
c.drawString(50, 400, "Total Number of If_else Blocks: " +str(n_if_else))
c.drawString(50, 380, "Total Number of Always Blocks: " +str(n_always))
c.drawString(50, 360, "Total Number of Always_FF Blocks: " +str(n_always_ff))
c.drawString(50, 340, "Total Number of Always_Comb Blocks: " +str(n_always_comb))
c.drawString(50, 320, "Total Number of Case Blocks: " +str(n_case))
c.drawString(50, 280, "Total Number of Keyword based Code Comment Matching in the Project: " +str(n_code_comment_match))

# Save the PDF file
c.save()

print("PDF file '{}' generated successfully.".format(pdf_filename)) #A confirmation message that pdf generated successfully


