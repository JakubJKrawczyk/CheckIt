import { useState } from "react";

interface ColumnPair {
  file1Column: string;
  file2Column: string;
}

interface DuplicateColumnAction {
  column: string;
  action: "first" | "last" | "min" | "max" | "sum" | "custom";
  customValue?: string;
}

const styles = {
  container: {
    minHeight: "100vh",
    width: "100%",
    margin: 0,
    padding: "40px 20px",
    backgroundColor: "#121212",
    color: "#e0e0e0",
    boxSizing: "border-box" as const,
    fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
  },
  content: {
    maxWidth: "1100px",
    width: "100%",
    margin: "0 auto",
  },
  title: {
    textAlign: "center" as const,
    marginBottom: "40px",
    fontSize: "2.2rem",
    color: "#ffffff",
  },
  grid: {
    display: "grid",
    gridTemplateColumns: "1fr 1fr",
    gap: "30px",
    marginBottom: "40px",
  },
  card: {
    backgroundColor: "#1e1e1e",
    borderRadius: "12px",
    padding: "25px",
    boxShadow: "0 4px 20px rgba(0, 0, 0, 0.4)",
    border: "1px solid #2e2e2e",
  },
  cardTitle: {
    textAlign: "center" as const,
    marginBottom: "20px",
    fontSize: "1.3rem",
    color: "#ffffff",
  },
  inputGroup: {
    display: "flex",
    gap: "10px",
    marginBottom: "15px",
  },
  input: {
    flex: 1,
    padding: "12px 15px",
    backgroundColor: "#2a2a2a",
    border: "1px solid #3a3a3a",
    borderRadius: "8px",
    color: "#e0e0e0",
    fontSize: "14px",
    outline: "none",
  },
  inputSmall: {
    padding: "8px 12px",
    backgroundColor: "#2a2a2a",
    border: "1px solid #3a3a3a",
    borderRadius: "6px",
    color: "#e0e0e0",
    fontSize: "13px",
    outline: "none",
    width: "100%",
    boxSizing: "border-box" as const,
  },
  button: {
    padding: "12px 20px",
    backgroundColor: "#2a2a2a",
    border: "1px solid #3a3a3a",
    borderRadius: "8px",
    color: "#e0e0e0",
    cursor: "pointer",
    fontSize: "14px",
    transition: "all 0.3s ease",
  },
  buttonPrimary: {
    padding: "15px 40px",
    backgroundColor: "#4a4a4a",
    border: "none",
    borderRadius: "8px",
    color: "#ffffff",
    cursor: "pointer",
    fontSize: "16px",
    fontWeight: "bold" as const,
    transition: "all 0.3s ease",
  },
  buttonSecondary: {
    padding: "10px 20px",
    backgroundColor: "#3a3a3a",
    border: "1px solid #4a4a4a",
    borderRadius: "8px",
    color: "#e0e0e0",
    cursor: "pointer",
    fontSize: "14px",
    transition: "all 0.3s ease",
    marginRight: "10px",
  },
  buttonDisabled: {
    opacity: 0.5,
    cursor: "not-allowed",
  },
  select: {
    width: "100%",
    padding: "12px 15px",
    backgroundColor: "#2a2a2a",
    border: "1px solid #3a3a3a",
    borderRadius: "8px",
    color: "#e0e0e0",
    fontSize: "14px",
    outline: "none",
    cursor: "pointer",
  },
  selectSmall: {
    padding: "8px 12px",
    backgroundColor: "#2a2a2a",
    border: "1px solid #3a3a3a",
    borderRadius: "6px",
    color: "#e0e0e0",
    fontSize: "13px",
    outline: "none",
    cursor: "pointer",
    width: "100%",
    boxSizing: "border-box" as const,
  },
  label: {
    display: "block",
    marginBottom: "8px",
    color: "#9e9e9e",
    fontSize: "14px",
  },
  successText: {
    color: "#66bb6a",
    margin: "10px 0",
    textAlign: "center" as const,
    fontSize: "14px",
  },
  errorText: {
    color: "#ef5350",
    textAlign: "center" as const,
    padding: "15px",
    backgroundColor: "rgba(239, 83, 80, 0.1)",
    borderRadius: "8px",
    marginTop: "20px",
    border: "1px solid rgba(239, 83, 80, 0.3)",
  },
  duplicateBox: {
    marginTop: "20px",
    padding: "20px",
    border: "1px solid #ffa726",
    borderRadius: "10px",
    backgroundColor: "rgba(255, 167, 38, 0.05)",
  },
  duplicateTitle: {
    color: "#ffa726",
    margin: "0 0 15px 0",
    textAlign: "center" as const,
    fontSize: "1rem",
  },
  table: {
    width: "100%",
    borderCollapse: "collapse" as const,
    backgroundColor: "#1e1e1e",
    borderRadius: "10px",
    overflow: "hidden",
  },
  th: {
    padding: "15px",
    textAlign: "center" as const,
    backgroundColor: "#252525",
    color: "#ffffff",
    fontWeight: "600" as const,
    borderBottom: "1px solid #3a3a3a",
  },
  td: {
    padding: "12px 15px",
    textAlign: "center" as const,
    borderBottom: "1px solid #2e2e2e",
    color: "#e0e0e0",
  },
  actionButton: {
    padding: "8px 16px",
    border: "none",
    borderRadius: "6px",
    cursor: "pointer",
    fontSize: "13px",
    fontWeight: "500" as const,
  },
  addButton: {
    backgroundColor: "#66bb6a",
    color: "#121212",
  },
  removeButton: {
    backgroundColor: "#ef5350",
    color: "#ffffff",
  },
  sectionTitle: {
    textAlign: "center" as const,
    marginBottom: "25px",
    fontSize: "1.5rem",
    color: "#ffffff",
  },
  sectionHeader: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "25px",
  },
  buttonGroup: {
    display: "flex",
    gap: "10px",
  },
  resultSuccess: {
    color: "#66bb6a",
    textAlign: "center" as const,
    fontWeight: "bold" as const,
    fontSize: "1.3rem",
    padding: "20px",
    backgroundColor: "rgba(102, 187, 106, 0.1)",
    borderRadius: "10px",
    marginTop: "30px",
    border: "1px solid rgba(102, 187, 106, 0.3)",
  },
};

function App() {
  const [file1Path, setFile1Path] = useState("");
  const [file1Columns, setFile1Columns] = useState<string[]>([]);
  const [file1KeyColumn, setFile1KeyColumn] = useState("");
  const [file1DuplicateActions, setFile1DuplicateActions] = useState<DuplicateColumnAction[]>([]);
  const [file1HasDuplicates, setFile1HasDuplicates] = useState(false);

  const [file2Path, setFile2Path] = useState("");
  const [file2Columns, setFile2Columns] = useState<string[]>([]);
  const [file2KeyColumn, setFile2KeyColumn] = useState("");
  const [file2DuplicateActions, setFile2DuplicateActions] = useState<DuplicateColumnAction[]>([]);
  const [file2HasDuplicates, setFile2HasDuplicates] = useState(false);

  const [columnPairs, setColumnPairs] = useState<ColumnPair[]>([]);
  const [newPair, setNewPair] = useState<ColumnPair>({ file1Column: "", file2Column: "" });

  const [differences, setDifferences] = useState<any[]>([]);
  const [isEqual, setIsEqual] = useState<boolean | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchColumns = async (path: string): Promise<string[]> => {
    const params = new URLSearchParams({ excel_file_path: path });
    const response = await fetch(`http://localhost:8000/extract/excel/columns?${params}`);
    const result = await response.json();
    if (result.error) throw new Error(result.error.message);
    return result.success.data;
  };

  const browseFile = async (
    setPath: (path: string) => void,
    setColumns: (cols: string[]) => void,
    setKeyColumn: (key: string) => void,
    setDuplicateActions: (actions: DuplicateColumnAction[]) => void,
    setHasDuplicates: (has: boolean) => void
  ) => {
    try {
      const response = await fetch("http://localhost:8000/browse/file");
      const result = await response.json();
      if (result.path) {
        setPath(result.path);
        setKeyColumn("");
        setHasDuplicates(false);
        setDuplicateActions([]);
        const columns = await fetchColumns(result.path);
        setColumns(columns);
      }
    } catch (err: any) {
      setError(err.message);
    }
  };

  const checkDuplicates = async (
    path: string,
    keyColumn: string,
    columns: string[],
    setHasDuplicates: (has: boolean) => void,
    setDuplicateActions: (actions: DuplicateColumnAction[]) => void
  ) => {
    try {
      const response = await fetch("http://localhost:8000/check-duplicates", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ file_path: path, key_column: keyColumn }),
      });
      const result = await response.json();
      if (result.success) {
        const hasDups = result.success.data.has_duplicates;
        setHasDuplicates(hasDups);
        if (hasDups) {
          setDuplicateActions(
            columns.filter((col) => col !== keyColumn).map((col) => ({ column: col, action: "first" as const }))
          );
        }
      }
    } catch (err: any) {
      setError(err.message);
    }
  };

  const handleKeyColumnChange = async (
    keyColumn: string,
    path: string,
    columns: string[],
    setKeyColumn: (key: string) => void,
    setHasDuplicates: (has: boolean) => void,
    setDuplicateActions: (actions: DuplicateColumnAction[]) => void
  ) => {
    setKeyColumn(keyColumn);
    if (keyColumn && path) {
      await checkDuplicates(path, keyColumn, columns, setHasDuplicates, setDuplicateActions);
    }
  };

  const updateDuplicateAction = (
    actions: DuplicateColumnAction[],
    setActions: (actions: DuplicateColumnAction[]) => void,
    columnIndex: number,
    action: "first" | "last" | "min" | "max" | "sum" | "custom",
    customValue?: string
  ) => {
    const updated = [...actions];
    updated[columnIndex] = {
      ...updated[columnIndex],
      action,
      customValue: action === "custom" ? customValue : undefined,
    };
    setActions(updated);
  };

  const addColumnPair = () => {
    if (!newPair.file1Column || !newPair.file2Column) {
      setError("Wybierz obie kolumny");
      return;
    }
    setColumnPairs([...columnPairs, newPair]);
    setNewPair({ file1Column: "", file2Column: "" });
    setError(null);
  };

  const removeColumnPair = (index: number) => {
    setColumnPairs(columnPairs.filter((_, i) => i !== index));
  };

  const addAllMatchingColumns = () => {
    // Znajdź wspólne kolumny (te same nazwy)
    const commonColumns = file1Columns.filter(
      (col) => file2Columns.includes(col) && col !== file1KeyColumn && col !== file2KeyColumn
    );

    // Dodaj tylko te, które jeszcze nie są zmapowane
    const existingFile1Cols = columnPairs.map((p) => p.file1Column);
    const newPairs = commonColumns
      .filter((col) => !existingFile1Cols.includes(col))
      .map((col) => ({ file1Column: col, file2Column: col }));

    if (newPairs.length > 0) {
      setColumnPairs([...columnPairs, ...newPairs]);
      setError(null);
    } else {
      setError("Brak nowych wspólnych kolumn do dodania");
    }
  };

  const clearAllColumnPairs = () => {
    setColumnPairs([]);
  };

  const handleCompare = async () => {
    if (!file1Path || !file2Path) {
      setError("Wybierz oba pliki");
      return;
    }
    if (!file1KeyColumn || !file2KeyColumn) {
      setError("Wybierz kolumny klucz");
      return;
    }
    if (columnPairs.length === 0) {
      setError("Dodaj przynajmniej jedną parę kolumn do porównania");
      return;
    }

    setLoading(true);
    setError(null);
    setDifferences([]);
    setIsEqual(null);

    try {
      const response = await fetch("http://localhost:8000/compare", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          file1_path: file1Path,
          file1_key_column: file1KeyColumn,
          file1_duplicate_actions: file1DuplicateActions,
          file2_path: file2Path,
          file2_key_column: file2KeyColumn,
          file2_duplicate_actions: file2DuplicateActions,
          column_pairs: columnPairs,
        }),
      });

      const result = await response.json();
      if (result.error) {
        setError(result.error.details || result.error.message);
      } else {
        setDifferences(result.success.data.result);
        setIsEqual(result.success.data.is_equal);
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const renderDuplicateConfig = (
    hasDuplicates: boolean,
    actions: DuplicateColumnAction[],
    setActions: (actions: DuplicateColumnAction[]) => void
  ) => {
    if (!hasDuplicates) return null;

    return (
      <div style={styles.duplicateBox}>
        <h4 style={styles.duplicateTitle}>⚠️ Znaleziono duplikaty</h4>
        <table style={styles.table}>
          <thead>
            <tr>
              <th style={{ ...styles.th, width: "35%" }}>Kolumna</th>
              <th style={{ ...styles.th, width: "30%" }}>Akcja</th>
              <th style={{ ...styles.th, width: "35%" }}>Wartość</th>
            </tr>
          </thead>
          <tbody>
            {actions.map((action, idx) => (
              <tr key={idx}>
                <td style={styles.td}>{action.column}</td>
                <td style={styles.td}>
                  <select
                    value={action.action}
                    onChange={(e) =>
                      updateDuplicateAction(actions, setActions, idx, e.target.value as "first" | "last" | "min" | "max" | "sum" | "custom", action.customValue)
                    }
                    style={styles.selectSmall}
                  >
                    <option value="first">Pierwszy</option>
                    <option value="last">Ostatni</option>
                    <option value="min">Minimum (data/liczba)</option>
                    <option value="max">Maximum (data/liczba)</option>
                    <option value="sum">Sumuj (liczby)</option>
                    <option value="custom">Ustaw wartość</option>
                  </select>
                </td>
                <td style={styles.td}>
                  {action.action === "custom" ? (
                    <input
                      type="text"
                      value={action.customValue || ""}
                      onChange={(e) => updateDuplicateAction(actions, setActions, idx, "custom", e.target.value)}
                      style={styles.inputSmall}
                      placeholder="Wpisz wartość"
                    />
                  ) : (
                    <span style={{ color: "#616161" }}>—</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  };

  const bothFilesLoaded = file1Columns.length > 0 && file2Columns.length > 0;
  const keysSelected = file1KeyColumn && file2KeyColumn;

  return (
    <div style={styles.container}>
      <div style={styles.content}>
        <h1 style={styles.title}>Porównanie plików Excel</h1>

        <div style={styles.grid}>
          <div style={styles.card}>
            <h3 style={styles.cardTitle}>Plik 1</h3>
            <div style={styles.inputGroup}>
              <input type="text" value={file1Path} readOnly placeholder="Wybierz plik..." style={styles.input} />
              <button
                onClick={() => browseFile(setFile1Path, setFile1Columns, setFile1KeyColumn, setFile1DuplicateActions, setFile1HasDuplicates)}
                style={styles.button}
              >
                Przeglądaj
              </button>
            </div>

            {file1Columns.length > 0 && (
              <>
                <p style={styles.successText}>✓ Załadowano {file1Columns.length} kolumn</p>
                <label style={styles.label}>Kolumna klucz:</label>
                <select
                  value={file1KeyColumn}
                  onChange={(e) =>
                    handleKeyColumnChange(e.target.value, file1Path, file1Columns, setFile1KeyColumn, setFile1HasDuplicates, setFile1DuplicateActions)
                  }
                  style={styles.select}
                >
                  <option value="">-- Wybierz klucz --</option>
                  {file1Columns.map((col) => (
                    <option key={col} value={col}>{col}</option>
                  ))}
                </select>
                {renderDuplicateConfig(file1HasDuplicates, file1DuplicateActions, setFile1DuplicateActions)}
              </>
            )}
          </div>

          <div style={styles.card}>
            <h3 style={styles.cardTitle}>Plik 2</h3>
            <div style={styles.inputGroup}>
              <input type="text" value={file2Path} readOnly placeholder="Wybierz plik..." style={styles.input} />
              <button
                onClick={() => browseFile(setFile2Path, setFile2Columns, setFile2KeyColumn, setFile2DuplicateActions, setFile2HasDuplicates)}
                style={styles.button}
              >
                Przeglądaj
              </button>
            </div>

            {file2Columns.length > 0 && (
              <>
                <p style={styles.successText}>✓ Załadowano {file2Columns.length} kolumn</p>
                <label style={styles.label}>Kolumna klucz:</label>
                <select
                  value={file2KeyColumn}
                  onChange={(e) =>
                    handleKeyColumnChange(e.target.value, file2Path, file2Columns, setFile2KeyColumn, setFile2HasDuplicates, setFile2DuplicateActions)
                  }
                  style={styles.select}
                >
                  <option value="">-- Wybierz klucz --</option>
                  {file2Columns.map((col) => (
                    <option key={col} value={col}>{col}</option>
                  ))}
                </select>
                {renderDuplicateConfig(file2HasDuplicates, file2DuplicateActions, setFile2DuplicateActions)}
              </>
            )}
          </div>
        </div>

        {bothFilesLoaded && keysSelected && (
          <div style={{ ...styles.card, marginBottom: "30px" }}>
            <div style={styles.sectionHeader}>
              <h3 style={{ ...styles.sectionTitle, marginBottom: 0 }}>Mapowanie kolumn do porównania</h3>
              <div style={styles.buttonGroup}>
                <button onClick={addAllMatchingColumns} style={styles.buttonSecondary}>
                  Dodaj wspólne
                </button>
                <button
                  onClick={clearAllColumnPairs}
                  style={{ ...styles.buttonSecondary, backgroundColor: "#4a3a3a", borderColor: "#5a4a4a" }}
                  disabled={columnPairs.length === 0}
                >
                  Wyczyść
                </button>
              </div>
            </div>

            <table style={styles.table}>
              <thead>
                <tr>
                  <th style={styles.th}>Kolumna z Pliku 1</th>
                  <th style={styles.th}>Kolumna z Pliku 2</th>
                  <th style={{ ...styles.th, width: "120px" }}>Akcja</th>
                </tr>
              </thead>
              <tbody>
                {columnPairs.map((pair, idx) => (
                  <tr key={idx}>
                    <td style={styles.td}>{pair.file1Column}</td>
                    <td style={styles.td}>{pair.file2Column}</td>
                    <td style={styles.td}>
                      <button
                        onClick={() => removeColumnPair(idx)}
                        style={{ ...styles.actionButton, ...styles.removeButton }}
                      >
                        Usuń
                      </button>
                    </td>
                  </tr>
                ))}
                <tr>
                  <td style={styles.td}>
                    <select
                      value={newPair.file1Column}
                      onChange={(e) => setNewPair({ ...newPair, file1Column: e.target.value })}
                      style={styles.select}
                    >
                      <option value="">-- Wybierz --</option>
                      {file1Columns.map((col) => (
                        <option key={col} value={col}>{col}</option>
                      ))}
                    </select>
                  </td>
                  <td style={styles.td}>
                    <select
                      value={newPair.file2Column}
                      onChange={(e) => setNewPair({ ...newPair, file2Column: e.target.value })}
                      style={styles.select}
                    >
                      <option value="">-- Wybierz --</option>
                      {file2Columns.map((col) => (
                        <option key={col} value={col}>{col}</option>
                      ))}
                    </select>
                  </td>
                  <td style={styles.td}>
                    <button
                      onClick={addColumnPair}
                      style={{ ...styles.actionButton, ...styles.addButton }}
                    >
                      Dodaj
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        )}

        <div style={{ textAlign: "center", marginBottom: "30px" }}>
          <button
            onClick={handleCompare}
            disabled={loading || !file1Path || !file2Path || !keysSelected || columnPairs.length === 0}
            style={{
              ...styles.buttonPrimary,
              ...(loading || !file1Path || !file2Path || !keysSelected || columnPairs.length === 0 ? styles.buttonDisabled : {}),
            }}
          >
            {loading ? "Porównuję..." : "Porównaj"}
          </button>
        </div>

        {error && <p style={styles.errorText}>{error}</p>}

        {isEqual === true && <p style={styles.resultSuccess}>✓ Pliki są identyczne!</p>}

        {isEqual === false && differences.length > 0 && (
          <div style={styles.card}>
            <h2 style={styles.sectionTitle}>Różnice ({differences.length})</h2>
            <table style={styles.table}>
              <thead>
                <tr>
                  <th style={styles.th}>Klucz</th>
                  <th style={styles.th}>Kolumna</th>
                  <th style={styles.th}>Plik 1</th>
                  <th style={styles.th}>Plik 2</th>
                </tr>
              </thead>
              <tbody>
                {differences.map((diff, idx) => (
                  <tr key={idx}>
                    <td style={styles.td}>{diff.key}</td>
                    <td style={styles.td}>{diff.column}</td>
                    <td style={{ ...styles.td, color: "#ef5350" }}>{String(diff.value1)}</td>
                    <td style={{ ...styles.td, color: "#66bb6a" }}>{String(diff.value2)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;