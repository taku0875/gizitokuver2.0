"use client";
import Link from "next/link";
import { useRef, useState } from "react";
import transcriptionVideo from "./transcriptionVideo"


export default function Home() {
  const inputRef = useRef();
  const [source, setSource] = useState();
  const [file, setFile] = useState();

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    const url = URL.createObjectURL(file);
    setFile(file);
    setSource(url);
  };
  const handleChoose = (event) => {
    inputRef.current.click();
  };
  const handleSubmit = async(event) => {
    event.preventDefault();
    if (!file) {
      alert("ファイルが選択されていません。");
      return;
    }

    try {
      const result = await transcriptionVideo(file);
      console.log("文字起こし結果：", result);
    } catch (error) {
      console.error("文字起こしに失敗しました", error);
    }
  };

  return (
    <>
      <div className="">
        <h1 className="">議事録作成アプリ（仮）</h1>
      </div>

      <div className="VideoInput">
        <input
          ref={inputRef}
          className="VideoInput_input"
          type="file"
          onChange={handleFileChange}
          accept=".mov, .mp4"
        />
        {!source && <button onClick={handleChoose}>動画を選択</button>}
        {source && (
          <>
            <video
              className="VideoInput_video"
              width="100%"
              height="400px"
              controls
              src={source}
            />
            <button onClick={handleSubmit}>文字起こしを実行</button>
          </>
        )}
        <div className="VideoInput_footer">
          {source || "ファイルが選択されていません"}
        </div>
      </div>
    </>
  )
}