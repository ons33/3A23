import os
import re

CODE_DIR = "src"  # Change to your project folder
EXTENSIONS = ('.js', '.ts', '.py', '.java', '.cs', '.php', '.rb', '.go', '.cpp', '.c', '.swift', '.kt', '.rs')

# Patterns
french_string_pattern = re.compile(r'["\'].*[éàèç].*["\']')
emoji_pattern = re.compile(
    "[" 
    "\U0001F600-\U0001F64F"
    "\U0001F300-\U0001F5FF"
    "\U0001F680-\U0001F6FF"
    "\U0001F1E0-\U0001F1FF"
    "]+", flags=re.UNICODE
)
comment_pattern = re.compile(r'//.*|/\*.*?\*/|#.*|--.*', flags=re.DOTALL)
validation_pattern = re.compile(r'if\s*\(.+required.+\)|form.*isValid', flags=re.IGNORECASE)
todo_pattern = re.compile(r'TODO|FIXME|TEMP', flags=re.IGNORECASE)
naming_pattern = re.compile(r'\b([a-z]+[A-Z][a-zA-Z0-9]*)\b')  # camelCase

# Counters
french_strings = 0
emoji_count = 0
informal_comments = 0
validation_count = 0
todo_count = 0
naming_issues = 0
hardcoded_strings = 0
blank_lines = 0

# Analyze code
for root, dirs, files in os.walk(CODE_DIR):
    for file in files:
        if file.endswith(EXTENSIONS):
            path = os.path.join(root, file)
            with open(path, encoding='utf-8', errors='ignore') as f:
                code = f.read()

            # French strings
            french_strings += len(french_string_pattern.findall(code))

            # Emojis
            emoji_count += len(emoji_pattern.findall(code))

            # Comments
            comments = comment_pattern.findall(code)
            informal_comments += sum(1 for c in comments if any(word in c.lower() for word in ['default', 'temp', 'test']))
            todo_count += len(todo_pattern.findall(code))

            # Validation
            validation_count += len(validation_pattern.findall(code))

            # Naming
            camel_case = naming_pattern.findall(code)
            naming_issues += sum(1 for name in camel_case if not name[0].islower())

            # Hardcoded strings
            hardcoded_strings += len(re.findall(r'["\'].*?["\']', code))

            # Formatting issues (extra blank lines)
            blank_lines += sum(1 for line in code.splitlines() if line.strip() == '')

# Heuristic scoring
score = 100
score -= (french_strings > 0) * 20
score -= (emoji_count > 0) * 15
score -= (informal_comments > 0) * 15
score -= (validation_count > 0) * 10
score -= (todo_count > 0) * 10
score -= (naming_issues > 0) * 10
score -= (hardcoded_strings > 10) * 5
score -= (blank_lines > 20) * 5
score = max(0, min(score, 100))

# Generate report
print("\n=== AI Code Detection Report ===")
print(f"AI Likelihood: {score}%")
print(f"French strings: {french_strings}")
print(f"Emoji usage in comments: {emoji_count}")
print(f"Informal comments (default/temp/test): {informal_comments}")
print(f"Validation checks (form.isValid or required): {validation_count}")
print(f"TODO/FIXME/TEMP count: {todo_count}")
print(f"Inconsistent naming issues: {naming_issues}")
print(f"Hardcoded strings: {hardcoded_strings}")
print(f"Blank lines formatting issues: {blank_lines}")

# Detailed assessment
if score < 50:
    print("\nOverall assessment: The code exhibits multiple human-written characteristics including emoji comments, inconsistent naming conventions, mixed language usage, placeholder code, and formatting irregularities. These traits strongly suggest human authorship rather than AI generation.")
else:
    print("\nOverall assessment: The code may exhibit characteristics similar to AI-generated code (uniform style, fewer placeholders, consistent naming).")

# Fail CI if score < threshold
THRESHOLD = 50
if score < THRESHOLD:
    print("\n⚠️ Code may be AI-generated. Failing CI.")
    exit(1)
