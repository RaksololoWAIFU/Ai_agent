# AI Agent

A simple AI agent created as part of an exercise/project on [boot.dev](https://www.boot.dev).

## About the Project
- **Main Logic:** Most of the codebase and implementation was written by me.
- **Calculators / Helper Functions:** Some helper modules (e.g., the calculator logic) were copied directly from the course materials to focus on the core AI agent functionality.

## Features
This AI agent is capable of:
- **Reading files** (`get_file_content`)
- **Inspecting directories and file info** (`get_files_info`)
- **Writing and updating files** (`write_file`)
- **Executing Python scripts** (`run_python_file`)

## Security
- **Sandboxed Execution:** The agent is restricted to its working directory and cannot access or modify files outside of it.