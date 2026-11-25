import os
import subprocess


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        absolute_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Paso 2: el archivo debe estar dentro del working_directory
        valid_target_file = os.path.commonpath([working_dir_abs, absolute_file_path]) == working_dir_abs
        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # Paso 3: debe existir y ser un archivo normal
        if not os.path.isfile(absolute_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        # Paso 4: debe terminar en .py
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        # Pasos 5 y 6: armar el comando con argumentos opcionales
        command = ["python", absolute_file_path]
        if args:
            command.extend(args)

        # Paso 7: ejecutar con directorio, salida capturada, texto y timeout
        result = subprocess.run(
            command,
            cwd=working_dir_abs,
            capture_output=True,
            text=True,
            timeout=30,
        )

        # Paso 8: armar el texto de salida
        output = []
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        if not result.stdout and not result.stderr:
            output.append("No output produced")
        else:
            if result.stdout:
                output.append(f"STDOUT:\n{result.stdout}")
            if result.stderr:
                output.append(f"STDERR:\n{result.stderr}")

        # Paso 9: devolver el texto
        return "\n".join(output)

    # Paso 10: cualquier error se devuelve como texto
    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a Python file relative to the working directory with optional arguments and returns its output",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to execute, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of command-line arguments to pass to the Python file",
                },
            },
            "required": ["file_path"],
        },
    },
}
