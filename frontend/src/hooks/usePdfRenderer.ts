import { useState, useEffect, useCallback, useRef } from 'react';
import * as pdfjsLib from 'pdfjs-dist';

// Configure PDF.js worker - use the worker from node_modules
pdfjsLib.GlobalWorkerOptions.workerSrc = new URL(
  'pdfjs-dist/build/pdf.worker.min.mjs',
  import.meta.url
).toString();

interface UsePdfRendererReturn {
  canvasRef: React.RefObject<HTMLCanvasElement>;
  renderPage: (file: File, pageNumber: number) => Promise<void>;
  loading: boolean;
  error: string | null;
  pageCount: number;
}

export const usePdfRenderer = () => {
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [pageCount, setPageCount] = useState<number>(0);
  const [pdfDocument, setPdfDocument] = useState<pdfjsLib.PDFDocumentProxy | null>(null);
  const renderTaskRef = useRef<pdfjsLib.RenderTask | null>(null);

  const loadPdfDocument = useCallback(async (file: File) => {
    try {
      setLoading(true);
      setError(null);

      const arrayBuffer = await file.arrayBuffer();
      const loadingTask = pdfjsLib.getDocument({ data: arrayBuffer });
      const pdf = await loadingTask.promise;

      setPdfDocument(pdf);
      setPageCount(pdf.numPages);

      return pdf;
    } catch (err: any) {
      setError(`Failed to load PDF: ${err.message}`);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const renderPage = useCallback(async (
    canvas: HTMLCanvasElement,
    file: File,
    pageNumber: number = 1,
    scale: number = 1.5
  ): Promise<{ width: number; height: number }> => {
    try {
      // Cancel any ongoing render operation
      if (renderTaskRef.current) {
        renderTaskRef.current.cancel();
        renderTaskRef.current = null;
      }

      setLoading(true);
      setError(null);

      // Load or reuse PDF document
      let pdf = pdfDocument;
      if (!pdf) {
        pdf = await loadPdfDocument(file);
      }

      // Get the page
      const page = await pdf.getPage(pageNumber);
      const viewport = page.getViewport({ scale });

      // Prepare canvas
      const context = canvas.getContext('2d');
      if (!context) {
        throw new Error('Could not get canvas context');
      }

      canvas.height = viewport.height;
      canvas.width = viewport.width;

      // Render PDF page
      const renderContext = {
        canvasContext: context,
        viewport: viewport,
      };

      const renderTask = page.render(renderContext);
      renderTaskRef.current = renderTask;

      await renderTask.promise;
      renderTaskRef.current = null;

      return {
        width: viewport.width,
        height: viewport.height,
      };
    } catch (err: any) {
      if (err.name === 'RenderingCancelledException') {
        // Rendering was cancelled, not an error
        return { width: 0, height: 0 };
      }
      setError(`Failed to render page: ${err.message}`);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [pdfDocument, loadPdfDocument]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (pdfDocument) {
        pdfDocument.destroy();
      }
    };
  }, [pdfDocument]);

  return {
    renderPage,
    loading,
    error,
    pageCount,
  };
};
