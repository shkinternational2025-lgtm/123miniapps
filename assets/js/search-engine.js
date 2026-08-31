/* ============================================
 123MiniApps.online v2.0
 File: search-engine.js
 Purpose: Fuzzy, ranked, category-grouped search
 over the tools database.
 ============================================ */

/**
 * A small purpose-built search index. Deliberately not a
 * dependency: the corpus is 95 short documents, so an
 * inverted index plus a scoring pass is both faster and
 * smaller than pulling in a library.
 *
 * Ranking, highest signal first:
 * exact name match 1000
 * name starts with query 600
 * name contains query 400
 * tag exact match 260
 * description contains 160
 * feature text contains 110
 * fuzzy (edit distance ≤ 2) 70
 * Popularity contributes a small tiebreaker so that when two
 * tools score identically the more-used one surfaces first.
 */
class SearchEngine {
 /**
 * @param {Array} tools - window.TOOLS
 * @param {Object} config - window.CONFIG
 */
 constructor(tools, config) {
 this.tools = tools;
 this.config = config;
 this.index = this.buildIndex(tools);
 this.maxUsage = Math.max(...tools.map((t) => t.usageCount), 1);
 }

 /**
 * Precompute a lowercase searchable blob per tool so the hot
 * path does no string allocation.
 * @param {Array} tools
 * @returns {Array<{tool: Object, name: string, desc: string, tags: string[], features: string}>}
 */
 buildIndex(tools) {
 return tools.map((tool) => ({
 tool,
 name: tool.name.toLowerCase(),
 desc: tool.description.toLowerCase(),
 tags: tool.tags.map((t) => t.toLowerCase()),
 features: tool.features.join(' ').toLowerCase()
 }));
 }

 /**
 * Run a query.
 * @param {string} rawQuery
 * @param {number} [limit]
 * @returns {Array} scored tools, best first
 */
 search(rawQuery, limit = this.config.searchMaxResults) {
 const query = String(rawQuery || '').trim().toLowerCase();
 if (!query) return [];

 const terms = query.split(/\s+/).filter(Boolean);
 const results = [];

 for (const entry of this.index) {
 let score = 0;

 for (const term of terms) {
 score += this.scoreTerm(entry, term);
 }

 if (score > 0) {
 // Popularity tiebreaker, capped so it can never outrank relevance.
 score += (entry.tool.usageCount / this.maxUsage) * 25;
 results.push({ tool: entry.tool, score });
 }
 }

 return results
 .sort((a, b) => b.score - a.score)
 .slice(0, limit)
 .map((r) => r.tool);
 }

 /**
 * Score one query term against one indexed tool.
 * @returns {number}
 */
 scoreTerm(entry, term) {
 if (entry.name === term) return 1000;
 if (entry.name.startsWith(term)) return 600;
 if (entry.name.includes(term)) return 400;
 if (entry.tags.includes(term)) return 260;
 if (entry.desc.includes(term)) return 160;
 if (entry.features.includes(term)) return 110;

 // Fuzzy fallback, only for terms long enough that a typo is
 // more likely than a genuinely different word.
 if (term.length >= 4) {
 const tolerance = term.length >= 7 ? 2 : 1;
 for (const word of entry.name.split(/\s+/)) {
 if (this.editDistance(word, term) <= tolerance) return 70;
 }
 for (const tag of entry.tags) {
 if (tag.length >= 4 && this.editDistance(tag, term) <= tolerance) return 55;
 }
 }

 return 0;
 }

 /**
 * Levenshtein distance with early exit.
 * Two-row rolling buffer, O(min(a,b)) memory.
 * @returns {number}
 */
 editDistance(a, b) {
 if (a === b) return 0;
 if (Math.abs(a.length - b.length) > 2) return 99;
 if (!a.length) return b.length;
 if (!b.length) return a.length;

 let prev = Array.from({ length: b.length + 1 }, (_, i) => i);
 let curr = new Array(b.length + 1);

 for (let i = 1; i <= a.length; i++) {
 curr[0] = i;
 for (let j = 1; j <= b.length; j++) {
 const cost = a[i - 1] === b[j - 1] ? 0 : 1;
 curr[j] = Math.min(curr[j - 1] + 1, prev[j] + 1, prev[j - 1] + cost);
 }
 [prev, curr] = [curr, prev];
 }

 return prev[b.length];
 }

 /**
 * Group a flat result list by category, preserving rank order
 * both within and across groups.
 * @param {Array} tools
 * @returns {Array<{category: Object, tools: Array}>}
 */
 groupByCategory(tools) {
 const groups = new Map();

 for (const tool of tools) {
 if (!groups.has(tool.category)) groups.set(tool.category, []);
 groups.get(tool.category).push(tool);
 }

 return Array.from(groups.entries()).map(([id, list]) => ({
 category: window.getCategory(id) || { id, name: id, icon: '🔧' },
 tools: list
 }));
 }

 /**
 * Suggest tools when a query returns nothing, the most popular
 * items are a better dead end than an empty list.
 * @returns {Array}
 */
 suggestions(n = 4) {
 return window.getPopularTools(n);
 }

 /* ------------------------------------------
 Recent searches (localStorage)
 ------------------------------------------ */

 /** @returns {string[]} */
 getRecent() {
 try {
 const raw = localStorage.getItem(this.config.storageKeys.recentSearches);
 const parsed = raw ? JSON.parse(raw) : [];
 return Array.isArray(parsed) ? parsed : [];
 } catch {
 return [];
 }
 }

 /** @param {string} query */
 addRecent(query) {
 const q = String(query || '').trim();
 if (q.length < 2) return;

 try {
 const list = this.getRecent().filter((item) => item !== q);
 list.unshift(q);
 localStorage.setItem(
 this.config.storageKeys.recentSearches,
 JSON.stringify(list.slice(0, this.config.recentSearchesMax))
 );
 } catch {
 /* storage unavailable, recents are a nicety, not a requirement */
 }
 }

 clearRecent() {
 try {
 localStorage.removeItem(this.config.storageKeys.recentSearches);
 } catch {
 /* no-op */
 }
 }

 /**
 * Wrap query matches in <mark>. Escapes first so tool data can
 * never inject markup.
 * @param {string} text
 * @param {string} query
 * @returns {string} safe HTML
 */
 highlight(text, query) {
 const safe = SearchEngine.escapeHtml(text);
 const terms = String(query || '').trim().split(/\s+/).filter((t) => t.length >= 2);
 if (!terms.length) return safe;

 const pattern = terms.map(SearchEngine.escapeRegex).join('|');
 return safe.replace(new RegExp(`(${pattern})`, 'gi'), '<mark>$1</mark>');
 }

 /** @returns {string} */
 static escapeHtml(str) {
 return String(str).replace(/[&<>"']/g, (ch) => ({
 '&': '&amp;',
 '<': '&lt;',
 '>': '&gt;',
 '"': '&quot;',
 "'": '&#39;'
 }[ch]));
 }

 /** @returns {string} */
 static escapeRegex(str) {
 return String(str).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
 }
}

window.SearchEngine = SearchEngine;
