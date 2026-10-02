import json, urllib.request, xml.etree.ElementTree as ET
from pathlib import Path
from email.utils import parsedate_to_datetime
from datetime import timezone

BLOGS = [{'title': '시간으로부터의 자유', 'id': 'calmwaves', 'url': 'https://blog.naver.com/calmwaves'}, {'title': '쏘쟁', 'id': 'zenwolf', 'url': 'https://blog.naver.com/zenwolf'}, {'title': '트루카피', 'id': 'audi72', 'url': 'https://blog.naver.com/audi72'}]

def txt(el, name):
    n=el.find(name)
    return (n.text or "").strip() if n is not None else ""

out={}
for b in BLOGS:
    url=f"https://rss.blog.naver.com/{b['id']}.xml"
    try:
        req=urllib.request.Request(url, headers={
            "User-Agent":"Mozilla/5.0 GitHubActions BookmarkDashboard/1.0",
            "Accept":"application/rss+xml, application/xml, text/xml, */*"
        })
        with urllib.request.urlopen(req, timeout=20) as r:
            xml=r.read()
        root=ET.fromstring(xml)
        item=root.find("./channel/item")
        if item is None:
            raise RuntimeError("RSS item 없음")
        pub=txt(item,"pubDate")
        try:
            dt=parsedate_to_datetime(pub)
            if dt.tzinfo is None: dt=dt.replace(tzinfo=timezone.utc)
            pub_iso=dt.isoformat()
        except Exception:
            pub_iso=pub
        out[b["id"]]={
            "blogTitle":b["title"],
            "blogUrl":b["url"],
            "postTitle":txt(item,"title"),
            "postUrl":txt(item,"link") or b["url"],
            "pubDate":pub_iso,
            "ok":True
        }
    except Exception as e:
        out[b["id"]]={"blogTitle":b["title"],"blogUrl":b["url"],"ok":False,"error":str(e)}

Path("data").mkdir(exist_ok=True)
Path("data/latest.json").write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps(out,ensure_ascii=False,indent=2))
