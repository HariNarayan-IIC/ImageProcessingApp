# cli.py

import os
import sys
import subprocess

def main():
    if len(sys.argv) < 2:
        print("Usage: ImageProcessingApp <command>")
        sys.exit(1)

    command = sys.argv[1]

    # Change to the directory where manage.py is located
    venv_path = os.getenv('VIRTUAL_ENV')
    if venv_path == None:
        venv_path = sys.executable[0:-10]
    manage_py_path = os.path.join(venv_path, 'Lib', 'site-packages', 'ImageProcessingApp')

    if not os.path.exists(manage_py_path):
        print("Error: manage.py not found in the current directory.")
        sys.exit(1)
    else: 
        os.chdir(manage_py_path)

    if command == 'run':
        runserver()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

def runserver():
    """Run Django development server."""
    subprocess.check_call([sys.executable, 'manage.py', 'runserver'])

if __name__ == '__main__':
    main()
