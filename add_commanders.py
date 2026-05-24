import json

commander_patterns = [
    # === S-TIER cEDH COMBO COMMANDERS ===
    {"id": "cmd-kinnan", "name": "Kinnan, Bonder Prodigy + Basalt Monolith", "description": "Kinnan fa produrre 1 mana extra ai mana rock. Basalt Monolith + Kinnan = mana infinito. Poi attiva Kinnan per mettere creature in gioco.", "result": "Infinite mana, cheat creatures into play", "category": "Combo Commander", "slots": [
        {"role": "Commander: Mana Doubler", "keyword": "kinnan_cmd", "cards": ["Kinnan, Bonder Prodigy"]},
        {"role": "Si Stappa per 3 (produce 4 con Kinnan)", "keyword": "kinnan_rock", "cards": ["Basalt Monolith", "Grim Monolith", "Mana Vault"]},
        {"role": "Outlet per Mana Infinito", "keyword": "kinnan_outlet", "cards": ["Kinnan, Bonder Prodigy", "Thrasios, Triton Hero", "Walking Ballista", "Staff of Domination", "Finale of Devastation"]}
    ]},
    {"id": "cmd-najeela", "name": "Najeela, the Blade-Blossom + Mana in Combat", "description": "Najeela crea token warrior quando attacca. Con mana extra in combat, attiva la sua abilita per combat infiniti.", "result": "Infinite combat phases, infinite tokens", "category": "Combo Commander", "slots": [
        {"role": "Commander: Combat Infiniti", "keyword": "najeela_cmd", "cards": ["Najeela, the Blade-Blossom"]},
        {"role": "Genera Mana in Combat (WUBRG)", "keyword": "najeela_mana", "cards": ["Derevi, Empyrial Tactician", "Nature's Will", "Sword of Feast and Famine", "Bear Umbra", "Druids' Repository", "Savage Ventmaw", "Grand Warlord Radha", "Cryptolith Rite"]}
    ]},
    {"id": "cmd-thrasios-tymna", "name": "Thrasios + Tymna (4-Color Value/Combo)", "description": "Thrasios e un outlet per mana infinito dalla command zone. Tymna pesca carte. Insieme abilitano qualsiasi combo 4 colori.", "result": "Infinite draw (Thrasios), card advantage (Tymna)", "category": "Combo Commander", "slots": [
        {"role": "Commander: Mana Sink", "keyword": "thrasios_cmd", "cards": ["Thrasios, Triton Hero"]},
        {"role": "Commander: Card Draw", "keyword": "tymna_cmd", "cards": ["Tymna the Weaver", "Kraum, Ludevic's Opus", "Rograkh, Son of Rohgahh"]},
        {"role": "Combo Mana Infinito (qualsiasi)", "keyword": "thrasios_combo", "cards": ["Dramatic Reversal + Isochron Scepter", "Freed from the Real + Bloom Tender", "Basalt Monolith + Rings of Brighthearth", "Dockside Extortionist + Temur Sabertooth", "Underworld Breach + Brain Freeze + Lion's Eye Diamond"]}
    ]},
    {"id": "cmd-kenrith", "name": "Kenrith, the Returned King (5-Color Outlet)", "description": "Kenrith ha 5 abilita attivate. Con mana infinito, da vita infinita, pesca infinita, rianima tutto, o pompa creature.", "result": "Win con qualsiasi combo di mana infinito", "category": "Combo Commander", "slots": [
        {"role": "Commander: 5-Color Outlet", "keyword": "kenrith_cmd", "cards": ["Kenrith, the Returned King"]},
        {"role": "Genera Mana Infinito", "keyword": "kenrith_mana", "cards": ["Basalt Monolith + Rings of Brighthearth", "Dramatic Reversal + Isochron Scepter", "Dockside Extortionist + Temur Sabertooth", "Freed from the Real + Bloom Tender", "Peregrine Drake + Deadeye Navigator", "Food Chain + Eternal Scourge"]}
    ]},
    {"id": "cmd-sisay", "name": "Sisay, Weatherlight Captain (Tutor in Command Zone)", "description": "Sisay cerca qualsiasi leggendario dal mazzo. Con abbastanza potere, cerca pezzi combo direttamente.", "result": "Tutor ripetibile dalla command zone", "category": "Combo Commander", "slots": [
        {"role": "Commander: Cerca Leggendari", "keyword": "sisay_cmd", "cards": ["Sisay, Weatherlight Captain"]},
        {"role": "Leggendari Combo Piece", "keyword": "sisay_targets", "cards": ["Jhoira, Weatherlight Captain", "Emry, Lurker of the Loch", "Kinnan, Bonder Prodigy", "Derevi, Empyrial Tactician", "Selvala, Heart of the Wilds", "Ashaya, Soul of the Wild", "Quirion Ranger"]}
    ]},
    {"id": "cmd-kess", "name": "Kess, Dissident Mage (Flashback Combo)", "description": "Kess permette di giocare istantanei/stregonerie dal cimitero. Raddoppia le risorse combo e abilita Consultation lines.", "result": "Flashback combo pieces, Consultation win", "category": "Combo Commander", "slots": [
        {"role": "Commander: Flashback", "keyword": "kess_cmd", "cards": ["Kess, Dissident Mage"]},
        {"role": "Win Condition", "keyword": "kess_win", "cards": ["Thassa's Oracle", "Demonic Consultation", "Tainted Pact", "Doomsday", "Underworld Breach", "Brain Freeze", "Lion's Eye Diamond"]}
    ]},

    # === A-TIER COMBO COMMANDERS ===
    {"id": "cmd-yuriko", "name": "Yuriko, the Tiger's Shadow (Damage Combo)", "description": "Yuriko fa danno pari al costo di mana della carta rivelata. Con manipolazione top-deck, fa 10+ danni per trigger.", "result": "Massive damage from commander trigger", "category": "Combo Commander", "slots": [
        {"role": "Commander: Danno su Ninja Hit", "keyword": "yuriko_cmd", "cards": ["Yuriko, the Tiger's Shadow"]},
        {"role": "Carte Alto Costo in Cima", "keyword": "yuriko_top", "cards": ["Scroll Rack", "Brainstorm", "Mystical Tutor", "Vampiric Tutor", "Sensei's Divining Top", "Lim-Dul's Vault"]},
        {"role": "Carte con CMC Alto", "keyword": "yuriko_bombs", "cards": ["Draco", "Blinkmoth Infusion", "Treasure Cruise", "Dig Through Time", "Temporal Trespass", "Commit // Memory", "Consign // Oblivion"]}
    ]},
    {"id": "cmd-gitrog", "name": "The Gitrog Monster (Dredge Combo)", "description": "Gitrog pesca quando una terra va al cimitero. Con Dakmor Salvage (dredge) e un discard outlet, loop infinito.", "result": "Infinite draw, infinite landfall, win", "category": "Combo Commander", "slots": [
        {"role": "Commander: Pesca su Terra al Cimitero", "keyword": "gitrog_cmd", "cards": ["The Gitrog Monster"]},
        {"role": "Dredge Terra", "keyword": "gitrog_dredge", "cards": ["Dakmor Salvage"]},
        {"role": "Discard Outlet", "keyword": "gitrog_discard", "cards": ["Putrid Imp", "Noose Constrictor", "Wild Mongrel", "Oblivion Crown", "Chains of Mephistopheles", "Skirge Familiar"]}
    ]},
    {"id": "cmd-korvold", "name": "Korvold, Fae-Cursed King (Sacrifice Value)", "description": "Korvold pesca e cresce ogni volta che sacrifichi. Con Food Chain o sac loops, pesca tutto il mazzo.", "result": "Draw entire deck, infinite power", "category": "Combo Commander", "slots": [
        {"role": "Commander: Pesca su Sacrificio", "keyword": "korvold_cmd", "cards": ["Korvold, Fae-Cursed King"]},
        {"role": "Sacrificio Infinito", "keyword": "korvold_sac", "cards": ["Food Chain + Eternal Scourge", "Dockside Extortionist + Temur Sabertooth", "Pitiless Plunderer + Gravecrawler", "Nim Deathmantle + Ashnod's Altar + token maker"]}
    ]},
    {"id": "cmd-urza", "name": "Urza, Lord High Artificer (Artifact Combo)", "description": "Urza rende ogni artefatto un mana rock. Con Dramatic Scepter o Winter Orb, domina.", "result": "All artifacts tap for mana, combo enabler", "category": "Combo Commander", "slots": [
        {"role": "Commander: Artefatti = Mana", "keyword": "urza_cmd", "cards": ["Urza, Lord High Artificer"]},
        {"role": "Combo Artefatti", "keyword": "urza_combo", "cards": ["Isochron Scepter + Dramatic Reversal", "Winter Orb", "Static Orb", "Mana Vault", "Grim Monolith", "Sensei's Divining Top + cost reducer", "Mystic Forge + top + cost reducer"]}
    ]},
    {"id": "cmd-selvala", "name": "Selvala, Heart of the Wilds (Big Mana Combo)", "description": "Selvala produce mana pari alla forza della creatura piu grande. Con creature grosse e untap, mana infinito.", "result": "Infinite mana from commander", "category": "Combo Commander", "slots": [
        {"role": "Commander: Mana = Forza Maggiore", "keyword": "selvala_cmd", "cards": ["Selvala, Heart of the Wilds"]},
        {"role": "Stappa Selvala", "keyword": "selvala_untap", "cards": ["Staff of Domination", "Umbral Mantle", "Sword of the Paruns", "Wirewood Symbiote", "Quirion Ranger", "Scryb Ranger", "Temur Sabertooth"]},
        {"role": "Creatura Grande (4+ forza)", "keyword": "selvala_big", "cards": ["Phyrexian Dreadnought", "Ghalta, Primal Hunger", "Impervious Greatwurm", "Craterhoof Behemoth", "Great Oak Guardian"]}
    ]},
    {"id": "cmd-brago", "name": "Brago, King Eternal (Flicker Combo)", "description": "Brago flickera tutti i tuoi non-terra quando fa danno. Con mana rock e ETB, valore infinito.", "result": "Flicker all nonlands on combat damage", "category": "Combo Commander", "slots": [
        {"role": "Commander: Flicker su Danno", "keyword": "brago_cmd", "cards": ["Brago, King Eternal"]},
        {"role": "Mana Rock (si stappano con flicker)", "keyword": "brago_rocks", "cards": ["Sol Ring", "Mana Vault", "Gilded Lotus", "Thran Dynamo", "Basalt Monolith", "Arcane Signet"]},
        {"role": "ETB Potente (flickerato ogni turno)", "keyword": "brago_etb", "cards": ["Strionic Resonator", "Lavinia of the Tenth", "Spine of Ish Sah", "Cloudblazer", "Venser, Shaper Savant", "Reality Acid", "Act of Authority", "Rishadan Brigand"]}
    ]},
    {"id": "cmd-meren", "name": "Meren of Clan Nel Toth (Recursion Combo)", "description": "Meren riporta creature dal cimitero ogni end step. Con sac outlet e creature con ETB, valore inarrestabile.", "result": "Free recursion every turn, combo enabler", "category": "Combo Commander", "slots": [
        {"role": "Commander: Rianima Gratis", "keyword": "meren_cmd", "cards": ["Meren of Clan Nel Toth"]},
        {"role": "Sac Outlet", "keyword": "meren_sac", "cards": ["Viscera Seer", "Carrion Feeder", "Altar of Dementia", "Ashnod's Altar", "Phyrexian Altar"]},
        {"role": "Creature Combo con Meren", "keyword": "meren_creatures", "cards": ["Protean Hulk", "Mikaeus, the Unhallowed", "Walking Ballista", "Woodfall Primus", "Eternal Witness", "Spore Frog", "Plaguecrafter"]}
    ]},
    {"id": "cmd-prossh", "name": "Prossh, Skyraider of Kher + Food Chain", "description": "Prossh crea token pari al mana speso. Con Food Chain, esilia Prossh per mana, rigiocalo per piu token. Infinito.", "result": "Infinite tokens, infinite mana", "category": "Combo Commander", "slots": [
        {"role": "Commander: Crea Token su Cast", "keyword": "prossh_cmd", "cards": ["Prossh, Skyraider of Kher"]},
        {"role": "Esilia per Mana Creature", "keyword": "prossh_fc", "cards": ["Food Chain"]},
        {"role": "Payoff Token Infiniti", "keyword": "prossh_payoff", "cards": ["Goblin Bombardment", "Blood Artist", "Zulaport Cutthroat", "Purphoros, God of the Forge", "Impact Tremors", "Altar of Dementia"]}
    ]},
    {"id": "cmd-narset", "name": "Narset, Enlightened Master (Free Spells)", "description": "Narset esilia 4 carte quando attacca e le gioca gratis. Con extra turn e combat, catena infinita.", "result": "Free spells on attack, potential infinite turns", "category": "Combo Commander", "slots": [
        {"role": "Commander: Cast Gratis su Attacco", "keyword": "narset_cmd", "cards": ["Narset, Enlightened Master"]},
        {"role": "Extra Turn / Extra Combat", "keyword": "narset_turns", "cards": ["Temporal Mastery", "Time Warp", "Beacon of Tomorrows", "Aggravated Assault", "Waves of Aggression", "Relentless Assault", "World at War"]},
        {"role": "Protezione / Enabler", "keyword": "narset_protect", "cards": ["Lightning Greaves", "Swiftfoot Boots", "Hall of the Bandit Lord", "Generator Servant", "Need for Speed", "Mass Hysteria"]}
    ]},
    {"id": "cmd-godo", "name": "Godo, Bandit Warlord + Helm of the Host", "description": "Godo cerca un equipaggiamento quando entra. Cerca Helm of the Host, equipaggia, ogni combat crea copia di Godo che da un altro combat.", "result": "Infinite combat phases (1-card combo in command zone)", "category": "Combo Commander", "slots": [
        {"role": "Commander: Cerca Equipaggiamento", "keyword": "godo_cmd", "cards": ["Godo, Bandit Warlord"]},
        {"role": "Equipaggiamento Win", "keyword": "godo_helm", "cards": ["Helm of the Host"]},
        {"role": "Acceleratori (cast Godo prima)", "keyword": "godo_fast", "cards": ["Mana Crypt", "Sol Ring", "Mana Vault", "Grim Monolith", "Treasonous Ogre", "Seething Song", "Desperate Ritual", "Pyretic Ritual", "Jeweled Lotus", "Ancient Tomb"]}
    ]},
    {"id": "cmd-heliod", "name": "Heliod, Sun-Crowned + Walking Ballista", "description": "Heliod da lifelink a Ballista. Ballista fa danno, guadagni vita, Heliod mette +1/+1 su Ballista. Loop infinito.", "result": "Infinite damage (2-card combo, 1 in command zone)", "category": "Combo Commander", "slots": [
        {"role": "Commander: +1/+1 su Lifegain", "keyword": "heliod_cmd", "cards": ["Heliod, Sun-Crowned"]},
        {"role": "Creatura che Fa Danno e Guadagna Vita", "keyword": "heliod_combo", "cards": ["Walking Ballista", "Triskelion"]},
        {"role": "Tutor per Ballista", "keyword": "heliod_tutor", "cards": ["Ranger of Eos", "Ranger-Captain of Eos", "Enlightened Tutor", "Stoneforge Mystic", "Recruiter of the Guard"]}
    ]},
]

def main():
    with open("patterns.json", "r", encoding="utf-8") as f:
        patterns = json.load(f)

    existing_names = {p["name"] for p in patterns}
    new = [p for p in commander_patterns if p["name"] not in existing_names]
    patterns.extend(new)

    with open("patterns.json", "w", encoding="utf-8") as f:
        json.dump(patterns, f, ensure_ascii=False)

    total_cards = len(set(c for p in patterns for s in p["slots"] for c in s["cards"]))
    print(f"{len(new)} commander combo pattern aggiunti")
    print(f"Totale: {len(patterns)} pattern, {total_cards} carte uniche")

if __name__ == "__main__":
    main()
