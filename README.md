# rule

自用分流规则，同时提供 Loon / Surge / Quantumult X 三种格式。

## 目录

```
sources/        规则源文件（只改这里）
Loon/<名称>/<名称>.list
Surge/<名称>/<名称>.list
QuantumultX/<名称>/<名称>.list
build.py        从 sources 生成三种格式
```

## 订阅链接（以 XiaoHongShu 为例）

**Loon**
```
RULE-SET,https://cdn.jsdelivr.net/gh/KaWnt/rule@main/Loon/XiaoHongShu/XiaoHongShu.list,DIRECT
```

**Surge**
```
RULE-SET,https://cdn.jsdelivr.net/gh/KaWnt/rule@main/Surge/XiaoHongShu/XiaoHongShu.list,DIRECT
```

**Quantumult X**（`[filter_remote]` 段，策略在行尾用 force-policy 指定）
```
https://cdn.jsdelivr.net/gh/KaWnt/rule@main/QuantumultX/XiaoHongShu/XiaoHongShu.list, tag=XiaoHongShu, force-policy=direct, update-interval=86400, opt-parser=false, enabled=true
```
> QX 文件里的 `PROXY` 只是占位，实际走向由 `force-policy` 决定。

## 新增规则

在 `sources/` 新建 `名称.txt`，每行 `类型,值`（DOMAIN / DOMAIN-SUFFIX / DOMAIN-KEYWORD / IP-CIDR / IP-CIDR6），运行 `python3 build.py`。
