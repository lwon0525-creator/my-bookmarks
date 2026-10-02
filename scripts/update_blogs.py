import json, urllib.request, xml.etree.ElementTree as ET
from pathlib import Path
from email.utils import parsedate_to_datetime
from datetime import timezone

BLOGS = [{'title': '시간으로부터의 자유', 'id': 'calmwaves', 'url': 'https://blog.naver.com/calmwaves', 'category': '블로그·콘텐츠'}, {'title': '쏘쟁', 'id': 'zenwolf', 'url': 'https://blog.naver.com/zenwolf', 'category': '블로그·콘텐츠'}, {'title': '트루카피', 'id': 'audi72', 'url': 'https://blog.naver.com/audi72', 'category': '블로그·콘텐츠'}, {'title': '대치대디', 'id': 'dachi-daddy', 'url': 'https://blog.naver.com/dachi-daddy', 'category': '블로그·콘텐츠'}, {'title': '망둥이', 'id': 'myouth35', 'url': 'https://blog.naver.com/myouth35', 'category': '블로그·콘텐츠'}, {'title': '라니옹', 'id': 'PostList.naver', 'url': 'https://m.blog.naver.com/PostList.naver?blogId=raniong&tab=1', 'category': '블로그·콘텐츠'}, {'title': '옥동자', 'id': 'jikolp78', 'url': 'https://blog.naver.com/jikolp78', 'category': '블로그·콘텐츠'}, {'title': '메르', 'id': 'ranto28', 'url': 'https://blog.naver.com/ranto28', 'category': '블로그·콘텐츠'}, {'title': '초보교수', 'id': 'acehigh3_2', 'url': 'https://blog.naver.com/acehigh3_2', 'category': '블로그·콘텐츠'}, {'title': '너 자산을 알라', 'id': 'PostList.naver', 'url': 'https://m.blog.naver.com/PostList.naver?blogId=goldenmore_&categoryNo=0&listStyle=post&tab=1', 'category': '블로그·콘텐츠'}, {'title': '98년생', 'id': 'xpfkwh56', 'url': 'https://blog.naver.com/xpfkwh56', 'category': '블로그·콘텐츠'}, {'title': '얼티메이텀', 'id': 'ondal0404', 'url': 'https://blog.naver.com/ondal0404', 'category': '블로그·콘텐츠'}, {'title': '따리', 'id': 'wattari2', 'url': 'https://blog.naver.com/wattari2', 'category': '블로그·콘텐츠'}, {'title': 'UQ', 'id': 'PostList.naver', 'url': 'https://m.blog.naver.com/PostList.naver?blogId=anordinarydad&tab=1', 'category': '블로그·콘텐츠'}, {'title': '숙주나물', 'id': 'PostList.naver', 'url': 'https://m.blog.naver.com/PostList.naver?blogId=ihappy0304&tab=1', 'category': '블로그·콘텐츠'}, {'title': '투자 오아시스', 'id': 'ams7899', 'url': 'https://blog.naver.com/ams7899', 'category': '블로그·콘텐츠'}, {'title': '자본주의', 'id': 'penguin0805', 'url': 'https://blog.naver.com/penguin0805', 'category': '블로그·콘텐츠'}, {'title': '성수동아저씨', 'id': 'seongsu-az', 'url': 'https://m.blog.naver.com/seongsu-az?tab=1', 'category': '블로그·콘텐츠'}, {'title': '인문학자', 'id': 'PostList.naver', 'url': 'https://m.blog.naver.com/PostList.naver?blogId=hwasikyuljeon&tab=1', 'category': '블로그·콘텐츠'}, {'title': '내 언어의 한계', 'id': 'bambooinvesting', 'url': 'https://blog.naver.com/bambooinvesting', 'category': '블로그·콘텐츠'}, {'title': '군포금융치료센터', 'id': 'doctordk', 'url': 'https://blog.naver.com/doctordk', 'category': '블로그·콘텐츠'}, {'title': '리치로드', 'id': 'robin324', 'url': 'https://blog.naver.com/robin324', 'category': '블로그·콘텐츠'}, {'title': 'Candl', 'id': 'PostList.naver', 'url': 'https://m.blog.naver.com/PostList.naver?blogId=martin332&tab=1', 'category': '블로그·콘텐츠'}, {'title': '낙민동 추노', 'id': 'gaunyu', 'url': 'https://blog.naver.com/gaunyu', 'category': '블로그·콘텐츠'}, {'title': '상해에서', 'id': 'PostList.naver', 'url': 'https://m.blog.naver.com/PostList.naver?blogId=nohappy0&tab=1', 'category': '블로그·콘텐츠'}, {'title': '월드모델 : 네이버 블로그', 'id': 'bizucafe', 'url': 'https://blog.naver.com/bizucafe/224287982803', 'category': '블로그·콘텐츠'}, {'title': '월급쟁이 루지', 'id': 'psung6', 'url': 'https://blog.naver.com/psung6', 'category': '블로그·콘텐츠'}, {'title': '시간투자', 'id': 'PostList.naver', 'url': 'https://m.blog.naver.com/PostList.naver?blogId=zest258&tab=1', 'category': '블로그·콘텐츠'}, {'title': '젠네', 'id': 'gentlenavy', 'url': 'https://blog.naver.com/gentlenavy', 'category': '블로그·콘텐츠'}, {'title': '신사람', 'id': 'shin0503988', 'url': 'https://blog.naver.com/shin0503988', 'category': '블로그·콘텐츠'}, {'title': '구빰', 'id': 'goobbam', 'url': 'https://m.blog.naver.com/goobbam?tab=1', 'category': '블로그·콘텐츠'}, {'title': '적당히 잘 살고', 'id': 'quincy312', 'url': 'https://blog.naver.com/quincy312', 'category': '블로그·콘텐츠'}, {'title': '돌묵선생', 'id': '911y', 'url': 'https://blog.naver.com/911y', 'category': '블로그·콘텐츠'}, {'title': '고하이', 'id': 'gohigh_realestate', 'url': 'https://blog.naver.com/gohigh_realestate', 'category': '블로그·콘텐츠'}, {'title': '페더씨의 아티클', 'id': 'feathers_mcgraw', 'url': 'https://blog.naver.com/feathers_mcgraw', 'category': '블로그·콘텐츠'}, {'title': '유다로', 'id': 'udaro', 'url': 'https://blog.naver.com/udaro', 'category': '블로그·콘텐츠'}, {'title': '닥터마빈', 'id': 'marbin1982', 'url': 'https://blog.naver.com/marbin1982', 'category': '블로그·콘텐츠'}, {'title': '짠돌이', 'id': 'jjandol_', 'url': 'https://m.blog.naver.com/jjandol_?tab=1', 'category': '블로그·콘텐츠'}, {'title': '작은투자', 'id': 'richyun0108', 'url': 'https://m.blog.naver.com/richyun0108?tab=1', 'category': '블로그·콘텐츠'}, {'title': '습관', 'id': 'cy2863', 'url': 'https://m.blog.naver.com/cy2863?tab=1', 'category': '블로그·콘텐츠'}, {'title': '지금', 'id': 'rwwrhappy', 'url': 'https://m.blog.naver.com/rwwrhappy?tab=1', 'category': '블로그·콘텐츠'}, {'title': '알바트로스', 'id': 'pillion21', 'url': 'https://blog.naver.com/pillion21', 'category': '블로그·콘텐츠'}, {'title': '이것 또한 지나가리라', 'id': 'tosoha1', 'url': 'https://blog.naver.com/tosoha1', 'category': '블로그·콘텐츠'}, {'title': '그러면서 투자하렵니까?', 'id': 'PostList.naver', 'url': 'https://m.blog.naver.com/PostList.naver?blogId=quantum_edge&tab=1', 'category': '블로그·콘텐츠'}, {'title': "G' day", 'id': 'PostList.naver', 'url': 'https://m.blog.naver.com/PostList.naver?blogId=skyrocket_jake&categoryNo=0&listStyle=post&tab=1&trackingCode=blog_comment', 'category': '블로그·콘텐츠'}, {'title': '민이군의 기록의 공간 : 네이버 블로그', 'id': 'bymin0418', 'url': 'https://blog.naver.com/bymin0418', 'category': '맛집'}, {'title': '움훼훼의 얼씨구 절씨구 밥타령! : 네이버 블로그', 'id': 'umstar81', 'url': 'https://blog.naver.com/umstar81', 'category': '맛집'}, {'title': '세콰노의 머거머거 : 네이버 블로그', 'id': 'gypsyone', 'url': 'https://blog.naver.com/gypsyone', 'category': '맛집'}, {'title': '스윗모카의 Foodie Life~ : 네이버 블로그', 'id': 'sweetmocha77', 'url': 'https://blog.naver.com/sweetmocha77', 'category': '맛집'}, {'title': '먹자, 마시자, 놀러 다니자 : 네이버 블로그', 'id': 'mardukas', 'url': 'https://blog.naver.com/mardukas', 'category': '맛집'}, {'title': '빠숑의 세상 답사기 : 네이버 블로그', 'id': 'ppassong', 'url': 'https://blog.naver.com/ppassong', 'category': '맛집'}, {'title': '부동산 투자시 절대 실패하지 않는 공식 : 네이버 블로그', 'id': 'ssaurajin7', 'url': 'https://blog.naver.com/ssaurajin7/220549973948', 'category': '맛집'}, {'title': '행복 부동산 투자 앨리스허 : 네이버 블로그', 'id': 'alicehuh2k', 'url': 'https://blog.naver.com/alicehuh2k', 'category': '맛집'}, {'title': '강남구청역 맛집 추천 호루몬규상 야끼니꾸 핫플.. : 네이버블로그', 'id': 'kizaki56', 'url': 'https://blog.naver.com/kizaki56/224162079124', 'category': '맛집'}]

def txt(el, name):
    n = el.find(name)
    return (n.text or "").strip() if n is not None else ""

out = {}
for b in BLOGS:
    url = f"https://rss.blog.naver.com/{b['id']}.xml"
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent":"Mozilla/5.0 GitHubActions BookmarkDashboard/2.0",
            "Accept":"application/rss+xml, application/xml, text/xml, */*"
        })
        with urllib.request.urlopen(req, timeout=20) as r:
            root = ET.fromstring(r.read())
        item = root.find("./channel/item")
        if item is None:
            raise RuntimeError("RSS item 없음")
        pub = txt(item,"pubDate")
        try:
            dt = parsedate_to_datetime(pub)
            if dt.tzinfo is None: dt=dt.replace(tzinfo=timezone.utc)
            pub = dt.isoformat()
        except Exception:
            pass
        out[b["id"]] = {
            "blogTitle":b["title"], "blogUrl":b["url"], "category":b["category"],
            "postTitle":txt(item,"title"), "postUrl":txt(item,"link") or b["url"],
            "pubDate":pub, "ok":True
        }
    except Exception as e:
        out[b["id"]] = {
            "blogTitle":b["title"], "blogUrl":b["url"], "category":b["category"],
            "ok":False, "error":str(e)
        }

Path("data").mkdir(exist_ok=True)
Path("data/latest.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8"
)
print(f"updated {sum(1 for v in out.values() if v.get('ok'))}/{len(out)} blogs")
