#!/usr/bin/env python3
"""
fetch_avatar.py — download the current avatar straight from a GitHub
profile, no manual photo upload required.

GitHub serves every user's live avatar at a stable, unauthenticated URL:

    https://github.com/<username>.png

That redirects to whatever avatar is currently set on the profile, so
re-running this script always grabs the latest photo — this is what lets
the portrait auto-update if you ever change your GitHub picture.

Usage:
    python scripts/fetch_avatar.py Berosin
Output:
    source-photo.png (in the current directory)
"""
import sys
import argparse
import requests


def fetch_avatar(username: str, output_path: str = "source-photo.png", size: int = 460) -> str:
    # `?size=` requests a specific resolution from GitHub's avatar CDN.
    url = f"https://github.com/{username}.png?size={size}"
    print(f"Fetching avatar for '{username}' ...")
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()

    with open(output_path, "wb") as f:
        f.write(resp.content)

    print(f"Saved: {output_path} ({len(resp.content)} bytes)")
    return output_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("username", help="GitHub username, e.g. Berosin")
    parser.add_argument("-o", "--output", default="source-photo.png")
    parser.add_argument("--size", type=int, default=460)
    args = parser.parse_args()

    try:
        fetch_avatar(args.username, args.output, args.size)
    except requests.RequestException as e:
        print(f"Failed to fetch avatar: {e}", file=sys.stderr)
        sys.exit(1)