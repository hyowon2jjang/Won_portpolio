import sys
import os

def convert_multiline_to_singleline(input_filepath, output_filepath):
    """
    Reads a multi-line text file, converts all newline characters to '\n',
    and writes the result as a single line to a new output file.

    Args:
        input_filepath (str): The path to the input text file.
        output_filepath (str): The path where the single-line output will be saved.
    """
    try:
        # Read the content of the input file with UTF-8 encoding
        with open(input_filepath, 'r', encoding='utf-8') as infile:
            content = infile.read()

        # Replace all newline characters with the '\n' escape sequence
        # This includes both Windows-style (\r\n) and Unix-style (\n) newlines
        single_line_content = content.replace('\r\n', '\\n').replace('\n', '\\n')

        # Write the modified content to the output file with UTF-8 encoding
        with open(output_filepath, 'w', encoding='utf-8') as outfile:
            outfile.write(single_line_content)

        print(f"Successfully converted '{input_filepath}' to a single line and saved to '{output_filepath}'")

    except FileNotFoundError:
        print(f"Error: The file '{input_filepath}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    """
    Main function to handle command-line arguments and call the conversion function.
    Usage: python script_name.py input.txt output.txt
    """
    if len(sys.argv) != 3:
        print("Usage: python convert_text.py <input_file.txt> <output_file.txt>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    convert_multiline_to_singleline(input_file, output_file)

if __name__ == "__main__":
    main()
