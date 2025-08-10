import sys
import whisper
import time

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')

    if len(sys.argv) < 2:
        print("❌ لم يتم تمرير مسار الملف الصوتي", file=sys.stderr)
        sys.exit(1)

    input_path = sys.argv[1]

    print("بدء تحميل الموديل...", file=sys.stderr)
    start = time.time()
    model = whisper.load_model("small")  # ممكن تجرب "tiny" إذا الموارد قليلة
    print("الموديل تم تحميله.", file=sys.stderr)

    print("بدء الترانسكريبت...", file=sys.stderr)
    result = model.transcribe(input_path, language="ar", temperature=0, best_of=3)
    end = time.time()

    print(f"مدة المعالجة: {end - start:.2f} ثانية", file=sys.stderr)
    print(result['text'].strip())
