import os



schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Simply write to the python file relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path of the file to write, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "The content to write into the file",
                },
            },
            "required": ["file_path", "content"],
        },
    },
}


available4_functions = [
    schema_write_file,
]


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:    
        working_in_dir = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_in_dir,file_path))

        
        valid_target_dir = os.path.commonpath([working_in_dir, target_file_path]) == working_in_dir

        if not valid_target_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(target_file_path),exist_ok=True)

        with open(target_file_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"