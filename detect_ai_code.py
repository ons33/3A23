import os
import re

# Dossier contenant le code à analyser
CODE_DIR = "src"  # Change selon ton projet

# Patterns pour heuristique
french_string_pattern = re.compile(r'["\'].*[éàèç].*["\']')
emoji_pattern = re.compile(
    "[" 
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F1E0-\U0001F1FF"  # flags
    "]+", flags=re.UNICODE)

# Pattern pour tous les types de commentaires (multi-langues)
comment_pattern = re.compile(
    r'//.*|/\*.*?\*/|#.*|--.*', flags=re.DOTALL
)

# Pattern pour validation minimale
validation_pattern = re.compile(r'if\s*\(.+required.+\)', flags=re.IGNORECASE)

# Extensions de fichiers à analyser
EXTENSIONS = ('.js', '.ts', '.py', '.java', '.cs', '.php', '.rb', '.go', '.cpp', '.c', '.swift', '.kt', '.rs')

# Initialisation des compteurs
french_strings_count = 0
emoji_count = 0
informal_comments_count = 0
validation_count = 0

# Parcours récursif des fichiers
for root, dirs, files in os.walk(CODE_DIR):
    for file in files:
        if file.endswith(EXTENSIONS):
            path = os.path.join(root, file)
            with open(path, encoding='utf-8', errors='ignore') as f:
                code = f.read()

            # Chaînes en français
            french_strings_count += len(french_string_pattern.findall(code))

            # Emojis
            emoji_count += len(emoji_pattern.findall(code))

            # Commentaires
            comments = comment_pattern.findall(code)
            informal_comments = [c for c in comments if any(word in c.lower() for word in ['default', 'temp', 'test'])]
            informal_comments_count += len(informal_comments)

            # Validation minimale
            validation_count += len(validation_pattern.findall(code))

# Calcul heuristique de probabilité AI
ai_likelihood = 100 - (
    (french_strings_count > 0)*30 +
    (emoji_count > 0)*20 +
    (informal_comments_count > 0)*20 +
    (validation_count > 0)*10
)
ai_likelihood = max(0, min(ai_likelihood, 100))

# Affichage du rapport
print("\n=== Detection Report ===")
print(f"AI Likelihood: {ai_likelihood}%")
print(f"Language Choice: {'French strings detected' if french_strings_count>0 else 'No French strings detected'}")
print(f"Emoji Usage: {emoji_count} emoji(s) found" if emoji_count>0 else "Emoji Usage: None")
print(f"Comment Style: {informal_comments_count} informal comment(s) detected" if informal_comments_count>0 else "Comment Style: None")
print(f"Error Handling Pattern: {validation_count} minimal validation check(s) detected" if validation_count>0 else "Error Handling Pattern: None")

# Optionnel : fail CI si AI likelihood > threshold
THRESHOLD = 50
if ai_likelihood > THRESHOLD:
    print("\n⚠️ Code may be AI-generated. Failing CI.")
    exit(1)
