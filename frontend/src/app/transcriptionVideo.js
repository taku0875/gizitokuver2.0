"use server";
import { revalidatePath } from 'next/cache';

export default async function transcriptionVideo(file) {
    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch(process.env.NEXT_PUBLIC_API_ENDPOINT + "/upload_audio", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: formData,
    });
    if (!res.ok) {
        throw new Error("Failed to transcribe video");
    }

    const data = await res .json();
    return data.text;
}