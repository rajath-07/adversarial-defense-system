
function ResultsPanel({ result }) {
  if (!result) return null;

  const attackSuccess =
    result.original_prediction !== result.attacked_prediction;
  const defenseSuccess =
    result.original_prediction === result.defended_prediction;

  const modelLabel = result.model === "mobilenet"
    ? "MobileNet V2"
    : result.model === "wideresnet"
    ? "WideResNet-28-10"
    : result.model;

  return (
    <div className="results-wrapper">

      {/* Section label */}

      {/* Meta pills */}
      <div className="meta-row">
        <div className="meta-pill model">
          <span className="meta-pill-dot" />
          {modelLabel}
        </div>
        <div className="meta-pill attack">
          <span className="meta-pill-dot" />
          {result.attack.toUpperCase()} Attack
        </div>
        <div className="meta-pill defense">
          <span className="meta-pill-dot" />
          {result.defense}
        </div>
      </div>

      {/* Status */}
      <div className="status-row">
        <div className={`status-badge ${attackSuccess ? "fail" : "success"}`}>
          <span className="status-badge-icon">
            {attackSuccess ? "⚡" : "🛡️"}
          </span>
          <div className="status-badge-text">
            <div className="label">Attack Status</div>
            <div className="value">
              {attackSuccess ? "Attack Succeeded" : "Attack Resisted"}
            </div>
          </div>
        </div>
        <div className={`status-badge ${defenseSuccess ? "success" : "fail"}`}>
          <span className="status-badge-icon">
            {defenseSuccess ? "✅" : "❌"}
          </span>
          <div className="status-badge-text">
            <div className="label">Defense Status</div>
            <div className="value">
              {defenseSuccess ? "Defense Successful" : "Defense Failed"}
            </div>
          </div>
        </div>
      </div>

      {/* Image comparison */}
      <div className="card" style={{ padding: "20px" }}>
        <div className="card-label">Image Comparison</div>
        <div className="images-grid">
          <div className="image-tile">
            <div className="image-tile-header">
              <span className="tile-label">Original</span>
              <span className="tile-dot original" />
            </div>
            <img
              src={`data:image/png;base64,${result.original_image}`}
              alt="Original"
            />
          </div>
          <div className="image-tile">
            <div className="image-tile-header">
              <span className="tile-label">Adversarial</span>
              <span className="tile-dot adversarial" />
            </div>
            <img
              src={`data:image/png;base64,${result.adversarial_image}`}
              alt="Adversarial"
            />
          </div>
          <div className="image-tile">
            <div className="image-tile-header">
              <span className="tile-label">Denoised</span>
              <span className="tile-dot denoised" />
            </div>
            <img
              src={`data:image/png;base64,${result.denoised_image}`}
              alt="Denoised"
            />
          </div>
        </div>
      </div>

      {/* Prediction cards */}
      <div className="card" style={{ padding: "20px" }}>
        <div className="card-label">Prediction Confidence</div>
        <div className="predictions-grid">
          <div className="pred-card">
            <div className="pred-card-header">
              <span className="pred-card-label">Original</span>
            </div>
            <div className="pred-card-class">
              {result.original_prediction}
            </div>
            <div className="confidence-track">
              <div
                className="confidence-fill original"
                style={{ width: `${result.original_confidence}%` }}
              />
            </div>
            <div className="confidence-pct">
              {result.original_confidence.toFixed(1)}% confidence
            </div>
          </div>

          <div className="pred-card">
            <div className="pred-card-header">
              <span className="pred-card-label">After Attack</span>
            </div>
            <div className="pred-card-class" style={{ color: "var(--danger)" }}>
              {result.attacked_prediction}
            </div>
            <div className="confidence-track">
              <div
                className="confidence-fill adversarial"
                style={{ width: `${result.attacked_confidence}%` }}
              />
            </div>
            <div className="confidence-pct">
              {result.attacked_confidence.toFixed(1)}% confidence
            </div>
          </div>

          <div className="pred-card">
            <div className="pred-card-header">
              <span className="pred-card-label">After Defense</span>
            </div>
            <div className="pred-card-class" style={{ color: "var(--success)" }}>
              {result.defended_prediction}
            </div>
            <div className="confidence-track">
              <div
                className="confidence-fill defended"
                style={{ width: `${result.defended_confidence}%` }}
              />
            </div>
            <div className="confidence-pct">
              {result.defended_confidence.toFixed(1)}% confidence
            </div>
          </div>
        </div>
      </div>

    </div>
  );
}

export default ResultsPanel;
