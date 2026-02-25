import subprocess
import traceback

try:
    result = subprocess.run(
        [r"c:\Users\mahab\JARVIs\CropSenseAI\venv\Scripts\python.exe", "debug_predict.py"],
        capture_output=True,
        text=True,
        encoding='utf-8'
    )
    with open("error_log_clean.txt", "w", encoding="utf-8") as f:
        f.write("STDOUT:\n")
        f.write(result.stdout)
        f.write("\nSTDERR:\n")
        f.write(result.stderr)
    print("Done writing to error_log_clean.txt")
except Exception as e:
    print("Wrapper failed", e)
