/* ============================================
   123MiniApps.online v2.0
   File: testimonials.js
   Purpose: Homepage data — FAQ items, plus a (currently empty)
            slot for real, attributed testimonials.

   TESTIMONIALS is deliberately EMPTY. The homepage no longer shows
   fabricated reviews — it shows honest, verifiable value props
   instead (the "Why 123MiniApps" section in index.html). When you
   collect genuine, permission-cleared feedback, add it here as
   { quote, name, role, stars } objects. Never ship invented reviews:
   they are an FTC problem and a trust problem.
   ============================================ */

/** @type {Array<{quote:string,name:string,role:string,stars:number}>} */
const TESTIMONIALS = [];

/** Homepage FAQ. Mirrors the FAQPage structured data in index.html. */
const FAQS = [
  {
    q: 'Is my data actually private?',
    a: 'Yes, and it is structural rather than a promise. Every tool runs as JavaScript inside your browser tab. There is no backend that receives your text, images or files, because there is no backend at all. You can verify this by opening DevTools, going to the Network tab, and using any tool: you will see zero outbound requests carrying your input.'
  },
  {
    q: 'Do I need an account?',
    a: 'No. There is no sign-up, no login and no email gate. Preferences like your chosen theme and saved favorites are stored in your own browser via localStorage, so they stay on your device.'
  },
  {
    q: 'Are the tools free? What does the Premium badge mean?',
    a: 'Every tool is free with no usage limits. The Premium badge marks tools with a deeper feature set such as batch processing and export options, not a paywall. Nothing on this site costs money.'
  },
  {
    q: 'Does it work offline?',
    a: 'Mostly. The site registers a service worker that caches the shell and each tool page you visit, so you can return to any previously loaded page without a connection.'
  },
  {
    q: 'Can I use these tools for commercial work?',
    a: 'Yes. Output you generate is yours to use however you like, including commercially. We claim no rights over anything you create here.'
  }
];

if (typeof window !== 'undefined') {
  window.TESTIMONIALS = TESTIMONIALS;
  window.FAQS = FAQS;
}
