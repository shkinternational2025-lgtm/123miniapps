# ============================================
# 123MiniApps.online - Article SEO/AEO/GEO upgrades: BATCH 3
# Merged onto existing posts by build-blog.py -> apply_upgrades().
# Text (keywords, FAQ + FAQPage schema, refined quick-answer) applies
# immediately; the hero + 3 in-body images stay gated on the hero WebP
# existing on disk, so each article is SEO-complete now and lights up
# with art when the images are dropped into:
#   assets/images/blog/<slug>/<slug>-1-hero.webp  (hero)
#   assets/images/blog/<slug>/<slug>-2.webp / -3.webp / -4.webp  (in-body)
# ============================================

from blog_upgrades import _hero, _imgs

MOD = "2026-10-08"

UPGRADES = {

 # ========================= FINANCE & MATHS =========================

 "compound-interest-explained": {
  "modified": MOD,
  "keywords": ["compound interest", "compound interest explained", "how compound interest works", "compound interest formula", "compound vs simple interest", "power of compounding", "interest on interest", "compound interest calculator", "daily vs monthly compounding", "rule of 72", "compound growth", "time value of money"],
  "standfirst": "Compound interest is interest earned on both your original money and the interest it has already earned, so your balance grows faster the longer you leave it, which is why starting early matters more than adding large amounts later.",
  "hero": _hero("compound-interest-explained", "A small amount of money accelerating into a large sum of stacked gold coins over time"),
  "images": _imgs("compound-interest-explained", [
    (2, "Interest layering on top of previous interest and growing on itself", "Compounding means each period's interest earns interest of its own."),
    (3, "Someone watching long-term savings grow on a laptop at home", "Time in the account matters more than the size of each deposit."),
    (4, "An exponential growth curve pulling away from a flat straight line", "Compound growth curves upward while simple interest stays linear."),
  ]),
  "faq": [
   ("What is compound interest in simple terms?", "It is interest you earn on your original deposit plus all the interest it has already earned, so each period grows from a larger base than the one before."),
   ("What is the difference between simple and compound interest?", "Simple interest is paid only on the original amount, while compound interest is paid on the original amount plus accumulated interest, so it grows faster over time."),
   ("Does compounding frequency matter?", "Yes. The more often interest compounds (daily versus monthly versus yearly), the slightly higher the total, because interest starts earning interest sooner."),
   ("What is the Rule of 72?", "A quick shortcut: divide 72 by the annual interest rate to estimate how many years it takes your money to double."),
  ],
 },

 "how-to-calculate-percentages": {
  "modified": MOD,
  "keywords": ["how to calculate percentages", "percentage calculator", "percentage increase", "percentage decrease", "percent of a number", "what percent is x of y", "percentage change formula", "work out a percentage", "percentage difference", "calculate discount percentage"],
  "standfirst": "To find a percentage of a number, multiply the number by the percent written as a decimal; to find what percent one number is of another, divide the part by the whole and multiply by 100.",
  "hero": _hero("how-to-calculate-percentages", "A portion separated from a whole object to represent a percentage"),
  "images": _imgs("how-to-calculate-percentages", [
    (2, "A highlighted group within a hundred to show the idea of per hundred", "Percent literally means per hundred: a share out of 100."),
    (3, "Working out a discount while shopping with a price tag", "The most common everyday use is working out a discount."),
    (4, "A part, an increase and a decrease shown as directional change", "The same idea covers a part of, an increase and a decrease."),
  ]),
  "faq": [
   ("How do I find a percentage of a number?", "Convert the percent to a decimal by dividing by 100, then multiply. For example, 20 percent of 80 is 0.20 times 80, which is 16."),
   ("How do I calculate a percentage increase?", "Subtract the old value from the new value, divide the result by the old value, then multiply by 100."),
   ("How do I work out what percent one number is of another?", "Divide the part by the whole and multiply by 100. For example, 30 out of 120 is 25 percent."),
   ("How do I reverse a percentage?", "To remove a 20 percent increase, divide by 1.2; to find the original price before a discount, divide by one minus the discount written as a decimal."),
  ],
 },

 "how-loan-repayments-work-amortization": {
  "modified": MOD,
  "keywords": ["amortization", "how loan repayments work", "amortization schedule", "loan amortization explained", "principal vs interest", "mortgage amortization", "why early payments are mostly interest", "amortization formula", "loan payment breakdown", "extra principal payments"],
  "standfirst": "With an amortizing loan, every payment is the same size but its split changes over time: early payments are mostly interest and little principal, and later payments are mostly principal, which is why paying extra early saves the most interest.",
  "hero": _hero("how-loan-repayments-work-amortization", "A loan balance of gold coins stepping down to zero over regular payments"),
  "images": _imgs("how-loan-repayments-work-amortization", [
    (2, "Each payment gradually shifting from mostly interest to mostly principal", "Every payment is split between interest and principal, and the mix shifts over time."),
    (3, "Reviewing loan repayments at the kitchen table", "Understanding the split helps you decide when extra payments are worth it."),
    (4, "Interest falling while principal rises across the loan term", "On an amortization schedule the two lines cross as the loan matures."),
  ]),
  "faq": [
   ("What does amortization mean?", "It is the process of paying off a loan with equal regular payments that cover both interest and principal until the balance reaches zero."),
   ("Why is so much of my early payment interest?", "Interest is charged on the outstanding balance, which is highest at the start, so early payments cover mostly interest and little principal."),
   ("Does paying extra early help?", "Yes, a lot. Extra payments go straight to principal, which lowers the balance all future interest is calculated on, often saving years and significant interest."),
   ("What is an amortization schedule?", "A table showing each payment split into interest and principal, along with the remaining balance after every payment."),
  ],
 },

 "how-currency-conversion-works": {
  "modified": MOD,
  "keywords": ["how currency conversion works", "exchange rate explained", "how exchange rates work", "currency converter", "why exchange rates change", "mid-market rate", "currency conversion fees", "foreign exchange basics", "converting money for travel", "bid ask spread currency"],
  "standfirst": "Converting currency means multiplying an amount by the exchange rate between two currencies; rates move constantly with supply and demand, and the rate you actually get is usually a little worse than the mid-market rate because of a margin or fee.",
  "hero": _hero("how-currency-conversion-works", "Value flowing from one currency coin into another across a bridge of light"),
  "images": _imgs("how-currency-conversion-works", [
    (2, "An exchange rate shown as an unequal balance between two currencies", "An exchange rate is simply how much of one currency equals another."),
    (3, "Changing money for a trip abroad with passport and banknotes", "Travel and online shopping are where most people meet exchange rates."),
    (4, "An exchange rate moving up and down over time", "Rates move constantly, so the number changes minute to minute."),
  ]),
  "faq": [
   ("How is a currency conversion calculated?", "Multiply the amount by the exchange rate between the two currencies. To convert back the other way, divide by the same rate."),
   ("Why do exchange rates keep changing?", "They are set by global supply and demand, influenced by interest rates, inflation, trade and market sentiment, so they move all the time."),
   ("What is the mid-market rate?", "The midpoint between the buy and sell prices of a currency, the fairest reference rate. Most providers add a margin on top of it."),
   ("Why is the rate I get worse than the one I see online?", "Banks and exchange services add a spread or fee to the mid-market rate, which is how they make money on the conversion."),
  ],
 },

 # ===================== REAL-WORLD / EDITORIAL =====================

 "how-much-to-tip-and-split-the-bill": {
  "modified": MOD,
  "keywords": ["how much to tip", "tipping guide", "split the bill", "how to split a restaurant bill", "tip calculator", "what percent to tip", "splitting bill with tip", "tip etiquette", "divide bill between friends", "calculate tip and split"],
  "standfirst": "To tip, multiply the pre-tax total by your chosen percentage (commonly 15 to 20 percent for table service in the US); to split a bill evenly, add the tip to the total and divide by the number of people.",
  "hero": _hero("how-much-to-tip-and-split-the-bill", "Paying and tipping on a restaurant bill with cash on a bill tray"),
  "images": _imgs("how-much-to-tip-and-split-the-bill", [
    (2, "One restaurant bill divided into equal shares", "Splitting evenly means adding the tip first, then dividing by the group."),
    (3, "Friends splitting the bill together at dinner", "For shared meals, an even split is usually the fairest and fastest."),
    (4, "A tip added on top of the bill total", "The tip is an extra percentage added to the total, not part of it."),
  ]),
  "faq": [
   ("How much should I tip?", "In the US, 15 to 20 percent of the pre-tax bill for table service is typical. Norms vary a lot by country, so check local custom."),
   ("Do I tip on the pre-tax or post-tax amount?", "Tipping on the pre-tax subtotal is standard, though many people simply tip on the final total for convenience."),
   ("How do I split a bill evenly?", "Add the tip to the bill total, then divide by the number of people to get each person's share."),
   ("How do I split a bill unevenly?", "Total each person's own items, add a proportional share of tax and tip to each, then add them up."),
  ],
 },

 "the-real-cost-of-meetings": {
  "modified": MOD,
  "keywords": ["cost of meetings", "meeting cost calculator", "real cost of meetings", "how to calculate meeting cost", "meetings waste money", "meeting cost per hour", "reduce meeting costs", "salary cost of meetings", "are meetings worth it", "meeting roi"],
  "standfirst": "The real cost of a meeting is roughly every attendee's hourly pay multiplied by the length, so a one-hour meeting with eight well-paid people can quietly cost hundreds of dollars, which is why fewer, shorter and smaller meetings pay off.",
  "hero": _hero("the-real-cost-of-meetings", "Meeting time literally costing money, a clock with hands made of coins"),
  "images": _imgs("the-real-cost-of-meetings", [
    (2, "Every attendee's time adding to the cost at once", "Cost multiplies by the number of people, even the quiet ones."),
    (3, "A long meeting where time and attention drain away", "The hidden cost is not just money but focus and momentum."),
    (4, "Cost piling up as meeting time elapses", "Every minute that passes adds to the total bill."),
  ]),
  "faq": [
   ("How do I calculate the cost of a meeting?", "Add up each attendee's hourly rate (annual salary divided by about 2,000 working hours) and multiply by the length of the meeting."),
   ("Why are meetings so expensive?", "Because cost scales with the number of people and their pay. Every extra attendee multiplies the hourly burn, even if they never speak."),
   ("How can I reduce meeting costs?", "Invite fewer people, set a clear agenda and a time limit, replace status meetings with written updates, and default to shorter slots."),
   ("Should every meeting have a cost estimate?", "Showing the rough dollar cost before scheduling makes people think twice, which naturally keeps meetings smaller and shorter."),
  ],
 },

 "the-pomodoro-technique-explained": {
  "modified": MOD,
  "keywords": ["pomodoro technique", "pomodoro method", "25 minute work sprints", "pomodoro timer", "how pomodoro works", "focus technique", "pomodoro breaks", "deep work pomodoro", "productivity technique", "time blocking"],
  "standfirst": "The Pomodoro Technique breaks work into focused 25-minute sprints separated by short 5-minute breaks, with a longer break after four sprints, which protects your attention from distraction and makes big tasks feel manageable.",
  "hero": _hero("the-pomodoro-technique-explained", "A tomato timer on a tidy desk for focused work sprints"),
  "images": _imgs("the-pomodoro-technique-explained", [
    (2, "Focus sprints separated by short breaks in a repeating rhythm", "Work and rest alternate in a steady, repeatable rhythm."),
    (3, "Working in a focused, timed sprint with distractions removed", "A running timer and a face-down phone keep the sprint protected."),
    (4, "A timer dial wound to a focused interval", "Each pomodoro is a single, visible block of focused time."),
  ]),
  "faq": [
   ("What is the Pomodoro Technique?", "A time-management method that splits work into 25-minute focus sessions called pomodoros, each followed by a short break."),
   ("Why 25 minutes?", "It is long enough to make real progress but short enough to hold full focus and to feel approachable, which lowers the urge to procrastinate."),
   ("What do I do on the breaks?", "Step away from the task and rest for about five minutes, then take a longer 15 to 30 minute break after every four pomodoros."),
   ("Can I change the timings?", "Yes. The 25/5 split is just a starting point; adjust the focus and break lengths to suit the task and your attention span."),
  ],
 },

 "how-to-make-a-professional-invoice": {
  "modified": MOD,
  "keywords": ["how to make an invoice", "professional invoice", "invoice template", "what to include on an invoice", "create an invoice free", "invoice for freelancers", "invoice format", "invoice number", "payment terms invoice", "send an invoice"],
  "standfirst": "A professional invoice clearly shows who is billing whom, a unique invoice number and date, an itemized list of work with amounts, the total due, and the payment terms and method, so the client knows exactly what to pay and by when.",
  "hero": _hero("how-to-make-a-professional-invoice", "A clean, professionally structured invoice on a desk"),
  "images": _imgs("how-to-make-a-professional-invoice", [
    (2, "The sections that make up an invoice: who, what and how much", "An invoice is really three zones: header, line items and totals."),
    (3, "A freelancer preparing and sending an invoice", "A clear invoice gets you paid faster and looks professional."),
    (4, "The highlighted total due on an invoice", "The total and the due date are the two things a client looks for first."),
  ]),
  "faq": [
   ("What must a professional invoice include?", "Your details and the client's, a unique invoice number, the issue and due dates, itemized line items with prices, the total, and the payment terms."),
   ("Do I need an invoice number?", "Yes. A unique, sequential invoice number keeps your records organized and is often required for tax and accounting."),
   ("What payment terms should I use?", "Common terms are due on receipt, net 14 or net 30. State the terms clearly and list the payment methods you accept."),
   ("Can I create an invoice for free?", "Yes. You can build a clean, professional invoice in a browser-based generator or a simple template without any paid software."),
  ],
 },

 # ============================ SECURITY ============================

 "how-encryption-works-keeping-text-private": {
  "modified": MOD,
  "keywords": ["how encryption works", "encryption explained", "what is encryption", "symmetric vs asymmetric encryption", "encryption keys", "end to end encryption", "how encryption keeps data private", "public key encryption", "cipher explained", "aes encryption basics"],
  "standfirst": "Encryption scrambles readable text into unreadable ciphertext using a mathematical key, so that only someone with the right key can turn it back into the original, which is how messages, passwords and files stay private even if they are intercepted.",
  "hero": _hero("how-encryption-works-keeping-text-private", "A message sealed in a vault so only the right key can open it"),
  "images": _imgs("how-encryption-works-keeping-text-private", [
    (2, "Ordered, readable information scrambled into protected form", "Encryption turns readable text into scrambled ciphertext."),
    (3, "Sending a private, protected message on a phone", "End-to-end encryption keeps messages private from everyone in between."),
    (4, "A matched key pair that locks and unlocks data", "Asymmetric encryption uses one key to lock and a matching key to unlock."),
  ]),
  "faq": [
   ("What is encryption in simple terms?", "A way of scrambling information with a key so that only someone holding the matching key can read it."),
   ("What is the difference between symmetric and asymmetric encryption?", "Symmetric uses one shared key to both lock and unlock, while asymmetric uses a public key to lock and a separate private key to unlock."),
   ("What does end-to-end encryption mean?", "Only the sender and recipient hold the keys, so not even the service carrying the message can read it."),
   ("Can encrypted data be broken?", "Strong, modern encryption with a long key is infeasible to break by brute force with today's computing, as long as the keys are kept secret."),
  ],
 },

 "what-is-a-hash-md5-sha256-explained": {
  "modified": MOD,
  "keywords": ["what is a hash", "hashing explained", "md5", "sha-256", "hash function", "digital fingerprint", "how hashing works", "hash vs encryption", "password hashing", "one way function"],
  "standfirst": "A hash function turns any input, of any size, into a short fixed-length fingerprint; the same input always produces the same hash, a tiny change produces a completely different one, and you cannot reverse a hash back into the original.",
  "hero": _hero("what-is-a-hash-md5-sha256-explained", "Any file reduced to one fixed-size digital fingerprint"),
  "images": _imgs("what-is-a-hash-md5-sha256-explained", [
    (2, "A one-way transformation you cannot reverse", "Hashing is a one-way function: you cannot get the original back."),
    (3, "Confirming a download matches the original file", "Matching hashes prove a downloaded file arrived intact."),
    (4, "A tiny input change producing a completely different hash", "Change one character and the whole fingerprint changes."),
  ]),
  "faq": [
   ("What is a hash?", "A fixed-length fingerprint of data produced by a hash function. It represents the input uniquely but cannot be turned back into it."),
   ("What is the difference between hashing and encryption?", "Encryption is reversible with a key, while hashing is one-way and has no key, so it is used for verification rather than for hiding recoverable data."),
   ("Why are MD5 and SHA-256 different?", "Both are hash functions, but MD5 is old and broken for security, while SHA-256 produces a longer, collision-resistant hash that is still considered secure."),
   ("What are hashes used for?", "Verifying file integrity, storing passwords safely, digital signatures, and quickly comparing or indexing data."),
  ],
 },

 "how-long-should-a-password-be": {
  "modified": MOD,
  "keywords": ["how long should a password be", "password length", "strong password", "password security", "minimum password length", "passphrase", "passphrase length", "how long to crack a password", "secure password tips", "password best practices"],
  "standfirst": "Length matters more than complexity: aim for at least 12 to 16 characters, and a passphrase of several random words is both stronger and easier to remember than a short string of symbols, because each extra character multiplies the number of guesses an attacker needs.",
  "hero": _hero("how-long-should-a-password-be", "A longer password forming a stronger lock"),
  "images": _imgs("how-long-should-a-password-be", [
    (2, "Each extra character multiplying the possible combinations", "Every character you add multiplies how long a password takes to crack."),
    (3, "Entering a strong password to log in securely", "A long passphrase is strong and still easy to type and remember."),
    (4, "A weak short lock versus a strong long one", "Short passwords are flimsy; long ones are effectively unbreakable by guessing."),
  ]),
  "faq": [
   ("How long should a password be?", "At least 12 characters, and ideally 16 or more. Longer is exponentially harder to crack."),
   ("Is length or complexity more important?", "Length. Each added character multiplies the possibilities far more than swapping a single letter for a symbol does."),
   ("Are passphrases better than passwords?", "Yes. A passphrase of several random, unrelated words is long, high-entropy and much easier to remember than a short complex string."),
   ("Should I reuse passwords?", "Never. Use a unique password for every account, ideally stored in a password manager, so one breach cannot unlock everything."),
  ],
 },

 "how-to-decode-a-jwt-safely": {
  "modified": MOD,
  "keywords": ["how to decode a jwt", "jwt decoder", "json web token", "decode jwt safely", "jwt structure", "jwt header payload signature", "is it safe to decode jwt online", "jwt explained", "jwt security", "verify jwt signature"],
  "standfirst": "A JWT is made of three parts separated by dots (header, payload and signature); the first two are only Base64-encoded, not encrypted, so anyone can read them, which is exactly why you should decode tokens locally and never paste a real token into a random website.",
  "hero": _hero("how-to-decode-a-jwt-safely", "A token made of three connected parts, handled carefully"),
  "images": _imgs("how-to-decode-a-jwt-safely", [
    (2, "The three parts of a token, with a sealed signature", "A JWT has a header, a payload and a signature that proves it is genuine."),
    (3, "Decoding a token safely, not pasting it on random sites", "A valid token can grant access, so decode it locally, never online."),
    (4, "A signature verifying the token has not been tampered with", "The signature is what lets a server trust the token."),
  ]),
  "faq": [
   ("What are the three parts of a JWT?", "A header, a payload and a signature, separated by dots. The signature is what proves the token has not been tampered with."),
   ("Is a JWT encrypted?", "No. By default it is only Base64-encoded, so the header and payload can be read by anyone who has the token; the signature provides integrity, not secrecy."),
   ("Is it safe to decode a JWT online?", "Avoid pasting real tokens into unknown websites, because a valid token can grant access to an account. Decode them locally in your browser instead."),
   ("What is the signature for?", "It lets the server verify the token was issued by it and has not been altered, using a secret or key that only the server holds."),
  ],
 },

 # ========================== DESIGN / UI ==========================

 "css-grid-explained-visual-layouts": {
  "modified": MOD,
  "keywords": ["css grid", "css grid explained", "css grid layout", "grid template columns", "css grid tutorial", "grid vs flexbox", "responsive grid css", "grid areas", "fr unit css grid", "modern css layout"],
  "standfirst": "CSS Grid is a two-dimensional layout system that lets you place elements into rows and columns you define, so you can build complex, responsive page layouts with far less code than older float or positioning tricks.",
  "hero": _hero("css-grid-explained-visual-layouts", "Panels snapping into an organised grid layout"),
  "images": _imgs("css-grid-explained-visual-layouts", [
    (2, "Items placed across the rows and columns of a grid", "You define rows and columns, then place items into the cells."),
    (3, "A layout adapting cleanly from desktop to mobile", "The same grid can rearrange itself for different screen sizes."),
    (4, "One grid item spanning several cells at once", "Items can span multiple rows or columns for richer layouts."),
  ]),
  "faq": [
   ("What is CSS Grid?", "A native CSS layout system for arranging elements in rows and columns at the same time, built for two-dimensional layouts."),
   ("What is the difference between Grid and Flexbox?", "Flexbox lays items out in one direction, a row or a column, while Grid handles both rows and columns together, making it better for whole-page layouts."),
   ("What is the fr unit?", "A flexible fraction unit that splits available space proportionally, so columns can share leftover space without fixed pixel widths."),
   ("Is CSS Grid responsive?", "Yes. With features like minmax, auto-fit and media queries, a grid can rearrange itself cleanly from desktop to mobile."),
  ],
 },

 "glassmorphism-frosted-glass-effect": {
  "modified": MOD,
  "keywords": ["glassmorphism", "frosted glass effect", "glassmorphism css", "backdrop-filter blur", "frosted glass ui", "glass effect design", "glassmorphism tutorial", "translucent ui", "blur background css", "modern ui trend"],
  "standfirst": "Glassmorphism is a UI style that makes panels look like frosted glass floating over a colourful background, created by blurring whatever is behind an element, adding slight transparency and a thin light border, usually with the CSS backdrop-filter property.",
  "hero": _hero("glassmorphism-frosted-glass-effect", "A frosted-glass panel floating over a colourful blur"),
  "images": _imgs("glassmorphism-frosted-glass-effect", [
    (2, "The layered recipe behind the frosted-glass look", "The effect is a blurred background, a translucent panel and a bright edge."),
    (3, "Frosted-glass cards in a real phone interface", "Used well, it adds depth and a premium feel to an interface."),
    (4, "The blur and edge highlight of frosted glass up close", "A soft blur-behind plus a crisp edge highlight sells the glass."),
  ]),
  "faq": [
   ("What is glassmorphism?", "A design style where elements look like translucent frosted glass, softly blurring the content behind them over a colourful backdrop."),
   ("How is the frosted-glass effect made in CSS?", "Mainly with backdrop-filter blur on a semi-transparent background, plus a subtle light border and a soft shadow for depth."),
   ("Does glassmorphism hurt performance or accessibility?", "Heavy blur can be costly on low-end devices, and low-contrast text over glass can be hard to read, so use it sparingly and keep contrast high."),
   ("When should I use glassmorphism?", "For cards, overlays and navigation over rich backgrounds where depth and lightness suit the brand, not for dense, text-heavy screens."),
  ],
 },

 "how-to-pair-fonts-that-work": {
  "modified": MOD,
  "keywords": ["how to pair fonts", "font pairing", "font combinations", "best font pairings", "typography pairing", "serif and sans serif pairing", "font pairing guide", "heading and body fonts", "choosing fonts for a website", "pairing fonts"],
  "standfirst": "Good font pairing works on contrast with harmony: pick one font for headings and another for body text that differ clearly in style but share a similar mood and proportions, which is why a classic pairing is one serif with one sans-serif.",
  "hero": _hero("how-to-pair-fonts-that-work", "Two complementary typefaces that work together as a pair"),
  "images": _imgs("how-to-pair-fonts-that-work", [
    (2, "Contrasting type shapes that still harmonise", "Aim for clear contrast between two fonts that still share a mood."),
    (3, "Choosing and pairing typefaces at a design desk", "A reliable formula is one characterful heading font with one clean body font."),
    (4, "A bold display shape paired with a light body shape", "Contrast in weight and size creates a clear hierarchy."),
  ]),
  "faq": [
   ("How do I pair fonts that work together?", "Choose two fonts with clear contrast, such as a serif heading with a sans-serif body, that still share a consistent mood, weight range and x-height."),
   ("How many fonts should I use?", "Usually two is ideal, one for headings and one for body. A third should only appear for a specific accent, or the design starts to look messy."),
   ("Can I pair two fonts from the same family?", "Yes. Using different weights or widths of one well-made superfamily is a safe, harmonious way to create hierarchy."),
   ("What makes a font pairing fail?", "Fonts that are too similar look like a mistake, while fonts with clashing moods or proportions feel disjointed. Aim for clear but comfortable contrast."),
  ],
 },

 # ======================= TECHNOLOGY / DATA =======================

 "http-status-codes-explained": {
  "modified": MOD,
  "keywords": ["http status codes", "http status codes explained", "404 error", "301 redirect", "500 error", "what does 404 mean", "status code list", "2xx 3xx 4xx 5xx", "http response codes", "common status codes"],
  "standfirst": "HTTP status codes are three-digit numbers a server returns with every response: 2xx means success, 3xx means redirect, 4xx means the request was wrong (like 404 not found), and 5xx means the server failed (like 500 internal error).",
  "hero": _hero("http-status-codes-explained", "A web request receiving a success, redirect or error status"),
  "images": _imgs("http-status-codes-explained", [
    (2, "A request going out and a colour-coded status coming back", "Every request you make gets a status code in reply."),
    (3, "Reaching a page-not-found error while browsing", "The 404 is the status code almost everyone has met in person."),
    (4, "The main families of status codes as colour groups", "The first digit tells you the family: success, redirect, client or server error."),
  ]),
  "faq": [
   ("What does a 404 status code mean?", "The server was reached but could not find the requested page or resource. The URL may be wrong or the page may have been removed."),
   ("What is the difference between a 301 and a 302 redirect?", "A 301 is a permanent redirect that passes ranking signals to the new URL, while a 302 is temporary and tells browsers the original may return."),
   ("What does a 500 error mean?", "An internal server error: something went wrong on the server side while handling the request, not with your browser or the URL."),
   ("What are the status code families?", "1xx informational, 2xx success, 3xx redirection, 4xx client errors, and 5xx server errors."),
  ],
 },

 "what-is-binary-code-text-to-binary-explained": {
  "modified": MOD,
  "keywords": ["what is binary code", "binary code explained", "text to binary", "how binary works", "binary numbers", "convert text to binary", "bits and bytes", "ascii binary", "binary to text", "base 2"],
  "standfirst": "Binary code represents all digital information using just two states, 0 and 1, called bits; letters and numbers are stored as fixed patterns of eight bits (a byte) using a character code like ASCII, which is how text becomes something a computer can store and process.",
  "hero": _hero("what-is-binary-code-text-to-binary-explained", "Digital information built from simple on and off states"),
  "images": _imgs("what-is-binary-code-text-to-binary-explained", [
    (2, "A character mapped to a fixed pattern of bits", "Each character becomes a number, and that number becomes a pattern of bits."),
    (3, "Binary working beneath everyday devices", "Every phone, laptop and app runs on this on/off layer underneath."),
    (4, "Bit positions doubling in value from right to left", "Each position is worth double the one before, which is how bits add up."),
  ]),
  "faq": [
   ("What is binary code?", "A way of representing information with only two symbols, 0 and 1, which map to the on and off states a computer can physically store."),
   ("How is text converted to binary?", "Each character is looked up in a character set like ASCII or Unicode, which assigns it a number, and that number is written as a pattern of bits."),
   ("What is a bit and a byte?", "A bit is a single 0 or 1. A byte is eight bits grouped together, enough to represent 256 different values, including one standard text character."),
   ("Why do computers use binary?", "Because electronic hardware reliably stores and switches between two states, on and off, which makes base-2 the natural and robust choice."),
  ],
 },

 "webp-vs-jpeg-vs-png": {
  "modified": MOD,
  "keywords": ["webp vs jpeg vs png", "best image format", "webp vs png", "jpeg vs png", "when to use webp", "image format comparison", "lossy vs lossless", "transparent image format", "which image format for web", "optimize images for web"],
  "standfirst": "Use JPEG for photographs where small size matters, PNG when you need transparency or sharp graphics and text, and WebP as the modern all-rounder that usually gives smaller files than both at similar quality, with support for transparency and animation.",
  "hero": _hero("webp-vs-jpeg-vs-png", "Three image formats compared side by side"),
  "images": _imgs("webp-vs-jpeg-vs-png", [
    (2, "The trade-off between file size and image quality", "Every format balances how small the file is against how good it looks."),
    (3, "Lighter image files loading faster on a website", "Choosing the right format makes pages load noticeably faster."),
    (4, "Formats that support transparency versus one that does not", "PNG and WebP keep transparency; JPEG does not."),
  ]),
  "faq": [
   ("Which image format should I use for the web?", "WebP is the best default for most web images. Fall back to JPEG for photos or PNG for transparency where WebP is not supported."),
   ("What is the difference between lossy and lossless?", "Lossy formats like JPEG discard some detail to shrink the file, while lossless formats like PNG keep every pixel but produce larger files."),
   ("Which formats support transparency?", "PNG and WebP support transparent backgrounds. JPEG does not."),
   ("Why is WebP smaller than JPEG and PNG?", "It uses more advanced compression, so it typically produces noticeably smaller files at the same visual quality."),
  ],
 },

 # ===================== HISTORICAL & GLOBAL =====================

 "how-roman-numerals-work": {
  "modified": MOD,
  "keywords": ["how roman numerals work", "roman numerals", "roman numeral converter", "roman numerals explained", "roman numeral chart", "convert roman numerals", "subtractive notation", "reading roman numerals", "roman numerals rules", "i v x l c d m"],
  "standfirst": "Roman numerals build numbers from seven letters (I, V, X, L, C, D, M) added together from largest to smallest, with a smaller letter placed before a larger one meaning subtraction, which is why IV is four and IX is nine.",
  "hero": _hero("how-roman-numerals-work", "The ancient Roman system of counting in carved strokes"),
  "images": _imgs("how-roman-numerals-work", [
    (2, "Roman marks combining by addition and subtraction", "Symbols are added from largest to smallest to build a number."),
    (3, "Roman numerals still used on clock faces today", "You still meet them on clocks, chapters, monarchs and monuments."),
    (4, "The subtractive rule where a mark before a larger one means minus", "A smaller symbol before a larger one is subtracted, like IV for four."),
  ]),
  "faq": [
   ("How do Roman numerals work?", "They combine seven base symbols by addition from largest to smallest, so VIII is 5 plus 1 plus 1 plus 1, which is eight."),
   ("What is the subtractive rule?", "When a smaller symbol appears before a larger one, you subtract it, so IV is 5 minus 1 (four) and XL is 50 minus 10 (forty)."),
   ("Why is there no zero in Roman numerals?", "The system was built for counting and tallying and never needed a symbol for nothing, so it has no zero."),
   ("Where are Roman numerals still used today?", "On clock faces, in book chapters and outlines, for monarchs and sequels, and on building dates and monuments."),
  ],
 },

 "time-zones-explained-converting-times": {
  "modified": MOD,
  "keywords": ["time zones explained", "how time zones work", "converting time zones", "utc offset", "gmt vs utc", "time zone converter", "daylight saving time", "world time zones", "schedule across time zones", "time difference between countries"],
  "standfirst": "Time zones divide the world into regions that set their clocks a fixed number of hours ahead of or behind UTC, so converting a time means adding or subtracting the difference between the two zones' offsets, with daylight saving shifting some zones by an hour part of the year.",
  "hero": _hero("time-zones-explained-converting-times", "One moment shown as different local times around the globe"),
  "images": _imgs("time-zones-explained-converting-times", [
    (2, "The world divided into longitudinal time zones", "Each zone sets its clocks a fixed offset from UTC."),
    (3, "Scheduling a call across different time zones", "The practical challenge is finding a time that works in every zone."),
    (4, "Converting a time by applying a fixed offset", "Convert by adding hours going east and subtracting going west."),
  ]),
  "faq": [
   ("How do time zones work?", "Each zone sets its local time a fixed offset from UTC, roughly following lines of longitude, so noon in one zone is a different clock time elsewhere."),
   ("How do I convert a time between zones?", "Find each zone's UTC offset and apply the difference, adding hours when moving east and subtracting when moving west."),
   ("What is the difference between GMT and UTC?", "They are almost the same reference time. UTC is the modern, precise standard, while GMT is the older term still used casually."),
   ("How does daylight saving time affect conversions?", "Some regions move their clocks forward an hour in summer, which temporarily changes their offset, so always check whether DST is active on the date."),
  ],
 },

}
