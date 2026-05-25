"""Municipality data bundled with the EWE WattMonitor integration."""

from __future__ import annotations

import json
import unicodedata
from functools import lru_cache
from pathlib import Path
from typing import TypedDict


class Municipality(TypedDict):
    """Supported municipality metadata."""

    key: str
    name: str
    county: str
    state: str


DATA_FILE = Path(__file__).parent / "data" / "municipalities.json"
MAX_SEARCH_RESULTS = 50


@lru_cache
def load_municipalities() -> dict[str, Municipality]:
    """Load bundled supported municipalities by official municipality key."""
    with DATA_FILE.open(encoding="utf-8") as data_file:
        payload = json.load(data_file)

    municipalities = payload.get("municipalities", [])
    return {
        str(item["key"]): {
            "key": str(item["key"]),
            "name": str(item.get("name") or item["key"]),
            "county": str(item.get("county") or ""),
            "state": str(item.get("state") or ""),
        }
        for item in municipalities
    }


def municipality_label(municipality: Municipality) -> str:
    """Return a human friendly municipality label."""
    parts = [municipality["name"]]
    if municipality["county"]:
        parts.append(municipality["county"])
    if municipality["state"]:
        parts.append(municipality["state"])
    return " · ".join(parts)


def _normalize(value: str) -> str:
    """Normalize text for forgiving municipality search."""
    value = unicodedata.normalize("NFKD", value.casefold())
    return "".join(char for char in value if not unicodedata.combining(char))


@lru_cache
def municipality_options() -> list[dict[str, str]]:
    """Return selector options for all supported municipalities."""
    municipalities = load_municipalities().values()
    return [
        {"value": municipality["key"], "label": municipality_label(municipality)}
        for municipality in sorted(
            municipalities,
            key=lambda item: (item["name"], item["county"], item["key"]),
        )
    ]


def search_municipality_options(
    query: str,
    limit: int = MAX_SEARCH_RESULTS,
) -> list[dict[str, str]]:
    """Return selector options matching a search term."""
    normalized_query = _normalize(query.strip())
    if not normalized_query:
        return municipality_options()[:limit]

    matches: list[tuple[int, str, dict[str, str]]] = []
    for municipality in load_municipalities().values():
        label = municipality_label(municipality)
        normalized_label = _normalize(label)
        key = municipality["key"]
        searchable = f"{normalized_label} {key}"
        if normalized_query not in searchable:
            continue

        if key == query.strip():
            rank = 0
        elif _normalize(municipality["name"]).startswith(normalized_query):
            rank = 1
        elif normalized_query in _normalize(municipality["name"]):
            rank = 2
        elif normalized_query in _normalize(municipality["county"]):
            rank = 3
        else:
            rank = 4

        matches.append((rank, label, {"value": key, "label": label}))

    matches.sort(key=lambda item: (item[0], item[1]))
    return [option for _, _, option in matches[:limit]]
