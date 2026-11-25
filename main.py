import os
import sys
import argparse
from dotenv import load_dotenv
from openai import OpenAI

from prompts import system_prompt
from call_function import available_functions, call_function

MAX_ITERATIONS = 20

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

if api_key is None:
    raise RuntimeError("No se encontró OPENROUTER_API_KEY. Revisa tu archivo .env")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

    # Paso 1: repetir hasta 20 veces
    for _ in range(MAX_ITERATIONS):
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions,
            temperature=0,
        )

        if response.usage is None:
            raise RuntimeError("La respuesta no trae datos de uso. Probablemente falló la petición a la API.")

        if args.verbose:
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")

        # Paso 2: guardar el mensaje del modelo en el historial
        message = response.choices[0].message
        messages.append(message)

        # Paso 4: sin tool_calls = respuesta final, terminar
        if not message.tool_calls:
            print("Final response:")
            print(message.content)
            return

        # Paso 3: ejecutar cada tool call y guardar su resultado
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, args.verbose)

            if not result_message.get("content"):
                raise RuntimeError(f"La función {tool_call.function.name} no devolvió ningún resultado")

            if args.verbose:
                print(f"-> {result_message['content']}")

            messages.append(result_message)

    # Paso 5: se acabaron las vueltas sin respuesta final
    print(f"Error: el agente no terminó después de {MAX_ITERATIONS} iteraciones.")
    sys.exit(1)


if __name__ == "__main__":
    main()
