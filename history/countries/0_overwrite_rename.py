import os

# Get the directory where the script is located
script_directory = os.path.dirname(os.path.abspath(__file__))

# Loop through all files in the script's directory
for filename in os.listdir(script_directory):
    if filename.endswith(".txt"):
        old_filepath = os.path.join(script_directory, filename)

        # Split name and extension
        name, extension = os.path.splitext(filename)

        # New filename with "_Overwrite"
        new_filename = f"{name}_Overwrite{extension}"
        new_filepath = os.path.join(script_directory, new_filename)

        # Rename the file
        os.rename(old_filepath, new_filepath)
        print(f"Renamed: {filename} -> {new_filename}")

print("Renaming complete.")