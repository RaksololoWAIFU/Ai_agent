import os
import subprocess


schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs a Python (.py) file in the working directory and returns its stdout/stderr and exit code. Use this whenever the user asks to run or execute a script. ",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path of the file to executing",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "Optional list of arguments to pass to the python script",
                },
            },
            "required": ["file_path"],
        },
    },
}


available3_functions = [
    schema_run_python_file,
]




def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_in_dir = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_in_dir,file_path))

        
        valid_target_dir = os.path.commonpath([working_in_dir, target_file_path]) == working_in_dir
        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not target_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        if not os.path.isfile(target_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        command = ["python", target_file_path]

        if args:
            command.extend(args)

        run_variable = subprocess.run(command,cwd=working_in_dir,capture_output=True,text=True,timeout=30)
        parts = []
        if run_variable.returncode != 0:
            parts.append(f"Process exited with code {run_variable.returncode}")
        if not run_variable.stdout and not run_variable.stderr:
            parts.append("No output produced")
        else:
            if run_variable.stdout:
                parts.append(f"STDOUT: {run_variable.stdout}")
            if run_variable.stderr:
                parts.append(f"STDERR: {run_variable.stderr}")
        return "\n".join(parts)
    except Exception as e:
        return f"Error: executing Python file: {e}"