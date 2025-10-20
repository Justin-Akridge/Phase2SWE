from typing import Optional, List
from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel

from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

app = FastAPI()

#frontend
app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    with open("templates/index.html") as f:
        return f.read()

#api spec

class PackageRating(BaseModel):
    NetScore: float
    BusFactor: float
    CodeQuality: float
    DatasetAndCode: float
    DatasetQuality: float
    License: float
    PerformanceClaims: float
    RampUp: float
    Size: float
    Reproducibility: float
    Reviewedness: float
    Treescore: float

class PackageInfo(BaseModel):
    ID: str
    Name: str
    Version: str

class LineageGraph(BaseModel):
    pass

@app.post("/package")
async def upload_package():
    pass

@app.get("/package/{package_id}/rate")
async def rate_package(package_id: str) -> PackageRating:

    # TODO find package and rate with metrics
    return PackageRating(
        NetScore          = 0,
        BusFactor         = 0,
        CodeQuality       = 0,
        DatasetAndCode    = 0,
        DatasetQuality    = 0,
        License           = 0,
        PerformanceClaims = 0,
        RampUp            = 0,
        Size              = 0,
        Reproducibility   = 0,
        Reviewedness      = 0,
        Treescore         = 0 
    )

@app.get("/package/{package_id}/download")
async def download_package(
    package_id: str,
    part: Optional[str] = Query(None, description="full, weights, or datasets")
):
    if part == "weights":
        pass
    elif part == "datasets":
        pass
    # return all
    else:
        pass

    return FileResponse("path/to/file.zip", filename="model.zip")

@app.post("/package/ingest")
async def ingest_huggingface_model(
    huggingface_url: str
):
    ratings = {}

    if any(score < 0.5 for score in ratings.values()):
        raise HTTPException(400, "Model does not meet quality threshold")

    return {"message": "Model ingested", "id": "package-id"}


@app.get("/packages")
async def list_packages(
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    name: Optional[str] = None,
    version: Optional[str] = None
) -> List[PackageInfo]:

    packages = []
    return packages

@app.get("/packages/search")
async def search_packages(
    query: str,
    field: str = Query("name", description="name")
):
    return []

@app.get("/packages/byVersion")
async def search_by_version(
    version: str
):
    return []

@app.get("/package/{package_id}/lineage")
async def get_lineage_graph(package_id: str) -> LineageGraph:
    return {}

@app.get("/package/{package_id}/cost")
async def get_size_cost(package_id: str):
    return {"size_bytes": 1234567, "size_mb": 1.23}

@app.post("/package/license-check")
async def check_license_compatibility(
    github_url: str,
    model_id: str
):
    return {"compatible": True, "reason": "Both MIT licensed"}

@app.delete("/reset")
async def reset_registry():
    return {"message": "Registry reset to default state"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "uptime": 12345,
        "requests_last_hour": 567,
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


#import sys
#import json
#from fastapi import FastAPI
#from typing import Dict, Any
#from cli.menu import Menu
#from cli.metrics.license_metric import LicenseMetric
#from cli.metrics.size_metric import SizeMetric
#from cli.metrics.bus_factor_metric import BusFactorMetric
#from cli.metrics.performance_claims_metric import PerformanceClaimsMetric
#from cli.metrics.rampup_metric import RampUpMetric
#from cli.metrics.dataset_and_code_metric import DatasetAndCodeMetric
#from cli.metrics.dataset_quality_metric import DatasetQualityMetric
#from cli.metrics.code_quality_metric import CodeQualityMetric
#
#
#WEIGHTS = {
#    "ramp_up_time": 0.20,
#    "bus_factor": 0.15,
#    "performance_claims": 0.15,
#    "license": 0.10,
#    "size_score": 0.15,
#    "dataset_and_code_score": 0.15,
#    "code_quality": 0.10,
#}
#
#
#def process_url(url: str):
#    metrics = [
#        RampUpMetric(),
#        BusFactorMetric(),
#        PerformanceClaimsMetric(),
#        LicenseMetric(),
#        SizeMetric(),
#        DatasetAndCodeMetric(),
#        DatasetQualityMetric(),
#        CodeQualityMetric(),
#    ]
#
#    metrics_results: Dict[str, Any] = {}
#    for metric in metrics:
#        metrics_results.update(metric.timed_calculate(url))
#
#
#    # Compute net_score as weighted sum
#    # size_score is an object; average its values for aggregation
#    size_obj = metrics_results.get("size_score", None)
#    size_mean = 0.0
#    if isinstance(size_obj, dict) and size_obj:
#        vals = [float(v) for v in size_obj.values()]
#        size_mean = sum(vals) / len(vals)
#
#    net = (
#        WEIGHTS["ramp_up_time"]
#        * float(metrics_results.get("ramp_up_time", 0.0))
#        + WEIGHTS["bus_factor"] * float(metrics_results.get("bus_factor", 0.0))
#        + WEIGHTS["performance_claims"]
#        * float(metrics_results.get("performance_claims", 0.0))
#        + WEIGHTS["license"] * float(metrics_results.get("license", 0.0))
#        + WEIGHTS["size_score"] * float(size_mean)
#        + WEIGHTS["dataset_and_code_score"]
#        * float(metrics_results.get("dataset_and_code_score", 0.0))
#        + WEIGHTS["code_quality"]
#        * float(metrics_results.get("code_quality", 0.0))
#    )
#
#    net = max(0.0, min(1.0, float(net)))
#    # collect net latency as sum of metric latencies
#    net_latency = sum(
#        int(v)
#        for k, v in metrics_results.items()
#        if k.endswith("_latency") and isinstance(v, (int, float))
#    )
#
#    results = metrics_results
#    results["net_score"] = net
#    results["net_score_latency"] = int(net_latency)
#
#    # Extracts name from URL, handling various formats
#    path_parts = url.split("/")
#    results["name"] = (
#        path_parts[-1]
#        if path_parts[-1] and path_parts[-1] != ""
#        else path_parts[-2]
#        if len(path_parts) > 2
#        else url
#    )
#
#    # Categorize URL type
#    if "huggingface.co/datasets" in url:
#        results["category"] = "DATASET"
#    elif "huggingface.co" in url:
#        results["category"] = "MODEL"
#    elif "github.com" in url:
#        results["category"] = "REPO"
#    else:
#        results["category"] = "UNKNOWN"
#
#    return results
#
#
#def main(argv: list[str] | None = None) -> int:
#    """CLI entrypoint.
#
#    Usage:
#      - Interactive menu: no arguments
#      - Score a urls file: main.py path/to/urls.txt
#      - Score a single URL: main.py --url https://huggingface.co/...
#    """
#    argv = argv or sys.argv[1:]
#    menu = Menu()
#
#    # no args -> interactive only when running from a terminal.
#    # When stdin is captured (for example, during pytest), behave like the
#    # previous implementation and print usage / exit so tests that call
#    # main() programmatically still receive SystemExit.
#    if not argv:
#        if sys.stdin is not None and sys.stdin.isatty():
#            menu.interactive()
#            return 0
#        # non-interactive environment: print usage and exit with error
#        print("Usage: python3 -m cli.main URL_FILE")
#        raise SystemExit(1)
#
#    # single URL via --url
#    if len(argv) >= 2 and argv[0] == "--url":
#        url = argv[1]
#        res = process_url(url)
#        print(json.dumps(res, separators=(",", ":")))
#        # Print a friendly net score summary to stderr so CLI users see it
#        net = res.get("net_score")
#        if net is not None:
#            print(f"net_score: {net}", file=sys.stderr)
#        return 0
#
#    # otherwise treat first arg as urls file
#    urls_file = argv[0]
#    urls = menu.read_urls(urls_file)
#    for u in urls:
#        result = process_url(u)
#        print(json.dumps(result, separators=(",", ":")))
#        # Also emit a simple net score line to stderr for visibility
#        net = result.get("net_score")
#        if net is not None:
#            print(f"net_score: {net}", file=sys.stderr)
#    return 0
#
#
#if __name__ == "__main__":
#    raise SystemExit(main())
