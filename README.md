Discord bot that transcribes audio messages using Whisper using https://deepgram.com/
- Works as of August 2024, but not documented or maintained.
- Made it because wanted high-quality automatic transcriptions.
- Sharing because heard someone else wanted to use it.

Notes —
- Works on uploaded audio files or on voice messages created using the native discord voice message feeature.
- If you were running this on a large discord it might get expensive. Would be cheaper to use a smaller Whisper model or deepgram's own model, but also transcriptions would be worse.
- It tries to transcribe all uploaded audio files, so as a cost-protection measure you might want to set some kind of length limit in case someone uploads a really long audio file.
