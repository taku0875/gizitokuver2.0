import aiohttp
import os

ASSEMBLY_API_KEY = os.getenv("ASSEMBLY_API_KEY")
UPLOAD_URL = "https://api.assemblyai.com/v2/upload"
TRANSCRIPT_URL = "https://api.assemblyai.com/v2/transcript"

async def transcribe_audio(file):
    headers = {"authorization": ASSEMBLY_API_KEY}

    async with aiohttp.ClientSession() as session:
        # 1. アップロード
        audio_data = await file.read()
        async with session.post(UPLOAD_URL, data=audio_data, headers=headers) as res:
            upload_response = await res.json()
            audio_url = upload_response["upload_url"]

        # 2. テキスト化リクエスト
        transcript_payload = {"audio_url": audio_url}
        async with session.post(TRANSCRIPT_URL, json=transcript_payload, headers=headers) as res:
            transcript_response = await res.json()
            transcript_id = transcript_response["id"]

        # 3. 完了待ち
        while True:
            async with session.get(f"{TRANSCRIPT_URL}/{transcript_id}", headers=headers) as res:
                status = await res.json()
                if status["status"] == "completed":
                    return status["text"]
                elif status["status"] == "error":
                    raise Exception("Transcription failed")
