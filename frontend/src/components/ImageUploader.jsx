import { useRef, useState } from "react";

function ImageUploader({ onImageChange }) {
  const [preview, setPreview] = useState(null);
  const [filename, setFilename] = useState("");
  const [filesize, setFilesize] = useState("");
  const [dragging, setDragging] = useState(false);
  const inputRef = useRef();

  const handleFile = (file) => {
    if (!file) return;
    setFilename(file.name);
    setFilesize((file.size / 1024).toFixed(1) + " KB");
    const reader = new FileReader();
    reader.onload = (e) => setPreview(e.target.result);
    reader.readAsDataURL(file);
    onImageChange(file);
  };

  const handleChange = (e) => handleFile(e.target.files[0]);

  const handleDrop = (e) => {
    e.preventDefault();
    setDragging(false);
    handleFile(e.dataTransfer.files[0]);
  };

  const handleRemove = () => {
    setPreview(null);
    setFilename("");
    setFilesize("");
    onImageChange(null);
    if (inputRef.current) inputRef.current.value = "";
  };

  return (
    <div>
      <input
        ref={inputRef}
        type="file"
        accept="image/*"
        style={{ display: "none" }}
        onChange={handleChange}
      />

      {preview ? (
        <div className="upload-preview">
          <img src={preview} alt="Preview" />
          <div className="upload-preview-info">
            <div className="filename">{filename}</div>
            <div className="filesize">{filesize}</div>
          </div>
          <button className="btn-remove" onClick={handleRemove} title="Remove">
            ✕
          </button>
        </div>
      ) : (
        <div
          className={`upload-zone ${dragging ? "drag-over" : ""}`}
          onClick={() => inputRef.current?.click()}
          onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
          onDragLeave={() => setDragging(false)}
          onDrop={handleDrop}
        >
          <div className="upload-icon">📷</div>
          <h3>Drop image here or click to browse</h3>
          <p>PNG, JPG, WEBP — CIFAR-10 compatible (32×32 recommended)</p>
        </div>
      )}
    </div>
  );
}

export default ImageUploader;
