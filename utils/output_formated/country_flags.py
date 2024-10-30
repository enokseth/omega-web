def get_flag(country):
    flags = {
        "France": "🇫🇷",
        "India": "🇮🇳",
        "Poland": "🇵🇱",
        "Hungary": "🇭🇺",
        "United States": "🇺🇸",
        "Russian Federation": "🇷🇺",
    }
    return flags.get(country, "🌍")
