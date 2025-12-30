from pydantic import BaseModel
from typing import List, Dict, Optional


class RegionRequest(BaseModel):
    x: int
    y: int
    width: int
    height: int


class PatternSearchRequestModel(BaseModel):
    pattern_region: RegionRequest
    page: int


class PatternMatchResponse(BaseModel):
    region: RegionRequest
    page: int
    text: str
    confidence: float


class ColumnRegionRequest(BaseModel):
    column_name: str
    region: RegionRequest
    page: int
    group_id: Optional[str] = None


class SeparatedColumnConfigRequest(BaseModel):
    region: RegionRequest
    page: int
    separator: str
    index_to_column: Dict[int, str]
    group_id: Optional[str] = None


class PatternExtractionRequest(BaseModel):
    pattern_search: PatternSearchRequestModel
    column_regions: List[ColumnRegionRequest]
    separated_configs: Optional[List[SeparatedColumnConfigRequest]] = None
    key_column_name: Optional[str] = None
