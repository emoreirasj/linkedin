#!/usr/bin/env python3
"""
Publish a text post to the authenticated member's own LinkedIn profile using
the official Posts API (scope w_member_social). Standard library only.

    python3 publish.py whoami                 # check the token, show who it posts as
    python3 publish.py post draft.txt         # preview only, nothing is sent
    python3 publish.py post draft.txt --yes   # publish for real

The access token comes from LINKEDIN_ACCESS_TOKEN or, if unset, from
~/.claude/linkedin/token (one line, chmod 600). It is never printed.
"""

import argparse
import json
import os
import re
import stat
import sys
import urllib.error
import urllib.request

API = "https://api.linkedin.com"
TOKEN_FILE = os.path.expanduser("~/.claude/linkedin/token")
# LinkedIn sunsets each monthly version after about a year; override with
# LINKEDIN_VERSION=YYYYMM when this one stops being accepted.
DEFAULT_VERSION = "202609"
MAX_CHARS = 3000

# Reserved characters of LinkedIn's "little" text format, used by the
# commentary field. Left unescaped, they can cut the post short.
RESERVED_RE = re.compile(r"([\\|{}@\[\]()<>#*_~])")


def load_token():
    token = os.environ.get("LINKEDIN_ACCESS_TOKEN", "").strip()
    if token:
        return token
    if not os.path.exists(TOKEN_FILE):
        sys.exit(
            "No token. Set LINKEDIN_ACCESS_TOKEN or save it to "
            f"{TOKEN_FILE} (see docs/configurar-api-linkedin.md)."
        )
    mode = os.stat(TOKEN_FILE).st_mode
    if mode & (stat.S_IRWXG | stat.S_IRWXO):
        print(f"warning: {TOKEN_FILE} is readable by others; run chmod 600 on it",
              file=sys.stderr)
    with open(TOKEN_FILE, encoding="utf-8") as fh:
        return fh.read().strip()


def request(method, path, token, body=None, rest=False):
    headers = {"Authorization": f"Bearer {token}"}
    if rest:
        headers["LinkedIn-Version"] = os.environ.get("LINKEDIN_VERSION", DEFAULT_VERSION)
        headers["X-Restli-Protocol-Version"] = "2.0.0"
    data = None
    if body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(API + path, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8")
            return resp.status, resp.headers, json.loads(raw) if raw else {}
    except urllib.error.HTTPError as err:
        detail = err.read().decode("utf-8", "replace")
        hint = ""
        if err.code == 401:
            hint = "\nThe token is invalid or expired (tokens last 60 days). Generate a new one."
        elif err.code == 403:
            hint = "\nThe token lacks a scope. It needs openid, profile and w_member_social."
        elif err.code == 426:
            hint = "\nLinkedIn-Version is no longer accepted. Set LINKEDIN_VERSION=YYYYMM to a recent month."
        sys.exit(f"LinkedIn API error {err.code}: {detail}{hint}")


def whoami(token):
    _, _, info = request("GET", "/v2/userinfo", token)
    return info


def escape(text):
    return RESERVED_RE.sub(r"\\\1", text)


def cmd_whoami(_args):
    info = whoami(load_token())
    print(f"name:   {info.get('name')}")
    print(f"author: urn:li:person:{info.get('sub')}")


def cmd_post(args):
    if args.file == "-":
        text = sys.stdin.read()
    else:
        with open(args.file, encoding="utf-8") as fh:
            text = fh.read()
    text = text.strip()
    if not text:
        sys.exit("The post is empty.")
    if len(text) > MAX_CHARS:
        sys.exit(f"The post has {len(text)} characters; LinkedIn allows {MAX_CHARS}.")
    if "{{" in text:
        sys.exit("The post still has a {{placeholder}}. Fill it in first.")

    print("-" * 60)
    print(text)
    print("-" * 60)
    print(f"{len(text)} characters")
    if not args.yes:
        print("Preview only. Nothing was sent. Run again with --yes to publish.")
        return

    token = load_token()
    info = whoami(token)
    body = {
        "author": f"urn:li:person:{info['sub']}",
        "commentary": escape(text),
        "visibility": args.visibility,
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": [],
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False,
    }
    _, headers, _ = request("POST", "/rest/posts", token, body, rest=True)
    urn = headers.get("x-restli-id", "")
    print(f"Published as {info.get('name')}.")
    if urn:
        print(f"https://www.linkedin.com/feed/update/{urn}/")


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("whoami", help="check the token").set_defaults(func=cmd_whoami)
    post = sub.add_parser("post", help="preview or publish a post")
    post.add_argument("file", help="text file with the post, or - for stdin")
    post.add_argument("--yes", action="store_true", help="actually publish")
    post.add_argument("--visibility", choices=["PUBLIC", "CONNECTIONS"], default="PUBLIC")
    post.set_defaults(func=cmd_post)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
