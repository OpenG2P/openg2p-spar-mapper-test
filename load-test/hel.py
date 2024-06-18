import re

# Sample log text
log_text = """
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
User 1 ID range: 11 - 20
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
User 1 ID range: 21 - 30
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
User 1 ID range: 31 - 40
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
length is 1
User 1 ID range: 0 - 0
length is 1
User 1 ID range: 0 - 0
length 1
"""

# Use regular expression to find all occurrences of "length is 1"
occurrences = re.findall(r'length 1', log_text)

# Print the count
print(f"The phrase 'length is 1' was printed {len(occurrences)} times.")
