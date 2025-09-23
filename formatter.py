# perfume-bot/formatter.py
# Formatting text responses.

def welcome_text():
    return (
        "Hello! 👋 I can help you find an affordable alternative to your favorite perfume.\n\n"
        "Typically, the production cost of an expensive perfume is less than 10%. The rest is marketing, packaging, and shipping."
        "Good news: we've compiled a database of the best clones. They smell just like the original—for a tiny fraction of the price.\n\n"
        "Try sending the original perfume name in the format: 'Brand Name', for example: Dior Sauvage."
    )

def format_response(original, copies):
    lines = []
    header = f"{original['brand']} {original['name']}".strip()
    if header:
        lines.append(header)
    lines.append("---------------------")
    
    if not copies:
        lines.append("Couldn't find what you were looking for. Please try again. 😅")
    else:
        for c in copies:
            brand, name = c["brand"], c["name"]
            if brand and name:
                lines.append(f"▪️ {brand}: {name}")
            elif name:
                lines.append(f"▪️ {name}")
            elif brand:
                lines.append(f"▪️ {brand}")

    lines.append("---------------------")
    lines.append("You did great!")
    lines.append("I recommend looking for these scents in your favorite perfume store or online marketplace.")
    return "\n".join(lines)
