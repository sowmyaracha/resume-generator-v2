import subprocess
result = subprocess.run(['grep', '-n', 'process_JD\|process_jd\|requires_citizenship\|profile_relevance', 'langChain.py'], capture_output=True, text=True)
print(result.stdout)
