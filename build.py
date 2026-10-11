#!/usr/bin/env python3
"""从 sources/*.txt 生成 Loon / Surge / QuantumultX 规则。
源文件格式: 每行 `类型,值`，类型: DOMAIN / DOMAIN-SUFFIX / DOMAIN-KEYWORD / IP-CIDR / IP-CIDR6
"""
import os, glob, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "sources")

QX_MAP = {"DOMAIN": "HOST", "DOMAIN-SUFFIX": "HOST-SUFFIX", "DOMAIN-KEYWORD": "HOST-KEYWORD",
          "IP-CIDR": "IP-CIDR", "IP-CIDR6": "IP6-CIDR"}

def parse(path):
    rules, title = [], None
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        if line.startswith("#"):
            if title is None:
                title = line.lstrip("# ").strip()
            continue
        t, v = [x.strip() for x in line.split(",", 1)]
        rules.append((t.upper(), v))
    return title, rules

def header(name, title, n, extra=""):
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    return f"# NAME: {name}\n# DESC: {title or name}\n# UPDATED: {ts}\n# TOTAL: {n}\n{extra}"

def build(name, title, rules):
    for app in ("Loon", "Surge", "QuantumultX"):
        os.makedirs(os.path.join(ROOT, app, name), exist_ok=True)
    out = {}
    # Loon / Surge: 规则无策略，IP 类加 no-resolve
    lines = []
    for t, v in rules:
        lines.append(f"{t},{v},no-resolve" if t.startswith("IP-CIDR") else f"{t},{v}")
    body = "\n".join(lines) + "\n"
    out["Loon"] = header(name, title, len(rules)) + body
    out["Surge"] = header(name, title, len(rules)) + body
    # QuantumultX: HOST-SUFFIX,xxx,策略   (在 filter_remote 里用 force-policy 覆盖)
    ql = []
    for t, v in rules:
        q = QX_MAP[t]
        ql.append(f"{q},{v},PROXY,no-resolve" if t.startswith("IP-CIDR") else f"{q},{v},PROXY")
    out["QuantumultX"] = header(name, title, len(rules)) + "\n".join(ql) + "\n"
    for app, text in out.items():
        ext = "list"
        with open(os.path.join(ROOT, app, name, f"{name}.{ext}"), "w", encoding="utf-8") as f:
            f.write(text)

def main():
    names = []
    for p in sorted(glob.glob(os.path.join(SRC, "*.txt"))):
        name = os.path.splitext(os.path.basename(p))[0]
        title, rules = parse(p)
        build(name, title, rules)
        names.append((name, title, len(rules)))
        print("built", name, len(rules))
    return names

if __name__ == "__main__":
    main()
