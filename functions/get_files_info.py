import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        work_directory = os.path.abspath(working_directory)
        target_directory = os.path.normpath(os.path.join(work_directory, directory))
        valid_target_directory = os.path.commonpath([work_directory, target_directory]) == work_directory
        lines = []
        if valid_target_directory == False:
            return f'   Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if os.path.isdir(target_directory) == False:
            return f'   Error: "{directory}" is not a directory'
        else:
            for i in os.listdir(target_directory):
               line = f"    - {i}:" + f" file_size={os.path.getsize(os.path.join(target_directory, i))} bytes," + f" is_dir={os.path.isdir(os.path.join(target_directory, i))}"
               lines.append(line)
            return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"

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
