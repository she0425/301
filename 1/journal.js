const fs = require('fs');
const path = require('path');
const readline = require('readline');
const crypto = require('crypto');

const DATA_FILE = path.join(__dirname, 'journal.json');
const VALID_MOODS = ['HAPPY', 'NEUTRAL', 'SAD', 'ANXIOUS', 'WORK'];

// --- ANSI COLOR CODES (NODE.JS YELLOW & NEON THEME) ---
const C = {
    yellow: '\x1b[38;5;220m',
    cyan: '\x1b[38;5;51m',
    green: '\x1b[38;5;82m',
    red: '\x1b[38;5;196m',
    gray: '\x1b[38;5;242m',
    reset: '\x1b[0m',
    bold: '\x1b[1m'
};

const BANNER = `
${C.yellow}${C.bold} ⚡ JS JOURNAL APP v2.0 (Node.js)${C.reset}
${C.cyan}───────────────────────────────────────────────────${C.reset}
`;

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

const prompt = (query) => new Promise((resolve) => rl.question(query, resolve));

class JournalManager {
    constructor() {
        this.filepath = DATA_FILE;
        this.entries = this.loadEntries();
    }

    loadEntries() {
        if (!fs.existsSync(this.filepath)) return [];
        try {
            return JSON.parse(fs.readFileSync(this.filepath, 'utf8'));
        } catch (err) {
            return [];
        }
    }

    saveEntries() {
        fs.writeFileSync(this.filepath, JSON.stringify(this.entries, null, 2), 'utf8');
    }

    createEntry(title, content, mood) {
        const now = new Date().toISOString().replace('T', ' ').substring(0, 16);
        const formattedMood = VALID_MOODS.includes(mood.toUpperCase()) ? mood.toUpperCase() : 'NEUTRAL';
        const entry = {
            id: crypto.randomUUID().substring(0, 8),
            title,
            content,
            mood: formattedMood,
            created_at: now,
            updated_at: now
        };
        this.entries.push(entry);
        this.saveEntries();
        console.log(`\n${C.green}✔ Created entry successfully! ID: [${entry.id}]${C.reset}`);
    }

    listEntries() {
        if (this.entries.length === 0) {
            console.log(`\n${C.red}✖ No journal entries found.${C.reset}`);
            return;
        }
        console.log(`\n${C.yellow}╭──────────┬──────────────────────────────┬──────────┬────────────────╮${C.reset}`);
        console.log(`${C.yellow}│ ID       │ TITLE                        │ MOOD     │ CREATED AT     │${C.reset}`);
        console.log(`${C.yellow}├──────────┼──────────────────────────────┼──────────┼────────────────┤${C.reset}`);
        this.entries.forEach((e) => {
            const titleShort = (e.title.length > 27 ? e.title.substring(0, 24) + '...' : e.title).padEnd(28);
            const moodShort = e.mood.padEnd(8);
            console.log(`│ ${C.cyan}${e.id.padEnd(8)}${C.reset} │ ${titleShort} │ ${C.green}${moodShort}${C.reset} │ ${C.gray}${e.created_at}${C.reset} │`);
        });
        console.log(`${C.yellow}╰──────────┴──────────────────────────────┴──────────┴────────────────╯${C.reset}`);
    }

    getEntryById(entryId) {
        return this.entries.find((e) => e.id === entryId) || null;
    }

    viewEntry(entryId) {
        const entry = this.getEntryById(entryId);
        if (!entry) {
            console.log(`\n${C.red}✖ Entry [${entryId}] not found.${C.reset}`);
            return;
        }
        console.log(`\n${C.cyan}╭───────────────────────────────────────────────────────────────────╮${C.reset}`);
        console.log(`${C.cyan}│ ${C.bold}${entry.title.padEnd(53)}${C.reset} ${C.cyan}[${entry.id}] │${C.reset}`);
        console.log(`${C.cyan}├───────────────────────────────────────────────────────────────────┤${C.reset}`);
        console.log(` ${C.yellow}Mood Tag:${C.reset} [${entry.mood}] | ${C.gray}Created: ${entry.created_at} | Updated: ${entry.updated_at}${C.reset}`);
        console.log(`${C.cyan}───────────────────────────── CONTENT ──────────────────────────────${C.reset}`);
        console.log(` ${entry.content}`);
        console.log(`${C.cyan}╰───────────────────────────────────────────────────────────────────╯${C.reset}`);
    }

    updateEntry(entryId, newTitle, newContent, newMood) {
        const entry = this.getEntryById(entryId);
        if (!entry) {
            console.log(`\n${C.red}✖ Entry [${entryId}] not found.${C.reset}`);
            return;
        }
        if (newTitle.trim()) entry.title = newTitle;
        if (newContent.trim()) entry.content = newContent;
        if (newMood.trim() && VALID_MOODS.includes(newMood.toUpperCase())) {
            entry.mood = newMood.toUpperCase();
        }
        entry.updated_at = new Date().toISOString().replace('T', ' ').substring(0, 16);
        this.saveEntries();
        console.log(`\n${C.green}✔ Entry [${entryId}] updated successfully!${C.reset}`);
    }

    deleteEntry(entryId) {
        const initialLength = this.entries.length;
        this.entries = this.entries.filter((e) => e.id !== entryId);
        if (this.entries.length === initialLength) {
            console.log(`\n${C.red}✖ Entry [${entryId}] not found.${C.reset}`);
            return;
        }
        this.saveEntries();
        console.log(`\n${C.red}✔ Entry [${entryId}] deleted successfully.${C.reset}`);
    }

    searchEntries(query) {
        const q = query.toLowerCase();
        const results = this.entries.filter(
            (e) => e.title.toLowerCase().includes(q) || e.content.toLowerCase().includes(q) || e.mood.toLowerCase() === q
        );
        if (results.length === 0) {
            console.log(`\n${C.red}✖ No matching entries found for '${query}'.${C.reset}`);
            return;
        }
        console.log(`\n${C.yellow}🔎 Search Results for '${query}' (${results.length} found):${C.reset}`);
        results.forEach((e) => {
            console.log(` • [${C.cyan}${e.id}${C.reset}] ${C.bold}${e.title}${C.reset} (${C.green}${e.mood}${C.reset})`);
        });
    }
}

async function main() {
    const manager = new JournalManager();
    console.log(BANNER);

    while (true) {
        console.log(`\n${C.cyan}───────────── DASHBOARD ─────────────${C.reset}`);
        console.log(` ${C.yellow}[1]${C.reset} Create Entry`);
        console.log(` ${C.yellow}[2]${C.reset} View All Entries`);
        console.log(` ${C.yellow}[3]${C.reset} Open Entry Details`);
        console.log(` ${C.yellow}[4]${C.reset} Update Entry`);
        console.log(` ${C.yellow}[5]${C.reset} Delete Entry`);
        console.log(` ${C.yellow}[6]${C.reset} Search Database`);
        console.log(` ${C.yellow}[7]${C.reset} Exit`);

        const choice = (await prompt(`${C.cyan}Select Action (1-7): ${C.reset}`)).trim();

        switch (choice) {
            case '1': {
                const t = await prompt('Title: ');
                const c = await prompt('Content: ');
                const m = await prompt(`Mood (${VALID_MOODS.join('/')}): `);
                manager.createEntry(t, c, m);
                break;
            }
            case '2':
                manager.listEntries();
                break;
            case '3':
                manager.viewEntry(await prompt('Enter Entry ID: '));
                break;
            case '4': {
                const id = await prompt('Enter Entry ID: ');
                console.log(`${C.gray}(Leave field blank to keep unchanged)${C.reset}`);
                manager.updateEntry(id, await prompt('New Title: '), await prompt('New Content: '), await prompt('New Mood: '));
                break;
            }
            case '5':
                manager.deleteEntry(await prompt('Enter Entry ID: '));
                break;
            case '6':
                manager.searchEntries(await prompt('Enter keyword/mood: '));
                break;
            case '7':
                console.log(`\n${C.yellow}Goodbye! ⚡${C.reset}`);
                rl.close();
                return;
            default:
                console.log(`\n${C.red}Invalid Option.${C.reset}`);
        }
    }
}

main();
