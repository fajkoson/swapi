import subprocess
import sys
import os

def run_main():
    test_files_and_dirs = [
        'src/tests/test_sw_world.py',
        'src/tests/test_yaml_mngr.py',
        'src/swpackage',
    ]
    
    for path in test_files_and_dirs:
        if path.endswith(".py"):            
            pytest_exit_code = subprocess.run([sys.executable, '-m', 'pytest', path]).returncode
            if pytest_exit_code != 0:
                return pytest_exit_code
            mypy_exit_code = subprocess.run([sys.executable, '-m', 'mypy', path]).returncode

            if mypy_exit_code != 0:
                return mypy_exit_code
                
        elif os.path.isdir(path):           
            mypy_exit_code = subprocess.run([sys.executable, '-m', 'mypy', path]).returncode
            if mypy_exit_code != 0:
                return mypy_exit_code

    return 0

if __name__ == "__main__":
    exit_code = run_main()
    sys.exit(exit_code)
