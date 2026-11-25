import os


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Paso 2: el archivo debe estar dentro del working_directory
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        if not valid_target_file:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # Paso 3: no se puede escribir sobre una carpeta
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        # Paso 4: crear las carpetas padre si no existen
        os.makedirs(os.path.dirname(target_file), exist_ok=True)

        # Paso 5: escribir (sobrescribe el contenido)
        with open(target_file, "w") as f:
            f.write(content)

        # Paso 6: mensaje de éxito
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    # Paso 7: cualquier error se devuelve como texto
    except Exception as e:
        return f"Error: {e}"


schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes or overwrites a file relative to the working directory, creating parent directories if needed",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to write, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "Text content to write to the file",
                },
            },
            "required": ["file_path", "content"],
        },
    },
}
