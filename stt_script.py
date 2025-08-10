import sys
import whisper

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')

    if len(sys.argv) < 2:
        print("❌ لم يتم تمرير مسار الملف الصوتي", file=sys.stderr)
        sys.exit(1)

    input_path = sys.argv[1]

    model = whisper.load_model("small")
    result = model.transcribe(input_path, language="ar", temperature=0, best_of=3)


    print(result['text'].strip())
