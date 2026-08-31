/* ============================================
 123MiniApps.online v2.0
 File: config.js
 Purpose: Global configuration constants.
 Loaded first; everything else reads from
 window.CONFIG.
 ============================================ */

/**
 * @typedef {Object} ThemeDef
 * @property {string} id - Value written to <html data-theme>
 * @property {string} name - Human label shown in the switcher
 * @property {'dark'|'light'} type - Used for system-preference matching
 * @property {string} color - Theme color for the browser chrome / meta tag
 */

/** @type {Object} Global app configuration. */
const CONFIG = {
 siteName: '123MiniApps.online',
 siteUrl: 'https://www.123miniapps.online',
 tagline: 'Free browser tools that never touch a server',
 version: '2.0.0',
 totalTools: 95,
 totalCategories: 11,

 defaultTheme: 'indigo-nova',
 storageKeys: {
 theme: '123miniapps-theme',
 favorites: '123miniapps-favorites',
 recentSearches: '123miniapps-recent-searches',
 cookieConsent: '123miniapps-cookie-consent',
 newsletter: '123miniapps-newsletter',
 feedback: '123miniapps-feedback'
 },

 /** @type {ThemeDef[]} */
 themes: [
 { id: 'indigo-nova', name: 'Indigo Nova', type: 'dark', color: '#0B1120' },
 { id: 'azure-trust', name: 'Azure Trust', type: 'light', color: '#F8FAFC' },
 { id: 'graphite-minimal', name: 'Graphite Minimal', type: 'light', color: '#FFFFFF' },
 { id: 'violet-dream', name: 'Violet Dream', type: 'dark', color: '#18181B' },
 { id: 'emerald-fresh', name: 'Emerald Fresh', type: 'light', color: '#ECFDF5' },
 { id: 'navy-cyan', name: 'Navy Cyan', type: 'dark', color: '#0A1834' },
 { id: 'sunburst', name: 'Sunburst', type: 'light', color: '#FFF7ED' },
 { id: 'teal-clean', name: 'Teal Clean', type: 'light', color: '#F0FDFA' },
 { id: 'violet-noir', name: 'Violet Noir', type: 'dark', color: '#0F0F14' },
 { id: 'crimson-edge', name: 'Crimson Edge', type: 'dark', color: '#0F0F0F' }
 ],

 searchDebounceMs: 200,
 searchMaxResults: 24,
 toastDurationMs: 4000,
 recentSearchesMax: 5,
 scrollOffset: 72,
 backToTopThreshold: 500,
 navScrollThreshold: 50,

 performance: {
 targetFPS: 60,
 enableParticles: true,
 enableParallax: true,
 particleCount: 42
 },

 /** Words cycled by the hero typewriter. */
 rotatingWords: [
 'passwords',
 'QR codes',
 'JSON',
 'colors',
 'hashes',
 'images',
 'Base64',
 'UUIDs'
 ]
};

// Freeze so no module can mutate shared config by accident.
Object.freeze(CONFIG.performance);
Object.freeze(CONFIG.storageKeys);
Object.freeze(CONFIG);

window.CONFIG = CONFIG;
