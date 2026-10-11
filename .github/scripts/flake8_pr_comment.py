"""Post flake8 results on a pull request.

The workflow runs flake8 first and writes flake8-report.txt. This script
then does three things:

1. Reads which lines the pull request changed, from the pulls files API.
2. Updates one summary comment on the pull request conversation.
3. Adds inline review comments on changed lines that flake8 flagged.

The process exits 1 when a changed line has a finding, which fails the
GitHub Actions job. Findings on lines the pull request did not change are
counted in the summary and do not fail the check.
"""

import json
import os
import re
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass

MARKER = "<!-- flake8-report -->"
INLINE_MARKER = "<!-- flake8:{code} -->"
HUNK = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@")
MAX_INLINE = 20
API_VERSION = "2022-11-28"


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    col: int
    code: str
    text: str


class GitHubAPIError(Exception):
    def __init__(self, method, url, status, detail):
        self.method = method
        self.url = url
        self.status = status
        self.detail = detail
        hint = ""
        if status == 403:
            hint = (
                " A 403 on a fork pull request is expected: "
                "GITHUB_TOKEN is read-only there."
            )
        message = (
            f"GitHub API {method} {url} failed: {status} {detail}.{hint}"
        )
        super().__init__(message)


def parse_report(text):
    findings = []
    for raw in text.splitlines():
        if not raw.strip():
            continue
        path, row, col, code, *rest = raw.split("::")
        if path.startswith("./"):
            path = path[2:]
        findings.append(
            Finding(path, int(row), int(col), code, "::".join(rest))
        )
    return findings


def added_lines(patch):
    """Line numbers in the new file that this patch adds or replaces.

    A modified line is a removed line followed by an added line. Only the
    added line exists in the pull request branch, and that is the line a
    review comment can be attached to. Context lines (no + or -) stay in
    the file but were not changed, so they are not included.
    """
    if not patch:
        return set()
    added = set()
    new_line = None
    for line in patch.splitlines():
        match = HUNK.match(line)
        if match:
            new_line = int(match.group(1))
            continue
        if new_line is None or line.startswith("\\"):
            continue
        if line.startswith("+"):
            added.add(new_line)
            new_line += 1
        elif line.startswith("-"):
            continue
        else:
            new_line += 1
    return added


def request(method, url, token, body=None):
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", API_VERSION)
    if body is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as response:
            payload = response.read().decode()
            parsed = json.loads(payload) if payload else None
            return parsed, response.headers
    except urllib.error.HTTPError as error:
        detail = error.read().decode()
        raise GitHubAPIError(method, url, error.code, detail) from error


def next_url(headers):
    link = headers.get("Link")
    if not link:
        return None
    for part in link.split(","):
        if 'rel="next"' in part:
            return part.split(";")[0].strip()[1:-1]
    return None


def get_all(url, token):
    items = []
    while url:
        payload, headers = request("GET", url, token)
        items.extend(payload)
        url = next_url(headers)
    return items


def summary_body(diff_findings, other_count, posted, run_url, review_error=""):
    lines = [
        MARKER,
        "### flake8",
        "",
        "Inline comments are posted on lines this pull request changes. "
        "The check fails only for those lines. Findings elsewhere in the "
        "repository are counted below and do not fail the check.",
        "",
        f"- Findings on changed lines: **{len(diff_findings)}**",
        f"- New inline comments this run: **{posted}**",
        f"- Other findings, not on this diff: **{other_count}**",
        "",
    ]
    if not diff_findings:
        lines.append(
            "No flake8 findings on the lines changed in this pull request."
        )
    else:
        lines.extend(
            [
                "| File | Line | Code | Message |",
                "| --- | --- | --- | --- |",
            ]
        )
        shown = diff_findings[:40]
        for finding in shown:
            message = finding.text.replace("|", "\\|")
            lines.append(
                f"| `{finding.path}` | {finding.line} "
                f"| `{finding.code}` | {message} |"
            )
        if len(diff_findings) > len(shown):
            lines.append("")
            hidden = len(diff_findings) - len(shown)
            lines.append(f"...and {hidden} more.")
    if review_error:
        lines.extend(
            [
                "",
                "Inline comments could not be posted:",
                "",
                "```",
                review_error,
                "```",
            ]
        )
    lines.extend(["", f"[View the run]({run_url})"])
    return "\n".join(lines) + "\n"


def inline_body(finding):
    marker = INLINE_MARKER.format(code=finding.code)
    return f"{marker}\n`{finding.code}` {finding.text}"


def already_commented(comments, finding):
    marker = INLINE_MARKER.format(code=finding.code)
    for comment in comments:
        if comment.get("path") != finding.path:
            continue
        if comment.get("line") != finding.line:
            continue
        if marker in (comment.get("body") or ""):
            return True
    return False


def workflow_escape(text):
    return text.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")


def annotate(finding):
    # ::error is a workflow command. GitHub shows it on the changed file
    # in the Checks tab. It is separate from the review comment API.
    message = workflow_escape(f"{finding.code} {finding.text}")
    print(
        f"::error file={finding.path},line={finding.line},"
        f"col={finding.col}::{message}"
    )


def upsert_summary(api, repo, pr_number, token, body):
    comments = get_all(
        f"{api}/repos/{repo}/issues/{pr_number}/comments?per_page=100",
        token,
    )
    existing = next(
        (
            comment
            for comment in comments
            if (comment.get("body") or "").startswith(MARKER)
        ),
        None,
    )
    if existing:
        request(
            "PATCH",
            f"{api}/repos/{repo}/issues/comments/{existing['id']}",
            token,
            {"body": body},
        )
        return
    request(
        "POST",
        f"{api}/repos/{repo}/issues/{pr_number}/comments",
        token,
        {"body": body},
    )


def main():
    token = os.environ["GITHUB_TOKEN"]
    repo = os.environ["GITHUB_REPOSITORY"]
    pr_number = os.environ["PR_NUMBER"]
    head_sha = os.environ["HEAD_SHA"]
    api = os.environ.get("GITHUB_API_URL", "https://api.github.com")
    report_path = os.environ.get("FLAKE8_REPORT", "flake8-report.txt")
    server = os.environ.get("GITHUB_SERVER_URL", "https://github.com")
    run_id = os.environ.get("GITHUB_RUN_ID", "")
    run_url = f"{server}/{repo}/actions/runs/{run_id}"

    with open(report_path, encoding="utf-8") as report:
        findings = parse_report(report.read())

    files = get_all(
        f"{api}/repos/{repo}/pulls/{pr_number}/files?per_page=100",
        token,
    )
    changed = {
        changed_file["filename"]: added_lines(changed_file.get("patch"))
        for changed_file in files
    }
    diff_findings = [
        finding
        for finding in findings
        if finding.line in changed.get(finding.path, ())
    ]
    other_count = len(findings) - len(diff_findings)

    review_comments = get_all(
        f"{api}/repos/{repo}/pulls/{pr_number}/comments?per_page=100",
        token,
    )
    to_post = [
        finding
        for finding in diff_findings
        if not already_commented(review_comments, finding)
    ][:MAX_INLINE]

    for finding in diff_findings:
        annotate(finding)
        print(
            f"{finding.path}:{finding.line}:{finding.col}: "
            f"{finding.code} {finding.text}"
        )

    posted = 0
    review_error = ""
    if to_post:
        try:
            request(
                "POST",
                f"{api}/repos/{repo}/pulls/{pr_number}/reviews",
                token,
                {
                    "commit_id": head_sha,
                    "event": "COMMENT",
                    "comments": [
                        {
                            "path": finding.path,
                            "line": finding.line,
                            "side": "RIGHT",
                            "body": inline_body(finding),
                        }
                        for finding in to_post
                    ],
                },
            )
            posted = len(to_post)
        except GitHubAPIError as error:
            review_error = str(error)
            print(review_error, file=sys.stderr)

    upsert_summary(
        api,
        repo,
        pr_number,
        token,
        summary_body(
            diff_findings, other_count, posted, run_url, review_error
        ),
    )

    if review_error:
        sys.exit(1)
    if diff_findings:
        count = len(diff_findings)
        print(
            f"flake8 found {count} issue(s) on changed lines.",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
