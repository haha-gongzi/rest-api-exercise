from typing import Any, Dict, List
import requests


class FDAClientError(Exception):
    pass


def fetch_drug_labels(query: str, limit: int = 3, skip: int = 0) -> Dict[str, Any]:
    # openFDA drug label endpoint
    url = "https://api.fda.gov/drug/label.json"
    params = {
        "search": query,
        "limit": limit,
        "skip": skip,
    }
    try:
        r = requests.get(url, params=params, timeout=10)
    except requests.RequestException as e:
        raise FDAClientError(f"Network error: {e}") from e

    # openFDA sometimes returns 404 for no results
    if r.status_code == 404:
        return {"results": [], "meta": {"note": "no results"}}

    if r.status_code != 200:
        raise FDAClientError(f"openFDA HTTP {r.status_code}: {r.text[:200]}")

    data = r.json()
    if "error" in data:
        # invalid query etc.
        return {"results": [], "meta": {"note": str(data['error'])}}

    return data


def _first_str(value: Any) -> str:
    if isinstance(value, list) and value:
        return str(value[0])
    if value is None:
        return ""
    return str(value)


def build_note_text_from_fda(data: Dict[str, Any], query: str, limit: int, skip: int) -> str:
    results: List[Dict[str, Any]] = data.get("results", []) or []
    lines: List[str] = []
    lines.append("openFDA drug/label search")
    lines.append(f"query={query!r}, limit={limit}, skip={skip}, results={len(results)}")

    if not results:
        lines.append("No results found.")
        return "\n".join(lines)

    for i, item in enumerate(results, start=1):
        openfda = item.get("openfda", {}) or {}
        brand = _first_str(openfda.get("brand_name"))
        generic = _first_str(openfda.get("generic_name"))
        purpose = _first_str(item.get("purpose"))
        warnings = _first_str(item.get("warnings"))

        warnings_short = warnings[:300].replace("\n", " ").strip()
        if len(warnings) > 300:
            warnings_short += "..."

        lines.append("")
        lines.append(f"{i}. brand={brand or 'N/A'}; generic={generic or 'N/A'}")
        lines.append(f"   purpose={purpose or 'N/A'}")
        lines.append(f"   warnings={warnings_short or 'N/A'}")

    return "\n".join(lines)
