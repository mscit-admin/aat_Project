"""Build the GSDN prototype: extract sites from the master workbook and embed them in app.html.

Usage: python3 -I build.py <GSDN_Site_Master_Template.xlsx> [output.html]
"""
import sys, json, openpyxl, datetime
wb=openpyxl.load_workbook(sys.argv[1],read_only=True,data_only=True)
COLS=[19,20,34,35,36,38,41,43,45,47,51,52,53,54,55,56,57,58,59,60,61,62,64,66,71,72,73,74,75,76,
      80,81,82,84,86,88,89,90,91,92,93,95,97,101,102,105,110,118,122,123,124,125,126,127,128,129,
      130,131,132,133,135,136,137,138,140,144,145,148,151,152,153,155,161,166,167]
def norm(v):
    if v is None: return None
    if isinstance(v,datetime.datetime): return v.strftime("%Y-%m-%d")
    if isinstance(v,float) and v.is_integer(): v=int(v)
    if isinstance(v,str):
        v=" ".join(v.split())
        return v or None
    return v
sites=[]
for r in wb["Master"].iter_rows(min_row=5,max_row=504,values_only=True):
    if r[1] in (None,""): continue
    g=lambda c: norm(r[c-1])
    sites.append({"id":g(2),"own":g(3),"nm":g(4),"rg":g(5),"sr":g(6),"la":g(8),"lo":g(9),
      "ty":g(10),"sc":g(11),"up":g(12),"to":g(13),"en":g(14),"rt":g(15),"tt":g(16),"th":g(17),
      "ph":g(24),"bt":g(25),"ds":g(26),
      "s":{"te":g(27),"sa":g(28),"ge":g(29),"hl":g(30),"fu":g(31),"ip":g(32),"dm":g(33)},
      "v":{str(c):g(c) for c in COLS if g(c) is not None}})
master={s["id"] for s in sites}
stray=[]
for r in wb["RF & Design"].iter_rows(min_row=2,values_only=True):
    if r[1] in (None,"") or isinstance(r[1],(int,float)) or not isinstance(r[0],(int,float)): continue
    sid=norm(r[1])
    if sid not in master:
        stray.append({"id":sid,"own":norm(r[2]),"nm":norm(r[3]),"rg":norm(r[4]),"la":norm(r[6]),"lo":norm(r[7]),"ty":norm(r[8])})
data={"sites":sites,"stray":stray}

import pathlib
here=pathlib.Path(__file__).resolve().parent
tpl=(here/"src"/"app.html").read_text(encoding="utf-8")
blob=json.dumps(data,ensure_ascii=False,separators=(",",":")).replace("</","<\\/")
out=pathlib.Path(sys.argv[2]) if len(sys.argv)>2 else here/"gsdn-prototype.html"
out.write_text(tpl.replace("__DATA__",blob),encoding="utf-8")
print(f"{out}: {len(sites)} sites, {len(stray)} stray")
