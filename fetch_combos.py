"""
Fetch combos from Commander Spellbook API and convert to pattern format.
"""
import requests
import json
import time
import sys
from collections import defaultdict

API_BASE = "https://backend.commanderspellbook.com"
OUTPUT_FILE = "patterns.json"

def fetch_combos(limit=500):
    """Fetch combos from Commander Spellbook API."""
    all_combos = []
    offset = 0
    page_size = 100

    while offset < limit:
        url = f"{API_BASE}/variants/?limit={page_size}&offset={offset}&ordering=popularity"
        print(f"  Fetching offset {offset}...")
        try:
            resp = requests.get(url, timeout=30)
            if resp.status_code != 200:
                print(f"  Error {resp.status_code}, trying alternate endpoint...")
                break
            data = resp.json()
            results = data.get("results", [])
            if not results:
                break
            all_combos.extend(results)
            offset += page_size
            if not data.get("next"):
                break
            time.sleep(0.2)
        except Exception as e:
            print(f"  Error: {e}")
            break

    return all_combos


def group_into_patterns(combos):
    """Group combos by their result to create patterns."""
    # Group by result type
    result_groups = defaultdict(list)

    for combo in combos:
        results = combo.get("produces", []) or combo.get("results", [])
        if not results:
            continue

        # Get result string
        result_str = ", ".join(r.get("name", str(r)) if isinstance(r, dict) else str(r) for r in results[:3])
        if not result_str:
            continue

        cards = []
        for card in combo.get("uses", []) or combo.get("cards", []):
            if isinstance(card, dict):
                name = card.get("card", {}).get("name", "") if "card" in card else card.get("name", "")
            else:
                name = str(card)
            if name:
                cards.append(name)

        if len(cards) >= 2:
            result_groups[result_str].append({
                "cards": cards,
                "steps": combo.get("description", ""),
                "prerequisites": combo.get("prerequisites", ""),
            })

    return result_groups


def create_pattern_database(result_groups):
    """Convert grouped combos into pattern format with slots."""
    patterns = []
    pattern_id = 0

    for result, combos in sorted(result_groups.items(), key=lambda x: -len(x[1])):
        if len(combos) < 2:
            # Single combo, just add as-is
            combo = combos[0]
            if len(combo["cards"]) >= 2:
                patterns.append({
                    "id": f"combo-{pattern_id}",
                    "name": " + ".join(combo["cards"][:3]),
                    "description": combo.get("steps", "")[:200] or f"Combo che produce: {result}",
                    "result": result,
                    "slots": [
                        {"role": f"Carta {i+1}", "keyword": f"card_{pattern_id}_{i}", "cards": [c]}
                        for i, c in enumerate(combo["cards"])
                    ]
                })
                pattern_id += 1
            continue

        # Multiple combos with same result - try to find common cards (slots)
        # Find which card positions have variation
        all_card_sets = [set(c["cards"]) for c in combos]
        all_cards = set()
        for cs in all_card_sets:
            all_cards.update(cs)

        # Find cards that appear in most combos (core) vs variable cards
        card_frequency = defaultdict(int)
        for cs in all_card_sets:
            for card in cs:
                card_frequency[card] += 1

        total = len(combos)
        core_cards = [c for c, freq in card_frequency.items() if freq > total * 0.6]
        variable_cards = [c for c, freq in card_frequency.items() if freq <= total * 0.6]

        if core_cards and variable_cards:
            # Pattern with core + variable slot
            slots = []
            if core_cards:
                slots.append({
                    "role": "Core",
                    "keyword": f"core_{pattern_id}",
                    "cards": sorted(core_cards)[:10]
                })
            if variable_cards:
                slots.append({
                    "role": "Variabile",
                    "keyword": f"var_{pattern_id}",
                    "cards": sorted(variable_cards)[:20]
                })

            patterns.append({
                "id": f"pattern-{pattern_id}",
                "name": f"{core_cards[0] if core_cards else 'Combo'} + varianti",
                "description": f"{len(combos)} varianti che producono: {result}",
                "result": result,
                "slots": slots
            })
        else:
            # Can't find clear pattern, add top combos individually
            for combo in combos[:5]:
                if len(combo["cards"]) >= 2:
                    patterns.append({
                        "id": f"combo-{pattern_id}",
                        "name": " + ".join(combo["cards"][:3]),
                        "description": combo.get("steps", "")[:200] or f"Combo che produce: {result}",
                        "result": result,
                        "slots": [
                            {"role": f"Carta {i+1}", "keyword": f"card_{pattern_id}_{i}", "cards": [c]}
                            for i, c in enumerate(combo["cards"])
                        ]
                    })

        pattern_id += 1

    return patterns


def main():
    print("=" * 60)
    print("COMMANDER SPELLBOOK → PATTERN DATABASE")
    print("=" * 60)

    print("\n[1/3] Scaricamento combo da Commander Spellbook...")
    combos = fetch_combos(limit=3000)
    print(f"  → {len(combos)} combo scaricate")

    if not combos:
        print("\nAPI non disponibile, uso approccio alternativo...")
        # Fallback: use a pre-built pattern database
        print("Generando database pattern manuale esteso...")
        patterns = generate_extended_patterns()
    else:
        print("\n[2/3] Raggruppamento in pattern...")
        result_groups = group_into_patterns(combos)
        print(f"  → {len(result_groups)} gruppi di risultati")

        print("\n[3/3] Creazione database pattern...")
        patterns = create_pattern_database(result_groups)

    # Merge with existing hand-crafted patterns
    try:
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            existing = json.load(f)
        # Keep existing patterns and add new ones
        existing_names = {p["name"] for p in existing}
        new_patterns = [p for p in patterns if p["name"] not in existing_names]
        final = existing + new_patterns
    except:
        final = patterns

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(final, f, ensure_ascii=False, indent=2)

    total_cards = len(set(c for p in final for s in p["slots"] for c in s["cards"]))
    print(f"\n{'='*60}")
    print(f"COMPLETATO: {len(final)} pattern, {total_cards} carte uniche")
    print(f"{'='*60}")


def generate_extended_patterns():
    """Generate a large pattern database manually covering major combo archetypes."""
    patterns = [
        # === INFINITE MANA ===
        {"id": "inf-mana-1", "name": "Mana Dork Grande + Stappa Equipaggiamento", "description": "Creatura che produce 4+ mana + equipaggiamento che stappa", "result": "Infinite mana", "slots": [
            {"role": "Produce 4+ Mana", "keyword": "big_mana_dork", "cards": ["Priest of Titania", "Elvish Archdruid", "Circle of Dreams Druid", "Karametra's Acolyte", "Marwyn, the Nurturer", "Selvala, Heart of the Wilds", "Nyxbloom Ancient", "Bloom Tender", "Faeburrow Elder", "Incubation Druid", "Gyre Sage", "Viridian Joiner", "Wirewood Channeler"]},
            {"role": "Stappa per 3 o meno", "keyword": "cheap_untap_equip", "cards": ["Staff of Domination", "Umbral Mantle", "Sword of the Paruns", "Pemmin's Aura", "Freed from the Real", "Halo Fountain", "Kogla and Yidaro", "Quirion Ranger", "Wirewood Symbiote", "Scryb Ranger", "Instill Energy", "Nature's Chosen"]}
        ]},
        {"id": "inf-mana-2", "name": "Basalt Monolith + Rings of Brighthearth", "description": "Copia l'abilita di stappare per generare mana netto", "result": "Infinite colorless mana", "slots": [
            {"role": "Artefatto che si stappa", "keyword": "self_untap_artifact", "cards": ["Basalt Monolith", "Grim Monolith", "Mana Vault"]},
            {"role": "Copia Abilita Attivata", "keyword": "copy_activated", "cards": ["Rings of Brighthearth", "Lithoform Engine", "Zirda, the Dawnwaker"]}
        ]},
        {"id": "inf-mana-3", "name": "Peregrine Drake + Flicker = Mana Infinito", "description": "Creatura che stappa 5+ terre + modo per flickerarla ripetutamente", "result": "Infinite mana", "slots": [
            {"role": "Stappa 5+ Terre ETB", "keyword": "untap_lands_etb", "cards": ["Peregrine Drake", "Palinchron", "Great Whale", "Cloud of Faeries", "Treachery", "Hyrax Tower Scout"]},
            {"role": "Flicker Ripetuto", "keyword": "repeatable_flicker", "cards": ["Deadeye Navigator", "Eldrazi Displacer", "Ghostly Flicker", "Displace", "Conjurer's Closet", "Thassa, Deep-Dwelling", "Emiel the Blessed", "Restoration Angel"]}
        ]},
        {"id": "inf-mana-4", "name": "Dramatic Reversal + Isochron Scepter", "description": "Stappa tutti i mana rock all'infinito", "result": "Infinite mana, infinite storm", "slots": [
            {"role": "Ripeti Istantaneo", "keyword": "isochron", "cards": ["Isochron Scepter"]},
            {"role": "Stappa Non-Terre", "keyword": "untap_nonlands", "cards": ["Dramatic Reversal", "Vitalize", "Mobilize", "Benefactor's Draught"]},
            {"role": "Mana Rocks (3+ mana totale)", "keyword": "mana_rocks_3plus", "cards": ["Sol Ring", "Mana Crypt", "Mana Vault", "Grim Monolith", "Arcane Signet", "Fellwar Stone", "Talisman of Dominance", "Izzet Signet", "Dimir Signet", "Simic Signet", "Chrome Mox", "Mox Diamond", "Mox Opal", "Lotus Petal"]}
        ]},
        {"id": "inf-mana-5", "name": "Nim Deathmantle + Ashnod's Altar + Token Maker", "description": "Sacrifica creatura che fa 2+ token, usa mana per rianimarla con Deathmantle", "result": "Infinite mana, infinite tokens", "slots": [
            {"role": "Rianima Pagando 4", "keyword": "nim_deathmantle", "cards": ["Nim Deathmantle"]},
            {"role": "Sac per 2 Mana", "keyword": "ashnods", "cards": ["Ashnod's Altar", "Krark-Clan Ironworks"]},
            {"role": "Fa 2+ Token Quando Muore/ETB", "keyword": "makes_2_tokens", "cards": ["Wurmcoil Engine", "Myr Battlesphere", "Grave Titan", "Marionette Master", "Abhorrent Overlord", "Siege-Gang Commander", "Chittering Witch", "Sengir Autocrat", "Pia and Kiran Nalaar", "Weaponcraft Enthusiast", "Ghoulcaller Gisa"]}
        ]},

        # === INFINITE TOKENS / CREATURES ===
        {"id": "inf-token-1", "name": "Splinter Twin / Kiki-Jiki + ETB Untapper", "description": "Copia creatura che stappa il copiante = token infiniti con rapidita", "result": "Infinite creature tokens with haste", "slots": [
            {"role": "Copia Creatura (tap)", "keyword": "copy_tap", "cards": ["Splinter Twin", "Kiki-Jiki, Mirror Breaker"]},
            {"role": "ETB Stappa Permanente", "keyword": "etb_untap_target", "cards": ["Pestermite", "Deceiver Exarch", "Zealous Conscripts", "Bounding Krasis", "Village Bell-Ringer", "Breaching Hippocamp", "Restoration Angel", "Felidar Guardian", "Hyrax Tower Scout", "Corridor Monitor", "Intruder Alarm"]}
        ]},
        {"id": "inf-token-2", "name": "Intruder Alarm + Tap per Token", "description": "Ogni token stappa tutte le creature, loop infinito", "result": "Infinite creature tokens", "slots": [
            {"role": "Stappa Tutto su ETB Creatura", "keyword": "intruder_alarm", "cards": ["Intruder Alarm"]},
            {"role": "Tap: Crea Token Creatura", "keyword": "tap_token_maker", "cards": ["Presence of Gond", "Imperious Perfect", "Steward of Solidarity", "Thraben Doomsayer", "Ant Queen", "Rhys the Redeemed", "Sliver Queen", "Lys Alana Huntmaster", "Marwyn, the Nurturer", "Kiki-Jiki, Mirror Breaker"]}
        ]},
        {"id": "inf-token-3", "name": "Squirrel Nest + Earthcraft", "description": "Tappa terra per token, tappa token per stappare terra", "result": "Infinite 1/1 tokens", "slots": [
            {"role": "Tappa Terra per Token", "keyword": "land_token", "cards": ["Squirrel Nest", "Presence of Gond"]},
            {"role": "Tappa Creatura per Stappare Terra", "keyword": "creature_untap_land", "cards": ["Earthcraft"]}
        ]},

        # === INFINITE DAMAGE ===
        {"id": "inf-dmg-1", "name": "Persist + Sac Outlet + Rimuovi Segnalino", "description": "Creatura con persist muore e torna all'infinito", "result": "Infinite damage/life/mill", "slots": [
            {"role": "Persist Creature", "keyword": "persist_creature", "cards": ["Kitchen Finks", "Murderous Redcap", "Glen Elendra Archmage", "Puppeteer Clique", "Woodfall Primus", "Safehold Elite", "Lesser Masticore", "Putrid Goblin", "River Kelpie"]},
            {"role": "Rimuovi -1/-1", "keyword": "remove_minus", "cards": ["Vizier of Remedies", "Melira, Sylvok Outcast", "Anafenza, Kin-Tree Spirit", "Good-Fortune Unicorn", "Grumgully, the Generous", "Renata, Called to the Hunt", "Metallic Mimic", "Rhythm of the Wild", "Cathars' Crusade"]},
            {"role": "Sac Outlet Gratuito", "keyword": "free_sac_outlet", "cards": ["Viscera Seer", "Carrion Feeder", "Goblin Bombardment", "Altar of Dementia", "Ashnod's Altar", "Phyrexian Altar", "Blasting Station", "Woe Strider", "Yahenni, Undying Partisan", "Nantuko Husk", "Spawning Pit"]}
        ]},
        {"id": "inf-dmg-2", "name": "Walking Ballista + Mana Infinito", "description": "Con mana infinito, Ballista fa danni infiniti", "result": "Infinite damage to any target", "slots": [
            {"role": "Mana Sink = Danno", "keyword": "mana_to_damage", "cards": ["Walking Ballista", "Goblin Cannon", "Staff of Domination", "Shivan Hellkite", "Fireball", "Torment of Hailfire", "Exsanguinate", "Debt to the Deathless", "Blue Sun's Zenith", "Finale of Devastation"]},
            {"role": "Fonte Mana Infinito (qualsiasi combo sopra)", "keyword": "inf_mana_source", "cards": ["Basalt Monolith + Rings", "Dramatic Scepter", "Peregrine Drake + Flicker", "Freed from the Real + Bloom Tender", "Food Chain + Eternal Scourge"]}
        ]},
        {"id": "inf-dmg-3", "name": "Niv-Mizzet + Curiosity = Pesca/Danno Infinito", "description": "Ogni carta pescata fa danno, ogni danno pesca una carta", "result": "Infinite damage, infinite draw", "slots": [
            {"role": "Danno Quando Peschi", "keyword": "damage_on_draw", "cards": ["Niv-Mizzet, the Firemind", "Niv-Mizzet, Parun", "Psychosis Crawler", "Glint-Horn Buccaneer"]},
            {"role": "Pesca Quando Fai Danno", "keyword": "draw_on_damage", "cards": ["Curiosity", "Ophidian Eye", "Tandem Lookout", "Mind Over Matter"]}
        ]},
        {"id": "inf-dmg-4", "name": "Sanguine Bond + Exquisite Blood", "description": "Ogni vita guadagnata drena, ogni drain guadagna vita", "result": "Infinite life drain", "slots": [
            {"role": "Danno Quando Guadagni Vita", "keyword": "damage_on_lifegain", "cards": ["Sanguine Bond", "Vito, Thorn of the Dusk Rose", "Marauding Blight-Priest", "Defiant Bloodlord"]},
            {"role": "Guadagni Vita Quando Fai Danno", "keyword": "life_on_damage", "cards": ["Exquisite Blood"]}
        ]},

        # === INFINITE DRAW / MILL ===
        {"id": "inf-draw-1", "name": "Sensei's Top + Cost Reducer + Draw Trigger", "description": "Pesca Top, rigiocalo gratis, trigger infiniti", "result": "Infinite draw, infinite storm", "slots": [
            {"role": "Si Mette in Cima", "keyword": "top_of_library", "cards": ["Sensei's Divining Top", "Bolas's Citadel"]},
            {"role": "Riduce Costo Artefatti", "keyword": "artifact_cost_reduce", "cards": ["Etherium Sculptor", "Foundry Inspector", "Cloud Key", "Helm of Awakening", "Jhoira's Familiar", "Ugin, the Ineffable"]},
            {"role": "Trigger su Cast/Draw", "keyword": "cast_trigger", "cards": ["Aetherflux Reservoir", "Mystic Forge", "Future Sight", "Bolas's Citadel"]}
        ]},
        {"id": "inf-draw-2", "name": "Thassa's Oracle + Demonic Consultation", "description": "Esilia tutto il mazzo, vinci con Oracle", "result": "Win the game", "slots": [
            {"role": "Vinci con Libreria Vuota", "keyword": "win_empty_lib", "cards": ["Thassa's Oracle", "Laboratory Maniac", "Jace, Wielder of Mysteries"]},
            {"role": "Svuota Libreria", "keyword": "exile_library", "cards": ["Demonic Consultation", "Tainted Pact", "Doomsday", "Paradigm Shift", "Leveler", "Mirror of Fate", "Thought Lash"]}
        ]},

        # === INFINITE TURNS ===
        {"id": "inf-turns-1", "name": "Extra Turn + Ricorsione", "description": "Gioca turno extra, riprendi la carta, ripeti", "result": "Infinite turns", "slots": [
            {"role": "Turno Extra", "keyword": "extra_turn", "cards": ["Time Warp", "Temporal Manipulation", "Capture of Jingzhou", "Walk the Aeons", "Beacon of Tomorrows", "Nexus of Fate", "Temporal Mastery"]},
            {"role": "Riprendi dalla Mano/Cimitero", "keyword": "recursion_spell", "cards": ["Eternal Witness", "Archaeomancer", "Mystic Sanctuary", "Narset's Reversal", "Isochron Scepter", "Seasons Past", "Regrowth"]}
        ]},

        # === LOCKS / STAX ===
        {"id": "lock-1", "name": "Knowledge Pool + Regola Sostitutiva", "description": "Knowledge Pool esilia magie, effetto impedisce di giocare dall'esilio", "result": "Opponents can't cast spells", "slots": [
            {"role": "Esilia Magie Lanciate", "keyword": "exile_cast", "cards": ["Knowledge Pool", "Possibility Storm", "Omen Machine"]},
            {"role": "Impedisci Cast dall'Esilio/Non-Mano", "keyword": "restrict_cast", "cards": ["Teferi, Mage of Zhalfir", "Drannith Magistrate", "Lavinia, Azorius Renegade", "Rule of Law", "Arcane Laboratory", "Eidolon of Rhetoric"]}
        ]},
        {"id": "lock-2", "name": "Stasis + Modo per Pagare/Evitare", "description": "Nessuno stappa, ma tu hai un modo per aggirarlo", "result": "Opponents can't untap", "slots": [
            {"role": "Nessuno Stappa", "keyword": "no_untap", "cards": ["Stasis", "Winter Orb", "Static Orb", "Rising Waters", "Hokori, Dust Drinker", "Mana Vortex"]},
            {"role": "Tu Stappi/Eviti", "keyword": "you_untap", "cards": ["Teferi, Temporal Archmage", "Derevi, Empyrial Tactician", "Brago, King Eternal", "Chromatic Lantern", "Forsaken City", "Chronatog", "Black Vise", "Dockside Extortionist"]}
        ]},
        {"id": "lock-3", "name": "Contamination + Token Ricorrente", "description": "Tutte le terre producono solo nero, sacrifica token ogni turno", "result": "Opponents can only produce black mana", "slots": [
            {"role": "Terre Producono Solo Nero", "keyword": "contamination", "cards": ["Contamination", "Infernal Darkness"]},
            {"role": "Token/Creatura Ricorrente", "keyword": "recurring_creature", "cards": ["Bitterblossom", "Squee, Goblin Nabob", "Reassembling Skeleton", "Ophiomancer", "Dreadhorde Invasion", "Jadar, Ghoulcaller of Nephalia", "Gravecrawler"]}
        ]},

        # === GRAVEYARD COMBOS ===
        {"id": "gy-1", "name": "Animate Dead + Worldgorger Dragon", "description": "Loop infinito di esilio/ritorno = mana infinito", "result": "Infinite mana, infinite ETB/LTB", "slots": [
            {"role": "Rianima come Aura", "keyword": "reanimate_aura", "cards": ["Animate Dead", "Dance of the Dead", "Necromancy"]},
            {"role": "Esilia Tutto ETB", "keyword": "worldgorger", "cards": ["Worldgorger Dragon"]},
            {"role": "Win Con con Mana Infinito", "keyword": "mana_wincon", "cards": ["Walking Ballista", "Torment of Hailfire", "Exsanguinate", "Ambassador Laquatus", "Shivan Hellkite", "Comet, Stellar Pup"]}
        ]},
        {"id": "gy-2", "name": "Gravecrawler + Phyrexian Altar + Payoff", "description": "Sacrifica Gravecrawler per mana nero, rigiocalo dal cimitero, ripeti", "result": "Infinite death triggers, infinite mana", "slots": [
            {"role": "Rigiocabile dal Cimitero", "keyword": "recursive_creature", "cards": ["Gravecrawler", "Reassembling Skeleton", "Bloodghast", "Nether Traitor", "Tenacious Dead"]},
            {"role": "Sac per Mana", "keyword": "sac_for_mana", "cards": ["Phyrexian Altar", "Ashnod's Altar", "Pitiless Plunderer"]},
            {"role": "Payoff su Morte", "keyword": "death_payoff", "cards": ["Blood Artist", "Zulaport Cutthroat", "Cruel Celebrant", "Bastion of Remembrance", "Vindictive Vampire", "Corpse Knight", "Wayward Servant", "Diregraf Captain"]}
        ]},
        {"id": "gy-3", "name": "Hermit Druid + No Basic Lands", "description": "Attiva Hermit Druid senza terre base = milli tutto il mazzo", "result": "Entire library in graveyard", "slots": [
            {"role": "Mill Fino a Terra Base", "keyword": "hermit_druid", "cards": ["Hermit Druid", "Mirror-Mad Phantasm", "Mesmeric Orb + Basalt Monolith"]},
            {"role": "Win dal Cimitero", "keyword": "gy_wincon", "cards": ["Thassa's Oracle", "Laboratory Maniac", "Dread Return + Angel of Glory's Rise", "Narcomoeba + Dread Return", "Underworld Breach"]}
        ]},

        # === FOOD CHAIN ===
        {"id": "fc-1", "name": "Food Chain + Cast from Exile", "description": "Esilia creatura per mana, rigiocala dall'esilio, netto positivo", "result": "Infinite creature mana, infinite casts", "slots": [
            {"role": "Esilia per Mana Creature", "keyword": "food_chain_card", "cards": ["Food Chain"]},
            {"role": "Giocabile dall'Esilio", "keyword": "from_exile", "cards": ["Misthollow Griffin", "Eternal Scourge", "Squee, the Immortal"]},
            {"role": "Payoff su Cast", "keyword": "cast_payoff", "cards": ["Aetherflux Reservoir", "Beast Whisperer", "Guardian Project", "The Great Henge", "Purphoros, God of the Forge", "Impact Tremors"]}
        ]},

        # === ENCHANTMENT COMBOS ===
        {"id": "ench-1", "name": "Enchantress + Serra's Sanctum + Bounce", "description": "Ogni incantesimo pesca, Sanctum produce mana, rimbalza incantesimi economici", "result": "Draw entire deck, infinite mana", "slots": [
            {"role": "Pesca per Incantesimo", "keyword": "enchantress_draw", "cards": ["Argothian Enchantress", "Enchantress's Presence", "Mesa Enchantress", "Eidolon of Blossoms", "Setessan Champion", "Sythis, Harvest's Hand"]},
            {"role": "Mana da Incantesimi", "keyword": "enchant_mana", "cards": ["Serra's Sanctum", "Sanctum Weaver", "Nykthos, Shrine to Nyx", "Gaea's Cradle"]},
            {"role": "Rimbalza Incantesimo Economico", "keyword": "bounce_enchant", "cards": ["Words of Wind", "Cloudstone Curio", "Whip Silk", "Shimmering Wings", "Flickering Ward"]}
        ]},

        # === ARTIFACT COMBOS ===
        {"id": "art-1", "name": "Krark-Clan Ironworks + Scrap Trawler + Myr Retriever", "description": "Sacrifica artefatti per mana, riprendi dal cimitero, loop", "result": "Infinite mana, infinite recursion", "slots": [
            {"role": "Sac Artefatto per 2 Mana", "keyword": "kci", "cards": ["Krark-Clan Ironworks", "Ashnod's Altar"]},
            {"role": "Riprendi Artefatto Quando Muore", "keyword": "artifact_recursion", "cards": ["Scrap Trawler", "Myr Retriever", "Junk Diver", "Workshop Assistant", "Retrieval Agent"]},
            {"role": "Artefatto Costo 0-1", "keyword": "cheap_artifact", "cards": ["Mox Opal", "Chromatic Star", "Chromatic Sphere", "Terrarion", "Mishra's Bauble", "Urza's Bauble", "Everflowing Chalice"]}
        ]},
        {"id": "art-2", "name": "Mycosynth Lattice + Vandalblast/Karn", "description": "Tutto diventa artefatto, poi distruggi tutti gli artefatti", "result": "Destroy all opponents' permanents", "slots": [
            {"role": "Tutto e Artefatto", "keyword": "everything_artifact", "cards": ["Mycosynth Lattice", "Enchanted Evening"]},
            {"role": "Distruggi/Esilia Artefatti", "keyword": "destroy_artifacts", "cards": ["Vandalblast", "Karn, the Great Creator", "Collector Ouphe", "Null Rod", "Stony Silence", "Bane of Progress", "Austere Command"]}
        ]},

        # === COMBAT COMBOS ===
        {"id": "combat-1", "name": "Aggravated Assault + Mana Extra Combat", "description": "Paga mana per combat extra, genera mana durante combat", "result": "Infinite combat phases", "slots": [
            {"role": "Paga per Combat Extra", "keyword": "extra_combat_pay", "cards": ["Aggravated Assault", "Hellkite Charger", "Moraug, Fury of Akoum", "Waves of Aggression"]},
            {"role": "Genera 5+ Mana in Combat", "keyword": "combat_mana", "cards": ["Savage Ventmaw", "Neheb, the Eternal", "Sword of Feast and Famine", "Bear Umbra", "Nature's Will", "Grand Warlord Radha", "Druid's Repository"]}
        ]},
        {"id": "combat-2", "name": "Helm of the Host + Combat Extra", "description": "Helm copia creatura che da combat extra = infiniti combattimenti", "result": "Infinite combat phases", "slots": [
            {"role": "Copia Creatura Ogni Combat", "keyword": "helm_host", "cards": ["Helm of the Host"]},
            {"role": "Creatura che Da Combat Extra", "keyword": "creature_extra_combat", "cards": ["Godo, Bandit Warlord", "Aurelia, the Warleader", "Combat Celebrant", "Port Razer"]}
        ]},

        # === PLANESWALKER COMBOS ===
        {"id": "pw-1", "name": "Doubling Season + Planeswalker Ultimate", "description": "Planeswalker entra con doppi segnalini, ultimate immediata", "result": "Immediate planeswalker ultimate", "slots": [
            {"role": "Raddoppia Segnalini", "keyword": "double_counters", "cards": ["Doubling Season", "Vorinclex, Monstrous Raider", "Deepglow Skate"]},
            {"role": "Planeswalker con Ultimate Potente", "keyword": "strong_ultimate", "cards": ["Tamiyo, Field Researcher", "Teferi, Temporal Archmage", "Ugin, the Spirit Dragon", "Nicol Bolas, Dragon-God", "Jace, Architect of Thought", "Liliana, Dreadhorde General", "Vraska, Golgari Queen"]}
        ]},

        # === LANDFALL ===
        {"id": "land-1", "name": "Landfall Infinito (Bounce Land + Retreat)", "description": "Terra che rimbalza se stessa + trigger landfall", "result": "Infinite landfall triggers", "slots": [
            {"role": "Terra che Rimbalza Terra", "keyword": "bounce_land", "cards": ["Simic Growth Chamber", "Guildless Commons", "Ghost Town", "Oboro, Palace in the Clouds", "Meloku the Clouded Mirror", "Trade Routes", "Storm Cauldron"]},
            {"role": "Landfall Payoff", "keyword": "landfall_payoff", "cards": ["Retreat to Coralhelm", "Lotus Cobra", "Amulet of Vigor", "Tatyova, Benthic Druid", "Omnath, Locus of Creation", "Scute Swarm", "Felidar Retreat", "Kodama of the East Tree"]}
        ]},
    ]
    return patterns


if __name__ == "__main__":
    main()
