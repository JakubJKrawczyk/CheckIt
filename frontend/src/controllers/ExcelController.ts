// src/utils/ExcelController.ts

interface DuplicateColumnAction {
  column: string;
  action: "first" | "last" | "min" | "max" | "sum" | "custom";
  customValue?: string;
}

interface ColumnPair {
  file1Column: string;
  file2Column: string;
}

interface ApiResponse<T = any> {
  success?: {
    message: string;
    data?: T;
  };
  error?: {
    type: string;
    message: string;
    details?: string;
  };
}

class ExcelController {
  private baseUrl: string;

  constructor(baseUrl: string = "http://localhost:21370") {
    this.baseUrl = baseUrl;
  }

  private logRequest(method: string, endpoint: string) {
    console.log(`→ ${method} ${endpoint}`);
  }

  private logError(endpoint: string, error: any) {
    console.error(`❌ API Error [${endpoint}]:`);
    if (error.type) console.error(`   Type: ${error.type}`);
    if (error.message) console.error(`   Message: ${error.message}`);
    if (error.details) console.error(`   Details: ${error.details}`);
    console.error(`   Full error:`, error);
  }

  private logSuccess(endpoint: string, message?: string) {
    console.log(`✓ ${endpoint}`, message || "OK");
  }

  async browseFile(): Promise<{ path: string | null; error?: string }> {
    const endpoint = "/api/browse/file";
    this.logRequest("GET", endpoint);

    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`);
      const result: ApiResponse = await response.json();

      if (result.error) {
        this.logError(endpoint, result.error);
        return { path: null, error: result.error.message };
      }

      this.logSuccess(endpoint, result.success?.message ? `File: ${result.success.message}` : "No file selected");
      return { path: result.success?.message || null };
    } catch (err: any) {
      console.error(`❌ Network error [${endpoint}]:`, err.message);
      return { path: null, error: err.message };
    }
  }

  async fetchColumns(filePath: string): Promise<{ columns: string[]; error?: string }> {
    const endpoint = "/api/extract/excel/columns";
    this.logRequest("GET", endpoint);

    try {
      const params = new URLSearchParams({ excel_file_path: filePath });
      const response = await fetch(`${this.baseUrl}${endpoint}?${params}`);
      const result: ApiResponse<string[]> = await response.json();

      if (result.error) {
        this.logError(endpoint, result.error);
        return { columns: [], error: result.error.message };
      }

      this.logSuccess(endpoint, `${result.success?.data?.length || 0} columns`);
      return { columns: result.success?.data || [] };
    } catch (err: any) {
      console.error(`❌ Network error [${endpoint}]:`, err.message);
      return { columns: [], error: err.message };
    }
  }

  async checkDuplicates(
    filePath: string,
    keyColumn: string
  ): Promise<{ hasDuplicates: boolean; duplicateCount: number; error?: string }> {
    const endpoint = "/api/check-duplicates";
    this.logRequest("POST", endpoint);

    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ file_path: filePath, key_column: keyColumn }),
      });
      const result: ApiResponse = await response.json();

      if (result.error) {
        this.logError(endpoint, result.error);
        return { hasDuplicates: false, duplicateCount: 0, error: result.error.message };
      }

      const hasDuplicates = result.success?.data?.has_duplicates || false;
      const duplicateCount = result.success?.data?.duplicate_keys_count || 0;

      this.logSuccess(
        endpoint,
        hasDuplicates ? `Found ${duplicateCount} duplicate keys` : "No duplicates"
      );
      return { hasDuplicates, duplicateCount };
    } catch (err: any) {
      console.error(`❌ Network error [${endpoint}]:`, err.message);
      return { hasDuplicates: false, duplicateCount: 0, error: err.message };
    }
  }

  async compareFiles(params: {
    file1Path: string;
    file1KeyColumn: string;
    file1DuplicateActions: DuplicateColumnAction[];
    file2Path: string;
    file2KeyColumn: string;
    file2DuplicateActions: DuplicateColumnAction[];
    columnPairs: ColumnPair[];
  }): Promise<{
    differences: any[];
    isEqual: boolean;
    error?: string;
  }> {
    const endpoint = "/api/compare";
    this.logRequest("POST", endpoint);

    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          file1_path: params.file1Path,
          file1_key_column: params.file1KeyColumn,
          file1_duplicate_actions: params.file1DuplicateActions,
          file2_path: params.file2Path,
          file2_key_column: params.file2KeyColumn,
          file2_duplicate_actions: params.file2DuplicateActions,
          column_pairs: params.columnPairs,
        }),
      });

      const result: ApiResponse = await response.json();

      if (result.error) {
        this.logError(endpoint, result.error);
        return {
          differences: [],
          isEqual: false,
          error: result.error.details || result.error.message,
        };
      }

      const differences = result.success?.data?.result || [];
      const isEqual = result.success?.data?.is_equal || false;

      this.logSuccess(
        endpoint,
        isEqual ? "Files are equal" : `Found ${differences.length} differences`
      );
      return { differences, isEqual };
    } catch (err: any) {
      console.error(`❌ Network error [${endpoint}]:`, err.message);
      return { differences: [], isEqual: false, error: err.message };
    }
  }
}

export const excelController = new ExcelController();