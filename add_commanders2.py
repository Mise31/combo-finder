import json

new_commanders = [
    {"id": "cmd-yawgmoth", "name": "Yawgmoth, Thran Physician (Sacrifice Engine)", "description": "Yawgmoth sacrifica creature per pescare e mettere -1/-1. Con Undying creatures, loop infinito di pesca e danno.", "result": "Infinite draw, infinite -1/-1 counters", "category": "Combo Commander", "slots": [
        {"role": "Commander: Sac per Pesca + -1/-1", "keyword": "yawgmoth_cmd", "cards": ["Yawgmoth, Thran Physician"]},
        {"role": "Creature con Undying", "keyword": "yawgmoth_undying", "cards": ["Geralf's Messenger", "Young Wolf", "Strangleroot Geist", "Butcher Ghoul", "Mikaeus, the Unhallowed"]},
        {"role": "Payoff / Protezione", "keyword": "yawgmoth_payoff", "cards": ["Blood Artist", "Zulaport Cutthroat", "Bastion of Remembrance", "Nest of Scarabs"]}
    ]},
    {"id": "cmd-mikaeus", "name": "Mikaeus, the Unhallowed + Sac Outlet", "description": "Mikaeus da Undying a tutte le creature non-umane. Con un sac outlet, ogni creatura muore e torna all'infinito.", "result": "Infinite death triggers, infinite ETB", "category": "Combo Commander", "slots": [
        {"role": "Commander: Da Undying a Tutti", "keyword": "mikaeus_cmd", "cards": ["Mikaeus, the Unhallowed"]},
        {"role": "Sac Outlet Gratuito", "keyword": "mikaeus_sac", "cards": ["Viscera Seer", "Carrion Feeder", "Altar of Dementia", "Ashnod's Altar", "Phyrexian Altar", "Blasting Station", "Goblin Bombardment"]},
        {"role": "Creatura Non-Umana con Effetto", "keyword": "mikaeus_creature", "cards": ["Walking Ballista", "Triskelion", "Murderous Redcap", "Puppeteer Clique", "Woodfall Primus", "Gray Merchant of Asphodel", "Plague Belcher"]}
    ]},
    {"id": "cmd-ghave", "name": "Ghave, Guru of Spores (Counter/Token Combo)", "description": "Ghave rimuove segnalini per fare token e sacrifica token per mettere segnalini. Con qualsiasi doubler, infinito.", "result": "Infinite tokens, infinite counters", "category": "Combo Commander", "slots": [
        {"role": "Commander: Token/Counter Engine", "keyword": "ghave_cmd", "cards": ["Ghave, Guru of Spores"]},
        {"role": "Doubler (raddoppia token o segnalini)", "keyword": "ghave_doubler", "cards": ["Doubling Season", "Parallel Lives", "Anointed Procession", "Cathars' Crusade", "Ivy Lane Denizen", "Good-Fortune Unicorn", "Grumgully, the Generous", "Renata, Called to the Hunt"]},
        {"role": "Mana per Attivare (1 per ciclo)", "keyword": "ghave_mana", "cards": ["Ashnod's Altar", "Phyrexian Altar", "Earthcraft", "Cryptolith Rite", "Pitiless Plunderer"]}
    ]},
    {"id": "cmd-niv-parun", "name": "Niv-Mizzet, Parun + Curiosity", "description": "Niv-Mizzet fa 1 danno quando peschi. Curiosity fa pescare quando fai danno. Loop infinito = kill.", "result": "Infinite damage, infinite draw", "category": "Combo Commander", "slots": [
        {"role": "Commander: Danno su Pesca", "keyword": "niv_cmd", "cards": ["Niv-Mizzet, Parun", "Niv-Mizzet, the Firemind"]},
        {"role": "Pesca su Danno", "keyword": "niv_curiosity", "cards": ["Curiosity", "Ophidian Eye", "Tandem Lookout", "Mind Over Matter"]}
    ]},
    {"id": "cmd-teshar", "name": "Teshar, Ancestor's Apostle (Artifact Recursion)", "description": "Teshar riporta creature costo 3 o meno quando giochi un artefatto. Con artefatti costo 0 e sac outlet, loop infinito.", "result": "Infinite ETB, infinite mana, infinite mill", "category": "Combo Commander", "slots": [
        {"role": "Commander: Rianima su Cast Artefatto", "keyword": "teshar_cmd", "cards": ["Teshar, Ancestor's Apostle"]},
        {"role": "Artefatto Costo 0 (rigiocabile)", "keyword": "teshar_0cost", "cards": ["Mox Amber", "Mishra's Bauble", "Urza's Bauble", "Ornithopter", "Memnite", "Phyrexian Walker", "Shield Sphere", "Tormod's Crypt"]},
        {"role": "Creatura CMC 3 o meno + Sac", "keyword": "teshar_creature", "cards": ["Junk Diver", "Myr Retriever", "Workshop Assistant", "Scrap Trawler", "Lion's Eye Diamond", "Ashnod's Altar", "Krark-Clan Ironworks"]}
    ]},
    {"id": "cmd-emry", "name": "Emry, Lurker of the Loch (Artifact Loop)", "description": "Emry gioca artefatti dal cimitero. Con artefatti che si sacrificano e producono mana, loop infinito.", "result": "Infinite artifact casts, infinite mana", "category": "Combo Commander", "slots": [
        {"role": "Commander: Gioca Artefatti dal Cimitero", "keyword": "emry_cmd", "cards": ["Emry, Lurker of the Loch"]},
        {"role": "Artefatto che si Sacrifica", "keyword": "emry_sac_artifact", "cards": ["Lion's Eye Diamond", "Lotus Petal", "Chromatic Star", "Chromatic Sphere", "Mishra's Bauble", "Grinding Station", "Mirran Spy"]},
        {"role": "Stappa Emry", "keyword": "emry_untap", "cards": ["Mirran Spy", "Chakram Retriever", "Intruder Alarm", "Grinding Station", "Jeskai Ascendancy"]}
    ]},
    {"id": "cmd-birgi", "name": "Birgi, God of Storytelling (Storm)", "description": "Birgi aggiunge 1 mana rosso ogni volta che giochi una magia. Con magie economiche, storm infinito.", "result": "Infinite storm, infinite mana", "category": "Combo Commander", "slots": [
        {"role": "Commander: Mana su Cast", "keyword": "birgi_cmd", "cards": ["Birgi, God of Storytelling"]},
        {"role": "Magia che Costa 1 e Pesca", "keyword": "birgi_cantrip", "cards": ["Grinning Ignus", "Haze of Rage", "Reiterate", "Bonus Round", "Jeska's Will", "Mana Geyser", "Runaway Steam-Kin"]},
        {"role": "Storm Payoff", "keyword": "birgi_payoff", "cards": ["Aetherflux Reservoir", "Grapeshot", "Empty the Warrens", "Sentinel Tower", "Guttersnipe", "Firebrand Archer"]}
    ]},
    {"id": "cmd-orvar", "name": "Orvar, the All-Form (Copy Combo)", "description": "Orvar crea copie di permanenti quando li bersagli con magie. Con magie economiche, copia terre e mana rock all'infinito.", "result": "Infinite copies of any permanent", "category": "Combo Commander", "slots": [
        {"role": "Commander: Copia su Bersaglio", "keyword": "orvar_cmd", "cards": ["Orvar, the All-Form"]},
        {"role": "Magia Economica che Bersaglia", "keyword": "orvar_spell", "cards": ["Whim of Volrath", "Clockspinning", "Gigadrowse", "Hidden Strings", "Ghostly Flicker", "Snap", "Essence Flux"]},
        {"role": "Permanente da Copiare", "keyword": "orvar_target", "cards": ["Sol Ring", "Mana Vault", "Gilded Lotus", "Nykthos, Shrine to Nyx", "Ancient Tomb", "Coveted Jewel", "Peregrine Drake"]}
    ]},
    {"id": "cmd-magda", "name": "Magda, Brazen Outlaw (Treasure Combo)", "description": "Magda crea Tesori quando i nani vengono tappati. Con 5 Tesori, cerca qualsiasi artefatto o drago dal mazzo.", "result": "Tutor any artifact/dragon, infinite treasures", "category": "Combo Commander", "slots": [
        {"role": "Commander: Tesori + Tutor", "keyword": "magda_cmd", "cards": ["Magda, Brazen Outlaw"]},
        {"role": "Tappa Nani Ripetutamente", "keyword": "magda_tap", "cards": ["Clock of Omens", "Springleaf Drum", "Survivors' Encampment", "Holdout Settlement", "Dwarven Bloodboiler", "Vehicles"]},
        {"role": "Bersaglio Tutor", "keyword": "magda_target", "cards": ["Maskwood Nexus", "Hellkite Tyrant", "Dockside Extortionist", "Cursed Mirror", "Terror of the Peaks", "Goldspan Dragon", "Ancient Copper Dragon"]}
    ]},
    {"id": "cmd-inalla", "name": "Inalla, Archmage Ritualist (Wizard ETB)", "description": "Inalla crea copie di maghi quando entrano pagando 1. Con maghi ETB potenti, valore raddoppiato o combo.", "result": "Double wizard ETB, infinite with loops", "category": "Combo Commander", "slots": [
        {"role": "Commander: Copia Mago ETB", "keyword": "inalla_cmd", "cards": ["Inalla, Archmage Ritualist"]},
        {"role": "Mago con ETB Combo", "keyword": "inalla_wizards", "cards": ["Wanderwine Prophets", "Timestream Navigator", "Bloodline Necromancer", "Dualcaster Mage", "Archaeomancer", "Spellseeker", "Thassa's Oracle", "Venser, Shaper Savant"]}
    ]},
    {"id": "cmd-tivit", "name": "Tivit, Seller of Secrets (Vote + Artifact)", "description": "Tivit crea 5 artefatti (Tesori/Indizi) quando entra o fa danno. Con flicker, valore enorme. Con Time Sieve, turni infiniti.", "result": "Infinite turns with Time Sieve", "category": "Combo Commander", "slots": [
        {"role": "Commander: Crea 5 Artefatti", "keyword": "tivit_cmd", "cards": ["Tivit, Seller of Secrets"]},
        {"role": "Turni Extra da Artefatti", "keyword": "tivit_turns", "cards": ["Time Sieve"]},
        {"role": "Flicker Tivit", "keyword": "tivit_flicker", "cards": ["Conjurer's Closet", "Thassa, Deep-Dwelling", "Deadeye Navigator", "Ghostly Flicker", "Displacer Kitten", "Panharmonicon"]}
    ]},
    {"id": "cmd-breya", "name": "Breya, Etherium Shaper (Artifact Sacrifice)", "description": "Breya sacrifica artefatti per danno/rimozione/vita. Con mana infinito o artefatti infiniti, win condition in command zone.", "result": "Infinite damage from command zone", "category": "Combo Commander", "slots": [
        {"role": "Commander: Sac 2 Artefatti = Effetto", "keyword": "breya_cmd", "cards": ["Breya, Etherium Shaper"]},
        {"role": "Artefatti Infiniti / Mana Infinito", "keyword": "breya_engine", "cards": ["Nim Deathmantle + Ashnod's Altar", "Krark-Clan Ironworks + Scrap Trawler", "Thopter Foundry + Sword of the Meek + Ashnod's Altar", "Dramatic Reversal + Isochron Scepter", "Dockside Extortionist + Temur Sabertooth"]}
    ]},
    {"id": "cmd-derevi", "name": "Derevi, Empyrial Tactician (Stax/Combo)", "description": "Derevi stappa/tappa permanenti quando creature fanno danno. Bypassa command tax. Abilita stax asimmetrico.", "result": "Asymmetric stax, infinite untaps", "category": "Combo Commander", "slots": [
        {"role": "Commander: Tap/Untap su Danno", "keyword": "derevi_cmd", "cards": ["Derevi, Empyrial Tactician"]},
        {"role": "Stax Simmetrico (tu lo bypasdi)", "keyword": "derevi_stax", "cards": ["Winter Orb", "Static Orb", "Stasis", "Rising Waters", "Hokori, Dust Drinker", "Meekstone"]},
        {"role": "Combo con Untap", "keyword": "derevi_combo", "cards": ["Najeela, the Blade-Blossom", "Edric, Spymaster of Trest", "Reconnaissance", "Nature's Will", "Bear Umbra", "Sword of Feast and Famine"]}
    ]},
    {"id": "cmd-tasigur", "name": "Tasigur, the Golden Fang (Infinite Recursion)", "description": "Tasigur riprende carte dal cimitero con la sua abilita. Con mana infinito, riprendi tutto il cimitero.", "result": "Infinite recursion with infinite mana", "category": "Combo Commander", "slots": [
        {"role": "Commander: Riprendi dal Cimitero", "keyword": "tasigur_cmd", "cards": ["Tasigur, the Golden Fang"]},
        {"role": "Mana Infinito (Sultai)", "keyword": "tasigur_mana", "cards": ["Dramatic Reversal + Isochron Scepter", "Freed from the Real + Bloom Tender", "Basalt Monolith + Rings of Brighthearth", "Peregrine Drake + Deadeye Navigator"]},
        {"role": "Win Con Ricorsiva", "keyword": "tasigur_win", "cards": ["Reality Shift", "Beast Within + Reality Shift loop", "Blue Sun's Zenith", "Stroke of Genius"]}
    ]},
    {"id": "cmd-zur", "name": "Zur the Enchanter (Tutor Incantesimi)", "description": "Zur cerca un incantesimo CMC 3 o meno quando attacca. Trova pezzi combo o lock pieces ogni turno.", "result": "Tutor enchantment every attack", "category": "Combo Commander", "slots": [
        {"role": "Commander: Cerca Incantesimo CMC 3", "keyword": "zur_cmd", "cards": ["Zur the Enchanter"]},
        {"role": "Incantesimi Combo/Lock", "keyword": "zur_targets", "cards": ["Necropotence", "Animate Dead", "Necromancy", "Rest in Peace", "Helm of Obedience", "Stasis", "Mystic Remora", "Rhystic Study", "Phyresis", "Diplomatic Immunity", "Vanishing", "Copy Enchantment"]}
    ]},
    {"id": "cmd-chatterfang", "name": "Chatterfang, Squirrel General (Token Combo)", "description": "Chatterfang crea token scoiattolo extra ogni volta che crei token. Con Pitiless Plunderer, loop infinito.", "result": "Infinite tokens, infinite death triggers", "category": "Combo Commander", "slots": [
        {"role": "Commander: Token Extra", "keyword": "chatterfang_cmd", "cards": ["Chatterfang, Squirrel General"]},
        {"role": "Crea Tesoro su Morte", "keyword": "chatterfang_plunderer", "cards": ["Pitiless Plunderer"]},
        {"role": "Sac Outlet (Chatterfang stesso!)", "keyword": "chatterfang_sac", "cards": ["Chatterfang, Squirrel General", "Viscera Seer", "Carrion Feeder", "Altar of Dementia"]},
        {"role": "Payoff", "keyword": "chatterfang_payoff", "cards": ["Blood Artist", "Zulaport Cutthroat", "Bastion of Remembrance", "Poison-Tip Archer"]}
    ]},
    {"id": "cmd-dockside-sabertooth", "name": "Dockside Extortionist + Temur Sabertooth (Mana Loop)", "description": "Dockside crea Tesori pari agli artefatti/incantesimi avversari. Sabertooth lo rimbalza per rigiocare. Se fa 5+ Tesori, mana infinito.", "result": "Infinite mana, infinite ETB", "category": "Combo Commander", "slots": [
        {"role": "Crea Tesori su ETB", "keyword": "dockside_etb", "cards": ["Dockside Extortionist"]},
        {"role": "Rimbalza in Mano", "keyword": "dockside_bounce", "cards": ["Temur Sabertooth", "Cloudstone Curio", "Erratic Portal", "Crystal Shard", "Kogla, the Titan Ape", "Emiel the Blessed"]},
        {"role": "Commander che Beneficia", "keyword": "dockside_commander", "cards": ["Korvold, Fae-Cursed King", "Prossh, Skyraider of Kher", "Kinnan, Bonder Prodigy", "Kenrith, the Returned King", "Thrasios, Triton Hero"]}
    ]},
]

def main():
    with open("patterns.json", "r", encoding="utf-8") as f:
        patterns = json.load(f)

    existing_names = {p["name"] for p in patterns}
    new = [p for p in new_commanders if p["name"] not in existing_names]
    patterns.extend(new)

    with open("patterns.json", "w", encoding="utf-8") as f:
        json.dump(patterns, f, ensure_ascii=False)

    total_cards = len(set(c for p in patterns for s in p["slots"] for c in s["cards"]))
    print(f"{len(new)} nuovi commander aggiunti")
    print(f"Totale: {len(patterns)} pattern, {total_cards} carte uniche")

if __name__ == "__main__":
    main()
