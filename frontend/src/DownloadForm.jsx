import React, { useState } from "react";

const DownloadForm = () => {
  const [url, setUrl] = useState("");
  const [mensaje, setMensaje] = useState("");
  const [filename, setFilename] = useState("");
  const [folderPath, setFolderPath] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!folderPath) {
      setMensaje("Por favor, ingresa una ruta de carpeta antes de descargar.");
      return;
    }
    console.log(folderPath);
    try {
      const response = await fetch(`http://localhost:8000/download`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url, download_folder: folderPath }),
      });

      if (!response.ok) {
        throw new Error("Error al descargar el video");
      }

      const data = await response.json();
      setMensaje(data.message || data.mensaje);
      setFilename(data.file);
    } catch (error) {
      setMensaje(`Error: ${error.message}`);
    }
  };

  return (
    <div>
      <h1>Descargar el video</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="URL del video"
          required
        />
        <input
          type="text"
          value={folderPath}
          onChange={(e) => setFolderPath(e.target.value)}
          placeholder="Ruta de la carpeta"
          required
        />
        <button type="submit">Descargar</button>
      </form>
      {mensaje && <p>{mensaje}</p>}
      {filename && <p>Archivo descargado: {filename}</p>}
    </div>
  );
};

export default DownloadForm;
