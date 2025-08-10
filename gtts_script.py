import argparse
from gtts import gTTS
import sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--text', type=str, required=True)
    parser.add_argument('--out_path', type=str, required=True)
    args = parser.parse_args()

    try:
        tts = gTTS(text=args.text, lang='ar', slow=False)
        tts.save(args.out_path)
        print(f"تم حفظ ملف الصوت في: {args.out_path}")
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
