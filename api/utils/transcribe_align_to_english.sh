cd ../current-trans
# echogarden translate-speech "$1" en-translation.txt --sourceLanguage="$2" --targetLanguage=en --whisper.model=small &> cache.txt
echogarden align-translation "$1" en-translation.txt en-subtitles.srt --sourceLanguage="$2" --targetLanguage=en &> cache.txt
rm cache.txt
cd ../src