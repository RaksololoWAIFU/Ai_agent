import os


schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}


available_functions = [
    schema_get_files_info,
]



def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_in_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_in_dir,directory))

    
        valid_target_dir = os.path.commonpath([working_in_dir, target_dir]) == working_in_dir
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        empty_list = []
        for x in os.listdir(target_dir):
            full_path = os.path.join(target_dir,x)
            name_of_file = x
            file_size = os.path.getsize(full_path)
            check_if_directory = os.path.isdir(full_path)
            empty_list.append(f"- {name_of_file}: file_size={file_size} bytes, is_dir={check_if_directory}")
        return "\n".join(empty_list)
            

    except Exception as e:
        return f"Error: {e}"

            

    
