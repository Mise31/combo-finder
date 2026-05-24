let patterns = [];
let currentTab = 'patterns';
let currentLang = 'it';
const SCRYFALL_API = 'https://api.scryfall.com/cards/named';

const i18n = {
    it: { search: 'Scrivi il nome di una carta...', searchBtn: 'Ricerca', allFormats: 'Tutti i formati', result: 'Risultato', steps: 'Come funziona:', step_play: 'Gioca', step_with: 'con', step_activate: 'Attiva', step_combo: 'Combinali insieme', step_result: 'Risultato', noResults: 'Nessun risultato. Prova un altro nome.', startMsg: 'Inserisci il nome di una carta e premi <strong style="color:#7c3aed;">Ricerca</strong> per trovare combo e pattern.', patterns: 'Pattern', combos: 'Combo', commanders: 'Commander', matrix: 'Matrice' },
    en: { search: 'Type a card name...', searchBtn: 'Search', allFormats: 'All formats', result: 'Result', steps: 'How it works:', step_play: 'Play', step_with: 'with', step_activate: 'Activate', step_combo: 'Combine them', step_result: 'Result', noResults: 'No results. Try another name.', startMsg: 'Type a card name and press <strong style="color:#7c3aed;">Search</strong> to find combos and patterns.', patterns: 'Patterns', combos: 'Combos', commanders: 'Commander', matrix: 'Matrix' },
    es: { search: 'Escribe el nombre de una carta...', searchBtn: 'Buscar', allFormats: 'Todos los formatos', result: 'Resultado', steps: 'Cómo funciona:', step_play: 'Juega', step_with: 'con', step_activate: 'Activa', step_combo: 'Combínalos', step_result: 'Resultado', noResults: 'Sin resultados. Prueba otro nombre.', startMsg: 'Escribe el nombre de una carta y pulsa <strong style="color:#7c3aed;">Buscar</strong> para encontrar combos.', patterns: 'Patrones', combos: 'Combos', commanders: 'Commander', matrix: 'Matriz' },
    de: { search: 'Kartenname eingeben...', searchBtn: 'Suchen', allFormats: 'Alle Formate', result: 'Ergebnis', steps: 'So funktioniert es:', step_play: 'Spiele', step_with: 'mit', step_activate: 'Aktiviere', step_combo: 'Kombiniere sie', step_result: 'Ergebnis', noResults: 'Keine Ergebnisse. Versuche einen anderen Namen.', startMsg: 'Gib einen Kartennamen ein und drücke <strong style="color:#7c3aed;">Suchen</strong> um Combos zu finden.', patterns: 'Muster', combos: 'Combos', commanders: 'Commander', matrix: 'Matrix' },
    fr: { search: 'Tapez un nom de carte...', searchBtn: 'Rechercher', allFormats: 'Tous les formats', result: 'Résultat', steps: 'Comment ça marche:', step_play: 'Jouez', step_with: 'avec', step_activate: 'Activez', step_combo: 'Combinez-les', step_result: 'Résultat', noResults: 'Aucun résultat. Essayez un autre nom.', startMsg: 'Tapez un nom de carte et appuyez sur <strong style="color:#7c3aed;">Rechercher</strong> pour trouver des combos.', patterns: 'Patterns', combos: 'Combos', commanders: 'Commander', matrix: 'Matrice' }
};

function t(key) { return i18n[currentLang][key] || i18n['en'][key] || key; }

function generateSteps(pattern) {
    if (pattern.steps && pattern.steps.length) return pattern.steps;
    // Auto-generate steps from slots
    const lang = currentLang;
    const steps = [];
    pattern.slots.forEach((slot, i) => {
        const example = slot.cards[0] || '?';
        steps.push(`${t('step_play')} ${example} (${slot.role})`);
    });
    steps.push(`${t('step_combo')} → ${pattern.result}`);
    return steps;
}

// Load data
async function init() {
    try {
        const resp = await fetch('./patterns.json');
        patterns = await resp.json();
    } catch (e) {
        patterns = [];
    }
    updateStats();
    // Don't render anything at start - wait for user to search
    document.getElementById('content').innerHTML = '<p style="text-align:center;color:#666;padding:40px 20px;font-size:0.95em;">' + t('startMsg') + '</p>';
}

function updateStats() {
    const totalCards = new Set(patterns.flatMap(p => p.slots.flatMap(s => s.cards))).size;
    const totalCombos = patterns.reduce((sum, p) => {
        const slotSizes = p.slots.map(s => s.cards.length);
        return sum + slotSizes.reduce((a, b) => a * b, 1);
    }, 0);
    document.getElementById('stats').textContent =
        `${patterns.length} pattern | ${totalCards} carte uniche | ${totalCombos} combinazioni possibili`;
}

function render() {
    const search = document.getElementById('search').value.toLowerCase();
    const formatFilter = document.getElementById('format-filter').value;
    const content = document.getElementById('content');

    if (currentTab === 'patterns') renderPatterns(content, search, formatFilter);
    else if (currentTab === 'combos') renderCombos(content, search, formatFilter);
    else if (currentTab === 'commanders') renderCommanders(content, search, formatFilter);
    else if (currentTab === 'matrix') renderMatrix(content, search, formatFilter);
}

function renderPatterns(container, search) {
    let filtered = patterns;
    if (search) {
        filtered = patterns.filter(p =>
            p.name.toLowerCase().includes(search) ||
            p.description.toLowerCase().includes(search) ||
            (p.formats || []).some(f => f.toLowerCase().includes(search)) ||
            p.slots.some(s => s.cards.some(c => c.toLowerCase().includes(search)))
        );
    }

    container.innerHTML = filtered.map(p => `
        <div class="pattern-card">
            <div class="pattern-name">${p.name}</div>
            <div class="pattern-desc">${p.description}</div>
            <div class="pattern-result">🏆 ${p.result}</div>
            <div class="pattern-formats">${(p.formats || []).map(f => `<span class="fmt-badge fmt-${f}">${f}</span>`).join('')}</div>
            <div class="slots">
                ${p.slots.map(s => `
                    <div class="slot">
                        <div class="slot-label">${s.role}</div>
                        <div class="slot-cards">
                            ${s.cards.map(c => `<span class="slot-card" data-card="${c}">${c}</span>`).join('')}
                        </div>
                    </div>
                `).join('')}
            </div>
            <div style="margin-top:10px;padding:10px;background:#0f0f1a;border-radius:6px;border-left:3px solid #7c3aed;">
                <div style="font-size:0.75em;color:#7c3aed;font-weight:bold;margin-bottom:6px;">${t('steps')}</div>
                <ol style="padding-left:18px;font-size:0.8em;color:#ccc;line-height:1.6;">
                    ${generateSteps(p).map(s => `<li>${s}</li>`).join('')}
                </ol>
            </div>
        </div>
    `).join('');
}

function renderCommanders(container, search, formatFilter) {
    let cmdPatterns = patterns.filter(p => (p.category === 'Combo Commander') || (p.slots && p.slots.some(s => s.role && s.role.toLowerCase().includes('commander'))));
    if (formatFilter) {
        cmdPatterns = cmdPatterns.filter(p => (p.formats || []).includes(formatFilter));
    }
    if (search) {
        cmdPatterns = cmdPatterns.filter(p =>
            p.name.toLowerCase().includes(search) ||
            p.description.toLowerCase().includes(search) ||
            p.slots.some(s => s.cards.some(c => c.toLowerCase().includes(search)))
        );
    }

    if (!cmdPatterns.length) {
        container.innerHTML = '<p style="text-align:center;color:#666;padding:40px;">Nessun commander combo trovato. Prova a cercare un nome (es: Kinnan, Najeela, Godo...)</p>';
        return;
    }

    container.innerHTML = cmdPatterns.map(p => `
        <div class="pattern-card">
            <div class="pattern-name">${p.name}</div>
            <div class="pattern-desc">${p.description}</div>
            <div class="pattern-result">🏆 ${p.result}</div>
            <div class="pattern-formats">${(p.formats || []).map(f => '<span class="fmt-badge fmt-' + f + '">' + f + '</span>').join('')}</div>
            <div class="slots">
                ${p.slots.map(s => `
                    <div class="slot">
                        <div class="slot-label">${s.role}</div>
                        <div class="slot-cards">
                            ${s.cards.map(c => '<span class="slot-card" data-card="' + c + '">' + c + '</span>').join('')}
                        </div>
                    </div>
                `).join('')}
            </div>
            <div style="margin-top:10px;padding:10px;background:#0f0f1a;border-radius:6px;border-left:3px solid #7c3aed;">
                <div style="font-size:0.75em;color:#7c3aed;font-weight:bold;margin-bottom:6px;">${t('steps')}</div>
                <ol style="padding-left:18px;font-size:0.8em;color:#ccc;line-height:1.6;">
                    ${generateSteps(p).map(s => '<li>' + s + '</li>').join('')}
                </ol>
            </div>
        </div>
    `).join('');
}

function renderCombos(container, search, formatFilter) {
    // Generate all specific combos from patterns
    let sourcePatterns = patterns;
    if (formatFilter) {
        sourcePatterns = sourcePatterns.filter(p => (p.formats || []).includes(formatFilter));
    }
    let combos = [];
    sourcePatterns.forEach(p => {
        if (p.slots.length === 2) {
            p.slots[0].cards.forEach(a => {
                p.slots[1].cards.forEach(b => {
                    combos.push({ pattern: p.name, cards: [a, b], result: p.result });
                });
            });
        } else if (p.slots.length === 3) {
            p.slots[0].cards.forEach(a => {
                p.slots[1].cards.forEach(b => {
                    p.slots[2].cards.forEach(c => {
                        combos.push({ pattern: p.name, cards: [a, b, c], result: p.result });
                    });
                });
            });
        }
    });

    if (search) {
        combos = combos.filter(c =>
            c.cards.some(card => card.toLowerCase().includes(search)) ||
            c.pattern.toLowerCase().includes(search)
        );
    }

    const shown = combos.slice(0, 100);
    container.innerHTML = `<p style="color:#888;font-size:0.8em;margin-bottom:12px;">${combos.length} combo totali (mostrate ${shown.length})</p>` +
        shown.map(c => `
            <div class="pattern-card" style="padding:10px;">
                <div style="font-size:0.9em;color:#fff;font-weight:bold;">${c.cards.join(' + ')}</div>
                <div style="font-size:0.75em;color:#888;margin-top:4px;">Pattern: ${c.pattern}</div>
                <div style="font-size:0.75em;color:#4ecca3;margin-top:2px;">→ ${c.result}</div>
            </div>
        `).join('');
}

function renderMatrix(container, search, formatFilter) {
    // Show matrix view: for each pattern with 2 slots, show a grid
    let html = '';
    let matrixPatterns = patterns.filter(p => p.slots.length === 2);
    if (formatFilter) {
        matrixPatterns = matrixPatterns.filter(p => (p.formats || []).includes(formatFilter));
    }
    matrixPatterns.forEach(p => {
        const slotA = p.slots[0];
        const slotB = p.slots[1];

        if (search && !p.name.toLowerCase().includes(search) &&
            !slotA.cards.some(c => c.toLowerCase().includes(search)) &&
            !slotB.cards.some(c => c.toLowerCase().includes(search))) return;

        html += `<div class="pattern-card">
            <div class="pattern-name">${p.name}</div>
            <div class="pattern-result">🏆 ${p.result}</div>
            <div style="overflow-x:auto;margin-top:10px;">
                <table style="border-collapse:collapse;font-size:0.7em;width:100%;">
                    <tr>
                        <th style="padding:4px;border:1px solid #2d2d44;background:#0f0f1a;color:#7c3aed;">↓ ${slotA.role} / ${slotB.role} →</th>
                        ${slotB.cards.map(c => `<th style="padding:4px;border:1px solid #2d2d44;background:#0f0f1a;color:#ddd;writing-mode:vertical-rl;max-width:30px;">${c}</th>`).join('')}
                    </tr>
                    ${slotA.cards.map(a => `
                        <tr>
                            <td style="padding:4px;border:1px solid #2d2d44;color:#ddd;white-space:nowrap;">${a}</td>
                            ${slotB.cards.map(b => `<td style="padding:4px;border:1px solid #2d2d44;text-align:center;background:#1a2e1a;color:#4ecca3;">✓</td>`).join('')}
                        </tr>
                    `).join('')}
                </table>
            </div>
        </div>`;
    });
    container.innerHTML = html || '<p style="color:#888;text-align:center;">Nessun pattern con matrice trovato</p>';
}


// === COMPARE FUNCTIONALITY ===
async function compareCard(cardName) {
    const results = document.getElementById('compare-results');
    results.innerHTML = '<p style="color:#888;">Cercando...</p>';

    const name = cardName.trim().toLowerCase();
    if (!name) { results.innerHTML = ''; return; }

    let matches = [];
    let newSuggestions = [];

    // 1. Check if card is already in any pattern
    patterns.forEach(p => {
        p.slots.forEach(s => {
            if (s.cards.some(c => c.toLowerCase().includes(name))) {
                matches.push({
                    type: 'existing',
                    pattern: p.name,
                    slot: s.role,
                    result: p.result
                });
            }
        });
    });

    // 2. Fetch card data from Scryfall to analyze abilities
    let cardData = null;
    try {
        const resp = await fetch(`https://api.scryfall.com/cards/named?fuzzy=${encodeURIComponent(cardName)}`);
        if (resp.ok) cardData = await resp.json();
    } catch (e) {}

    if (cardData) {
        const oracle = (cardData.oracle_text || '').toLowerCase();
        const typeLine = (cardData.type_line || '').toLowerCase();

        // 3. Analyze oracle text for pattern matching
        const abilityPatterns = [
            { keyword: 'etb_untap', test: () => oracle.includes('untap') && (oracle.includes('enters') || oracle.includes('when') && typeLine.includes('creature')) },
            { keyword: 'mana_dork', test: () => oracle.includes('{t}') && oracle.includes('add') && typeLine.includes('creature') },
            { keyword: 'repeatable_untap', test: () => oracle.includes('untap') && (oracle.includes('equipped') || oracle.includes('enchanted') || oracle.includes('{')) },
            { keyword: 'persist', test: () => oracle.includes('persist') },
            { keyword: 'free_sac', test: () => oracle.includes('sacrifice a creature') || oracle.includes('sacrifice another') },
            { keyword: 'remove_counter', test: () => oracle.includes("don't get") || oracle.includes('enter with a +1') || oracle.includes('remove a') },
            { keyword: 'flicker_engine', test: () => oracle.includes('exile') && oracle.includes('return') && oracle.includes('battlefield') },
            { keyword: 'strong_etb', test: () => oracle.includes('when') && oracle.includes('enters') && (oracle.includes('untap') || oracle.includes('draw') || oracle.includes('destroy') || oracle.includes('damage')) },
            { keyword: 'death_trigger', test: () => oracle.includes('whenever') && (oracle.includes('dies') || oracle.includes('leaves the battlefield')) && (oracle.includes('life') || oracle.includes('damage') || oracle.includes('token') || oracle.includes('mana')) },
            { keyword: 'recursion', test: () => oracle.includes('return') && oracle.includes('from your graveyard') && oracle.includes('battlefield') },
            { keyword: 'tap_make_token', test: () => oracle.includes('{t}') && oracle.includes('token') },
            { keyword: 'copy_permanent', test: () => oracle.includes('copy') && oracle.includes('creature') && (oracle.includes('token') || oracle.includes('that\'s a copy')) },
            { keyword: 'symmetric_lock', test: () => (oracle.includes("can't") || oracle.includes("don't untap")) && !oracle.includes('you control') },
            { keyword: 'empty_library', test: () => oracle.includes('exile') && oracle.includes('library') },
            { keyword: 'mana_sink', test: () => oracle.includes('{x}') || (oracle.includes('pay') && oracle.includes('damage')) },
        ];

        abilityPatterns.forEach(ap => {
            if (ap.test()) {
                // Find patterns that use this keyword
                patterns.forEach(p => {
                    p.slots.forEach(s => {
                        if (s.keyword === ap.keyword && !s.cards.some(c => c.toLowerCase() === cardData.name.toLowerCase())) {
                            newSuggestions.push({
                                type: 'suggestion',
                                pattern: p.name,
                                slot: s.role,
                                result: p.result,
                                reason: `Ha abilita simile a: ${s.cards.slice(0, 3).join(', ')}`
                            });
                        }
                    });
                });
            }
        });
    }

    // Render results
    let html = '';

    if (matches.length > 0) {
        html += `<p style="color:#4ecca3;font-size:0.85em;margin-bottom:8px;">✓ Presente in ${matches.length} combo:</p>`;
        matches.forEach(m => {
            html += `<div class="compare-match">
                <div class="compare-match-title">${m.pattern}</div>
                <div class="compare-match-info">Ruolo: ${m.slot} → ${m.result}</div>
            </div>`;
        });
    }

    if (newSuggestions.length > 0) {
        html += `<p style="color:#ffd700;font-size:0.85em;margin:12px 0 8px;">⚡ ${newSuggestions.length} nuove combo suggerite:</p>`;
        newSuggestions.forEach(s => {
            html += `<div class="compare-match compare-new">
                <div class="compare-match-title">NUOVA: ${cardData.name} in "${s.pattern}"</div>
                <div class="compare-match-info">Slot: ${s.slot}<br>${s.reason}<br>→ ${s.result}</div>
            </div>`;
        });

        // Add card to patterns (locally)
        if (cardData) {
            newSuggestions.forEach(s => {
                const pattern = patterns.find(p => p.name === s.pattern);
                if (pattern) {
                    const slot = pattern.slots.find(sl => sl.role === s.slot);
                    if (slot && !slot.cards.includes(cardData.name)) {
                        slot.cards.push(cardData.name);
                    }
                }
            });
            updateStats();
        }
    }

    if (!matches.length && !newSuggestions.length) {
        html = `<p style="color:#e94560;font-size:0.85em;">Nessuna combo trovata per questa carta. Prova con un nome diverso o piu specifico.</p>`;
        if (cardData) {
            html += `<p style="color:#888;font-size:0.8em;margin-top:8px;">Carta trovata: ${cardData.name}<br>Tipo: ${cardData.type_line}<br>Testo: ${(cardData.oracle_text || '').slice(0, 150)}...</p>`;
        }
    }

    results.innerHTML = html;
}

// === EVENT LISTENERS ===
document.getElementById('search-btn').addEventListener('click', render);
document.getElementById('format-filter').addEventListener('change', render);
document.getElementById('search').addEventListener('keydown', (e) => {
    if (e.key === 'Enter') render();
});
document.getElementById('lang-select').addEventListener('change', (e) => {
    currentLang = e.target.value;
    document.getElementById('search').placeholder = t('search');
    document.getElementById('search-btn').textContent = t('searchBtn');
    // Update tab labels
    document.querySelectorAll('.tab').forEach(tab => {
        const key = tab.dataset.tab;
        if (i18n[currentLang][key]) tab.textContent = i18n[currentLang][key];
    });
    render();
});

document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => {
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        currentTab = tab.dataset.tab;
        render();
    });
});

document.getElementById('compare-btn').addEventListener('click', () => {
    document.getElementById('compare-modal').classList.add('active');
    document.getElementById('compare-input').focus();
});

document.getElementById('compare-close').addEventListener('click', () => {
    document.getElementById('compare-modal').classList.remove('active');
    document.getElementById('compare-results').innerHTML = '';
});

document.getElementById('compare-go').addEventListener('click', () => {
    const val = document.getElementById('compare-input').value;
    if (val) compareCard(val);
});

document.getElementById('compare-input').addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
        const val = document.getElementById('compare-input').value;
        if (val) compareCard(val);
    }
});

// Card image tooltip on hover
document.addEventListener('mouseover', (e) => {
    if (e.target.classList.contains('slot-card')) {
        const name = e.target.dataset.card;
        const tooltip = document.getElementById('card-tooltip');
        tooltip.querySelector('img').src = `https://api.scryfall.com/cards/named?exact=${encodeURIComponent(name)}&format=image&version=small`;
        tooltip.style.display = 'block';
        tooltip.style.left = (e.clientX + 10) + 'px';
        tooltip.style.top = (e.clientY + 10) + 'px';
    }
});

document.addEventListener('mouseout', (e) => {
    if (e.target.classList.contains('slot-card')) {
        document.getElementById('card-tooltip').style.display = 'none';
    }
});

// === DECKLIST SEARCH ===
document.getElementById('decklist-btn').addEventListener('click', () => {
    document.getElementById('decklist-modal').classList.add('active');
    document.getElementById('decklist-input').focus();
});

document.getElementById('decklist-close').addEventListener('click', () => {
    document.getElementById('decklist-modal').classList.remove('active');
});

document.getElementById('decklist-go').addEventListener('click', () => {
    const card = document.getElementById('decklist-input').value.trim();
    if (card) window.open('https://www.mtgtop8.com/search?MD_check=1&SB_check=1&cards=' + encodeURIComponent(card), '_blank');
});

document.getElementById('decklist-go2').addEventListener('click', () => {
    const card = document.getElementById('decklist-input').value.trim();
    if (card) window.open('https://mtgdecks.net/decks/containing/' + encodeURIComponent(card.replace(/ /g, '-').toLowerCase()), '_blank');
});

document.getElementById('decklist-go3').addEventListener('click', () => {
    const card = document.getElementById('decklist-input').value.trim();
    if (card) window.open('https://www.mtggoldfish.com/q?query_string=' + encodeURIComponent(card) + '&commit=Search', '_blank');
});

document.getElementById('decklist-input').addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
        const card = document.getElementById('decklist-input').value.trim();
        if (card) window.open('https://www.mtgtop8.com/search?MD_check=1&SB_check=1&cards=' + encodeURIComponent(card), '_blank');
    }
});

// === COPY / SCREENSHOT ===
document.getElementById('copy-btn').addEventListener('click', () => {
    document.getElementById('copy-modal').classList.add('active');
    document.getElementById('copy-feedback').style.display = 'none';
});

document.getElementById('copy-close').addEventListener('click', () => {
    document.getElementById('copy-modal').classList.remove('active');
});

document.getElementById('copy-text-btn').addEventListener('click', () => {
    const content = document.getElementById('content').innerText;
    navigator.clipboard.writeText(content).then(() => {
        const fb = document.getElementById('copy-feedback');
        fb.textContent = '✓ Testo copiato negli appunti!';
        fb.style.display = 'block';
    }).catch(() => {
        // Fallback for older browsers
        const ta = document.createElement('textarea');
        ta.value = document.getElementById('content').innerText;
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        document.body.removeChild(ta);
        const fb = document.getElementById('copy-feedback');
        fb.textContent = '✓ Testo copiato!';
        fb.style.display = 'block';
    });
});

document.getElementById('copy-screenshot-btn').addEventListener('click', async () => {
    const fb = document.getElementById('copy-feedback');
    fb.textContent = 'Cattura in corso...';
    fb.style.display = 'block';

    try {
        // Use html2canvas-like approach via canvas
        const content = document.querySelector('body');
        const canvas = await htmlToCanvas(content);
        canvas.toBlob(async (blob) => {
            if (navigator.share && navigator.canShare && navigator.canShare({files: [new File([blob], 'combo.png', {type: 'image/png'})]})) {
                // Mobile: use share API
                const file = new File([blob], 'combo-finder.png', {type: 'image/png'});
                await navigator.share({files: [file], title: 'MTG Combo Finder'});
                fb.textContent = '✓ Condiviso!';
            } else {
                // Desktop: download
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'combo-finder-screenshot.png';
                a.click();
                URL.revokeObjectURL(url);
                fb.textContent = '✓ Screenshot salvato!';
            }
        }, 'image/png');
    } catch (e) {
        fb.textContent = 'Errore: ' + e.message;
    }
});

// Simple html-to-canvas using native API
async function htmlToCanvas(element) {
    const canvas = document.createElement('canvas');
    const rect = element.getBoundingClientRect();
    canvas.width = Math.min(window.innerWidth, 1440);
    canvas.height = Math.min(document.body.scrollHeight, 2560);
    const ctx = canvas.getContext('2d');

    // Draw background
    ctx.fillStyle = '#0f0f1a';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Draw text content
    ctx.fillStyle = '#e0e0e0';
    ctx.font = '13px sans-serif';
    const lines = element.innerText.split('\n').slice(0, 100);
    lines.forEach((line, i) => {
        ctx.fillText(line.slice(0, 100), 10, 20 + i * 16);
    });
    return canvas;
}

// Init
init();
