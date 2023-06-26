import csv
import re
import os


def find_matching_words(code, comments):
    matching_words = []
    for code_line_number, code_line in code:
        for comment_line_number, comment_line in comments:
            if code_line_number in range(comment_line_number , comment_line_number+5) :
                code_words = re.findall(r'[a-zA-Z]+', code_line.lower())
                comment_words = re.findall(r'\w+', comment_line.lower())
                matching = set(code_words) & set(comment_words)
                if matching:
                    matching_words.append((code_line_number, comment_line_number, code_line, comment_line, matching))
    return matching_words

def find_relation(matching_words):
    relations = []
    for code_line_number, comment_line_number, code_line, comment_line, matching in matching_words:
        if code_line_number < comment_line_number:
            relation = 'Code line comes before Comment line'
        elif code_line_number > comment_line_number:
            relation = 'Code line comes after Comment line'
        else:
            relation = 'Code line and Comment line are on the same line'
        relations.append((code_line_number, comment_line_number, code_line, comment_line, matching, relation))
    return relations

# Read code and comments from a file
def read_code_and_comments(file_path):
    code = []
    comments = []
    with open(file_path, encoding="utf8") as file:
        lines = file.readlines()
        for line_number, line in enumerate(lines, start=1):
            if '//' in line and not line.startswith('//'):
                code_t, comments_t = line.split('//', 1)  # Split the line at the first occurrence of '#'
                code_t = code_t.strip()
                comments_t = comments_t.strip()
                comments.append((line_number, comments_t))

                code.append((line_number, code_t))
                
            elif line.startswith('//'):
                comments.append((line_number, line.strip()))
            else:
                code.append((line_number, line.strip()))
    return code, comments

# Export results to a CSV file
def export_to_csv(file_path, results):
    #for file_name in os.listdir(file_path):
        if file_path.endswith(".sv") or file_path.endswith(".v"):
            csv_file_name = os.path.splitext(file_path)[0] + ".csv"
            csv_file_path = os.path.join(file_path, csv_file_name)

            with open(csv_file_path, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(['Line Number', 'Code Line', 'Comment Line', 'Matching Words', 'Relation'])
                writer.writerows(results)

            print(f"CSV file '{csv_file_name}' created.")


def analyze_comments(directory):



    # Iterate through all Python files in the directory
    for root, _, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith(".sv") or file_name.endswith(".v"):
                file_path = os.path.join(root, file_name)
                code, comments = read_code_and_comments(file_path)
                matching_words = find_matching_words(code, comments)
                relations = find_relation(matching_words)
                export_to_csv(file_path, relations)
                

    
                


# Usage example
path = input(r"Enter the Project Path Here: ")
#print(path)
analyze_comments(path)







