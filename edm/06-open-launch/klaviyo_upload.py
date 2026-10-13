"""Push the two 06-open launch emails into Klaviyo as drafts.

What it does (nothing is sent or scheduled):
  1. Uploads the 4 local images in assets/ to the Klaviyo image library
     (cached in klaviyo_assets.json so a re-run never uploads twice).
  2. Writes dist/06-open-public.html and dist/06-open-waitlist.html with the
     assets/... paths swapped for the Klaviyo CDN URLs.
  3. Creates two CODE templates from those files.
  4. With --public-list/--waitlist-segment: creates two DRAFT campaigns
     (Oct 13 2026, 8:00 AM New York prefilled) and attaches the templates.
     Scheduling stays a manual click in Klaviyo after test sends.

Usage (stdlib only, Python 3.9+):
  export KLAVIYO_API_KEY=pk_...        # private key: images, templates, campaigns write
  python3 klaviyo_upload.py                    # dry run, prints the plan
  python3 klaviyo_upload.py --apply            # images + templates
  python3 klaviyo_upload.py --apply \\
      --public-list <LIST_OR_SEGMENT_ID> --waitlist-segment <SEGMENT_ID> \\
      --from-email hi@ronini.com --from-label Ronini          # + draft campaigns
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request
import uuid
from pathlib import Path

HERE = Path(__file__).parent
API = "https://a.klaviyo.com/api"
REVISION = os.environ.get("KLAVIYO_REVISION", "2024-10-15")
CACHE = HERE / "klaviyo_assets.json"

IMAGES = ["bottle-5oz.png", "bottle-8oz.png", "burst-10.png", "venting-tube.png"]
EMAILS = {
    "public": dict(file="06-open-public.html", name="06-open · PUBLIC · Oct 13",
                   subject="Ronini is open.",
                   preview="The Wrapped Glass Bottle: glass inside, silicone molded on. From $60 a pair."),
    "waitlist": dict(file="06-open-waitlist.html", name="06-open · WAITLIST · Oct 13",
                     subject="Ronini is open. Your 15% code is inside.",
                     preview="Good through Sunday, October 18, with a free Venting Tube 2-pack on your first order."),
}
# Oct 13 2026 08:00 America/New_York (EDT, UTC-4)
SEND_AT = "2026-10-13T12:00:00+00:00"


def call(method, path, body=None, key=None, raw=None, ctype=None):
    headers = {"Authorization": f"Klaviyo-API-Key {key}", "revision": REVISION,
               "accept": "application/vnd.api+json"}
    data = raw
    if body is not None:
        data = json.dumps(body).encode()
        headers["content-type"] = "application/vnd.api+json"
    if ctype:
        headers["content-type"] = ctype
    req = urllib.request.Request(f"{API}/{path}", data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req) as r:
            txt = r.read().decode()
            return json.loads(txt) if txt else {}
    except urllib.error.HTTPError as e:
        sys.exit(f"{method} {path} -> {e.code}\n{e.read().decode()}")


def upload_image(path, key):
    boundary = uuid.uuid4().hex
    parts = []
    for name, value in (("name", path.stem), ("hidden", "false")):
        parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"\r\n\r\n{value}\r\n'.encode())
    parts.append((f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="{path.name}"\r\n'
                  f'Content-Type: image/png\r\n\r\n').encode() + path.read_bytes() + b"\r\n")
    parts.append(f"--{boundary}--\r\n".encode())
    res = call("POST", "image-upload/", key=key, raw=b"".join(parts),
               ctype=f"multipart/form-data; boundary={boundary}")
    return res["data"]["attributes"]["image_url"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="actually call Klaviyo (default: dry run)")
    ap.add_argument("--public-list", help="list/segment id(s) for the public send, comma-separated")
    ap.add_argument("--waitlist-segment", help="waitlist segment id (also excluded from public)")
    ap.add_argument("--from-email")
    ap.add_argument("--from-label", default="Ronini")
    a = ap.parse_args()
    key = os.environ.get("KLAVIYO_API_KEY")
    if a.apply and not key:
        sys.exit("Set KLAVIYO_API_KEY first.")

    # 1. images
    urls = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    for img in IMAGES:
        if img in urls:
            print(f"image  {img}: cached {urls[img]}")
        elif a.apply:
            urls[img] = upload_image(HERE / "assets" / img, key)
            CACHE.write_text(json.dumps(urls, indent=2))
            print(f"image  {img}: uploaded {urls[img]}")
        else:
            print(f"image  {img}: would upload")

    # 2. html with CDN urls
    out = HERE / "dist"
    out.mkdir(exist_ok=True)
    html = {}
    for k, e in EMAILS.items():
        s = (HERE / e["file"]).read_text()
        for img, u in urls.items():
            s = s.replace(f"assets/{img}", u)
        left = [img for img in IMAGES if f"assets/{img}" in s]
        (out / e["file"]).write_text(s)
        html[k] = s
        print(f"html   dist/{e['file']}" + (f"  (still local: {left})" if left else "  (all images on Klaviyo)"))
    if not a.apply:
        print("\nDry run only. Re-run with --apply.")
        return

    # 3. templates
    tpl = {}
    for k, e in EMAILS.items():
        res = call("POST", "templates/", key=key, body={"data": {"type": "template", "attributes": {
            "name": e["name"], "editor_type": "CODE", "html": html[k]}}})
        tpl[k] = res["data"]["id"]
        print(f"template {e['name']}: {tpl[k]}")

    # 4. draft campaigns
    if not (a.public_list and a.waitlist_segment):
        print("\nNo --public-list/--waitlist-segment: stopping after templates.")
        return
    audiences = {
        "public": {"included": a.public_list.split(","), "excluded": [a.waitlist_segment]},
        "waitlist": {"included": [a.waitlist_segment], "excluded": []},
    }
    for k, e in EMAILS.items():
        content = {"subject": e["subject"], "preview_text": e["preview"], "from_label": a.from_label}
        if a.from_email:
            content["from_email"] = a.from_email
        res = call("POST", "campaigns/", key=key, body={"data": {"type": "campaign", "attributes": {
            "name": e["name"],
            "audiences": audiences[k],
            "send_strategy": {"method": "static", "options_static": {"datetime": SEND_AT, "is_local": False}},
            "campaign-messages": {"data": [{"type": "campaign-message", "attributes": {
                "channel": "email", "label": e["name"], "content": content}}]},
        }}})
        cid = res["data"]["id"]
        mid = res["data"]["relationships"]["campaign-messages"]["data"][0]["id"]
        call("POST", "campaign-message-assign-template/", key=key, body={"data": {
            "type": "campaign-message", "id": mid,
            "relationships": {"template": {"data": {"type": "template", "id": tpl[k]}}}}})
        print(f"campaign {e['name']}: {cid} (draft, template attached)")
    print("\nDone. In Klaviyo: send a test of each, check EARLY15 + the discount link, then schedule.")


if __name__ == "__main__":
    main()
