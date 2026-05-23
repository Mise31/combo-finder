"""
Add 'Cheat Into Play' and 'Soft Combo / Synergy' patterns to the database.
These are not infinite loops but powerful strategies that generate insurmountable advantage.
"""
import json

cheat_patterns = [
    # === CHEAT CREATURE INTO PLAY ===
    {"id": "cheat-oath", "name": "Oath of Druids + Creature Devastante", "description": "Se l'avversario ha piu creature, rivela carte finche non trovi una creatura. Gioca senza creature tue per attivarlo.", "result": "Creatura enorme in gioco gratis al turno 2-3", "category": "Cheat Into Play", "slots": [
        {"role": "Enabler: Oath", "keyword": "oath_enabler", "cards": ["Oath of Druids"]},
        {"role": "Attivatore (da token all'avversario)", "keyword": "oath_activator", "cards": ["Forbidden Orchard", "Beast Within", "Hunted Phantasm", "Hunted Troll", "Alliance of Arms", "Akroan Horse", "Varchild, Betrayer of Kjeldor"]},
        {"role": "Bersaglio Devastante", "keyword": "oath_target", "cards": ["Emrakul, the Aeons Torn", "Griselbrand", "Omniscience", "Blightsteel Colossus", "Progenitus", "Tidespout Tyrant", "Cognivore", "Spirit of the Night", "Akroma, Angel of Wrath", "Inkwell Leviathan", "Sphinx of the Steel Wind", "Worldspine Wurm", "Atraxa, Grand Unifier"]}
    ]},
    {"id": "cheat-sneak", "name": "Sneak Attack + Creature Enormi", "description": "Paga 1 mana rosso per mettere qualsiasi creatura in gioco con rapidita. Muore a fine turno ma il danno e fatto.", "result": "15-20 danni al turno 2-3", "category": "Cheat Into Play", "slots": [
        {"role": "Enabler: Metti in Gioco con Rapidita", "keyword": "sneak_enabler", "cards": ["Sneak Attack", "Through the Breach", "Ilharg, the Raze-Boar", "Purphoros, Bronze-Blooded"]},
        {"role": "Creatura Enorme (15+ danni)", "keyword": "sneak_target", "cards": ["Emrakul, the Aeons Torn", "Griselbrand", "Blightsteel Colossus", "Worldspine Wurm", "Serra's Emissary", "Atraxa, Grand Unifier", "Craterhoof Behemoth", "Xenagos, God of Revels", "Inferno Titan", "Ulamog, the Ceaseless Hunger", "It That Betrays", "Progenitus"]}
    ]},
    {"id": "cheat-show", "name": "Show and Tell + Permanente Imbattibile", "description": "Entrambi i giocatori mettono un permanente in gioco. Tu metti qualcosa di inarrestabile.", "result": "Permanente game-winning in gioco al turno 1-2", "category": "Cheat Into Play", "slots": [
        {"role": "Enabler: Metti in Gioco Gratis", "keyword": "show_tell_enabler", "cards": ["Show and Tell", "Eureka", "Hypergenesis", "Dream Halls"]},
        {"role": "Permanente Imbattibile", "keyword": "show_tell_target", "cards": ["Omniscience", "Emrakul, the Aeons Torn", "Griselbrand", "Blightsteel Colossus", "Progenitus", "Form of the Dragon", "Sandstone Oracle", "Atraxa, Grand Unifier", "Hullbreaker Horror", "Archon of Cruelty"]}
    ]},
    {"id": "cheat-natural-order", "name": "Natural Order + Finisher Verde", "description": "Sacrifica una creatura verde economica per cercare qualsiasi creatura verde dal mazzo.", "result": "Creatura game-ending al turno 3", "category": "Cheat Into Play", "slots": [
        {"role": "Enabler: Cerca Creatura", "keyword": "natural_order_enabler", "cards": ["Natural Order", "Green Sun's Zenith", "Finale of Devastation", "Chord of Calling", "Eldritch Evolution", "Neoform", "Birthing Pod"]},
        {"role": "Sacrificio Economico (verde)", "keyword": "cheap_green", "cards": ["Llanowar Elves", "Birds of Paradise", "Elvish Mystic", "Fyndhorn Elves", "Noble Hierarch", "Gilded Goose", "Dryad Arbor", "Allosaurus Shepherd"]},
        {"role": "Finisher", "keyword": "green_finisher", "cards": ["Craterhoof Behemoth", "Progenitus", "Verdant Force", "Woodfall Primus", "Terastodon", "Hornet Queen", "End-Raze Forerunners", "Hullbreacher", "Archon of Valor's Reach", "Runic Armasaur"]}
    ]},
    {"id": "cheat-tinker", "name": "Tinker + Artefatto Devastante", "description": "Sacrifica un artefatto economico per cercare qualsiasi artefatto dal mazzo e metterlo in gioco.", "result": "Artefatto inarrestabile al turno 2-3", "category": "Cheat Into Play", "slots": [
        {"role": "Enabler: Cerca Artefatto", "keyword": "tinker_enabler", "cards": ["Tinker", "Reshape", "Transmute Artifact", "Kuldotha Forgemaster", "Master Transmuter", "Arcum Dagsson"]},
        {"role": "Artefatto Economico (sacrificio)", "keyword": "cheap_artifact_sac", "cards": ["Mox Opal", "Mox Diamond", "Chrome Mox", "Lotus Petal", "Seat of the Synod", "Darksteel Citadel", "Ichor Wellspring", "Servo Schematic", "Chromatic Star"]},
        {"role": "Artefatto Devastante", "keyword": "tinker_target", "cards": ["Blightsteel Colossus", "Darksteel Colossus", "Inkwell Leviathan", "Myr Battlesphere", "Sundering Titan", "Bolas's Citadel", "Possessed Portal", "Spine of Ish Sah", "Phyrexian Processor", "Memory Jar", "Mindslaver"]}
    ]},

    # === REANIMATOR STRATEGIES ===
    {"id": "cheat-reanimate", "name": "Reanimate + Creatura nel Cimitero", "description": "Metti una creatura enorme nel cimitero (scarto/mill) e riportala in gioco per 1-2 mana.", "result": "Creatura enorme al turno 1-2", "category": "Cheat Into Play", "slots": [
        {"role": "Enabler: Metti nel Cimitero", "keyword": "entomb_enabler", "cards": ["Entomb", "Buried Alive", "Faithless Looting", "Careful Study", "Putrid Imp", "Oona's Prowler", "Unmarked Grave", "Persist", "Goryo's Vengeance"]},
        {"role": "Rianima", "keyword": "reanimate_spell", "cards": ["Reanimate", "Animate Dead", "Dance of the Dead", "Necromancy", "Exhume", "Life // Death", "Shallow Grave", "Dread Return", "Unburial Rites", "Persist"]},
        {"role": "Bersaglio Reanimation", "keyword": "reanimate_target", "cards": ["Griselbrand", "Emrakul, the Aeons Torn", "Archon of Cruelty", "Serra's Emissary", "Atraxa, Grand Unifier", "Akroma, Angel of Wrath", "Inkwell Leviathan", "Sphinx of the Steel Wind", "Elesh Norn, Grand Cenobite", "Iona, Shield of Emeria", "Sire of Insanity", "Tidespout Tyrant", "Jin-Gitaxias, Core Augur"]}
    ]},

    # === TOOLBOX / TUTOR CHAINS ===
    {"id": "cheat-survival", "name": "Survival of the Fittest + Toolbox", "description": "Scarta una creatura per cercarne qualsiasi altra. Trova sempre la risposta perfetta.", "result": "Accesso a qualsiasi creatura nel mazzo", "category": "Toolbox", "slots": [
        {"role": "Enabler: Cerca Creatura Ripetutamente", "keyword": "survival_enabler", "cards": ["Survival of the Fittest", "Fauna Shaman", "Birthing Pod", "Vannifar, Evolved Enigma", "Yisan, the Wanderer Bard", "Fiend Artisan"]},
        {"role": "Toolbox Creature (risposte)", "keyword": "toolbox_creatures", "cards": ["Reclamation Sage", "Acidic Slime", "Gilded Drake", "Collector Ouphe", "Hullbreacher", "Opposition Agent", "Aven Mindcensor", "Containment Priest", "Thalia, Guardian of Thraben", "Linvala, Keeper of Silence", "Kataki, War's Wage", "Magus of the Moon", "Venser, Shaper Savant", "Eternal Witness"]}
    ]},
    {"id": "cheat-rector", "name": "Academy Rector + Incantesimo Potente", "description": "Quando Rector muore, cerca qualsiasi incantesimo dal mazzo e mettilo in gioco.", "result": "Incantesimo game-winning gratis", "category": "Cheat Into Play", "slots": [
        {"role": "Enabler: Cerca Incantesimo su Morte", "keyword": "rector_enabler", "cards": ["Academy Rector", "Arena Rector", "Zur the Enchanter", "Heliod's Pilgrim", "Idyllic Tutor", "Enlightened Tutor"]},
        {"role": "Modo per Uccidere Rector", "keyword": "kill_rector", "cards": ["Cabal Therapy", "Phyrexian Tower", "High Market", "Viscera Seer", "Goblin Bombardment", "Flash"]},
        {"role": "Incantesimo Devastante", "keyword": "rector_target", "cards": ["Omniscience", "Overwhelming Splendor", "Decree of Silence", "Sandwurm Convergence", "Eldrazi Conscription", "Doubling Season", "Parallax Wave", "Sneak Attack", "Pattern of Rebirth", "Recurring Nightmare", "Necropotence", "Yawgmoth's Bargain"]}
    ]},

    # === MANA DENIAL / LAND DESTRUCTION ===
    {"id": "cheat-armageddon", "name": "Mana Denial + Board Superiore", "description": "Distruggi tutte le terre quando hai gia creature in campo. L'avversario non puo rispondere.", "result": "Avversario senza mana, tu con creature", "category": "Mana Denial", "slots": [
        {"role": "Distruggi Tutte le Terre", "keyword": "armageddon_effect", "cards": ["Armageddon", "Ravages of War", "Cataclysm", "Catastrophe", "Jokulhaups", "Obliterate", "Decree of Annihilation", "Sunder", "Upheaval"]},
        {"role": "Board Superiore (sopravvive)", "keyword": "survives_armageddon", "cards": ["Terravore", "Knight of the Reliquary", "Crucible of Worlds", "Ramunap Excavator", "Teferi, Time Raveler", "Planeswalker qualsiasi", "Mox Diamond", "Chrome Mox", "Boros Charm", "Avacyn, Angel of Hope", "Heroic Intervention"]}
    ]},
    {"id": "cheat-wasteland", "name": "Wasteland + Ricorsione Terre", "description": "Distruggi terre avversarie ogni turno rigiocando Wasteland dal cimitero.", "result": "Avversario bloccato senza mana", "category": "Mana Denial", "slots": [
        {"role": "Terra che Distrugge Terra", "keyword": "wasteland_effect", "cards": ["Wasteland", "Strip Mine", "Ghost Quarter", "Field of Ruin", "Dust Bowl", "Rishadan Port", "Tectonic Edge"]},
        {"role": "Rigioca Terra dal Cimitero", "keyword": "land_recursion", "cards": ["Crucible of Worlds", "Ramunap Excavator", "Life from the Loam", "Wrenn and Six", "Elvish Reclaimer", "Crop Rotation", "Expedition Map"]}
    ]},

    # === CARD ADVANTAGE ENGINES ===
    {"id": "cheat-necropotence", "name": "Necropotence / Pesca Massiva + Win", "description": "Pesca enormi quantita di carte pagando vita, poi vinci con la mano piena.", "result": "7-20 carte extra, vittoria quasi certa", "category": "Card Advantage Engine", "slots": [
        {"role": "Pesca Massiva", "keyword": "mass_draw", "cards": ["Necropotence", "Ad Nauseam", "Griselbrand", "Peer into the Abyss", "Sylvan Library", "Rhystic Study", "Mystic Remora", "Consecrated Sphinx", "Jin-Gitaxias, Core Augur", "Notion Thief + Wheel"]},
        {"role": "Win Condition dalla Mano Piena", "keyword": "hand_wincon_2", "cards": ["Tendrils of Agony", "Aetherflux Reservoir", "Thassa's Oracle", "Bolas's Citadel", "Peer into the Abyss + Thassa's Oracle", "Psychosis Crawler", "Borborygmos Enraged", "Sickening Dreams"]}
    ]},

    # === PRISON / HATE ===
    {"id": "cheat-blood-moon", "name": "Blood Moon / Back to Basics + Mana Base Immune", "description": "Trasforma tutte le terre non-base in montagne. Tu giochi terre base, l'avversario e bloccato.", "result": "Avversario con terre inutili", "category": "Prison", "slots": [
        {"role": "Hate Terre Non-Base", "keyword": "nonbasic_hate", "cards": ["Blood Moon", "Back to Basics", "Magus of the Moon", "Ruination", "From the Ashes", "Wave of Vitriol", "Price of Progress"]},
        {"role": "Mana Base Immune", "keyword": "immune_mana", "cards": ["Terre base", "Dryad of the Ilysian Grove", "Chromatic Lantern", "Prismatic Omen", "Mox Diamond", "Chrome Mox", "Simian Spirit Guide"]}
    ]},
    {"id": "cheat-chalice", "name": "Chalice of the Void + Curve Asimmetrica", "description": "Chalice a 1 blocca tutte le magie a costo 1. Tu giochi carte a costo diverso.", "result": "Avversario non puo giocare meta del mazzo", "category": "Prison", "slots": [
        {"role": "Lock su Costo Specifico", "keyword": "chalice_lock", "cards": ["Chalice of the Void", "Trinisphere", "Thorn of Amethyst", "Sphere of Resistance", "Thalia, Guardian of Thraben", "Vryn Wingmare", "Glowrider", "Lodestone Golem"]},
        {"role": "Mana Veloce (gioca prima)", "keyword": "fast_mana_prison", "cards": ["Ancient Tomb", "City of Traitors", "Simian Spirit Guide", "Chrome Mox", "Mox Diamond", "Sol Ring", "Mana Crypt", "Grim Monolith", "Mishra's Workshop"]}
    ]},

    # === TEMPO / SYNERGY COMBOS ===
    {"id": "cheat-vial", "name": "Aether Vial + Creature Flash/ETB", "description": "Metti creature in gioco gratis a velocita istantanea ogni turno.", "result": "Creature gratis ogni turno, non counterabili", "category": "Tempo Engine", "slots": [
        {"role": "Metti Creature Gratis", "keyword": "vial_enabler", "cards": ["Aether Vial", "Collected Company", "Cavern of Souls", "Allosaurus Shepherd"]},
        {"role": "Creature con ETB Potente", "keyword": "vial_creatures", "cards": ["Flickerwisp", "Skyclave Apparition", "Thalia, Guardian of Thraben", "Meddling Mage", "Phantasmal Image", "Reflector Mage", "Spell Queller", "Kitesail Freebooter", "Thought-Knot Seer", "Restoration Angel", "Soulherder"]}
    ]},
    {"id": "cheat-cascade", "name": "Cascade + Magia Specifica", "description": "Cascade trova sempre la stessa carta se costruisci il mazzo giusto.", "result": "Magia potente garantita gratis", "category": "Cheat Into Play", "slots": [
        {"role": "Cascade Enabler", "keyword": "cascade_enabler", "cards": ["Shardless Agent", "Bloodbraid Elf", "Violent Outburst", "Demonic Dread", "Ardent Plea", "Living End", "Restore Balance"]},
        {"role": "Unico Bersaglio nel Mazzo", "keyword": "cascade_target", "cards": ["Living End", "Restore Balance", "Ancestral Vision", "Crashing Footfalls", "Glimpse of Tomorrow", "Hypergenesis"]}
    ]},
    {"id": "cheat-storm", "name": "Storm Engine + Finisher Storm", "description": "Gioca molte magie in un turno, poi lancia una magia con Storm per copiarla X volte.", "result": "20+ copie di una magia letale", "category": "Storm", "slots": [
        {"role": "Genera Storm Count", "keyword": "storm_engine", "cards": ["Dark Ritual", "Cabal Ritual", "Lion's Eye Diamond", "Lotus Petal", "Rite of Flame", "Desperate Ritual", "Pyretic Ritual", "Manamorphose", "Gitaxian Probe", "Past in Flames", "Yawgmoth's Will", "Underworld Breach"]},
        {"role": "Finisher Storm", "keyword": "storm_finisher", "cards": ["Tendrils of Agony", "Grapeshot", "Brain Freeze", "Empty the Warrens", "Mind's Desire", "Temporal Fissure", "Aetherflux Reservoir"]}
    ]},
    {"id": "cheat-dredge", "name": "Dredge Engine + Payoff dal Cimitero", "description": "Riempi il cimitero con Dredge, poi usa carte che funzionano dal cimitero.", "result": "Board enorme senza pagare mana", "category": "Graveyard Engine", "slots": [
        {"role": "Dredge (riempi cimitero)", "keyword": "dredge_engine", "cards": ["Golgari Grave-Troll", "Stinkweed Imp", "Life from the Loam", "Shambling Shell", "Dakmor Salvage", "Golgari Thug"]},
        {"role": "Enabler Scarto", "keyword": "dredge_discard", "cards": ["Faithless Looting", "Cathartic Reunion", "Breakthrough", "Careful Study", "Bazaar of Baghdad", "Cephalid Coliseum", "Lion's Eye Diamond"]},
        {"role": "Payoff dal Cimitero", "keyword": "dredge_payoff", "cards": ["Narcomoeba", "Prized Amalgam", "Creeping Chill", "Bridge from Below", "Ichorid", "Nether Shadow", "Cabal Therapy", "Dread Return", "Hogaak, Arisen Necropolis", "Bloodghast"]}
    ]},
]

def main():
    with open("patterns.json", "r", encoding="utf-8") as f:
        patterns = json.load(f)

    existing_names = {p["name"] for p in patterns}
    new = [p for p in cheat_patterns if p["name"] not in existing_names]
    patterns.extend(new)

    with open("patterns.json", "w", encoding="utf-8") as f:
        json.dump(patterns, f, ensure_ascii=False)

    total_cards = len(set(c for p in patterns for s in p["slots"] for c in s["cards"]))
    print(f"{len(new)} nuovi pattern aggiunti")
    print(f"Totale: {len(patterns)} pattern, {total_cards} carte uniche")

if __name__ == "__main__":
    main()
