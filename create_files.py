import os
import shutil

def recursive_copy(source_dir, destination_dir):
    for root, dirs, files in os.walk(source_dir):
        # Remove hidden folders and 'upload' folder from dirs
        dirs[:] = [d for d in dirs if not d.startswith('.') and d.lower() != 'upload']

        # Skip files in the root of the source folder
        if root == source_dir:
            continue

        for file in files:
            # Skip hidden files
            if file.startswith('.'):
                continue

            # Get the full path of the source file
            source_path = os.path.join(root, file)
            
            # Create the new file name
            relative_path = os.path.relpath(root, source_dir)
            new_file_name = "_".join(relative_path.split(os.sep) + [file])
            
            # Get the full path of the destination file
            destination_path = os.path.join(destination_dir, new_file_name)
            
            # Copy the file
            shutil.copy2(source_path, destination_path)
            print(f"Copied: {source_path} -> {destination_path}")

def clean_destination(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')
    print(f"All files in {directory} have been removed.")

# Example usage
source_directory = "./"
destination_directory = "upload"

# Ensure the destination directory exists
os.makedirs(destination_directory, exist_ok=True)

# Clean the upload directory before copying new files
clean_destination(destination_directory)

# Run the recursive copy function
recursive_copy(source_directory, destination_directory)