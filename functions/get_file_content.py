import os
from config import character_limit


schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Get file content and watch out if the file characters are too large, relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path of the file to read, relative to the working directory",
                },
            },
            "required": ["file_path"],  
        },
    },
}


available2_functions = [
    schema_get_file_content,
]


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_in_dir = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_in_dir,file_path))

        
        valid_target_dir = os.path.commonpath([working_in_dir, target_file_path]) == working_in_dir
        if not valid_target_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_file_path, "r") as f:
            file_content_string = f.read(character_limit)
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {character_limit} characters]'
            return file_content_string
    except Exception as e:
        return f"Error: {e}"