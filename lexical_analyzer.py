# Aiden Cary
# 10/3/2025
# Lexical Analyzer for jack language to xml output
# Lab 1 PoPL

# Imports
import os # For clearing terminal

def print_menu():
    print("\nMenu Options:")
    print("1. Print original jack file text")
    print("2. Print tokens in XML format")
    print("3. Print file name")
    print("4. Change file name")
    print("5. Clear terminal")
    print("6. Exit\n")

def print_jack_file(file_name):
    # Read character by character and print
    # (This function is mainly for debugging and to show the original file content)
    # Open the input file with error handling
    try:
        with open(file_name, 'r') as file:
            while True:
                char = file.read(1)
                if not char:
                    break
                print(char, end='')  # Print each character without adding extra newlines
    except FileNotFoundError:
        print(f"Error: File '{file_name}' does not exist.")
        return
    except IOError:
        print(f"Error: Could not read file '{file_name}'.")
        return

def filter_comments(lines):
    filtered_lines = []
    for line in lines:
        stripped_line = line.strip()
        # Skip lines that start with comments or contain comment patterns
        if (stripped_line.startswith('*') or
            stripped_line.startswith('//') or 
            stripped_line.startswith('/*') or 
            stripped_line.startswith('/**') or
            '//' in stripped_line or
            '/*' in stripped_line):
            continue
        filtered_lines.append(line)
    return filtered_lines

def print_tokens_xml(file_name):
    # Read line by line, skip lines with comments, then process character by character
    # Figure out token category with switch statements
    # "_" is a alphabet
    # In the example output, there was a tab for each lexeme after <tokens> so I added that to match it exactly.
    # A \t is put before each print of a token

    # Open the input file with error handling
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: File '{file_name}' does not exist.")
        return
    except IOError:
        print(f"Error: Could not read file '{file_name}'.")
        return
        
    # Filter out lines with comments
    filtered_lines = filter_comments(lines)

    # Create output XML filename (replace .jack with T.xml)
    if file_name.endswith('.jack'):
        xml_file_name = file_name[:-5] + 'T.xml'
    else:
        xml_file_name = file_name + 'T.xml'
    
    # Open output XML file with error handling
    try:
        xml_file = open(xml_file_name, 'w')
    except IOError:
        print(f"Error: Could not create output file '{xml_file_name}'.")
        return

    # Helper function to write to both terminal and file
    def dual_print(text):
        print(text)
        xml_file.write(text + '\n')

    # Start XML output
    dual_print("<tokens>")

    # Process the filtered content character by character
    # Join filtered lines back into a single string for processing
    content = ''.join(filtered_lines)
    i = 0
    # Character by character processing
    while i < len(content):
        char = content[i]
        # Skips whitespace
        if char.isspace():
            i += 1
            continue
        # Switch statement for symbols
        switch = {
            '(': 'symbol',
            ')': 'symbol',
            '[': 'symbol',
            ']': 'symbol',
            '{': 'symbol',
            '}': 'symbol',
            ',': 'symbol',
            ';': 'symbol',
            '=': 'symbol',
            '.': 'symbol',
            '+': 'symbol',
            '-': 'symbol',
            '*': 'symbol',
            '/': 'symbol',
            '&': 'symbol',
            '|': 'symbol',
            '~': 'symbol',
            '<': 'symbol',
            '>': 'symbol'
        }
        # Check if the character is a symbol
        if char in switch:
            # Handle XML escaping for <, >, ", and & symbols
            if char == '<':
                escaped_char = '&lt;'
            elif char == '>':
                escaped_char = '&gt;'
            elif char == '"':
                escaped_char = '&quot;'
            elif char == '&':
                escaped_char = '&amp;'
            else:
                escaped_char = char
            
            # Print to terminal with original character, file gets escaped version
            print(f"\t<{switch[char]}> {char} </{switch[char]}>")
            xml_file.write(f"\t<{switch[char]}> {escaped_char} </{switch[char]}>\n")
            i += 1
        # Check for integer constants
        elif char.isdigit():
            num = char
            i += 1
            while i < len(content) and content[i].isdigit():
                num += content[i]
                i += 1
            dual_print(f"\t<integerConstant> {num} </integerConstant>")
        # Check for identifiers and keywords
        elif char.isalpha() or char == '_':
            identifier = char
            i += 1
            # Read until a non-alphanumeric character is found
            # Using isalnum() to check for alphanumeric characters
            while i < len(content) and (content[i].isalnum() or content[i] == '_'):
                identifier += content[i]
                i += 1
            # Check if identifier is a keyword
            keywords = {
                'class', 'constructor', 'method', 'function', 'int', 'boolean', 'char', 'void',
                'var', 'static', 'field', 'let', 'do', 'if', 'else', 'while', 'return',
                'true', 'false', 'null', 'this'
            }
            if identifier in keywords:
                dual_print(f"\t<keyword> {identifier} </keyword>")
            else:
                dual_print(f"\t<identifier> {identifier} </identifier>")
        # Check for string constants
        elif char == '"':
            string_const = ''
            i += 1
            # Read until the closing quote
            while i < len(content) and content[i] != '"': 
                string_const += content[i]
                i += 1
            if i < len(content):  # Skip the closing quote
                i += 1
            dual_print(f"\t<stringConstant> {string_const} </stringConstant>")
        # Handle '/' separately to avoid confusion with comments
        elif char == '/':
            # Since we've already filtered out comment lines, treat '/' as a symbol
            dual_print(f"\t<symbol> / </symbol>")
            i += 1
        # Unrecognized characters for debugging
        else:
            dual_print(f"\tUnrecognized character: {char}")
            i += 1
    
    # End XML output
    dual_print("</tokens>")

    # Close the XML output file
    xml_file.close()
    print(f"\nXML output has been saved to: {xml_file_name}")
    

def main():
    '''
    Jack Syntax:
    White spaces & comments:
    '//', '/*', '/**', '*'
    Symbols:
    '()', '[]', '{}', ',', ';', '=', '.', '+', '-', '*', '/', '&', '|', '~', '<', '>'
    Reserverd/Key words:
    'class', 'constructor', 'method', 'function', 'int', 'boolean', 'char', 'void'
    'var', 'static', 'field', 'let', 'do', 'if', 'else', 'while', 'return'
    'true', 'false', 'null', 'this'
    '''

    # Set default file name
    file_name = "Main.jack"

    print("Welcome to Aiden's Lexical Analyzer for the Jack language!")
    print("This program reads a .jack file and outputs its tokens in XML format."
          "\nIt handles symbols, keywords, identifiers, integer constants, and string constants. Lines with comments are ignored.")
    print("Please ensure the input file is in the same directory as this script.")
    print(f"Default file name is {file_name}. You can change it using the menu options.")
    
    # Main loop for menu
    while True:
        print_menu()
        choice = input("Enter your choice (1-5): ")
        if choice == '1':
            print("\nOriginal jack file text:\n")
            print_jack_file(file_name)
            continue
        elif choice == '2':
            print("\nTokens in XML format:\n")       
            print_tokens_xml(file_name)
            continue
        elif choice == '3':
            print(f"Current file name: {file_name}")
            continue
        elif choice == '4':
            print(f"Current file name: {file_name}")
            new_file_name = input("\nEnter new file name (with .jack extension): ")
            # Use built in endswith method to check for .jack extension (I love Python built-in methods!)
            while not new_file_name.endswith('.jack'):
                new_file_name = input("Invalid file name. Make sure it ends with .jack: ")
            file_name = new_file_name
            print(f"File name changed to: {file_name}")
            continue
        elif choice == '5':
            os.system('cls')
            continue
        elif choice == '6':
            print("Exiting the program. Goodbye!")
            break

if __name__ == "__main__":
            main()