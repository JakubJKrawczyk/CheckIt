import { useState, useRef, useEffect } from "react";
import InternalApi from "./internal_api/internalApi";
import type {
  PatternMatch,
  Region,
  ColumnRegion,
  SeparatedColumnConfig,
  PatternSearchRequest,
} from "./internal_api/internalApi.pdf";
import { usePdfRenderer } from "./hooks/usePdfRenderer";

const api = new InternalApi();

function App() {
  const [pdfFile, setPdfFile] = useState<File | null>(null);
  const [step, setStep] = useState<number>(1);
  const [patternRegion, setPatternRegion] = useState<Region | null>(null);
  const [patternPage, setPatternPage] = useState<number>(1);
  const [matches, setMatches] = useState<PatternMatch[]>([]);
  const [columnRegions, setColumnRegions] = useState<ColumnRegion[]>([]);
  const [separatedConfigs, setSeparatedConfigs] = useState<SeparatedColumnConfig[]>([]);
  const [extractedData, setExtractedData] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const [isDrawing, setIsDrawing] = useState<boolean>(false);
  const [startPoint, setStartPoint] = useState<{ x: number; y: number } | null>(null);
  const [currentRect, setCurrentRect] = useState<Region | null>(null);

  const canvasRef = useRef<HTMLCanvasElement>(null);
  const pdfCanvasRef = useRef<HTMLCanvasElement>(null);

  const { renderPage, loading: pdfLoading, error: pdfError, pageCount } = usePdfRenderer();

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setPdfFile(file);
      setStep(2);
    }
  };

  // Re-render PDF when page number changes or file is uploaded
  useEffect(() => {
    const renderPdfPage = async () => {
      if (!pdfFile || !pdfCanvasRef.current || step < 2) return;

      try {
        const { width, height } = await renderPage(pdfCanvasRef.current, pdfFile, patternPage);

        // Update the drawing canvas to match PDF canvas size
        if (canvasRef.current) {
          canvasRef.current.width = width;
          canvasRef.current.height = height;
        }
      } catch (err) {
        console.error("Failed to render PDF:", err);
      }
    };

    renderPdfPage();
  }, [patternPage, pdfFile, step, renderPage]);

  const handleMouseDown = (e: React.MouseEvent<HTMLCanvasElement>) => {
    if (!canvasRef.current) return;
    const rect = canvasRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    setIsDrawing(true);
    setStartPoint({ x, y });
  };

  const handleMouseMove = (e: React.MouseEvent<HTMLCanvasElement>) => {
    if (!isDrawing || !startPoint || !canvasRef.current) return;
    const rect = canvasRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    const width = x - startPoint.x;
    const height = y - startPoint.y;

    setCurrentRect({
      x: startPoint.x,
      y: startPoint.y,
      width,
      height,
    });

    drawCanvas();
  };

  const handleMouseUp = () => {
    if (currentRect && step === 2) {
      setPatternRegion(currentRect);
      setStep(3);
    } else if (currentRect && step === 4) {
      const columnName = prompt("Enter column name:");
      if (columnName) {
        setColumnRegions([
          ...columnRegions,
          {
            column_name: columnName,
            region: currentRect,
            page: patternPage,
          },
        ]);
      }
    }
    setIsDrawing(false);
    setStartPoint(null);
    setCurrentRect(null);
  };

  const drawCanvas = () => {
    if (!canvasRef.current) return;
    const ctx = canvasRef.current.getContext("2d");
    if (!ctx) return;

    ctx.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);

    if (currentRect) {
      ctx.strokeStyle = "red";
      ctx.lineWidth = 2;
      ctx.strokeRect(currentRect.x, currentRect.y, currentRect.width, currentRect.height);
    }

    if (step === 3 && matches.length > 0) {
      matches.forEach((match) => {
        ctx.strokeStyle = "blue";
        ctx.lineWidth = 2;
        ctx.strokeRect(
          match.region.x,
          match.region.y,
          match.region.width,
          match.region.height
        );
      });
    }

    if (step >= 4 && columnRegions.length > 0) {
      columnRegions.forEach((col, idx) => {
        const colors = ["green", "orange", "purple", "cyan", "magenta"];
        ctx.strokeStyle = colors[idx % colors.length];
        ctx.lineWidth = 2;
        ctx.strokeRect(col.region.x, col.region.y, col.region.width, col.region.height);
      });
    }
  };

  const searchPattern = async () => {
    if (!pdfFile || !patternRegion) return;

    setLoading(true);
    setError(null);

    try {
      const searchRequest: PatternSearchRequest = {
        pattern_region: patternRegion,
        page: patternPage,
      };

      const results = await api.pdf.searchPattern(pdfFile, searchRequest);
      setMatches(results);
      setStep(4);
      setTimeout(() => drawCanvas(), 100);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const extractData = async () => {
    if (!pdfFile || !patternRegion || columnRegions.length === 0) return;

    setLoading(true);
    setError(null);

    try {
      const config = {
        pattern_search: {
          pattern_region: patternRegion,
          page: patternPage,
        },
        column_regions: columnRegions,
        separated_configs: separatedConfigs.length > 0 ? separatedConfigs : undefined,
      };

      const data = await api.pdf.extractData(pdfFile, config);
      setExtractedData(data);
      setStep(5);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const addSeparatedConfig = () => {
    if (!currentRect) {
      alert("Please draw a region first");
      return;
    }

    const separator = prompt("Enter separator (e.g., ', '):");
    if (!separator) return;

    const mapping: Record<number, string> = {};
    let idx = 0;
    while (true) {
      const colName = prompt(`Enter column name for index ${idx} (or cancel to finish):`);
      if (!colName) break;
      mapping[idx] = colName;
      idx++;
    }

    if (Object.keys(mapping).length > 0) {
      setSeparatedConfigs([
        ...separatedConfigs,
        {
          region: currentRect,
          page: patternPage,
          separator,
          index_to_column: mapping,
        },
      ]);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>PDF Pattern Extraction</h1>

      {step === 1 && (
        <div>
          <h2>Step 1: Upload PDF</h2>
          <input type="file" accept="application/pdf" onChange={handleFileUpload} />
        </div>
      )}

      {step === 2 && pdfFile && (
        <div>
          <h2>Step 2: Select Pattern Region</h2>
          <p>Draw a rectangle around the pattern you want to search for</p>
          {pdfLoading && <p>Loading PDF...</p>}
          {pdfError && <p style={{ color: "red" }}>{pdfError}</p>}
          <div style={{ marginBottom: "20px" }}>
            <div style={{ position: "relative", display: "inline-block" }}>
              <canvas
                ref={pdfCanvasRef}
                style={{ maxWidth: "800px", display: "block", border: "1px solid #ccc" }}
              />
              <canvas
                ref={canvasRef}
                style={{
                  position: "absolute",
                  top: 0,
                  left: 0,
                  cursor: "crosshair",
                  pointerEvents: "auto",
                }}
                onMouseDown={handleMouseDown}
                onMouseMove={handleMouseMove}
                onMouseUp={handleMouseUp}
              />
            </div>
          </div>
          <div style={{ marginTop: "10px", position: "relative", zIndex: 1000 }}>
            <label>
              Page number:
              <input
                type="number"
                value={patternPage}
                onChange={(e) => setPatternPage(parseInt(e.target.value))}
                min={1}
                max={pageCount || 1}
                style={{ marginLeft: "5px", width: "60px" }}
              />
            </label>
            {pageCount > 0 && <span style={{ marginLeft: "10px" }}>of {pageCount}</span>}
          </div>
        </div>
      )}

      {step === 3 && (
        <div>
          <h2>Step 3: Search Pattern</h2>
          <button onClick={searchPattern} disabled={loading}>
            {loading ? "Searching..." : "Search Pattern"}
          </button>
          {error && <p style={{ color: "red" }}>{error}</p>}
          {matches.length > 0 && (
            <div>
              <p>Found {matches.length} matches</p>
              <div style={{ position: "relative", display: "inline-block" }}>
                <canvas
                  ref={pdfCanvasRef}
                  style={{ maxWidth: "800px", display: "block", border: "1px solid #ccc" }}
                />
                <canvas
                  ref={canvasRef}
                  style={{
                    position: "absolute",
                    top: 0,
                    left: 0,
                  }}
                />
              </div>
            </div>
          )}
        </div>
      )}

      {step === 4 && (
        <div>
          <h2>Step 4: Define Column Regions</h2>
          <p>Draw rectangles around column values</p>
          <div style={{ marginBottom: "20px" }}>
            <div style={{ position: "relative", display: "inline-block" }}>
              <canvas
                ref={pdfCanvasRef}
                style={{ maxWidth: "800px", display: "block", border: "1px solid #ccc" }}
              />
              <canvas
                ref={canvasRef}
                style={{
                  position: "absolute",
                  top: 0,
                  left: 0,
                  cursor: "crosshair",
                  pointerEvents: "auto",
                }}
                onMouseDown={handleMouseDown}
                onMouseMove={handleMouseMove}
                onMouseUp={handleMouseUp}
              />
            </div>
          </div>
          <div style={{ marginTop: "10px", position: "relative", zIndex: 1000 }}>
            <h3>Defined Columns:</h3>
            <ul>
              {columnRegions.map((col, idx) => (
                <li key={idx}>{col.column_name}</li>
              ))}
            </ul>
            <button onClick={addSeparatedConfig} style={{ marginRight: "10px" }}>
              Add Separated Column Config
            </button>
            <button onClick={extractData} disabled={loading || columnRegions.length === 0}>
              {loading ? "Extracting..." : "Extract Data"}
            </button>
          </div>
          {error && <p style={{ color: "red" }}>{error}</p>}
        </div>
      )}

      {step === 5 && extractedData.length > 0 && (
        <div>
          <h2>Step 5: Extracted Data</h2>
          <table border={1} style={{ borderCollapse: "collapse", width: "100%" }}>
            <thead>
              <tr>
                {Object.keys(extractedData[0]).map((key) => (
                  <th key={key} style={{ padding: "8px" }}>
                    {key}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {extractedData.map((row, idx) => (
                <tr key={idx}>
                  {Object.values(row).map((val: any, i) => (
                    <td key={i} style={{ padding: "8px" }}>
                      {val}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default App;
