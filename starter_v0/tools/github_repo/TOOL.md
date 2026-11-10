---
name: github_repo
track: bonus
kind: live_api
provider: GitHub REST API
requires_env: []
inputs: [repo, max_releases]
outputs: [repo, url, description, stars, forks, language, license, pushed_at, releases, items]
side_effect: false
---
# github_repo

Fetches repository metadata (stars, forks, primary language, license, latest push timestamp)
and up to `max_releases` recent releases for a specific GitHub repository (`owner/name`)
via the GitHub REST API.

Optional environment variable: `GITHUB_TOKEN` (increases GitHub API rate limit, not required).

