import os

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        work_directory = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(work_directory, file_path))
        valid_target_directory = os.path.commonpath([work_directory, target_path]) == work_directory
        if valid_target_directory == False:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if os.path.isfile(target_path) == False:
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(target_path, "r") as f:
            read_file = f.read(10000)
            if f.read(1):
                read_file += f'[...File "{file_path}" truncated at 10000 characters]'
        return read_file
    except Exception as e:
        return f"Error: {e}"

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads file content in a specified directory relative to the working directory, returning text/content from a specific file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to a specific file, relative to the working directory",
                },
            },
            "required": ["file_path"]
        },
    },
}
