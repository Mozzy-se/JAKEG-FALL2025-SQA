import os
import sys
import random
import string
import traceback
from datetime import datetime, timedelta
import logging

# Path setup
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Directories for MLForensics modules
MINING_DIR = os.path.join(ROOT_DIR, "MLForensics", "MLForensics-farzana", "mining")
FAME_ML_DIR = os.path.join(ROOT_DIR, "MLForensics", "MLForensics-farzana", "FAME-ML")

# Add module paths to sys.path
sys.path.append(MINING_DIR)
sys.path.append(FAME_ML_DIR)

# Logging config
LOG_FILE = os.path.join(ROOT_DIR, "forensics.log")
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",)
logger = logging.getLogger(__name__)

import mining 
import py_parser

# Generates random strings with set max length for fuzzing
def random_string(max_len: int = 200) -> str:
    length = random.randint(0, max_len)
    return "".join(random.choices(string.printable, k=length))

# Generates a random filename for fuzzing
def random_filename(suffix: str = ".txt") -> str:
    name = "".join(random.choices(string.ascii_letters + string.digits, k=10))
    return f"fuzz_{name}{suffix}"

# Generates a random list of integers for fuzzing
def random_list(max_len: int = 50):
    length = random.randint(0, max_len)
    return [random.randint(-100, 100) for _ in range(length)]

# Generate a random chunk size for fuzzing
def random_chunk_size() -> int:
    return random.randint(-5, 10)

# Generates a random datetime for fuzzing
def random_date() -> datetime:
    base = datetime(2000, 1, 1)
    offset_days = random.randint(0, 365 * 20)
    return base + timedelta(days=offset_days)

# Generates a temporary Python file with random content for fuzzing
def random_python_file() -> str:
    filename = random_filename(suffix=".py")
    write_valid = random.random() < 0.5

    with open(filename, "w", encoding="utf-8", errors="ignore") as f:
        if write_valid:
            f.write("x = 1 + 2\n")
            f.write("print(x)\n")
        else:
            f.write(random_string())

    return filename

# Fuzzing helper function
def fuzz_function(name: str, call_fn, iterations: int = 200) -> None:
    print(f"[FUZZ] Starting fuzzing for {name} with {iterations} iterations")
    bug_count = 0

    for i in range(iterations):
        try:
            call_fn()
        except Exception as e:
            bug_count += 1
            print(f"[BUG] {name} crashed on iteration {i}: {e}")
            traceback.print_exc()

    print(f"[FUZZ] Done fuzzing {name}. Total crashes: {bug_count}")
    print("-" * 60)

# Fuzzes mining.giveTimeStamp which has no parameters
def fuzz_giveTimeStamp() -> None:
    def call():
        _ = mining.giveTimeStamp()

    fuzz_function("mining.giveTimeStamp", call)

# Generates random content and file paths to fuzz dumpContentIntoFile
def fuzz_dumpContentIntoFile() -> None:
    def call():
        content = random_string()
        path = random_filename(suffix=".txt")
        try:
            mining.dumpContentIntoFile(content, path)
        finally:
            if os.path.exists(path):
                os.remove(path)

    fuzz_function("mining.dumpContentIntoFile", call)

# Generates random lists and chunk sizes to fuzz makeChunks
def fuzz_makeChunks() -> None:
    def call():
        lst = random_list()
        size = random_chunk_size()
        for _ in mining.makeChunks(lst, size):
            pass

    fuzz_function("mining.makeChunks", call)

# Generates random dates and checks that subtracting them never crashes
def fuzz_days_between() -> None:
    def call():
        d1 = random_date()
        d2 = random_date()
        _ = mining.days_between(d1, d2)

    fuzz_function("mining.days_between", call)

# Generates temp python files with either valid code or garbage to fuzz the parser
def fuzz_getPythonParseObject() -> None:
    def call():
        path = random_python_file()
        try:
            _ = py_parser.getPythonParseObject(path)
        finally:
            if os.path.exists(path):
                os.remove(path)

    fuzz_function("py_parser.getPythonParseObject", call)

# Main entry point
def main() -> None:
    fuzz_giveTimeStamp()
    fuzz_dumpContentIntoFile()
    fuzz_makeChunks()
    fuzz_days_between()
    fuzz_getPythonParseObject()

if __name__ == "__main__":
    main()
