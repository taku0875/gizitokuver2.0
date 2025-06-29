from fastapi import FastAPI, UploadFile, File
from app.services.assemblyai import transcribe_audio
from app.services.openai_summary import summarize_text
from app.services.supabase_client import save_to_supabase
from app.schemas import TextSummaryResponse

app = FastAPI()

@app.post("/upload_audio", response_model=TextSummaryResponse)
async def upload_audio(file: UploadFile = File(...)):
    """
    音声ファイルを受け取り、AssemblyAIで文字起こし → OpenAIで要約 → Supabaseに保存し、結果を返す。
    """
    # 1. AssemblyAIで文字起こし
    transcript_text = await transcribe_audio(file)

    # 2. OpenAIで要約
    summary = await summarize_text(transcript_text)

    # 3. Supabaseに保存
    text_id = await save_to_supabase(transcript_text, summary)

    # 4. クライアントに返す
    return TextSummaryResponse(
        text_id=text_id,
        transcription=transcript_text,
        summary=summary
    )


@app.get("/ping")
async def ping():
    """
    確認用エンドポイント。起動チェック用。
    """
    return {"message": "pong"}
