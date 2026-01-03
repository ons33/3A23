import os
import re
import sys
import traceback

# ===========================
# CONFIGURATION
# ===========================
CODE_DIR = "src"  # Path to your project code
EXTENSIONS = ('.js', '.ts', '.py', '.java', '.cs', '.php', '.rb', '.go', '.cpp', '.c', '.swift', '.kt', '.rs')

THRESHOLD = 50   # Score threshold to consider AI-generated
FAIL_CI = True   # If True, exit(1) when score < threshold

REPORT_FILE = "ai_detection_report.txt"  # Save report

# ===========================
# REGEX PATTERNS
# ===========================
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
hardcoded_string_pattern = re.compile(r'["\'].*?["\']')
try_catch_pattern = re.compile(r'\btry\b|\bcatch\b|\bfinally\b', flags=re.IGNORECASE)  # Error handling

# ===========================
# COUNTERS
# ===========================
french_strings = 0
emoji_count = 0
informal_comments = 0
validation_count = 0
todo_count = 0
naming_issues = 0
hardcoded_strings = 0
blank_lines = 0
error_handling_count = 0

# ===========================
# ERROR HANDLING
# ===========================
try:
    for root, dirs, files in os.walk(CODE_DIR):
        for file in files:
            if file.endswith(EXTENSIONS):
                path = os.path.join(root, file)
                try:
                    with open(path, encoding='utf-8', errors='ignore') as f:
                        code = f.read()
                except Exception as e:
                    print(f"Warning: Could not read {path}: {e}")
                    continue

                # French strings
                french_strings += len(french_string_pattern.findall(code))

                # Emoji usage
                emoji_count += len(emoji_pattern.findall(code))

                # Comments
                comments = comment_pattern.findall(code)
                informal_comments += sum(1 for c in comments if any(word in c.lower() for word in ['default', 'temp', 'test']))
                todo_count += len(todo_pattern.findall(code))

                # Validation checks
                validation_count += len(validation_pattern.findall(code))

                # Naming inconsistencies
                camel_case_names = naming_pattern.findall(code)
                naming_issues += sum(1 for name in camel_case_names if not name[0].islower())

                # Hardcoded strings
                hardcoded_strings += len(hardcoded_string_pattern.findall(code))

                # Blank lines
                blank_lines += sum(1 for line in code.splitlines() if line.strip() == '')

                # Error Handling Pattern
                error_handling_count += len(try_catch_pattern.findall(code))

    # ===========================
    # HEURISTIC SCORING
    # ===========================
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

    # ===========================
    # GENERATE REPORT
    # ===========================
    report_lines = [
        "=== AI Code Detection Report ===",
        f"AI Likelihood: {score}%",
        f"French strings: {french_strings}",
        f"Emoji usage in comments: {emoji_count}",
        f"Informal comments (default/temp/test): {informal_comments}",
        f"Validation checks (form.isValid or required): {validation_count}",
        f"TODO/FIXME/TEMP count: {todo_count}",
        f"Inconsistent naming issues: {naming_issues}",
        f"Hardcoded strings: {hardcoded_strings}",
        f"Blank lines formatting issues: {blank_lines}",
        f"Error Handling Pattern (try/catch/finally): {error_handling_count}",
        ""
    ]

    if score < THRESHOLD:
        report_lines.append("Overall assessment: The code exhibits multiple human-written characteristics including emoji comments, inconsistent naming conventions, mixed language usage, placeholder code, formatting irregularities, and error handling patterns. These traits strongly suggest human authorship rather than AI generation.")
        report_lines.append("⚠️ Code may be AI-generated. Failing CI." if FAIL_CI else "⚠️ Code may be AI-generated. CI continues.")
    else:
        report_lines.append("Overall assessment: The code may exhibit characteristics similar to AI-generated code (uniform style, fewer placeholders, consistent naming, minimal try/catch).")

    report_text = "\n".join(report_lines)
    print(report_text)

    # Save report
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(report_text)

    # ===========================
    # FAIL CI IF NEEDED
    # ===========================
    if FAIL_CI and score < THRESHOLD:
        exit(1)

except Exception as e:
    print("\nUnexpected error occurred during AI detection:")
    traceback.print_exc()
    exit(1)
