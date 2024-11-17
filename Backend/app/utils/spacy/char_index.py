# create a function that determines the start and end index of a string in a text
import re
from typing import Tuple

def find_substring(text: str, substring: str) -> Tuple[int, int]:
    # Find the start index of the substring in the text
    start_index = text.find(substring)
    
    # If the substring is not found, return (-1, -1)
    if start_index == -1:
        return (-1, -1)
    
    # Calculate the end index of the substring
    end_index = start_index + len(substring)
    
    return (start_index, end_index)

# Test the function with a sample text and substring

text = "Dear Alec, our team at Stitch Fix is reviewing your application for the AI Engineer role."
substring = "Stitch Fix"

start, end = find_substring(text, substring) #Company
print(f"Start Index: {start}, End Index: {end}")

#Position was not found in the text
substring = "AI Engineer"

start, end = find_substring(text, substring) #Position
print(f"Start Index: {start}, End Index: {end}")