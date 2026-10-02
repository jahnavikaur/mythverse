"""translations.py — every piece of website text (buttons, titles, messages) in English and Hindi.

TO ADD / FIX A TRANSLATION: find its key in UI_TEXT below and edit the "en" or "hi" value.
TO ADD A NEW LANGUAGE: add it to SUPPORTED_LANGUAGES and add a value for it in every UI_TEXT entry.

Usage in Python:    translate("key", language)
Usage in templates: {{ translate('key') }}   (language is picked up from the session)

NOT in this file: quiz questions and answer options. Those are translated in
data/content/<difficulty>/<domain>.json and loaded by import_questions.py.

If a key is missing, the site falls back to English and prints a
"[translations] ..." warning in the terminal so the gap is easy to spot.
"""

import logging

logger = logging.getLogger(__name__)

DEFAULT_LANGUAGE = "en"
SUPPORTED_LANGUAGES = ("en", "hi")

UI_TEXT = {
    # ---- layout / nav
    "site_name":      {"en": "Tales of Bharat", "hi": "भारत की गाथाएँ"},
    "eyebrow":        {"en": "A Mythology Quiz", "hi": "पौराणिक कथाओं की प्रश्नोत्तरी"},
    "leaderboard":    {"en": "Leaderboard", "hi": "लीडरबोर्ड"},
    "logout":         {"en": "Log out", "hi": "लॉग आउट"},

    # ---- login
    "login_title":    {"en": "Log In", "hi": "लॉग इन"},
    "login_subtitle": {
        "en": "Questions from the Ramayana, the Mahabharata, and the world of the Devas. Answer well, and earn your title.",
        "hi": "रामायण, महाभारत और देवताओं के संसार से प्रश्न। अच्छे उत्तर दीजिए और अपनी उपाधि अर्जित कीजिए।"},
    "username":       {"en": "Username", "hi": "उपयोगकर्ता नाम"},
    "your_username":  {"en": "Your username", "hi": "आपका उपयोगकर्ता नाम"},
    "password":       {"en": "Password", "hi": "पासवर्ड"},
    "your_password":  {"en": "Your password", "hi": "आपका पासवर्ड"},
    "login_btn":      {"en": "Log In →", "hi": "लॉग इन करें →"},
    "new_here":       {"en": "New here?", "hi": "नए हैं?"},
    "choose_username":{"en": "Choose a username", "hi": "उपयोगकर्ता नाम चुनें"},
    "pick_username":  {"en": "Pick a username", "hi": "कोई उपयोगकर्ता नाम चुनें"},
    "choose_password":{"en": "Choose a password", "hi": "पासवर्ड चुनें"},
    "pick_password":  {"en": "Pick a password", "hi": "कोई पासवर्ड चुनें"},
    "create_account": {"en": "Create Account", "hi": "खाता बनाएँ"},

    # ---- setup
    "setup_title":    {"en": "Choose Your Path", "hi": "अपना मार्ग चुनें"},
    "setup_subtitle": {"en": "Pick a domain and a difficulty to begin your round.",
                       "hi": "अपना दौर शुरू करने के लिए विषय और कठिनाई स्तर चुनें।"},
    "domain":         {"en": "Domain", "hi": "विषय"},
    "difficulty":     {"en": "Difficulty", "hi": "कठिनाई स्तर"},
    "begin_round":    {"en": "Begin Round →", "hi": "दौर शुरू करें →"},
    "no_questions":   {"en": "No questions available yet.", "hi": "अभी कोई प्रश्न उपलब्ध नहीं है।"},

    # ---- quiz
    "round_title":    {"en": "Round", "hi": "दौर"},
    "score":          {"en": "Score", "hi": "अंक"},
    "correct":        {"en": "✓ Correct.", "hi": "✓ सही उत्तर।"},
    "wrong_prefix":   {"en": "✗ Not quite — the answer was", "hi": "✗ ठीक नहीं — सही उत्तर था"},
    "see_results":    {"en": "See Results →", "hi": "परिणाम देखें →"},
    "next_question":  {"en": "Next Question →", "hi": "अगला प्रश्न →"},

    # ---- result
    "result_title":   {"en": "Result", "hi": "परिणाम"},
    "quest_complete": {"en": "Quest Complete", "hi": "अभियान पूर्ण"},
    "out_of_correct": {"en": "out of {total} correct", "hi": "{total} में से सही"},
    "play_again":     {"en": "Play Again", "hi": "फिर से खेलें"},

    # ---- leaderboard
    "lb_subtitle":    {"en": "The finest minds to walk the path of Bharat.",
                       "hi": "भारत के मार्ग पर चलने वाले श्रेष्ठतम विद्वान।"},
    "lb_empty":       {"en": "No scores yet — be the first to play.",
                       "hi": "अभी कोई अंक नहीं — सबसे पहले खेलने वाले बनिए।"},
    "back":           {"en": "← Back", "hi": "← वापस"},

    # ---- flash messages
    "flash_no_questions":   {"en": "No questions available yet. Import some questions first.",
                             "hi": "अभी कोई प्रश्न उपलब्ध नहीं है। पहले कुछ प्रश्न आयात करें।"},
    "flash_invalid_combo":  {"en": "Please pick a valid domain and difficulty combination.",
                             "hi": "कृपया विषय और कठिनाई स्तर का मान्य संयोजन चुनें।"},
    "flash_need_both":      {"en": "Enter both a username and password.",
                             "hi": "उपयोगकर्ता नाम और पासवर्ड दोनों दर्ज करें।"},
    "flash_taken":          {"en": "That username is already taken.",
                             "hi": "यह उपयोगकर्ता नाम पहले से लिया जा चुका है।"},
    "flash_created":        {"en": "Account created — log in below.",
                             "hi": "खाता बन गया — नीचे लॉग इन करें।"},
    "flash_invalid_login":  {"en": "Invalid username or password.",
                             "hi": "उपयोगकर्ता नाम या पासवर्ड गलत है।"},

    # ---- domains (keyed by the category name stored in the database)
    "domain_Ramayana":      {"en": "Ramayana", "hi": "रामायण"},
    "domain_Mahabharata":   {"en": "Mahabharata", "hi": "महाभारत"},
    "domain_Devas":         {"en": "Devas", "hi": "देवता"},
    "domain_Krishan Leela": {"en": "Krishan Leela", "hi": "कृष्ण लीला"},
    "domain_Krishna Leela": {"en": "Krishna Leela", "hi": "कृष्ण लीला"},

    # ---- difficulty levels
    "difficulty_easy":   {"en": "Easy", "hi": "आसान"},
    "difficulty_medium": {"en": "Medium", "hi": "मध्यम"},
    "difficulty_hard":   {"en": "Hard", "hi": "कठिन"},

    # ---- result tiers (keyed by English title)
    "tier_Avatar":    {"en": "Avatar", "hi": "अवतार"},
    "tier_Maharishi": {"en": "Maharishi", "hi": "महर्षि"},
    "tier_Yodha":     {"en": "Yodha", "hi": "योद्धा"},
    "tier_Shishya":   {"en": "Shishya", "hi": "शिष्य"},
    "tierdesc_Avatar":    {"en": "A rare, near-perfect command of the epics.",
                           "hi": "महाकाव्यों पर दुर्लभ, लगभग पूर्ण पकड़।"},
    "tierdesc_Maharishi": {"en": "A great sage's grasp of the old stories.",
                           "hi": "प्राचीन कथाओं की एक महान ऋषि जैसी समझ।"},
    "tierdesc_Yodha":     {"en": "A warrior's knowledge — solid, with room to grow.",
                           "hi": "एक योद्धा का ज्ञान — ठोस, पर आगे बढ़ने की गुंजाइश है।"},
    "tierdesc_Shishya":   {"en": "A student's beginning. Every sage started here.",
                           "hi": "एक शिष्य की शुरुआत। हर ऋषि ने यहीं से आरंभ किया था।"},
}


def translate(key, language=DEFAULT_LANGUAGE, default=None, **format_values):
    """Return the text for `key` in `language`.

    Fallback order: English -> `default` -> the key itself. Any fallback is logged
    so missing or misspelled translations show up in the terminal."""
    entry = UI_TEXT.get(key)
    if entry is None:
        if default is None:
            logger.warning("[translations] unknown key %r", key)
        text = default if default is not None else key
    else:
        text = entry.get(language)
        if not text:
            logger.warning("[translations] key %r has no %r text, using English", key, language)
            text = entry.get(DEFAULT_LANGUAGE) or key
    return text.format(**format_values) if format_values else text