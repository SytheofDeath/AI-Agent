import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        work_directory = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(work_directory, file_path))
        valid_target_directory = os.path.commonpath([work_directory, target_path]) == work_directory
        if valid_target_directory == False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if os.path.isfile(target_path) == False:
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if file_path.endswith('.py') == False:
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", target_path]
        if args != None:
            command.extend(args)
        result = subprocess.run(command, cwd=work_directory, capture_output=True, text=True, timeout=30)
        output_string = ""
        if result.returncode != 0:
            output_string += f"Process exited with code {result.returncode}"
        if result.stdout == "" and result.stderr == "":
            output_string += "\n"f"No output produced"
        else:
            output_string += "\n"f"STDOUT: {result.stdout}"
            output_string += "\n"f"STDERR: {result.stderr}"
        return output_string
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a Python file at the specified path and returns its output",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to run, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string",
                    },
                    "description": "Optional list of arguments to pass to the Python script"
                }
            },
            "required": ["file_path"],
        },
    },
}
