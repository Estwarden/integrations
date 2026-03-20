#!/usr/bin/env python3
"""EstWarden Telegram Bot — query threat data from Telegram.

Commands:
  /threat  — current threat level + score
  /report  — today's daily report summary
  /narr    — active narrative classifications
  /camps   — detected influence campaigns
  /sub     — subscribe to daily briefings

Usage:
  TELEGRAM_BOT_TOKEN=... python3 bot.py

Requires: pip install python-telegram-bot
"""

import json
import os
import urllib.request

API = "https://estwarden.eu"

def api(path):
    with urllib.request.urlopen(f"{API}{path}", timeout=10) as r:
        return json.loads(r.read())

def threat_text():
    d = api("/api/threat-index")
    emoji = {"GREEN": "🟢", "YELLOW": "🟡", "ORANGE": "🟠", "RED": "🔴"}.get(d.get("level", ""), "⚪")
    return f"{emoji} <b>Baltic Threat Level: {d.get('level', '?')}</b>\nCTI Score: {d.get('score', 0):.1f}/100\nDate: {d.get('date', '?')}"

def report_text():
    d = api("/api/today")
    summary = d.get("summary", "No report yet.")
    level = d.get("threat_level", d.get("level", "?"))
    return f"🛡 <b>Daily Report</b> — {level}\n\n{summary[:500]}\n\n<a href='https://estwarden.eu'>Full report →</a>"

def narratives_text():
    data = api("/api/influence/narratives?days=7")
    items = data if isinstance(data, list) else data.get("narratives", [])
    codes = {"N1": "Russophobia", "N2": "War Panic", "N3": "Aid=Theft", "N4": "Delegitimize", "N5": "Victimhood"}
    text = "📊 <b>Active Narratives</b> (7 days)\n\n"
    for i in items:
        c = i.get("code", "?")
        text += f"  <b>{c}</b> ({codes.get(c, '?')}): {i.get('count', 0)} signals\n"
    return text or "No active narratives."

def campaigns_text():
    data = api("/api/influence/campaigns?days=30")
    items = data if isinstance(data, list) else data.get("campaigns", [])
    text = "🎯 <b>Influence Campaigns</b> (30 days)\n\n"
    for c in items[:5]:
        text += f"• <b>{c.get('name', '?')}</b> [{c.get('severity', '?')}]\n  {c.get('summary', '')[:150]}\n\n"
    return text if items else "No campaigns detected."

# --- Bot setup ---
try:
    from telegram import Update
    from telegram.ext import Application, CommandHandler, ContextTypes

    async def cmd_threat(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(threat_text(), parse_mode="HTML")

    async def cmd_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(report_text(), parse_mode="HTML")

    async def cmd_narr(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(narratives_text(), parse_mode="HTML")

    async def cmd_camps(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(campaigns_text(), parse_mode="HTML")

    async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "🛡 <b>EstWarden Bot</b>\n\n"
            "/threat — current threat level\n"
            "/report — daily report\n"
            "/narr — narrative classifications\n"
            "/camps — influence campaigns\n\n"
            "<a href='https://estwarden.eu'>estwarden.eu</a>",
            parse_mode="HTML"
        )

    def main():
        token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
        if not token:
            print("Set TELEGRAM_BOT_TOKEN"); return
        app = Application.builder().token(token).build()
        app.add_handler(CommandHandler("start", cmd_start))
        app.add_handler(CommandHandler("threat", cmd_threat))
        app.add_handler(CommandHandler("report", cmd_report))
        app.add_handler(CommandHandler("narr", cmd_narr))
        app.add_handler(CommandHandler("camps", cmd_camps))
        print("Bot running...")
        app.run_polling()

    if __name__ == "__main__":
        main()

except ImportError:
    print("Install: pip install python-telegram-bot")
