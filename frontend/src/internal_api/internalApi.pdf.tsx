import axioClient from "../axioClient";

export interface Region {
    x: number;
    y: number;
    width: number;
    height: number;
}

export interface PatternSearchRequest {
    pattern_region: Region;
    page: number;
}

export interface PatternMatch {
    region: Region;
    page: number;
    text: string;
    confidence: number;
}

export interface ColumnRegion {
    column_name: string;
    region: Region;
    page: number;
    group_id?: string;
}

export interface SeparatedColumnConfig {
    region: Region;
    page: number;
    separator: string;
    index_to_column: Record<number, string>;
    group_id?: string;
}

export interface PatternExtractionConfig {
    pattern_search: PatternSearchRequest;
    column_regions: ColumnRegion[];
    separated_configs?: SeparatedColumnConfig[];
    key_column_name?: string;
}

class PdfApi {
    async searchPattern(file: File, patternSearch: PatternSearchRequest): Promise<PatternMatch[]> {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('pattern_search', JSON.stringify(patternSearch));

        const response = await axioClient.post('/pdf/search-pattern', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });

        if (response.data.error) {
            throw new Error(response.data.error.details);
        }

        return response.data.success.data.matches;
    }

    async extractData(file: File, config: PatternExtractionConfig): Promise<any[]> {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('extraction_config', JSON.stringify(config));

        const response = await axioClient.post('/pdf/extract-data', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });

        if (response.data.error) {
            throw new Error(response.data.error.details);
        }

        return response.data.success.data.data;
    }
}

export default PdfApi;
