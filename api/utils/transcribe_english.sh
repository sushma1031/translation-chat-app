echogarden transcribe "$1" "$2" --language=en &> cache.txt
# subprocess.run(["sh.exe", "./transcribe_english.sh", audio_file, f"{audio_clip}-result.txt"]).returncode
rm cache.txt