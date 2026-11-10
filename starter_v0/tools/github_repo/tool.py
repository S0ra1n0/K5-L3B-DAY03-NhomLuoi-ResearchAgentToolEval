from __future__ import annotations

import os
import re
from typing import Any

import requests

from tools._shared import TIMEOUT, err

_REPO_PATTERN = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")


def _validate_repo(repo: Any) -> tuple[str, str]:
    """Validate and split 'owner/name' repository identifier."""
    if not isinstance(repo, str):
        raise ValueError("repo must be a string in 'owner/name' format")
    cleaned = repo.strip()
    if not cleaned:
        raise ValueError("repo must not be empty; expected 'owner/name'")
    if "://" in cleaned or cleaned.lower().startswith("github.com/"):
        raise ValueError("repo must be 'owner/name', not a full URL")
    if "@" in cleaned:
        raise ValueError("repo must not contain '@'")
    if cleaned.lower().endswith(".git"):
        raise ValueError("repo must not end with '.git'")
    if not _REPO_PATTERN.fullmatch(cleaned):
        raise ValueError("repo must be in 'owner/name' format (e.g. 'openai/whisper')")
    owner, name = cleaned.split("/", 1)
    if owner in {".", ".."} or name in {".", ".."}:
        raise ValueError("repo owner and name must be valid identifiers")
    return owner, name


def _validate_max_releases(max_releases: Any) -> int:
    """Validate max_releases is an integer within 0..10."""
    if isinstance(max_releases, bool) or not isinstance(max_releases, int):
        raise ValueError("max_releases must be an integer between 0 and 10")
    if max_releases < 0 or max_releases > 10:
        raise ValueError("max_releases must be between 0 and 10")
    return max_releases


def _github_headers() -> dict[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": os.getenv("GITHUB_USER_AGENT", "AI20k-Day03-Research-Agent/1.0"),
    }
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _fetch_releases(owner: str, name: str, max_releases: int, headers: dict[str, str]) -> list[dict[str, Any]]:
    if max_releases == 0:
        return []
    response = requests.get(
        f"https://api.github.com/repos/{owner}/{name}/releases",
        params={"per_page": max_releases},
        headers=headers,
        timeout=TIMEOUT,
    )
    response.raise_for_status()
    raw = response.json()
    if not isinstance(raw, list):
        return []
    return [
        {
            "tag_name": item.get("tag_name"),
            "name": item.get("name"),
            "published_at": item.get("published_at"),
            "url": item.get("html_url"),
            "prerelease": bool(item.get("prerelease", False)),
        }
        for item in raw[:max_releases]
        if isinstance(item, dict)
    ]


def _extract_license(repo_data: dict[str, Any]) -> str | None:
    license_info = repo_data.get("license")
    if not isinstance(license_info, dict):
        return None
    spdx = license_info.get("spdx_id")
    if spdx and spdx != "NOASSERTION":
        return spdx
    return license_info.get("name")


def _build_summary(
    description: str | None,
    stars: Any,
    forks: Any,
    language: str | None,
    license_name: str | None,
    pushed_at: str | None,
    releases: list[dict[str, Any]],
) -> str:
    parts: list[str] = []
    if description:
        parts.append(description.strip())
    parts.append(
        f"Stars: {stars} | Forks: {forks} | Language: {language or 'N/A'} "
        f"| License: {license_name or 'N/A'} | Pushed at: {pushed_at or 'N/A'}"
    )
    if releases:
        latest_tag = releases[0].get("tag_name") or releases[0].get("name") or "unknown"
        parts.append(f"Latest release: {latest_tag}")
    return " — ".join(parts)


def get_github_repo(repo: str = "", max_releases: int = 3) -> dict[str, Any]:
    """Fetch metadata and recent releases for a specific GitHub repository."""
    try:
        owner, name = _validate_repo(repo)
        limit = _validate_max_releases(max_releases)
        headers = _github_headers()

        response = requests.get(
            f"https://api.github.com/repos/{owner}/{name}",
            headers=headers,
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        repo_data = response.json()
        if not isinstance(repo_data, dict):
            raise ValueError("Unexpected GitHub repository response payload")

        releases = _fetch_releases(owner, name, limit, headers)
        full_name = repo_data.get("full_name") or f"{owner}/{name}"
        html_url = repo_data.get("html_url") or f"https://github.com/{owner}/{name}"
        description = repo_data.get("description")
        stars = repo_data.get("stargazers_count")
        forks = repo_data.get("forks_count")
        language = repo_data.get("language")
        license_name = _extract_license(repo_data)
        pushed_at = repo_data.get("pushed_at")

        summary = _build_summary(description, stars, forks, language, license_name, pushed_at, releases)
        return {
            "tool": "github_repo",
            "repo": full_name,
            "url": html_url,
            "description": description,
            "stars": stars,
            "forks": forks,
            "language": language,
            "license": license_name,
            "pushed_at": pushed_at,
            "releases": releases,
            "items": [
                {
                    "title": full_name,
                    "url": html_url,
                    "source": "github.com",
                    "summary": summary,
                }
            ],
        }
    except Exception as exc:
        return err("github_repo", exc)

