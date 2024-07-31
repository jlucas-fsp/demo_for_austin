import os

def get_prompt(name: str) -> str:
    path = os.path.join('prompts', f"{name}.adoc")
    if os.path.isfile(path):
        with open(path, "r") as f:
            lines = f.readlines()
            # Remove comments from prompt
            lines = [line for line in lines if not line.strip().startswith('//')]
            return ''.join(lines)
    else:
        raise FileNotFoundError(f"Prompt file {path} not found")

def get_document(name: str) -> str:
    path = os.path.join('documents', f"{name}.txt")
    if os.path.isfile(path):
        with open(path, "r") as f:
            return f.read()
    else:
        raise FileNotFoundError(f"Document file {path} not found")
