from supabase import create_client, Client
from dotenv import load_dotenv
import os
from pathlib import Path

# .env を絶対パスで指定（backend/.env）
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
print("読み込むenvパス:", env_path)
load_dotenv(dotenv_path=env_path)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

# ログ出力で確認
print("SUPABASE_URL:", SUPABASE_URL)
print("SUPABASE_KEY:", SUPABASE_KEY[:5], "...(hidden)")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("環境変数の読み込みに失敗しました。SUPABASE_URLまたはSUPABASE_SERVICE_KEYが空です。")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

async def save_to_supabase(text: str, summary: str) -> str:
    data = {
        "user_id": "current_user_id",  # フロントから渡すならここで処理
        "summary": summary,
        "context": text
    }
    result = supabase.table("text").insert(data).execute()
    return result.data[0]["id"]
