"""Build a single readable HTML page from finished Listener reports (video-agnostic).
Usage: build_report_page.py OUT.html "Tab title=path/to/REPORT.md" ... [--title T] [--repo-url URL] [--method path.md]
Strips process-only sections (cold-read revision, verification notes, check logs), links repo paths, highlights timestamps."""
import html, re, sys, markdown
args = sys.argv[1:]; out = args.pop(0)
opts = {"--title": "Listener report", "--repo-url": "", "--method": "", "--sub": ""}
tabs = []
while args:
    a = args.pop(0)
    if a in opts: opts[a] = args.pop(0)
    else: k, v = a.split("=", 1); tabs.append((k, v))
DROP = re.compile(r"^(cold-read revision|\d+\.\s*verification notes|verification notes|check log|fact-check log)\b", re.I)
def clean(md):
    lines, keep, outl = md.splitlines(), True, []
    for ln in lines:
        m = re.match(r"^(#{1,6})\s+(.*)", ln)
        if m and len(m.group(1)) <= 2: keep = not DROP.match(m.group(2).strip())
        if keep and not ln.startswith("**Checked against:**"): outl.append(ln)
    return "\n".join(outl)
def linkify(h):
    def rep(m):
        p = html.unescape(m.group(1))
        if opts["--repo-url"] and re.match(r"^(v1|videos|testvideos)/[\w./*-]+$", p) and "*" not in p:
            return f'<a class="path" href="{opts["--repo-url"]}/{p}">{m.group(1)}</a>'
        return f"<code>{m.group(1)}</code>"
    h = re.sub(r"<code>([^<]+)</code>", rep, h)
    h = re.sub(r"(?<![\w:.])(\d{1,2}:\d{2}(?:\.\d+)?)(?![\w:])", r'<span class="ts">\1</span>', h)
    h = re.sub(r"\b(OBS|INT|SPEC)\b(?![^<]*</a>)", r'<abbr class="tag tag-\1" title="\1">\1</abbr>', h)
    return h
sections = []
for i, (name, path) in enumerate(tabs):
    md = clean(open(path, encoding="utf-8").read())
    body = linkify(markdown.markdown(md, extensions=["tables", "sane_lists"]))
    sid = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    sections.append((sid, name, body))
if opts["--method"]:
    sections.append(("method", "How it was made", linkify(markdown.markdown(open(opts["--method"]).read(), extensions=["tables"]))))
nav = "".join(f'<a href="#{s}" data-tab="{s}">{html.escape(n)}</a>' for s, n, _ in sections)
arts = "".join(f'<article id="{s}" class="report" {"" if i == 0 else "hidden"}>{b}</article>' for i, (s, _, b) in enumerate(sections))
tpl = open(__file__.replace("build_report_page.py", "report_page_template.html"), encoding="utf-8").read()
page = tpl.replace("{{TITLE}}", html.escape(opts["--title"])).replace("{{SUB}}", html.escape(opts["--sub"])).replace("{{NAV}}", nav).replace("{{ARTICLES}}", arts).replace("{{FIRST}}", sections[0][0])
open(out, "w", encoding="utf-8").write(page); print("wrote", out, len(page), "bytes")
