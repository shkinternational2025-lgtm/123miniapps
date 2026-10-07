# ============================================
# 123MiniApps.online - Article SEO/AEO/GEO upgrades (Batch 1 + Batch 2)
# Merged onto existing posts by build-blog.py -> apply_upgrades().
# URLs and primary keywords are unchanged; we only ADD depth:
# expanded semantic keywords, a hero + 3 in-body images, and a FAQ
# (which also emits FAQPage structured data).
#
# Image files placed at:
#   assets/images/blog/<slug>/<slug>-1-hero.webp   (hero)
#   assets/images/blog/<slug>/<slug>-2.webp        (in-body)
#   assets/images/blog/<slug>/<slug>-3.webp        (in-body)
#   assets/images/blog/<slug>/<slug>-4.webp        (in-body)
# ============================================


def _hero(slug, alt):
    return (f"assets/images/blog/{slug}/{slug}-1-hero.webp", alt)


def _img(slug, n, alt, cap):
    return ("img", f"assets/images/blog/{slug}/{slug}-{n}.webp", alt, cap)


def _imgs(slug, specs):
    # specs: list of (n, alt, cap)
    return [_img(slug, n, alt, cap) for (n, alt, cap) in specs]


MOD = "2026-10-03"

UPGRADES = {

 # ===================== PREMIUM: SaaS metrics =====================
 # Gated on its hero WebP, like every batch entry. Drop 4 images into
 # assets/images/blog/saas-metrics-explained-complete-guide/ and they appear.
 "saas-metrics-explained-complete-guide": {
  "hero": _hero("saas-metrics-explained-complete-guide", "A SaaS metrics dashboard showing recurring revenue, churn and retention trends"),
  "images": _imgs("saas-metrics-explained-complete-guide", [
    (2, "The four movements of monthly recurring revenue: new, expansion, contraction and churn", "Every month MRR is pushed up by new and expansion revenue and pulled down by contraction and churn."),
    (3, "Net revenue retention compounding an existing customer base above 100 percent", "Retention above 100 percent is the compounding engine: the base grows without a single new customer."),
    (4, "Customer lifetime value weighed against acquisition cost on a balance scale", "Healthy growth means the value a customer returns clearly outweighs what it cost to win them."),
  ]),
 },


 # ========================= BATCH 1 =========================

 "does-bionic-reading-work": {
  "modified": MOD,
  "keywords": ["does bionic reading work", "bionic reading", "bionic reading evidence", "does bionic reading help you read faster", "bionic reading adhd", "bionic reading dyslexia", "bionic reading vs speed reading", "bionic reading benefits", "fixation points reading", "speed reading", "read faster", "bionic reading converter"],
  "hero": _hero("does-bionic-reading-work", "Open book with the start of each word emphasised and an eye-focus motif above it"),
  "images": _imgs("does-bionic-reading-work", [
    (2, "Close-up of a line of text with the leading letters of each word emphasised", "Bionic reading bolds the opening of each word as a fixation cue for the eye."),
    (3, "A tablet showing a guided-reading paragraph beside a plain one", "The idea is that bold openings let the eye jump from word to word faster."),
    (4, "A reading-flow path with glowing fixation points across a row of words", "Feeling more focused is real, but it is not the same as measurably faster reading."),
  ]),
  "faq": [
   ("Does bionic reading make you read faster?", "Not reliably. Controlled studies that measured reading speed with and without bionic-style bolding have generally found no consistent improvement, and a few found a slight slowdown. Some readers do feel more focused, but feeling faster and being faster are not the same thing."),
   ("Is bionic reading good for ADHD?", "Some people with attention difficulties say the bold word-openings help them hold their place and resist skipping, so it can work as a focus aid. There is no strong controlled evidence that it improves reading for ADHD specifically, so treat it as one option to try, not a proven treatment."),
   ("Does bionic reading help with dyslexia?", "The evidence is weak. A few readers with dyslexia report it helps them stay on the line, but established supports such as wider letter spacing and dyslexia-friendly fonts have much better research behind them. Try bionic reading if it feels comfortable, but do not rely on it as a dyslexia aid."),
   ("What is the best fixation setting?", "Usually somewhere in the middle. A light fixation bolds only the first letter or two and reads almost like normal text; a heavy fixation bolds most of each word and can feel cluttered until the cue loses meaning. Adjust it to your own eye rather than leaving it at the default."),
   ("Is the bionic reading converter free and private?", "Yes. It is free with no account or sign-up, and the conversion runs entirely in your browser, so your text is never uploaded. The result uses real bold Unicode characters, so you can copy and paste it elsewhere."),
  ],
 },

 "dice-notation-explained": {
  "modified": MOD,
  "keywords": ["dice notation explained", "what does 2d6 mean", "dnd dice notation", "d20 d6 d8", "dice roller notation", "xdy+z format", "tabletop rpg dice", "dice modifiers", "how to read dice notation", "rpg dice explained"],
  "hero": _hero("dice-notation-explained", "Polyhedral tabletop RPG dice arranged dramatically with cinematic lighting"),
  "images": _imgs("dice-notation-explained", [
    (2, "A six-sided die beside symbolic multiplier and plus markers", "Dice notation is read as number-of-dice, die-size, then any modifier."),
    (3, "Top-down dice, a pencil and a blank character sheet", "The same notation drives physical dice and online dice rollers alike."),
    (4, "A translucent twenty-sided die captured mid-roll", "Every roll resolves to a number the notation describes in advance."),
  ]),
  "faq": [
   ("What does 2d6 mean?", "It means roll two six-sided dice and add them together, giving a result from 2 to 12. The first number is how many dice you roll and the number after the d is how many sides each die has, so 3d8 is three eight-sided dice."),
   ("What does the plus number in dice notation mean?", "A trailing modifier like 1d20+5 means roll the die, then add a fixed bonus to the result. So 1d20+5 gives 6 to 25. A minus works the same way in reverse, subtracting from the total."),
   ("What dice are used in Dungeons and Dragons?", "D&D uses a standard polyhedral set: d4, d6, d8, d10, d12 and d20, plus a percentile d100. The d20 handles most checks and attacks, while damage and other rolls use the smaller dice, often several at once."),
   ("What does advantage and disadvantage mean?", "Advantage means roll two d20 and keep the higher result; disadvantage means roll two and keep the lower. It is a simple way to make a roll more or less likely to succeed without changing the target number."),
   ("Can I roll dice notation online for free?", "Yes. Our dice roller accepts standard notation like 2d6+3 or 4d8, rolls instantly in your browser with no sign-up, and shows each die plus the total so you can use it for any tabletop game."),
  ],
 },

 "what-to-use-a-word-repeater-for": {
  "modified": MOD,
  "keywords": ["what to use a word repeater for", "word repeater tool", "repeat text multiple times", "duplicate a word or phrase", "bulk repeat text", "copy text n times", "repeat word online", "repeat text with line breaks"],
  "hero": _hero("what-to-use-a-word-repeater-for", "A single content card duplicating outward into a neat aligned grid"),
  "images": _imgs("what-to-use-a-word-repeater-for", [
    (2, "A vertical stack of repeated identical tiles with separators", "A word repeater copies your text as many times as you need, with optional separators."),
    (3, "A laptop showing an editor filled with repeating content blocks", "Repeated text is handy for testing layouts, filler and spacing checks."),
    (4, "Identical glossy tokens moving forward in sequence", "The tool mass-produces exact copies on demand, far faster than retyping."),
  ]),
  "faq": [
   ("What is a word repeater?", "A word repeater is a small tool that takes a word or phrase and copies it as many times as you ask, instantly. You type the text once, choose how many repeats you want, and it outputs the full block ready to copy."),
   ("What is a word repeater used for?", "Common uses include creating placeholder or filler text, stress-testing how a design handles long input, generating repeated separators or spacers, making patterned social posts, and any task where retyping the same thing many times would be tedious."),
   ("Can I repeat text with a separator or on new lines?", "Yes. A good repeater lets you choose what goes between each copy, such as a space, comma, or a line break, so you can produce a single long string or a neat vertical list depending on what you need."),
   ("Is there a limit to how many times I can repeat?", "Practical limits depend on your browser and device memory rather than the tool, and very large outputs can be slow to render. For most uses a few hundred to a few thousand repeats is comfortable."),
   ("Is the word repeater free and private?", "Yes. It runs entirely in your browser with no account or sign-up, and nothing you type is uploaded, so it stays private on your device."),
  ],
 },

 "why-stacked-discounts-never-add-up": {
  "modified": MOD,
  "keywords": ["why stacked discounts never add up", "stacked discount calculation", "20 off then 10 off", "compound discount", "discount on discount", "combining coupons", "sequential discounts math", "how to calculate stacked discounts"],
  "hero": _hero("why-stacked-discounts-never-add-up", "Two price tags linked by a stepped downward path showing one discount after another"),
  "images": _imgs("why-stacked-discounts-never-add-up", [
    (2, "A bar shrinking in two separate stages, each smaller than the last", "Each discount applies to the price left after the previous one, not to the original."),
    (3, "A shopping cart with two layered discount badges", "Stacked coupons feel bigger than they are because the second acts on a smaller number."),
    (4, "A descending staircase of glossy blocks, each smaller than the last", "Percentages compound instead of adding, so two discounts fall short of their sum."),
  ]),
  "faq": [
   ("Does 20% off then 10% off equal 30% off?", "No. The 10% comes off the already-reduced price, not the original, so 20% then 10% equals 28% off, not 30%. Stacked percentage discounts are always a little smaller than the two figures added together."),
   ("How do you calculate two stacked discounts?", "Multiply the price by the remaining fraction for each discount. For 20% then 10%: price times 0.80 times 0.90 equals price times 0.72, which is a 28% total discount. The order does not change the final price."),
   ("Does the order of discounts matter?", "For the final price, no. Multiplying by 0.80 then 0.90 gives the same result as 0.90 then 0.80. Order can matter for tax or for rules about which coupon applies first, but the math of the discount itself is identical."),
   ("Is a single 30% discount better than 20% plus 10%?", "Yes. A single 30% off beats stacking 20% and 10%, because stacking only reaches 28%. Whenever you can choose one larger discount over two that add up to the same number, the single one saves more."),
   ("How can I calculate stacked discounts quickly?", "Use our percentage and discount calculator: enter the price and each discount and it shows the final price and the true combined percentage, so you can compare a stacked offer against a single discount in seconds."),
  ],
 },

 "how-to-use-a-countdown-timer": {
  "modified": MOD,
  "keywords": ["how to use a countdown timer", "online countdown timer", "set a timer", "countdown to a date", "countdown to an event", "full screen countdown", "countdown vs stopwatch", "timer for study", "free online timer"],
  "hero": _hero("how-to-use-a-countdown-timer", "A luminous circular countdown ring paired with a glass hourglass"),
  "images": _imgs("how-to-use-a-countdown-timer", [
    (2, "A calendar page with one date emphasised beside a timer ring", "A countdown timer can run for a set duration or down to a specific date and time."),
    (3, "A productivity desk with a digital timer, notebook and coffee", "Timed focus sessions are one of the most popular uses for a countdown timer."),
    (4, "A countdown ring almost complete with a bright progress edge", "The timer alerts you the moment it reaches zero."),
  ]),
  "faq": [
   ("How do I set a countdown timer?", "Enter the amount of time you want, in hours, minutes and seconds, then press start. The timer counts down to zero and alerts you when it finishes. Most online timers also let you pause, resume and reset with one click."),
   ("Can I count down to a specific date?", "Yes. As well as a duration, many countdown timers let you pick a target date and time, so you can count down to a deadline, a launch, a birthday or the new year, with the remaining days, hours and minutes updating live."),
   ("What is the difference between a countdown timer and a stopwatch?", "A countdown timer starts from a set time and counts down to zero, best for deadlines and timed tasks. A stopwatch starts at zero and counts up, best for measuring how long something takes. They are opposites of each other."),
   ("What are countdown timers good for?", "Common uses include focus and study sessions like the Pomodoro technique, cooking, workouts and rest intervals, timeboxing work, timed presentations or exams, and counting down to an event so everyone can see how long is left."),
   ("Is the online countdown timer free?", "Yes. It runs in your browser with no account or sign-up, works on phone and desktop, and keeps counting even if you switch tabs, so you can start a timer and carry on with other things."),
  ],
 },

 "what-a-checksum-actually-proves": {
  "modified": MOD,
  "keywords": ["what a checksum actually proves", "checksum meaning", "file integrity check", "verify a download", "md5 sha256 checksum", "hash comparison", "detect file corruption", "does a checksum prove authenticity"],
  "hero": _hero("what-a-checksum-actually-proves", "A file linked by a beam of light to a fingerprint pattern and a verification shield"),
  "images": _imgs("what-a-checksum-actually-proves", [
    (2, "Two files, one with a matching fingerprint and check, one mismatching", "A matching checksum means the file arrived exactly as it left; a mismatch means it changed."),
    (3, "A laptop with a download arrow and an integrity-check shield", "Comparing checksums after a download catches corruption before you trust the file."),
    (4, "Glowing data strands arranged into a fingerprint-like pattern", "A checksum is a fingerprint of the file's exact contents, nothing more."),
  ]),
  "faq": [
   ("What is a checksum?", "A checksum is a short string of characters produced by running a file through a hash function. The same file always produces the same checksum, and even a tiny change to the file produces a completely different one, which makes it a fingerprint for the data."),
   ("What does a checksum actually prove?", "It proves integrity: that a file is byte-for-byte identical to the original when the checksums match. If even one bit changed, the checksums differ, so it reliably detects corruption or accidental changes during download or copying."),
   ("Does a matching checksum prove a file is safe or authentic?", "No. A checksum only confirms the file matches the reference value you were given. If an attacker replaced both the file and the published checksum, they would still match. For authenticity you need a signature or a checksum from a trusted, separate source."),
   ("What is the difference between MD5 and SHA-256?", "Both produce a checksum, but MD5 is older and can be deliberately fooled, so it is fine for spotting accidental corruption but not for security. SHA-256 is stronger and is the modern default when the check needs to resist tampering."),
   ("How do I check a file's checksum?", "Generate the checksum of your downloaded file and compare it to the value the source published. Our hash tool lets you produce MD5 or SHA-256 in your browser and paste in the expected value to confirm they match."),
  ],
 },

 "what-makes-a-strong-key-or-secret": {
  "modified": MOD,
  "keywords": ["what makes a strong key or secret", "strong secret key", "api key security", "entropy in keys", "random key generator", "key length", "password vs key", "storing secrets safely", "how to generate a strong key"],
  "hero": _hero("what-makes-a-strong-key-or-secret", "A key built from particles of light sliding toward a premium padlock"),
  "images": _imgs("what-makes-a-strong-key-or-secret", [
    (2, "Two strength bars, one short and weak, one long and intense", "Strength comes from length and randomness together, not from clever patterns."),
    (3, "A shield emblem with a glowing key-shaped core", "A generated random key is far stronger than anything a human would invent."),
    (4, "Randomised symbol clusters etched into a reflective surface", "Strength comes from unpredictable, high-entropy characters with no pattern to guess."),
  ]),
  "faq": [
   ("What makes a key or secret strong?", "Two things: length and randomness. A strong key is long and made of unpredictable characters with high entropy, so there is no pattern to guess and far too many combinations to try. Cleverness or memorability does not help; raw unpredictability does."),
   ("What is entropy in a key?", "Entropy measures how unpredictable a key is, usually in bits. Each extra bit doubles the number of possibilities. A key with more entropy takes exponentially longer to guess, which is why random generation beats anything a person types from memory."),
   ("How long should a secret key be?", "For API keys, tokens and secrets, aim for at least 128 bits of entropy, which is roughly 22 random characters from a full character set, and 256 bits for anything high-value. Longer is always safer when the key does not need to be memorised."),
   ("What is the difference between a password and a key?", "A password is chosen by a person and must be remembered, so it is usually shorter and weaker. A key or secret is generated by a machine, does not need to be memorised, and can therefore be much longer and fully random."),
   ("How should I store secret keys safely?", "Never hard-code secrets in public code or commit them to a repository. Keep them in environment variables or a secrets manager, restrict who can read them, and rotate them if they may have leaked. Generate them with a proper random tool, not by hand."),
  ],
 },

 "how-many-words-is-that-word-count-guide": {
  "modified": MOD,
  "keywords": ["word count guide", "how many words", "essay word count", "word count for articles", "characters vs words", "reading time from word count", "average words per page", "word count for social posts", "how many words per page"],
  "hero": _hero("how-many-words-is-that-word-count-guide", "A clean document page with a floating counter badge and counting indicators"),
  "images": _imgs("how-many-words-is-that-word-count-guide", [
    (2, "Two panels comparing grouped word units versus individual character units", "Words and characters are counted differently, and many limits use one or the other."),
    (3, "A document paired with a clock representing reading time", "Reading time is roughly word count divided by about 225 words per minute."),
    (4, "A stack of document pages with precise edges", "Length is easiest to judge by word count rather than by how the pages feel."),
  ]),
  "faq": [
   ("How many words is one page?", "A typical double-spaced page in a standard font is about 250 words, and a single-spaced page about 500. So a five-page double-spaced essay is roughly 1,250 words, though fonts, spacing and margins change the exact figure."),
   ("How many words is a typical essay or blog post?", "Short essays run about 500 words, standard ones 1,000 to 2,000, and longer assignments 3,000 or more. Blog posts that rank well are often 1,000 to 2,000 words, enough to cover a topic without padding."),
   ("What is the difference between word count and character count?", "Word count is the number of words separated by spaces; character count is every letter, number, space and symbol. Essays usually use word limits, while social posts, meta descriptions and SMS use character limits."),
   ("How do I estimate reading time from word count?", "Divide the word count by about 200 to 250 words per minute for silent reading. So a 1,000-word article takes roughly four to five minutes to read. Speaking aloud is slower, around 130 to 150 words per minute."),
   ("How do I count words online?", "Paste your text into our word counter and it shows the words, characters, sentences and estimated reading time instantly, in your browser with nothing uploaded, so you can check against any essay or post limit."),
  ],
 },

 "apply-photo-filters-in-your-browser": {
  "modified": MOD,
  "keywords": ["apply photo filters in your browser", "online photo filters", "edit photos free no upload", "brightness contrast saturation", "grayscale sepia vintage filter", "browser image editor", "private photo editing", "add filter to photo online"],
  "hero": _hero("apply-photo-filters-in-your-browser", "A framed photo divided into several colour-graded variations"),
  "images": _imgs("apply-photo-filters-in-your-browser", [
    (2, "An in-browser editing interface with brightness, contrast and saturation sliders", "Filters are just adjustments to brightness, contrast, colour and tone."),
    (3, "A split image of a plain photo and a richly graded version", "A good filter transforms the mood of a photo in one click."),
    (4, "A laptop showing a photo editor open inside a browser window", "Because it runs in your browser, your photo never leaves your device."),
  ]),
  "faq": [
   ("How do I apply filters to a photo online?", "Open the photo in a browser-based editor, choose a filter or adjust sliders for brightness, contrast, saturation and warmth, then download the result. No software to install, and with our tool nothing is uploaded to a server."),
   ("Can I edit photos without uploading them anywhere?", "Yes. Our photo filter tool processes the image entirely in your browser, so the file stays on your device and is never sent to a server. That keeps private photos private while you edit."),
   ("What filters can I apply?", "Common options include grayscale and sepia, vintage and warm or cool tones, blur and sharpen, and manual control over brightness, contrast, saturation and hue, so you can either pick a preset look or fine-tune the image yourself."),
   ("Will applying a filter reduce my photo quality?", "Adjusting brightness, contrast and colour does not meaningfully reduce quality. Quality loss mainly comes from re-saving as a compressed JPEG, so export at a high quality setting, or use PNG or WebP, to keep the image sharp."),
   ("Is the online photo filter tool free?", "Yes. It is free with no account or sign-up, works on phone and desktop, and runs client-side so your images stay private while you add filters and adjustments."),
  ],
 },

 "why-1tb-drive-shows-931gb": {
  "modified": MOD,
  "keywords": ["why 1tb drive shows 931gb", "why is my 1tb ssd only 931gb", "missing storage space", "gb vs gib", "decimal vs binary bytes", "1000 vs 1024", "formatted capacity", "real usable drive space"],
  "hero": _hero("why-1tb-drive-shows-931gb", "An SSD beside a capacity visualization with a subtle missing portion"),
  "images": _imgs("why-1tb-drive-shows-931gb", [
    (2, "Two stacks of cubes, one decimal and one slightly smaller binary", "Manufacturers count in 1,000s; your computer counts in 1,024s, which is where the gap comes from."),
    (3, "A drive beside a donut chart of usable space and the difference", "No space is missing; the same bytes are just measured two different ways."),
    (4, "A storage device circuit board with subtle capacity motifs", "The bytes are all there, simply counted in binary units."),
  ]),
  "faq": [
   ("Why does a 1TB drive show only 931GB?", "Because the maker counts a terabyte as 1,000,000,000,000 bytes, but your operating system divides by 1,024 at each step. The same bytes work out to about 931 in the computer's units, so nothing is missing; it is just measured differently."),
   ("What is the difference between GB and GiB?", "A gigabyte (GB) is 1,000,000,000 bytes using the decimal system makers use. A gibibyte (GiB) is 1,073,741,824 bytes using the binary system computers use. Windows labels the binary figure as GB, which causes the confusion."),
   ("Is the missing storage space lost or wasted?", "No. Every byte you paid for is there. The lower number is the same capacity expressed in binary units, minus a little reserved for the file system. You are not losing space to a fault or to the manufacturer."),
   ("How much real space will I actually get?", "As a rough rule, multiply the advertised size by about 0.909 to get the figure your computer will show. So 1TB shows about 931GB, 2TB about 1.82TB, and 500GB about 466GB, before a small amount used for formatting."),
   ("Why do computers use 1024 instead of 1000?", "Computers work in binary, where capacities fall naturally on powers of two, and 1,024 is two to the tenth power. Historically the industry reused the decimal prefixes kilo, mega and giga for these binary amounts, which is why the two systems disagree."),
  ],
 },

 "how-to-calculate-exact-age": {
  "modified": MOD,
  "standfirst": "Your exact age is the time from your date of birth to today, expressed in years, months and days. Here is how it is worked out, how leap years are handled, and how to get it right in seconds.",
  "keywords": ["how to calculate exact age", "exact age calculator", "age in years months days", "chronological age", "age from date of birth", "how old am i exactly", "age difference calculator", "calculate age"],
  "hero": _hero("how-to-calculate-exact-age", "A calendar with a birthday candle and a years-months-days counter motif"),
  "images": _imgs("how-to-calculate-exact-age", [
    (2, "A glowing timeline from a birth-date marker to a present-day marker", "Exact age counts the full span from your birth date to the chosen date."),
    (3, "Three counter dials for years, months and days", "The result is usually broken into years, then remaining months, then days."),
    (4, "A calendar page turning in soft dramatic light", "Exact age is simply the full span from your birth date to today."),
  ]),
  "faq": [
   ("How do I calculate my exact age?", "Count the whole years from your birth date to today, then the leftover months, then the leftover days. Doing it by hand is fiddly because months vary in length, so an age calculator that tracks each step is the reliable way."),
   ("How is age in years, months and days worked out?", "Start from the full years since birth, then add the completed months since your last birthday, then the days since that month mark. If the current day is earlier than your birth day, you borrow days from the previous month, just like subtraction."),
   ("How do leap years affect age calculation?", "Leap years add a 29 February every four years, which a good calculator accounts for automatically. People born on 29 February simply have their birthday recognised on 28 February or 1 March in non-leap years, depending on the rule used."),
   ("Can I calculate age on a past or future date?", "Yes. Exact age is just the gap between two dates, so you can set the end date to any day, past or future, to find how old someone was or will be on that date, for example on a wedding or an anniversary."),
   ("Is the age calculator free and private?", "Yes. Enter a birth date and it returns the exact age instantly in your browser, with no sign-up and nothing uploaded, so the dates you enter stay on your device."),
  ],
 },

 "how-to-calculate-days-between-dates": {
  "modified": MOD,
  "standfirst": "The number of days between two dates is the count of days from the earlier date to the later one. Here is how to count them, whether to include the end date, and how business days differ from calendar days.",
  "keywords": ["how to calculate days between dates", "days between dates", "how many days between two dates", "date difference calculator", "count days between dates", "business days vs calendar days", "days until a date", "weeks between dates", "calculate days between two dates"],
  "hero": _hero("how-to-calculate-days-between-dates", "Two calendar dates linked by a luminous arc dotted with day markers"),
  "images": _imgs("how-to-calculate-days-between-dates", [
    (2, "A monthly calendar with a continuous range of days highlighted", "Counting days means measuring the span from the start date to the end date."),
    (3, "A calendar with a marker on a future date and a countdown path", "The same method tells you how many days remain until a future date."),
    (4, "A desk with a planner, pen and a small clock", "Counting with a tool avoids month-length and leap-year mistakes."),
  ]),
  "append_sections": [
   ("h2", "Business days versus calendar days"),
   ("p", "Calendar days count every day in the span, including weekends and holidays. Business days count only working days, usually Monday to Friday, and often skip public holidays too. The difference matters a lot for things like shipping estimates, payment terms and project deadlines, where only working days move the timeline forward. As a rough guide, a span of calendar days contains about five business days for every seven, so a 30-day window is roughly 21 to 22 business days before you remove any holidays. When a deadline is quoted in business days, always convert carefully rather than assuming it is the same as the calendar gap, because over a long period the two drift apart by several days."),
  ],
  "faq": [
   ("How do I count the number of days between two dates?", "Subtract the earlier date from the later one. Because months have different lengths and leap years add a day, doing it by hand is error-prone, so a date calculator that counts the exact span is the dependable way to get it right."),
   ("Does the count include the end date?", "It depends on what you need. The plain difference between two dates excludes the end date, so 1 March to 3 March is two days. If you are counting the days you will actually use something, like nights booked, you may want to add one to include both ends."),
   ("What is the difference between business days and calendar days?", "Calendar days include every day, weekends and holidays. Business days count only working days, normally Monday to Friday and excluding public holidays. Shipping, payment and legal deadlines are often in business days, which is fewer than the calendar gap."),
   ("How do I find how many days until a date?", "Set the start date to today and the end date to the future date, and the day count is how many days remain. This is handy for counting down to a deadline, an event, a holiday or a birthday."),
   ("How do I calculate days between dates online?", "Enter the two dates in our days-between-dates tool and it returns the exact number of days instantly, along with weeks and months, in your browser with nothing uploaded."),
  ],
 },

 "how-qr-codes-work-and-how-to-make-one": {
  "modified": MOD,
  "standfirst": "A QR code is a square barcode that stores data, most often a web link, which a phone camera can read in an instant. Here is how QR codes work and how to make your own for free.",
  "keywords": ["how qr codes work", "how to make a qr code", "qr code generator", "create a qr code free", "how do qr codes work", "how are qr codes made", "qr code for url wifi text", "scan a qr code", "static vs dynamic qr code"],
  "hero": _hero("how-qr-codes-work-and-how-to-make-one", "A smartphone scanning a crisp QR code with a visible scan beam"),
  "images": _imgs("how-qr-codes-work-and-how-to-make-one", [
    (2, "A QR code dissolving into streams of data particles", "A QR code stores data in a grid of modules with built-in error correction."),
    (3, "A QR code surrounded by icons for a link, wifi and a contact card", "A QR code can hold a link, wifi details, contact information and more."),
    (4, "An extreme close-up of a QR code's corner finder pattern", "The three corner squares let a camera locate and orient the code instantly."),
  ]),
  "faq": [
   ("How do QR codes work?", "A QR code stores data as a grid of black and white squares. The three large corner squares let a camera find and orient the code, and the rest encodes the data with built-in error correction, so a phone can read it quickly even if part is dirty or damaged."),
   ("How do I make a QR code?", "Choose what the code should contain, such as a web address, then enter it into a QR generator and download the image. Our generator makes a QR code instantly in your browser for a link, plain text and more, with no sign-up."),
   ("What can a QR code store?", "Most commonly a web link, but also plain text, a phone number, an email, an SMS, wifi network details, and contact cards. The more data you store, the denser the pattern becomes, so short links scan most reliably."),
   ("Do QR codes expire or cost money?", "A basic static QR code never expires and is free; it simply encodes your data directly. Dynamic QR codes, which let you change the destination later and track scans, are a paid feature of some services because they route through their server."),
   ("Are QR codes safe to scan?", "The code itself is just data, but it can point to a malicious site, so treat an unknown QR code like an unknown link. Most phones show the destination before opening it, so check the address looks right before you continue."),
  ],
 },

 "make-a-favicon-for-every-browser": {
  "modified": MOD,
  "standfirst": "A favicon is the small icon shown in a browser tab, bookmark and history for your site. Here are the sizes you actually need, how to make one, and the HTML to add it so it shows everywhere.",
  "keywords": ["make a favicon for every browser", "favicon size", "favicon generator", "favicon sizes 16x16 32x32", "favicon.ico", "apple touch icon", "favicon for all devices", "add favicon to website", "what size should a favicon be"],
  "hero": _hero("make-a-favicon-for-every-browser", "A browser window with a crisp tab icon and a sequence of icon-size squares"),
  "images": _imgs("make-a-favicon-for-every-browser", [
    (2, "A row of the same icon rendered from very small to larger sizes", "One design needs to be exported at several sizes for different devices."),
    (3, "A close-up of a browser tab with a sharp miniature icon", "A favicon has to stay recognisable even at 16 pixels."),
    (4, "A smartphone home screen featuring one crisp app icon", "The same icon follows your site onto phone home screens too."),
  ]),
  "faq": [
   ("What size should a favicon be?", "Provide several sizes. The classic tab icon is 16x16 and 32x32 pixels, modern browsers like a 48x48, the Apple touch icon for iPhones is 180x180, and Android uses 192x192 and 512x512. A generator can create them all from one square image."),
   ("What is a favicon?", "A favicon is the small square icon a browser shows next to your page title in the tab, in bookmarks, in history and sometimes in search results. It helps people recognise your site at a glance among many open tabs."),
   ("How do I make a favicon?", "Start with a simple, square, high-contrast image that reads well when tiny, then use a favicon generator to export the required sizes. Our tool creates the icon set in your browser so you can download and add it to your site."),
   ("How do I add a favicon to my website?", "Place the icon files in your site, then add link tags in the page head: a standard icon link for the .ico or .png, an apple-touch-icon link for iPhones, and entries for the larger PNG sizes so every browser and device finds the right one."),
   ("Why is my favicon not showing?", "Browsers cache favicons aggressively, so a new one can take a while to appear; a hard refresh or clearing the cache helps. Also check the file path in your link tag is correct and the image is a supported size and format."),
  ],
 },

 "morse-code-explained-how-to-read-and-translate": {
  "modified": MOD,
  "standfirst": "Morse code represents letters and numbers as short dots and long dashes. Here is how to read it, the full alphabet, how to write and translate it, and the famous SOS signal.",
  "keywords": ["morse code explained", "morse code alphabet", "how to read morse code", "how to write in morse code", "morse code translator", "dots and dashes", "sos in morse code", "letters in morse code", "learn morse code", "morse code to text"],
  "hero": _hero("morse-code-explained-how-to-read-and-translate", "A vintage brass telegraph key under cinematic light with signal waves radiating"),
  "images": _imgs("morse-code-explained-how-to-read-and-translate", [
    (2, "A stream of dot-and-dash pulses forming a clean wave pattern", "Each letter and number has its own sequence of dots and dashes."),
    (3, "An orderly grid of cells each holding a dot-and-dash pattern", "A chart maps every letter to its own rhythm of short and long signals."),
    (4, "A signal lamp flashing a short-long-short SOS rhythm", "SOS is three dots, three dashes, three dots, sent as one continuous signal."),
  ]),
  "faq": [
   ("How do you read morse code?", "Read each letter as a pattern of short signals, called dots, and long signals, called dashes. A short gap separates letters and a longer gap separates words. Once you know the pattern for each letter you can decode a message symbol by symbol."),
   ("What is SOS in morse code?", "SOS is three dots, three dashes, then three dots, sent as one unbroken sequence with no gaps between the letters. It was chosen as a distress signal because the rhythm is simple, distinctive and easy to recognise even in poor conditions."),
   ("How do I write my name in morse code?", "Translate each letter to its dot-and-dash pattern, leave a short gap between letters, and a longer gap between words. A morse translator does this instantly: type your text and it outputs the dots and dashes ready to copy, flash or tap."),
   ("Is morse code still used today?", "Yes, in limited ways. Amateur radio operators still use it, aviation uses it to identify navigation beacons, and it remains a reliable fallback because a simple tone, light or tap can carry it when voice and data cannot."),
   ("How do I translate morse code to text?", "Paste the dots and dashes into a morse translator and it converts them back to letters, or type text to get the code. Our translator works both ways in your browser, with nothing uploaded."),
  ],
 },

 "how-strikethrough-text-works": {
  "modified": MOD,
  "keywords": ["how strikethrough text works", "strikethrough text", "strikethrough generator", "cross out text", "strikethrough on whatsapp", "strikethrough on discord", "unicode strikethrough", "how to strike through text", "strikethrough in markdown"],
  "hero": _hero("how-strikethrough-text-works", "Neat text-line shapes with one bright strike bar passing through them"),
  "images": _imgs("how-strikethrough-text-works", [
    (2, "Two stacked line blocks, the top plain and the bottom struck through", "Strikethrough adds an invisible combining mark to each character."),
    (3, "A phone screen with a message card where part of the text is crossed out", "Because the mark travels with the characters, it pastes into chat and social boxes."),
    (4, "A single symbol with a crisp strike mark over it", "The strike is a combining mark attached to each character, not formatting."),
  ]),
  "faq": [
   ("How do I make strikethrough text?", "Use a strikethrough generator: type your text and it adds a combining line mark to each character, then copy the result. Because the strike is built into the characters, it pastes into places that have no formatting button."),
   ("How do I strike through text on WhatsApp?", "WhatsApp has its own shortcut: put a tilde on each side of the text, like ~this~, and it shows as struck through. For apps without that shortcut, a Unicode strikethrough generator produces text that pastes in already crossed out."),
   ("How does Unicode strikethrough work?", "It uses combining characters, special marks that have no width of their own and attach to the character before them. A strike mark after every letter draws a line through each one, and the effect travels with the text when copied."),
   ("Where does strikethrough text work and not work?", "It pastes into most chat and social boxes, including Discord, Instagram, Facebook and X, because they store the characters as typed. It fails in fields that strip text down to plain letters, such as some sign-up forms and search boxes."),
   ("Is the strikethrough generator free?", "Yes, it is free with no sign-up and runs in your browser, so nothing is uploaded. You can copy the crossed-out text and paste it wherever plain characters are allowed."),
  ],
 },

 "url-encoding-percent-encoding-explained": {
  "modified": MOD,
  "keywords": ["url encoding percent encoding explained", "percent encoding", "what is %20", "url encode online", "encode special characters in url", "reserved characters url", "encodeuricomponent", "decode a url", "url space encoding"],
  "hero": _hero("url-encoding-percent-encoding-explained", "A browser address bar where special characters turn into encoded token blocks"),
  "images": _imgs("url-encoding-percent-encoding-explained", [
    (2, "A row of special-character chips linked by arrows to encoded chips", "Unsafe characters are replaced with a percent sign and their code."),
    (3, "A URL-path object with a gap transforming into an encoded segment", "A space becomes %20 so the URL stays a single valid string."),
    (4, "A developer monitor showing an encoded query string", "Encoding keeps special characters from breaking the structure of a link."),
  ]),
  "faq": [
   ("What is percent-encoding?", "Percent-encoding, also called URL encoding, replaces characters that are not safe in a web address with a percent sign followed by two hex digits. It lets URLs carry spaces, symbols and non-English letters without breaking the link's structure."),
   ("Why is a space written as %20?", "A raw space would end or break a URL, so it is encoded. The space character is number 32, which is 20 in hexadecimal, so it becomes %20. Some parts of a URL use a plus sign for a space instead, but %20 always works."),
   ("Which characters need to be URL-encoded?", "Reserved characters that have a special meaning, such as space, question mark, ampersand, hash, slash, plus and percent, must be encoded when used as data rather than as structure. Letters, digits and a few symbols like hyphen and underscore are safe as-is."),
   ("How do I encode or decode a URL?", "Paste the text or address into a URL encoder to convert unsafe characters to percent codes, or into a decoder to turn them back. Our tool does both instantly in your browser, which is handy for query strings and API links."),
   ("What is the difference between encodeURI and encodeURIComponent?", "encodeURI keeps the overall URL working and leaves structural characters like slash and question mark alone. encodeURIComponent encodes those too, so it is the right choice for a single value you are putting into a query parameter."),
  ],
 },

 "metric-to-imperial-unit-conversion-explained": {
  "modified": MOD,
  "standfirst": "Converting metric to imperial means turning centimetres, kilometres, kilograms and Celsius into inches, miles, pounds and Fahrenheit. Here are the formulas, the common conversions, and a quick reference chart.",
  "keywords": ["metric to imperial conversion", "metric to imperial", "cm to inches", "km to miles", "kg to pounds", "celsius to fahrenheit", "metric to imperial formula", "metric imperial chart", "metric to imperial converter"],
  "hero": _hero("metric-to-imperial-unit-conversion-explained", "A ruler transitioning from metric markings to imperial markings with a scale"),
  "images": _imgs("metric-to-imperial-unit-conversion-explained", [
    (2, "Paired icons for length, distance and weight linked by two-way arrows", "Each conversion is a fixed multiply-or-divide by a known factor."),
    (3, "Two panels, one metric and one imperial, joined by a conversion bridge", "The same factors work in reverse to go from imperial back to metric."),
    (4, "A dual-scale measuring tape showing centimetres and inches", "A dual-scale tape makes the relationship between the two systems visible."),
  ]),
  "faq": [
   ("How do I convert metric to imperial?", "Multiply by the right factor for each unit. Centimetres to inches, divide by 2.54; kilometres to miles, multiply by 0.621; kilograms to pounds, multiply by 2.205. For temperature, multiply Celsius by 9/5 and add 32 to get Fahrenheit."),
   ("How many inches are in a centimetre?", "One centimetre is about 0.394 inches, and one inch is exactly 2.54 centimetres. To convert centimetres to inches, divide by 2.54; to go the other way, multiply inches by 2.54."),
   ("How do I convert kilometres to miles?", "Multiply kilometres by 0.621 to get miles, or divide by 1.609. So 5 km is about 3.1 miles and 10 km is about 6.2 miles. A quick mental estimate is to take roughly five-eighths of the kilometre figure."),
   ("How do I convert Celsius to Fahrenheit?", "Multiply the Celsius temperature by 9, divide by 5, then add 32. For example, 20C becomes 68F and 30C becomes 86F. To reverse it, subtract 32, multiply by 5 and divide by 9."),
   ("Is there a quick way to convert units online?", "Yes. Our unit converter handles length, weight, temperature and more in both directions, instantly in your browser, so you do not have to remember every factor by hand."),
  ],
 },

 "how-to-calculate-fuel-cost-of-a-trip": {
  "modified": MOD,
  "standfirst": "Trip fuel cost is the distance divided by your fuel efficiency, multiplied by the fuel price. Here is the formula, a worked example, and how to handle both MPG and litres per 100km.",
  "keywords": ["how to calculate fuel cost of a trip", "trip fuel cost calculator", "gas cost estimator", "miles per gallon", "fuel efficiency", "road trip cost", "litres per 100km", "how to calculate fuel cost for a trip", "petrol cost calculator"],
  "hero": _hero("how-to-calculate-fuel-cost-of-a-trip", "A fuel pump, a winding road and subtle coin motifs"),
  "images": _imgs("how-to-calculate-fuel-cost-of-a-trip", [
    (2, "Three icons in sequence: distance, fuel price and vehicle efficiency", "You need three numbers: distance, fuel price, and your vehicle's efficiency."),
    (3, "A car on a highway with a fuel gauge and a trail of cost markers", "A more efficient vehicle covers the same distance for less fuel cost."),
    (4, "A fuel gauge needle near a stack of coins", "Halve your efficiency and the fuel cost of the trip doubles."),
  ]),
  "faq": [
   ("How do I calculate the fuel cost of a trip?", "Work out how much fuel the trip needs, then multiply by the price per unit. In MPG: divide the distance by your miles per gallon to get gallons, then multiply by the price per gallon. The result is your trip fuel cost."),
   ("What is the fuel cost formula?", "Fuel cost equals distance divided by fuel efficiency, times fuel price. With metric figures: litres used equals distance in km times litres-per-100km divided by 100, then multiply litres by the price per litre."),
   ("Can you give a worked example?", "For a 300-mile trip at 30 MPG with fuel at 4 dollars a gallon: 300 divided by 30 is 10 gallons, times 4 dollars is 40 dollars for the trip. Halve your MPG and the cost doubles, which shows why efficiency matters."),
   ("What is the difference between MPG and litres per 100km?", "MPG measures distance per unit of fuel, so higher is better. Litres per 100km measures fuel per fixed distance, so lower is better. They describe the same thing from opposite directions and both can be used in a fuel cost calculation."),
   ("How can I lower my trip fuel cost?", "Drive smoothly and within the speed limit, keep tyres properly inflated, remove extra weight and roof racks, combine errands into one trip, and compare fuel prices along your route. Small habits add up over a long journey."),
  ],
 },

 "what-is-ascii-text-to-character-codes": {
  "modified": MOD,
  "keywords": ["what is ascii", "ascii text to character codes", "ascii table", "text to ascii", "ascii codes a-z", "character to number", "ascii vs unicode", "ascii to text converter", "decimal hex ascii values"],
  "hero": _hero("what-is-ascii-text-to-character-codes", "Letter forms transforming into number blocks and binary patterns in a grid"),
  "images": _imgs("what-is-ascii-text-to-character-codes", [
    (2, "A character tile linked by an arrow to a number tile and a binary pattern", "Each character has a fixed numeric code that computers store instead of the letter."),
    (3, "A keyboard key connected by a beam of light to a microchip", "Pressing a key sends its character code, which software turns back into the letter."),
    (4, "A grid of glowing cells like an encoded character table", "ASCII assigns every character a fixed number from 0 to 127."),
  ]),
  "faq": [
   ("What is ASCII?", "ASCII is a character encoding that assigns a number from 0 to 127 to letters, digits, punctuation and control signals. It lets computers store and exchange text as numbers, so an uppercase A is always 65 and a lowercase a is always 97."),
   ("How do I convert text to ASCII codes?", "Take each character and look up its code: A is 65, B is 66, and so on. A converter does this instantly, turning a word into its list of numbers, and can also show the values in hexadecimal or binary."),
   ("What is the difference between ASCII and Unicode?", "ASCII covers 128 characters, enough for basic English. Unicode extends this to cover every writing system, emoji and symbol, while keeping the first 128 codes identical to ASCII, so plain English text is valid in both."),
   ("What are ASCII codes for A to Z?", "Uppercase A to Z are codes 65 to 90, and lowercase a to z are 97 to 122. Digits 0 to 9 are 48 to 57. The 32-code gap between upper and lower case is why flipping one bit changes a letter's case."),
   ("How do I convert ASCII codes back to text?", "Map each number to its character: 72 is H, 105 is i, and so on. Our ASCII tool converts text to codes and codes back to text in your browser, in decimal, hex or binary, with nothing uploaded."),
  ],
 },

 # ========================= BATCH 2 =========================

 "crop-image-to-right-aspect-ratio": {
  "modified": MOD,
  "standfirst": "Cropping to the right aspect ratio means trimming an image to a fixed width-to-height shape, like 1:1 or 16:9, so it fits where it needs to without stretching. Here is how to do it cleanly.",
  "keywords": ["crop image to aspect ratio", "crop to 1:1", "crop to 16:9", "crop to 4:3", "instagram crop size", "youtube thumbnail crop", "crop without stretching", "fixed ratio crop online", "resize vs crop"],
  "hero": _hero("crop-image-to-right-aspect-ratio", "A photo with a crop frame overlay snapping to a fixed ratio"),
  "images": _imgs("crop-image-to-right-aspect-ratio", [
    (2, "The same image shown cropped to square, 16:9 and 4:3 frames", "Each platform wants a specific ratio, so one photo often needs several crops."),
    (3, "A crop handle being dragged on an image with the ratio locked", "Locking the ratio keeps the crop proportional while you choose what to keep."),
    (4, "A full photo beside its cropped version", "Cropping trims the frame; it does not squash the picture like a bad resize does."),
  ]),
  "faq": [
   ("What does cropping to an aspect ratio mean?", "It means trimming an image to a fixed width-to-height shape, such as 1:1 (square), 16:9 (widescreen) or 4:3. You keep the part you want and cut the rest, so the result fits a specific slot without being stretched or squashed."),
   ("What is the difference between cropping and resizing?", "Cropping removes part of the image to change its shape or framing. Resizing keeps the whole image but changes its pixel dimensions. To fit a fixed ratio without distortion you usually crop first, then resize the result."),
   ("What aspect ratio should I use for social media?", "Common ones are 1:1 for an Instagram feed post, 4:5 for an Instagram portrait, 9:16 for stories and reels, and 16:9 for YouTube thumbnails and most video. Crop to the target ratio before uploading so the platform does not crop it for you."),
   ("Will cropping reduce my image quality?", "Cropping itself does not lower quality; it only removes pixels from the edges. Quality drops only if you then enlarge the smaller cropped image or re-save it as a heavily compressed JPEG. Crop from a high-resolution original where possible."),
   ("How do I crop an image to a ratio online?", "Open the image in our crop tool, choose or lock the aspect ratio, position the frame over the part you want, and export. It runs in your browser with nothing uploaded, so your image stays private."),
  ],
 },

 "css-box-shadow-explained": {
  "modified": MOD,
  "keywords": ["css box-shadow explained", "box-shadow property", "css drop shadow", "box-shadow offset blur spread", "inset box shadow", "multiple box shadows", "css shadow generator", "soft shadow css", "card shadow css"],
  "hero": _hero("css-box-shadow-explained", "A card floating above a surface with a soft realistic shadow"),
  "images": _imgs("css-box-shadow-explained", [
    (2, "Several cards with different shadow depths and blur amounts", "Changing offset, blur and spread turns a flat box into one that feels lifted off the page."),
    (3, "A shadow shown with its offset, blur and spread highlighted by light", "box-shadow takes an x and y offset, a blur radius, a spread, and a colour."),
    (4, "A UI button with a subtle elevated shadow, close up", "Soft, low-contrast shadows look the most natural and premium."),
  ]),
  "faq": [
   ("What does the CSS box-shadow property do?", "box-shadow draws a shadow around an element's box. You control the horizontal and vertical offset, the blur radius, an optional spread, and the colour, which together make an element look raised, pressed, or softly floating above the page."),
   ("What do the box-shadow values mean?", "The order is horizontal offset, vertical offset, blur radius, spread radius, then colour. Offsets move the shadow, a larger blur makes it softer, spread grows or shrinks it, and the colour, usually a low-opacity black, sets how strong it looks."),
   ("How do I make a soft, natural shadow?", "Use small offsets, a generous blur, a slightly negative or zero spread, and a low-opacity colour such as rgba(0,0,0,0.1). Hard, dark, offset shadows look dated; soft diffuse ones look modern and premium."),
   ("What is an inset box-shadow?", "Adding the keyword inset draws the shadow inside the element instead of outside, which makes a box look pressed in or recessed. It is useful for input fields, pressed buttons and subtle inner depth."),
   ("Can I add more than one shadow?", "Yes. Separate several shadows with commas and they stack from front to back. Layering a tight, darker shadow with a wider, lighter one is a common trick for realistic, polished depth."),
  ],
 },

 "how-to-make-writing-easier-to-read": {
  "modified": MOD,
  "keywords": ["how to make writing easier to read", "improve readability", "readability tips", "plain language writing", "short sentences", "readability score", "make text clear", "write for the web", "reading level"],
  "hero": _hero("how-to-make-writing-easier-to-read", "A clean, well-spaced paragraph with generous line spacing, calm and legible"),
  "images": _imgs("how-to-make-writing-easier-to-read", [
    (2, "Dense cramped text beside airy well-spaced text", "Short paragraphs and white space make a page feel approachable, not daunting."),
    (3, "A readability gauge beside a block of text", "A readability score estimates how much effort a reader needs to follow your writing."),
    (4, "Long sentence bars shortened into several short bars", "Shorter sentences and simpler words lower the effort it takes to read."),
  ]),
  "faq": [
   ("How do I make my writing easier to read?", "Use short sentences and short paragraphs, prefer plain everyday words over jargon, put the main point first, break text with subheadings and white space, and read it aloud to catch anything clumsy. Small changes add up to much clearer writing."),
   ("What is a good reading level to aim for?", "For a general audience, aim for roughly a grade 7 to 9 reading level, which most readability tools report. That is not dumbing down; even expert readers prefer clear, low-effort writing, especially on screens where people skim."),
   ("How long should sentences and paragraphs be?", "Keep most sentences under about 20 words and vary their length so the rhythm does not feel flat. On the web, paragraphs of one to three sentences are easiest to scan, with plenty of white space between them."),
   ("Does readability affect SEO?", "Indirectly, yes. Clear, well-structured writing keeps readers on the page longer and is easier for search and answer engines to understand and quote, which helps. Readability is not a direct ranking number, but it supports everything that is."),
   ("How do I check my writing's readability?", "Paste your text into our readability checker and it reports a reading level and flags long sentences and dense passages, in your browser with nothing uploaded, so you can tighten the parts that need it."),
  ],
 },

 "what-is-a-base64-image-data-uri": {
  "modified": MOD,
  "keywords": ["what is a base64 image", "data uri", "base64 image data uri", "embed image in html", "inline image base64", "convert image to base64", "data url image", "base64 vs image file", "when to use base64 images"],
  "hero": _hero("what-is-a-base64-image-data-uri", "An image dissolving into a stream of encoded characters embedded in code"),
  "images": _imgs("what-is-a-base64-image-data-uri", [
    (2, "An image file transforming into a long string of encoded text", "Base64 turns an image's bytes into text that can live directly inside code."),
    (3, "An HTML block with an image embedded inline rather than linked", "A data URI puts the whole image into the page, so there is no separate file to fetch."),
    (4, "A comparison of an external image link versus inline embedded data", "Inline base64 saves a request but makes the file bigger; large images are better linked."),
  ]),
  "faq": [
   ("What is a base64 image data URI?", "It is an image encoded as text and embedded directly in a web page or stylesheet using a data: URL. Instead of linking to a separate image file, the whole image travels inside the HTML or CSS as a base64 string the browser decodes."),
   ("Why would I embed an image as base64?", "To avoid a separate network request, which can speed up tiny, frequently used images like icons, and to keep an image self-contained in a single file or email. It removes the need to host or link the image elsewhere."),
   ("What are the downsides of base64 images?", "Base64 makes the data about a third larger than the original file, it cannot be cached separately by the browser, and large embedded images bloat your HTML or CSS. For big images, a normal linked file is usually faster."),
   ("When should I use a data URI versus a normal image file?", "Use base64 for very small, reused assets such as icons and simple backgrounds, or when you need everything in one file. Use a normal linked image for photos and anything large, so the browser can cache it and load the page faster."),
   ("How do I convert an image to base64?", "Upload or drop the image into our base64 tool and it outputs the data URI ready to paste into your HTML or CSS. It runs in your browser, so the image is never sent to a server."),
  ],
 },

 "how-to-build-a-color-palette": {
  "modified": MOD,
  "keywords": ["how to build a color palette", "color palette generator", "choose brand colors", "color harmony", "complementary colors", "analogous colors", "60 30 10 rule", "website color scheme", "accessible color palette"],
  "hero": _hero("how-to-build-a-color-palette", "An elegant arrangement of harmonious colour swatches"),
  "images": _imgs("how-to-build-a-color-palette", [
    (2, "A colour wheel with harmonious points selected", "Colour harmony comes from picking relationships on the wheel, not random colours."),
    (3, "A clean UI mockup using one cohesive palette", "A small, consistent palette makes a design feel intentional and professional."),
    (4, "A base colour expanded into tints and shades", "A few tints and shades of each colour give you a full, flexible palette."),
  ]),
  "faq": [
   ("How do I build a colour palette?", "Start with one main brand colour, then build around it using harmony: a complementary colour for contrast, or analogous colours for calm. Add a neutral or two and a few tints and shades, and limit yourself to a small set so the result stays cohesive."),
   ("What is the 60-30-10 rule?", "It is a balance guide: use your dominant colour for about 60% of a design, a secondary colour for 30%, and an accent for the final 10%. It stops any one colour from overwhelming the others and keeps the result harmonious."),
   ("What are complementary and analogous colours?", "Complementary colours sit opposite each other on the colour wheel and give strong contrast, good for accents. Analogous colours sit next to each other and feel calm and unified, good for backgrounds and larger areas."),
   ("How many colours should a palette have?", "For most brands and websites, a core of three to five colours works best: one or two main colours, one accent, and a couple of neutrals. Too many colours make a design feel busy and inconsistent."),
   ("How do I keep a palette accessible?", "Check that text and background colours have enough contrast, roughly a 4.5-to-1 ratio for normal text, and never rely on colour alone to convey meaning. A contrast checker confirms your combinations are readable for everyone."),
  ],
 },

 "text-to-speech-in-your-browser": {
  "modified": MOD,
  "keywords": ["text to speech in your browser", "tts online free", "read text aloud", "browser text to speech", "convert text to audio", "natural voice tts", "listen to articles", "accessibility read aloud", "text to voice"],
  "hero": _hero("text-to-speech-in-your-browser", "A document with sound waves radiating from it beside a speaker motif"),
  "images": _imgs("text-to-speech-in-your-browser", [
    (2, "A block of text transforming into an audio waveform", "Text-to-speech turns written words into spoken audio on the fly."),
    (3, "A browser window with a play button over a passage of text", "Modern browsers can read a page aloud without any extra software."),
    (4, "Headphones resting beside a document", "Listening lets you take in writing while your eyes and hands are busy."),
  ]),
  "faq": [
   ("How does text to speech in the browser work?", "Modern browsers include a built-in speech engine that converts written text into spoken audio. A text-to-speech tool sends your text to that engine, which reads it aloud using one of the voices installed on your device, with no download needed."),
   ("Is browser text to speech free?", "Yes. It uses the voices already built into your operating system and browser, so a web-based text-to-speech tool is free, works offline once the page is loaded for many voices, and needs no account."),
   ("Can I choose the voice and speed?", "Usually yes. Most text-to-speech tools let you pick from the voices installed on your device, change the speaking rate, and adjust the pitch, so you can make the reading faster for review or slower for careful listening."),
   ("What is text to speech useful for?", "It helps with accessibility for people who find reading hard, lets you listen to articles while multitasking, catches awkward phrasing when you proofread by ear, and supports language learning by pairing text with pronunciation."),
   ("Is my text private when using an online reader?", "With our tool the conversion happens in your browser using your device's own voices, so the text is not uploaded to a server. Always check any text-to-speech service's policy if it uses cloud voices instead."),
  ],
 },

 "what-bmi-measures-and-what-it-doesnt": {
  "modified": MOD,
  "keywords": ["what bmi measures", "what bmi does not measure", "bmi meaning", "bmi limitations", "bmi vs body fat", "is bmi accurate", "bmi categories", "body mass index explained", "bmi for athletes"],
  "hero": _hero("what-bmi-measures-and-what-it-doesnt", "A clean gauge with a marker, an abstract health-measurement concept"),
  "images": _imgs("what-bmi-measures-and-what-it-doesnt", [
    (2, "Two bars representing height and weight combined into a single figure", "BMI is just weight compared to height, reduced to one number."),
    (3, "A gauge with labelled range zones", "BMI sorts that number into broad categories, nothing more."),
    (4, "Two abstract forms of equal weight but different composition", "BMI cannot tell muscle from fat, which is its biggest blind spot."),
  ]),
  "faq": [
   ("What does BMI actually measure?", "BMI, or body mass index, is simply your weight divided by your height squared. It is a quick ratio that sorts people into broad categories. It measures weight relative to height and nothing else, which is why it is only a rough screening tool."),
   ("What does BMI not measure?", "BMI cannot tell muscle from fat, where fat is stored, or your overall fitness. A muscular athlete and someone carrying excess fat can share the same BMI, so it says nothing about body composition or health on its own."),
   ("How is BMI calculated?", "Divide your weight in kilograms by your height in metres squared. In imperial units, multiply weight in pounds by 703 and divide by height in inches squared. The result is a single number placed into a category."),
   ("What are the BMI categories?", "The common adult ranges are under 18.5 underweight, 18.5 to 24.9 normal, 25 to 29.9 overweight, and 30 or above in the obese range. These are population guides, not a diagnosis for any individual."),
   ("Is BMI accurate for everyone?", "No. It is a useful population-level screen but a poor individual measure, especially for athletes, older adults, and different body types. Treat it as one rough signal and talk to a health professional for a fuller picture. This is general information, not medical advice."),
  ],
 },

 "aspect-ratio-explained-16-9-4-3": {
  "modified": MOD,
  "keywords": ["aspect ratio explained", "16:9 vs 4:3", "what is aspect ratio", "common aspect ratios", "1:1 square ratio", "9:16 vertical video", "aspect ratio calculator", "widescreen ratio", "image ratio for social media"],
  "hero": _hero("aspect-ratio-explained-16-9-4-3", "Nested rectangles showing 16:9, 4:3 and 1:1 proportions"),
  "images": _imgs("aspect-ratio-explained-16-9-4-3", [
    (2, "A screen showing a 16:9 frame beside a 4:3 frame", "16:9 is wide and modern; 4:3 is the taller, older TV shape."),
    (3, "The same image letterboxed in one frame and cropped in another", "Fitting content into a different ratio means either bars or cropping."),
    (4, "Proportional rectangles sized to common ratios", "Each ratio is just a fixed relationship between width and height."),
  ]),
  "faq": [
   ("What is an aspect ratio?", "An aspect ratio is the relationship between an image or screen's width and height, written as two numbers like 16:9. It describes the shape, not the size, so a 16:9 image has the same proportions whether it is tiny or huge."),
   ("What is the difference between 16:9 and 4:3?", "16:9 is widescreen, the modern standard for TVs, monitors and most video. 4:3 is nearly square and taller, the shape of older televisions and many cameras. The same picture looks wider in 16:9 and more boxed-in at 4:3."),
   ("What are the most common aspect ratios?", "16:9 for video and most screens, 4:3 for older displays and some photos, 1:1 square for social feed posts, 9:16 vertical for phone video and stories, and 3:2 for many cameras and prints. Each suits a different place."),
   ("How do I change an image's aspect ratio?", "You crop it to the new shape, which trims part of the picture, or you add bars (letterboxing) to keep everything visible. Stretching to a new ratio distorts the image and should be avoided."),
   ("How do I calculate an aspect ratio?", "Divide the width by the height and simplify, or keep the width-to-height pair. Our aspect ratio tool works out the ratio, or the missing dimension for a target ratio, instantly in your browser."),
  ],
 },

 "barcodes-explained-how-to-generate-one": {
  "modified": MOD,
  "keywords": ["barcodes explained", "how to generate a barcode", "barcode generator", "how do barcodes work", "upc ean barcode", "code 128 barcode", "barcode vs qr code", "create a barcode free", "1d barcode"],
  "hero": _hero("barcodes-explained-how-to-generate-one", "A crisp barcode with a scanner beam passing over it"),
  "images": _imgs("barcodes-explained-how-to-generate-one", [
    (2, "A barcode's bars dissolving into data", "The widths and spacing of the bars encode numbers a scanner reads."),
    (3, "A product on a shelf with a barcode, retail scene", "Barcodes let a till look up a product and its price in an instant."),
    (4, "An extreme close-up of barcode lines", "A quiet zone and start and stop patterns tell the scanner where the code begins and ends."),
  ]),
  "faq": [
   ("How do barcodes work?", "A barcode encodes numbers or text as a pattern of parallel bars and spaces of varying width. A scanner shines light across them and reads the reflected pattern, decoding it back into the data, usually a product number the system looks up."),
   ("What is the difference between a barcode and a QR code?", "A traditional barcode is one-dimensional, a row of vertical lines that store a small amount of data like a product number. A QR code is two-dimensional and holds far more, such as a full web link, by using a grid of squares."),
   ("What are UPC, EAN and Code 128?", "UPC and EAN are retail product barcodes used on packaging worldwide. Code 128 is a flexible format that can encode letters and numbers, common in shipping and logistics. The right one depends on what you are labelling."),
   ("How do I generate a barcode?", "Choose the barcode type, enter the number or text you want to encode, and the generator produces the image to download and print. Our barcode tool does this in your browser for common formats with no sign-up."),
   ("Do I need to register a barcode number?", "For selling products in shops you usually need an official, registered number from a body like GS1 so it is unique worldwide. For internal use, inventory, or personal projects, you can generate any barcode you like without registering."),
  ],
 },

 "how-to-reverse-text-words-lines": {
  "modified": MOD,
  "keywords": ["how to reverse text", "reverse words", "reverse lines", "backwards text generator", "flip text order", "reverse string online", "mirror text", "reverse text tool", "reverse each word"],
  "hero": _hero("how-to-reverse-text-words-lines", "A row of blocks flipping into reverse order with a mirror motif"),
  "images": _imgs("how-to-reverse-text-words-lines", [
    (2, "A sequence of tokens reversing direction with arrows", "Reversing can flip characters, the order of words, or the order of lines."),
    (3, "A mirror reflecting a row of tokens", "Character reversal reads the whole string backwards, letter by letter."),
    (4, "Stacked lines reordered from bottom to top", "Line reversal flips the order of lines while keeping each line intact."),
  ]),
  "faq": [
   ("What are the different ways to reverse text?", "There are three common kinds: reverse the characters so the whole string reads backwards, reverse the order of words while keeping each word spelled normally, or reverse the order of lines. A good tool lets you pick which one you need."),
   ("How do I reverse the letters in text?", "Character reversal takes the string and reads it from the last character to the first. A reverse-text tool does it instantly: paste your text, choose character reversal, and copy the backwards result."),
   ("How is reversing words different from reversing letters?", "Reversing letters flips every character, so hello becomes olleh. Reversing word order keeps each word readable but flips their sequence, so hello world becomes world hello. They are different operations for different needs."),
   ("What is reversing text used for?", "Common uses include creating playful backwards or mirror text for social posts, flipping word or line order when reformatting lists, testing how software handles reversed input, and simple puzzles or novelty effects."),
   ("Is the reverse text tool free and private?", "Yes. It runs entirely in your browser with no sign-up and nothing uploaded, so you can reverse characters, words or lines and copy the result while your text stays on your device."),
  ],
 },

 "how-habit-tracking-builds-consistency": {
  "modified": MOD,
  "keywords": ["how habit tracking builds consistency", "habit tracker benefits", "why habit tracking works", "build a habit", "habit streak", "don't break the chain", "daily habit tracker", "habit formation", "consistency over motivation"],
  "hero": _hero("how-habit-tracking-builds-consistency", "An elegant habit-tracker grid with check marks forming a streak"),
  "images": _imgs("how-habit-tracking-builds-consistency", [
    (2, "A calendar with a growing streak of marked days", "A visible streak turns an abstract goal into something you do not want to break."),
    (3, "A small daily action building into an upward progress curve", "Tiny, consistent actions compound far more than occasional big efforts."),
    (4, "A chain of check marks linked together", "The don't-break-the-chain effect makes each completed day motivate the next."),
  ]),
  "faq": [
   ("How does habit tracking build consistency?", "Tracking makes an invisible habit visible. Marking each day done gives a small hit of progress, builds a streak you do not want to break, and shows your pattern over time, which keeps you going on days when motivation alone would not."),
   ("Why does the don't-break-the-chain method work?", "Each marked day creates a growing chain, and the longer it gets the more you want to protect it. That loss-avoidance is a stronger, steadier motivator than enthusiasm, which fades, so the chain carries you through low-energy days."),
   ("How long does it take to form a habit?", "Research suggests it varies widely, often roughly two to three months rather than the popular 21 days, depending on the habit and the person. Consistency matters more than speed, and tracking helps you stay consistent long enough for it to stick."),
   ("What makes a habit easier to keep?", "Make it small and specific, attach it to an existing routine, reduce the friction to start, and track it so you can see progress. Missing one day is fine; the key is never missing twice in a row."),
   ("Do I need an app to track habits?", "No. A simple calendar, a grid on paper, or a basic browser tracker all work. The method matters more than the tool: the point is a visible, daily record that shows your streak and keeps you accountable."),
  ],
 },

 "understanding-color-hex-rgb-hsl": {
  "modified": MOD,
  "keywords": ["color hex rgb hsl", "what is a hex color", "rgb explained", "hsl color model", "convert hex to rgb", "hex to hsl", "css color formats", "how hex colors work", "color codes explained"],
  "hero": _hero("understanding-color-hex-rgb-hsl", "A colour swatch surrounded by its hex, RGB and HSL representations"),
  "images": _imgs("understanding-color-hex-rgb-hsl", [
    (2, "Three light beams for red, green and blue combining into a colour", "RGB builds a colour by mixing amounts of red, green and blue light."),
    (3, "An HSL wheel showing hue, saturation and lightness", "HSL describes a colour by its hue, how vivid it is, and how light it is."),
    (4, "A hex swatch with a colour dropper", "A hex code is just the same red, green and blue values written in base 16."),
  ]),
  "faq": [
   ("What is the difference between hex, RGB and HSL?", "They are three ways to write the same colour. RGB lists amounts of red, green and blue light. Hex is those same three values written in base-16, like #2563eb. HSL describes the colour by hue, saturation and lightness, which is easier to adjust by eye."),
   ("How does a hex colour code work?", "A hex code has three pairs of characters after the hash, one each for red, green and blue, from 00 to FF. So #FF0000 is full red, #00FF00 is full green, and #2563EB mixes some red, more green and strong blue to make a blue."),
   ("What is RGB?", "RGB stands for red, green and blue. Screens make colours by mixing these three channels of light, each from 0 to 255. Equal full amounts make white, all zeros make black, and different mixes make every other colour."),
   ("Why use HSL instead of hex or RGB?", "HSL is intuitive to adjust: change the hue to shift the colour, raise saturation to make it more vivid, or raise lightness to make it paler. That makes it easy to build tints, shades and harmonious variations by eye."),
   ("How do I convert between hex, RGB and HSL?", "Each format describes the same colour, so they convert exactly. Our colour tool shows a colour in hex, RGB and HSL at once and converts between them instantly in your browser, which is handy when a design calls for a specific format."),
  ],
 },

 "what-is-a-uuid-and-when-you-need-one": {
  "modified": MOD,
  "keywords": ["what is a uuid", "when to use a uuid", "uuid vs id", "uuid v4", "generate a uuid", "unique identifier", "guid vs uuid", "uuid for database", "random id generator"],
  "hero": _hero("what-is-a-uuid-and-when-you-need-one", "A single glowing unique identifier standing out among many identical tokens"),
  "images": _imgs("what-is-a-uuid-and-when-you-need-one", [
    (2, "A stream of unique identifiers, each different", "A UUID is designed to be unique without any central authority handing out numbers."),
    (3, "Database records each tagged with a unique key", "UUIDs let separate systems create records that never clash."),
    (4, "A UUID string shown as an abstract pattern of light", "A UUID is a 128-bit value, large enough that collisions are effectively impossible."),
  ]),
  "faq": [
   ("What is a UUID?", "A UUID, or universally unique identifier, is a 128-bit value written as 32 hexadecimal characters in five groups, like 550e8400-e29b-41d4-a716-446655440000. It is designed so that anyone can generate one and it will almost certainly be unique worldwide."),
   ("When do I need a UUID?", "Use a UUID when separate systems or devices must create identifiers without coordinating, such as distributed databases, offline-first apps, merging data from many sources, or public IDs you do not want to be guessable or sequential."),
   ("What is the difference between a UUID and a normal ID?", "A normal database ID is usually a sequential number assigned by one central database. A UUID is random or time-based and can be generated anywhere independently, so it avoids clashes across systems but is longer and not human-friendly."),
   ("Is a UUID guaranteed to be unique?", "Not absolutely, but effectively yes. A version-4 UUID has so many possible values (over 10 to the 36th) that the chance of two randomly generated ones colliding is vanishingly small, small enough to treat as unique in practice."),
   ("How do I generate a UUID?", "Our UUID tool generates version-4 UUIDs instantly in your browser, one or many at a time, with nothing uploaded. You can copy them straight into code, a database seed, or test data."),
  ],
 },

 "how-to-test-regular-expressions": {
  "modified": MOD,
  "keywords": ["how to test regular expressions", "regex tester", "test regex online", "regex match", "debug regex", "regex capture groups", "regex flags", "regular expression examples", "regex cheat sheet"],
  "hero": _hero("how-to-test-regular-expressions", "A magnifying glass over text with matched segments highlighted"),
  "images": _imgs("how-to-test-regular-expressions", [
    (2, "A pattern highlighting the substrings it matches in a block of text", "A regex tester shows exactly what your pattern matches as you type."),
    (3, "A developer console with regex matches glowing", "Testing against real sample text catches mistakes before they reach your code."),
    (4, "A funnel separating matching items from non-matching ones", "Capture groups let you pull specific pieces out of each match."),
  ]),
  "faq": [
   ("How do I test a regular expression?", "Paste your pattern and some sample text into a regex tester. It highlights every match live as you edit the pattern, so you can see what it catches and misses and refine it until it matches exactly what you intend."),
   ("Why should I test regex against sample text?", "Regular expressions are easy to get subtly wrong, matching too much or too little. Testing against realistic examples, including edge cases you want to exclude, is the fastest way to catch those mistakes before the pattern goes into code."),
   ("What are capture groups?", "Parentheses in a pattern create capture groups that pull out specific parts of each match, such as the year, month and day from a date. A good tester shows each group separately so you can confirm you are extracting the right pieces."),
   ("What do regex flags like g and i do?", "Flags change how matching behaves. The g flag finds all matches instead of just the first, i makes it case-insensitive, and m changes how line anchors work. A tester lets you toggle flags to see their effect instantly."),
   ("Is the regex tester free and private?", "Yes. Our regex tester runs in your browser with no sign-up, so your pattern and sample text are never uploaded, and it shows matches, groups and flags live while you work."),
  ],
 },

 "html-vs-markdown-when-to-use-each": {
  "modified": MOD,
  "keywords": ["html vs markdown", "when to use markdown", "markdown vs html", "difference between html and markdown", "markdown for writing", "html for web pages", "convert markdown to html", "markdown advantages", "when to use html"],
  "hero": _hero("html-vs-markdown-when-to-use-each", "Two documents side by side, one richly structured and one simple and plain"),
  "images": _imgs("html-vs-markdown-when-to-use-each", [
    (2, "Simple plain text transforming into formatted output", "Markdown is quick plain text that converts into formatted HTML."),
    (3, "A balance between flexibility and simplicity", "HTML offers full control; Markdown trades control for speed and readability."),
    (4, "A split view of raw markup beside its rendered result", "You write in the simpler form and the browser or tool renders the result."),
  ]),
  "faq": [
   ("What is the difference between HTML and Markdown?", "HTML is the full markup language browsers use, with tags for every element and total control over structure and styling. Markdown is a lightweight shorthand that stays readable as plain text and converts into HTML, trading flexibility for speed and simplicity."),
   ("When should I use Markdown?", "Use Markdown for writing that is mostly text: notes, README files, documentation, blog drafts, forum posts and chat. It is fast to write, easy to read in its raw form, and converts cleanly to HTML when you need a web page."),
   ("When should I use HTML?", "Use HTML when you need precise structure, custom layouts, forms, embedded media, accessibility attributes, or anything Markdown cannot express. Final web pages are HTML even when the content was first written in Markdown."),
   ("Can I mix HTML inside Markdown?", "Yes, in most Markdown processors you can drop raw HTML into a Markdown document for the few things Markdown does not cover, like a specific table layout or an embed. The rest stays as simple Markdown."),
   ("How do I convert Markdown to HTML?", "A converter turns Markdown's shorthand into the equivalent HTML tags. Our tool does this in your browser so you can write in Markdown and copy clean HTML, with nothing uploaded."),
  ],
 },

 "keyword-density-and-why-stuffing-backfires": {
  "modified": MOD,
  "keywords": ["keyword density", "keyword stuffing", "why keyword stuffing backfires", "ideal keyword density", "seo keyword usage", "over optimization penalty", "natural keyword placement", "keyword density myth", "semantic seo"],
  "hero": _hero("keyword-density-and-why-stuffing-backfires", "A clean document with a few highlighted keywords beside an overcrowded one"),
  "images": _imgs("keyword-density-and-why-stuffing-backfires", [
    (2, "A density gauge sitting comfortably in the green versus pushed into the red", "A natural amount of a keyword helps; forcing it in tips into harm."),
    (3, "A page overloaded with repeated identical tokens, visibly cluttered", "Stuffing the same phrase everywhere reads badly and signals low quality."),
    (4, "A balanced passage with a few keywords and many related terms", "Modern SEO rewards natural language and related terms over repetition."),
  ]),
  "faq": [
   ("What is keyword density?", "Keyword density is how often a target phrase appears in a page compared to its total word count, as a percentage. It was once used as an SEO target, but modern search engines understand meaning, so there is no magic number to hit."),
   ("What is the ideal keyword density?", "There is no official ideal. Rather than aim for a percentage, use your main keyword naturally where it fits, a handful of times in a normal-length article, plus related terms and synonyms. Writing for the reader usually lands in a healthy range on its own."),
   ("Why does keyword stuffing backfire?", "Cramming a phrase in repeatedly makes writing awkward, drives readers away, and search engines detect it as manipulation, which can suppress rankings. It signals low quality, the opposite of what stuffing is meant to achieve."),
   ("What should I do instead of stuffing keywords?", "Cover the topic thoroughly with natural language, include related terms, synonyms and the questions people actually ask, and structure the page clearly. This semantic approach tells search engines the page is genuinely about the subject."),
   ("Does keyword density still matter for SEO?", "Not as a number to optimise. What matters is relevance and quality: using the right words naturally, matching search intent, and covering related concepts. Density is a symptom of good writing, not a lever to pull."),
  ],
 },

 "placeholder-images-why-and-how": {
  "modified": MOD,
  "keywords": ["placeholder images", "placeholder image generator", "why use placeholder images", "dummy image", "image placeholder url", "mockup images", "placeholder.com alternative", "test images for layout", "grey placeholder box"],
  "hero": _hero("placeholder-images-why-and-how", "A layout mockup with neat grey placeholder image boxes"),
  "images": _imgs("placeholder-images-why-and-how", [
    (2, "A placeholder box labelled with its dimensions as a design motif", "Placeholders reserve the exact space a real image will later fill."),
    (3, "A wireframe page built from placeholder blocks", "They let you build and test a layout before the final images exist."),
    (4, "A placeholder box transforming into a finished image", "When the real asset is ready it simply drops into the reserved space."),
  ]),
  "faq": [
   ("What is a placeholder image?", "A placeholder image is a temporary stand-in, often a plain grey box of a specific size, used where a real image will go later. It reserves the correct space so a layout can be built and tested before the final pictures are ready."),
   ("Why use placeholder images?", "They let designers and developers lay out a page, check spacing and responsiveness, and demonstrate a design before the real photos exist. They also keep a layout from collapsing when content is still being produced."),
   ("How do I create a placeholder image?", "Pick the width and height you need and a placeholder tool generates a simple image at exactly that size, often showing the dimensions. Our tool makes placeholder images in your browser so you can drop them straight into a mockup."),
   ("What size should a placeholder image be?", "Match the size of the real image that will replace it, so the layout behaves identically. If you are testing responsiveness, generate a few sizes to see how the design adapts from mobile to desktop."),
   ("Are placeholder images okay to use on a live site?", "Only temporarily. They are for building and testing; a published page should use real, relevant images. Leaving grey placeholders on a live site looks unfinished and offers nothing to visitors or search engines."),
  ],
 },

 "unix-timestamps-epoch-time-explained": {
  "modified": MOD,
  "keywords": ["unix timestamp", "epoch time explained", "what is unix time", "convert unix timestamp", "epoch to date", "unix time in seconds", "timestamp to date", "epoch converter", "unix epoch 1970"],
  "hero": _hero("unix-timestamps-epoch-time-explained", "A clock dissolving into a stream of numbers, an epoch-time concept"),
  "images": _imgs("unix-timestamps-epoch-time-explained", [
    (2, "A timeline starting from the 1970 epoch with a marker further along", "Unix time counts seconds forward from a single fixed starting point."),
    (3, "A counter ticking up second by second", "The value is just a running count of seconds, which makes date math simple."),
    (4, "A clock beside a number-and-binary motif", "Storing time as one number avoids timezone and format confusion."),
  ]),
  "faq": [
   ("What is a Unix timestamp?", "A Unix timestamp is the number of seconds that have passed since midnight UTC on 1 January 1970, known as the epoch. It represents a moment in time as a single number, which computers find far easier to store and compare than a formatted date."),
   ("What is epoch time?", "Epoch time is another name for Unix time. The epoch is the fixed reference point, 1 January 1970 at 00:00 UTC, and the timestamp counts seconds from there. It gives every instant a single, timezone-free number."),
   ("Why do computers use Unix timestamps?", "Because a single number is simple to store, sort and do arithmetic on. Finding the gap between two moments is just subtraction, and because the value is in UTC it avoids the ambiguity of timezones and date formats."),
   ("How do I convert a Unix timestamp to a date?", "Divide or interpret the seconds since 1970 and the system maps them to a calendar date and time, usually letting you pick a timezone. Our timestamp tool converts a Unix timestamp to a readable date, and a date back to a timestamp, in your browser."),
   ("What is the year 2038 problem?", "Systems that store Unix time in a signed 32-bit integer will run out of room in January 2038, when the count exceeds what that integer can hold. Modern systems use 64-bit values, which push the limit billions of years into the future."),
  ],
 },

 "watermark-images-to-protect-your-work": {
  "modified": MOD,
  "keywords": ["watermark images", "how to watermark a photo", "protect images from theft", "add watermark online", "transparent watermark", "logo watermark", "batch watermark", "photo copyright watermark", "watermark tool"],
  "hero": _hero("watermark-images-to-protect-your-work", "A photo with an elegant semi-transparent watermark overlay"),
  "images": _imgs("watermark-images-to-protect-your-work", [
    (2, "A subtle watermark pattern tiled across an image", "A repeated watermark is harder to crop out than a single corner mark."),
    (3, "A photograph with a protective shield motif over it", "A watermark deters casual copying and marks the work as yours."),
    (4, "An unmarked image beside a watermarked version", "A good watermark protects the image without ruining how it looks."),
  ]),
  "faq": [
   ("What is a watermark and why use one?", "A watermark is text or a logo laid over an image, usually semi-transparent, to show who owns it. It deters casual copying, credits you when the image is shared, and makes stolen use easy to spot, which protects photographers and creators."),
   ("How do I watermark a photo?", "Open the image in a watermark tool, add your text or logo, set its position, size and transparency, then export. Our tool does this in your browser so the photo is never uploaded, keeping your original private while you protect it."),
   ("Where should I place a watermark?", "A corner is least intrusive but easy to crop off. For stronger protection, place it over part of the subject or tile it faintly across the whole image, balancing deterrence against keeping the photo pleasant to look at."),
   ("Does a watermark fully prevent image theft?", "No. A determined person can crop or edit one out, so treat it as a deterrent and a credit, not absolute protection. Combine it with lower-resolution public versions and your copyright notice for better coverage."),
   ("Can I watermark many images at once?", "Yes, some tools support batch watermarking so you can apply the same mark to a whole set in one go, which saves time when protecting a gallery or a product catalogue."),
  ],
 },

 "why-format-your-html": {
  "modified": MOD,
  "keywords": ["why format your html", "format html online", "html beautifier", "indent html", "clean up html code", "html formatter", "minify vs format html", "readable html", "prettify html"],
  "hero": _hero("why-format-your-html", "Tangled code transforming into clean, neatly indented code"),
  "images": _imgs("why-format-your-html", [
    (2, "Two code blocks side by side, one tangled and one tidy", "Consistent indentation shows the structure of the page at a glance."),
    (3, "A code editor displaying neatly indented, nested structure", "Well-formatted HTML is far easier to read, debug and hand to someone else."),
    (4, "Minified single-line code expanding into formatted lines", "Formatting is for humans; minifying is for shipping to the browser."),
  ]),
  "faq": [
   ("Why should I format my HTML?", "Formatting adds consistent indentation and line breaks so the structure of the page is obvious. It makes the code far easier to read, debug and maintain, helps you spot unclosed tags, and makes collaborating with others much smoother."),
   ("What is the difference between formatting and minifying HTML?", "Formatting (or beautifying) adds spacing and indentation to make code readable for humans. Minifying strips all of that out to make the file as small as possible for fast loading. You format while developing and minify what you ship."),
   ("Does formatted HTML affect website speed?", "The extra spaces and line breaks add a tiny amount to the file size, which is negligible once the server compresses the response. For production you can minify, but formatted source has no meaningful impact on real-world speed."),
   ("How do I format messy HTML?", "Paste it into an HTML formatter and it re-indents the tags and nests them correctly. Our formatter does this in your browser with nothing uploaded, turning a tangled block into clean, readable code you can copy back."),
   ("Will formatting change how my page works?", "No. A proper formatter only changes whitespace and indentation, not the tags or content, so the rendered page looks and behaves exactly the same. It simply makes the underlying code easier for people to work with."),
  ],
 },

}
