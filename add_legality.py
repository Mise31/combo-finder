"""
Add format legality to each pattern by checking all cards via Scryfall.
A pattern is legal in a format only if ALL cards in ALL slots are legal there.
"""
import json
import requests
import time
import sys

FORMATS = ["standard", "pioneer", "modern", "legacy", "vintage", "commander", "pauper", "premodern"]
SCRYFALL_COLLECTION = "https://api.scryfall.com/cards/collection"

def fetch_legalities_batch(card_names):
    """Fetch legalities for up to 75 cards at once using Scryfall collection endpoint."""
    legalities = {}
    # Scryfall collection accepts max 75 identifiers per request
    batches = [card_names[i:i+75] for i in range(0, len(card_names), 75)]
    
    for batch_num, batch in enumerate(batches):
        identifiers = [{"name": name} for name in batch]
        resp = requests.post(SCRYFALL_COLLECTION, json={"identifiers": identifiers})
        
        if resp.status_code != 200:
            print(f"  Errore batch {batch_num}: {resp.status_code}")
            time.sleep(1)
            continue
        
        data = resp.json()
        for card in data.get("data", []):
            name = card.get("name", "")
            legs = card.get("legalities", {})
            legalities[name] = {fmt: legs.get(fmt, "not_legal") for fmt in FORMATS}
        
        # Cards not found
        for nf in data.get("not_found", []):
            name = nf.get("name", "")
            if name:
                legalities[name] = {fmt: "unknown" for fmt in FORMATS}
        
        if batch_num < len(batches) - 1:
            time.sleep(0.1)  # Rate limit
        
        print(f"  Batch {batch_num + 1}/{len(batches)} completato ({len(data.get('data', []))} carte)")
    
    return legalities


def compute_pattern_formats(pattern, card_legalities):
    """Determine which formats a pattern is legal in."""
    legal_formats = []
    
    for fmt in FORMATS:
        all_legal = True
        for slot in pattern["slots"]:
            # A slot is "available" in a format if at least one card in it is legal
            slot_has_legal = False
            for card in slot["cards"]:
                leg = card_legalities.get(card, {}).get(fmt, "not_legal")
                if leg in ("legal", "restricted"):
                    slot_has_legal = True
                    break
            if not slot_has_legal:
                all_legal = False
                break
        
        if all_legal:
            legal_formats.append(fmt)
    
    return legal_formats


def main():
    print("=" * 60)
    print("AGGIUNTA LEGALITA' AI PATTERN")
    print("=" * 60)
    
    # Load patterns
    with open("patterns.json", "r", encoding="utf-8") as f:
        patterns = json.load(f)
    
    # Collect all unique card names
    all_cards = set()
    for p in patterns:
        for s in p["slots"]:
            for c in s["cards"]:
                # Skip composite entries like "Basalt Monolith + Rings"
                if " + " not in c:
                    all_cards.add(c)
    
    print(f"\n[1/2] Verifica legalita di {len(all_cards)} carte su Scryfall...")
    card_legalities = fetch_legalities_batch(list(all_cards))
    print(f"  → {len(card_legalities)} carte verificate")
    
    print(f"\n[2/2] Calcolo formati per {len(patterns)} pattern...")
    for p in patterns:
        p["formats"] = compute_pattern_formats(p, card_legalities)
    
    # Stats
    fmt_counts = {fmt: 0 for fmt in FORMATS}
    for p in patterns:
        for fmt in p["formats"]:
            fmt_counts[fmt] += 1
    
    print("\n  Pattern legali per formato:")
    for fmt, count in sorted(fmt_counts.items(), key=lambda x: -x[1]):
        print(f"    {fmt}: {count}")
    
    # Save
    with open("patterns.json", "w", encoding="utf-8") as f:
        json.dump(patterns, f, ensure_ascii=False)
    
    print(f"\n{'='*60}")
    print(f"COMPLETATO: legalita aggiunta a {len(patterns)} pattern")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
