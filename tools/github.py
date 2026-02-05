from crewai import Tool
import httpx


def search_github_repos(query: str) -> str:
    """Search GitHub repositories by query"""
    try:
        url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page=5"
        resp = httpx.get(
            url,
            timeout=10.0,
            headers={"Accept": "application/vnd.github.v3+json"},
        )
        resp.raise_for_status()

        repos = resp.json().get("items", [])
        results = [
            f"{r['name']}: {r['stargazers_count']} stars - {(r['description'] or 'No description')[:100]}"
            for r in repos
        ]
        return "\n".join(results) or "No repos found."

    except Exception as e:
        return f"Error searching GitHub: {str(e)}"


GitHubTool = Tool.from_function(
    name="github_tool",
    description="Search GitHub repos by topic, get top starred",
    func=search_github_repos,
)
