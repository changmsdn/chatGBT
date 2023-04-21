import whisper

model = whisper.load_model("base")
result = model.transcribe("test_long.mp4")
print(result["text"])