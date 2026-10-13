import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        work_directory = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(work_directory, file_path))
        valid_target_directory = os.path.commonpath([work_directory, target_path]) == work_directory
        if valid_target_directory == False:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_path) == True:
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        with open(target_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Opens file content in a specified directory relative to the working directory, writing over any text already in the file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to a specific file, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "Content that will overwite any text that is already in the specified file",
                },
            },
            "required": ["file_path", "content"]
        },
    },
}
