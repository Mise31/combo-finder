import json, re

with open("patterns.json", "r", encoding="utf-8") as f:
    patterns = json.load(f)

fixed = 0
for p in patterns:
    result = p.get("result", "")
    if "feature" in result and "name" in result:
        names = re.findall(r"'name':\s*'([^']+)'", result)
        if names:
            p["result"] = ", ".join(names)
            fixed += 1
        else:
            p["result"] = "Combo"
            fixed += 1

with open("patterns.json", "w", encoding="utf-8") as f:
    json.dump(patterns, f, ensure_ascii=False)

print(f"{fixed} risultati puliti su {len(patterns)} pattern")
for p in patterns[:5]:
    print(f"  {p['name'][:50]} -> {p['result'][:80]}")
