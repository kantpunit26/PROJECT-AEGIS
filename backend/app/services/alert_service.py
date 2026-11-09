import requests
from typing import Dict, Any, Optional
from app.core.config import settings

class SurveillanceAlertService:
    """Dispatches real-time outbreak threshold alerts to Slack and Discord webhooks."""

    @staticmethod
    def send_slack_notification(title: str, message: str, severity: str = "HIGH") -> bool:
        webhook_url = settings.SLACK_WEBHOOK_URL
        if not webhook_url:
            return False

        color_map = {
            "INFO": "#2E8B57",
            "WARNING": "#FF8C00",
            "HIGH": "#8B0000",
            "CRITICAL": "#FF0000"
        }
        payload = {
            "attachments": [
                {
                    "color": color_map.get(severity, "#8B0000"),
                    "title": f"🚨 [AEGIS ALERT - {severity}] {title}",
                    "text": message,
                    "footer": "PROJECT AEGIS Genomic Intelligence Engine",
                }
            ]
        }
        try:
            resp = requests.post(webhook_url, json=payload, timeout=5)
            return resp.status_code == 200
        except Exception:
            return False

    @staticmethod
    def send_discord_notification(title: str, message: str, severity: str = "HIGH") -> bool:
        webhook_url = settings.DISCORD_WEBHOOK_URL
        if not webhook_url:
            return False

        payload = {
            "content": f"**[AEGIS SURVEILLANCE NOTIFICATION]**\n**{title}**\n{message}"
        }
        try:
            resp = requests.post(webhook_url, json=payload, timeout=5)
            return resp.status_code in (200, 204)
        except Exception:
            return False

alert_service = SurveillanceAlertService()

