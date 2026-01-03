import re
import os

# Folder containing your code
CODE_DIR = "src"

# Patterns for heuristics
french_string_pattern = re.compile(r'["\'].*[éàèç].*["\']')
emoji_pattern = re.compile(
    "[" 
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F1E0-\U0001F1FF"  # flags
    "]+", flags=re.UNICODE)
comment_pattern = re.compile(r'//.*|/\*.*?\*/', flags=re.DOTALL)
validation_pattern = re.compile(r'if\s*\(.+required.+\)', flags=re.IGNORECASE)

# Initialize counters
french_strings_count = 0
emoji_count = 0
informal_comments_count = 0
validation_count = 0

# Analyze all files recursively
for root, dirs, files in os.walk(CODE_DIR):
    for file in files:
        if file.endswith(('.js', '.ts', '.py', '.java')):  # adjust for your languages
            path = os.path.join(root, file)
            with open(path, encoding='utf-8', errors='ignore') as f:
                code = f.read()

            # French strings
            french_strings_count += len(french_string_pattern.findall(code))

            # Emojis in comments
            emoji_count += len(emoji_pattern.findall(code))

            # Comments
            comments = comment_pattern.findall(code)
            informal_comments = [c for c in comments if any(word in c.lower() for word in ['default', 'temp', 'test'])]
            informal_comments_count += len(informal_comments)

            # Minimal validation
            validation_count += len(validation_pattern.findall(code))

# Heuristic AI likelihood (simple)
ai_likelihood = 100 - (
    (french_strings_count > 0)*30 +
    (emoji_count > 0)*20 +
    (informal_comments_count > 0)*20 +
    (validation_count > 0)*10
)
ai_likelihood = max(0, min(ai_likelihood, 100))

# Print report
print("\nDetection Report")
print("----------------")
print(f"AI Likelihood: {ai_likelihood}%")
print(f"Language Choice: {'French strings detected' if french_strings_count>0 else 'No French strings detected'}")
print(f"Emoji Usage: {emoji_count} emoji(s) found" if emoji_count>0 else "Emoji Usage: None")
print(f"Comment Style: {informal_comments_count} informal comment(s) detected" if informal_comments_count>0 else "Comment Style: None")
print(f"Error Handling Pattern: {validation_count} minimal validation check(s) detected" if validation_count>0 else "Error Handling Pattern: None")

# Exit with code 1 if AI likelihood > threshold (optional for GitHub Actions)
THRESHOLD = 50
if ai_likelihood > THRESHOLD:
    print("\n⚠️ Code may be AI-generated. Failing CI.")
    exit(1)
