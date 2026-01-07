export type ComparisonDifference = {
  key: unknown;
  column: unknown;
  value1: unknown;
  value2: unknown;
};

const getFileNameFromPath = (filePath: string) => {
  const normalized = (filePath || "").trim();
  if (!normalized) return "";
  const parts = normalized.split(/[\\/]/);
  return parts[parts.length - 1] || normalized;
};

const escapeHtml = (value: unknown) => {
  const str = String(value ?? "");
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/\"/g, "&quot;")
    .replace(/'/g, "&#039;");
};

export const printComparisonReport = (params: {
  file1Path: string;
  file2Path: string;
  differences: ComparisonDifference[];
}) => {
  const { file1Path, file2Path, differences } = params;
  if (!differences || differences.length === 0) return;

  const file1Name = getFileNameFromPath(file1Path) || "(brak)";
  const file2Name = getFileNameFromPath(file2Path) || "(brak)";

  const rowsHtml = differences
    .map((diff) => {
      const key = escapeHtml(diff?.key);
      const column = escapeHtml(diff?.column);
      const value1 = escapeHtml(diff?.value1);
      const value2 = escapeHtml(diff?.value2);
      return `
          <tr>
            <td>${key}</td>
            <td>${column}</td>
            <td class="v1">${value1}</td>
            <td class="v2">${value2}</td>
          </tr>
        `;
    })
    .join("");

  const html = `<!doctype html>
<html lang="pl">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Raport porównania</title>
    <style>
      :root { color-scheme: light; }
      body { font-family: Segoe UI, Tahoma, Geneva, Verdana, sans-serif; margin: 24px; color: #111; }
      h1 { margin: 0 0 8px; font-size: 18px; }
      .meta { margin: 0 0 18px; font-size: 13px; }
      .meta div { margin: 2px 0; }
      table { width: 100%; border-collapse: collapse; font-size: 12px; }
      th, td { border: 1px solid #ddd; padding: 8px; text-align: left; vertical-align: top; }
      th { background: #f6f6f6; }
      .v1 { color: #b00020; }
      .v2 { color: #0b6b2b; }
      @media print {
        body { margin: 12mm; }
        a { color: inherit; text-decoration: none; }
      }
    </style>
  </head>
  <body>
    <h1>Raport porównania</h1>
    <div class="meta">
      <div><strong>Plik 1:</strong> ${escapeHtml(file1Name)}</div>
      <div><strong>Plik 2:</strong> ${escapeHtml(file2Name)}</div>
      <div><strong>Liczba różnic:</strong> ${escapeHtml(differences.length)}</div>
    </div>

    <table>
      <thead>
        <tr>
          <th>Klucz</th>
          <th>Kolumna</th>
          <th>Wartość (Plik 1)</th>
          <th>Wartość (Plik 2)</th>
        </tr>
      </thead>
      <tbody>
        ${rowsHtml}
      </tbody>
    </table>
  </body>
</html>`;

  // In PyWebView, window.open("about:blank") may be delegated to OS and fail.
  // Printing through an iframe works reliably in both browser and embedded webviews.
  const iframe = document.createElement("iframe");
  iframe.style.position = "fixed";
  iframe.style.right = "0";
  iframe.style.bottom = "0";
  iframe.style.width = "0";
  iframe.style.height = "0";
  iframe.style.border = "0";
  iframe.style.visibility = "hidden";

  document.body.appendChild(iframe);

  const frameWindow = iframe.contentWindow;
  const frameDocument = iframe.contentDocument || frameWindow?.document;
  if (!frameWindow || !frameDocument) {
    iframe.remove();
    return;
  }

  frameDocument.open();
  frameDocument.write(html);
  frameDocument.close();

  // Give the browser/webview a moment to layout before printing
  setTimeout(() => {
    try {
      frameWindow.focus();
      frameWindow.print();
    } finally {
      // Cleanup after print dialog is spawned
      setTimeout(() => iframe.remove(), 500);
    }
  }, 250);
};
