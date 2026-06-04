import { useState } from "react";
import ImageUploader from "./components/ImageUploader";
import ResultsPanel from "./components/ResultsPanel";
import { predictImage } from "./services/api";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [model, setModel] = useState("mobilenet");
  const [attack, setAttack] = useState("pgd");

  const handlePredict = async () => {
    if (!file) {
      alert("Please upload an image first.");
      return;
    }
    try {
      setLoading(true);
      setResult(null);
      const response = await predictImage(file, model, attack);
      setResult(response);
    } catch (error) {
      console.error(error);
      alert("Prediction failed. Please check the server and try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-wrapper">
      <div className="app-inner">

        {/* Header */}
        <header className="app-header">
                  <h1>
            Adversarial <span>Defense</span> System
          </h1>
          <p>
            WideResNet-28-10 &amp; MobileNetV2 · FGSM / PGD Attacks · Hybrid Autoencoder Defense
          </p>
        </header>

        {/* Upload */}
        <div className="card" style={{ animationDelay: "0.05s" }}>
          <ImageUploader onImageChange={setFile} />
        </div>

        {/* Controls */}
        <div className="card" style={{ animationDelay: "0.1s" }}>
          <div className="controls-grid">
            <div className="control-group">
              <label>Classifier Model</label>
              <select value={model} onChange={(e) => setModel(e.target.value)}>
                <option value="mobilenet">MobileNet V2</option>
                <option value="wideresnet">WideResNet-28-10</option>
              </select>
            </div>
            <div className="control-group">
              <label>Attack Type</label>
              <select value={attack} onChange={(e) => setAttack(e.target.value)}>
                <option value="fgsm">FGSM — Fast Gradient Sign Method</option>
                <option value="pgd">PGD — Projected Gradient Descent</option>
              </select>
            </div>
          </div>
        </div>

        {/* Run */}
        <button
          className="btn-run"
          onClick={handlePredict}
          disabled={loading || !file}
        >
          {loading ? (
            <>
              <span className="spinner" />
              Processing Pipeline…
            </>
          ) : (
            <>
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                <path d="M3 2.5l10 5.5-10 5.5V2.5z" fill="currentColor" />
              </svg>
              Run Prediction
            </>
          )}
        </button>

        {/* Results */}
        {result && <ResultsPanel result={result} />}

      </div>
    </div>
  );
}

export default App;
