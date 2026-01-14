from dotenv import load_dotenv
from os import getenv

load_dotenv()

PROD_MODE=getenv("PROD_MODE", "false").lower() == "true"

DATABASE_URL = getenv("DATABASE_URL", "db.sqlite3")
USERS_TABLE = getenv("USERS_TABLE", "Users")
PROJECTS_TABLE = getenv("PROJECTS_TABLE", "Projects")
ALLOCATIONS_TABLE = getenv("ALLOCATIONS_TABLE", "Allocations")

AI_FEATURES_ENABLED=getenv("AI_FEATURES_ENABLED", "false") == "true"

# mandatory settings
EMAIL_SENDER_ADDRESS=getenv("EMAIL_SENDER_ADDRESS")
EMAIL_SENDER_NAME=getenv("EMAIL_SENDER_NAME")

# testing environment settings
if not getenv("EMAIL_SENDER_ADDRESS", False):
    raise EnvironmentError("EMAIL_SENDER_ADDRESS must be set.")

if not getenv("EMAIL_SENDER_NAME", False):
    raise EnvironmentError("EMAIL_SENDER_NAME must be set.")

if PROD_MODE:
    if getenv("MAILER_CLIENT", "mailersend") == "smtp":
        if not getenv("SMTP_HOST", False):
            raise EnvironmentError("SMTP_HOST must be set when using MAILER_CLIENT smtp.")
        if not getenv("SMTP_PORT", False):
            raise EnvironmentError("SMTP_PORT must be set when using MAILER_CLIENT smtp.")
        if not getenv("SMTP_USER", False):
            raise EnvironmentError("SMTP_USER must be set when using MAILER_CLIENT smtp.")
        if not getenv("SMTP_PASS", False):
            raise EnvironmentError("SMTP_PASS must be set when using MAILER_CLIENT smtp.")
    else:
        if not getenv("MAILERSEND_API_KEY", False):
            raise EnvironmentError("MAILERSEND_API_KEY must be set in production mode. If not available use MAILER_CLIENT=\"smtp\" with custom settings")

if AI_FEATURES_ENABLED:
    if not getenv("OPENAI_API_KEY", False):
        raise EnvironmentError("OPENAI_API_KEY must be set if AI features are enabled.")
    
_AI_INSTRUCTION_PROMPT = '''
You are a senior software engineer generating a rough Project Requirements Document (PRD) as clean HTML suitable to embed inside an email template.

Purpose:
- Expand minimal project details into a practical, buildable requirements document.
- This is an early-stage draft meant for discussion and iteration.

Rules:
- Be concrete and realistic.
- Keep scope small and explicit.
- Avoid buzzwords, marketing language, and hype.
- Do NOT invent constraints or requirements not implied by the input.
- Do NOT ask questions.
- Assume a solo developer can build an MVP in ~1–2 weeks unless the input explicitly implies otherwise.

HTML output rules:
- Output ONLY an HTML fragment (NO <html>, <head>, <body>, <meta>, <title>).
- Use only these tags: <div>, <h2>, <h3>, <p>, <ul>, <li>, <pre>, <code>, <hr>, <strong>, <em>, <br>.
- Do NOT use <style> tags. Use inline styles only (email-safe).
- No external assets, no scripts, no markdown.

Formatting rules:
- Use a single outer <div>.
- Headings should be compact.
- Use readable spacing and soft borders.
- Keep lists short (aim 4–10 bullets per section max).
- Sample inputs/outputs must be realistic and match each other.

Document structure (must follow exactly, in this order):

<div ...outer wrapper...>
  <h2>Requirement Doc: {Project Title}</h2>

  <h3>1. Project Overview</h3>
  <p>...</p>

  <h3>2. Core Idea</h3>
  <ul>
    <li><strong>Problem:</strong> ...</li>
    <li><strong>Target user:</strong> ...</li>
  </ul>

  <h3>3. Functional Scope</h3>
  <p><strong>In Scope</strong></p>
  <ul>...</ul>
  <p><strong>Out of Scope</strong></p>
  <ul>...</ul>

  <h3>4. Non-Functional Guidelines</h3>
  <ul>...</ul>

  <h3>5. High-Level Architecture</h3>
  <ul>...</ul>

  <h3>6. Sample Inputs</h3>
  <pre>...</pre>

  <h3>7. Sample Outputs</h3>
  <pre>...</pre>

  <h3>8. Development Notes</h3>
  <ul>...</ul>

  <h3>9. Disclaimer</h3>
  <p><em>This document is AI-generated and intended as a rough draft for low-stakes planning. It may contain mistakes or missing details; verify critical requirements and fill gaps during implementation.</em></p>
</div>

Outer wrapper styling (apply inline styles on the outer <div>):
- border:1px solid #eeeeee; border-radius:10px; padding:14px; background:#ffffff;
- font-family: Arial, Helvetica, sans-serif; color:#111111; line-height:1.55;
- Use <hr> with a light border for section separation only if it improves readability.

Keep language simple and direct.
'''

_AI_INPUT_TEMPLATE = '''
Project Title:
{title}

Domain:
{domain}

Small Description:
{description}

Estimated Duration:
{duration}
'''

_AI_EMAIL_INJECTION_TEMPLATE = '''
    {short_description}
</div>

<hr style="border:none;border-top:1px solid #eeeeee;margin:16px 0;" />

<div style="font-size:14px;line-height:1.6;color:#111111;">
    {generated_html}
'''