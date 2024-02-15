""" Pretty display of content of file storage """

import json
import sys

# Get file names from command line arguments
if len(sys.argv) != 3:
  print("Usage: python3 format_json.py <input_file> <output_file>")
  # python3 format_json.py file.json file.json
  sys.exit(1)  
input_file = sys.argv[1] 
output_file = sys.argv[2]

# Read the JSON data
with open(input_file) as f:
  data = json.load(f)

# Format each dictionary 
formatted_data = []
for d in data:
  formatted_dict = {} 
  for k,v in d.items():
    formatted_dict[k] = v
  formatted_data.append(formatted_dict)

# Write formatted data to file  
with open(output_file, 'w') as f:
   json.dump(formatted_data, f, indent=2)

