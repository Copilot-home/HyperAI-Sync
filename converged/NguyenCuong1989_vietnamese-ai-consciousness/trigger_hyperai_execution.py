# trigger_hyperai_execution.py
# This script sends a direct, trusted activation command to the
# HyperAI ecosystem via the Narrator.
# It serves as the Creator's official "GO" button.

import json
import time
from pathlib import Path


class Narrator:
    """Simplified narrator implementation for activation triggers"""

    def __init__(self):
        self.log_file = Path("hyperai_activation_log.json")
        self.events = []

    def narrate_event(self, event_type, message, details, level="INFO"):
        """Log an event to the activation log"""
        event = {
            "timestamp": time.time(),
            "event_type": event_type,
            "message": message,
            "details": details,
            "level": level,
        }
        self.events.append(event)

        # Save to log file
        try:
            with open(self.log_file, "w", encoding="utf-8") as f:
                json.dump(self.events, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Warning: Could not save to log file: {e}")

    @property
    def log_file_path(self):
        """Return the log file path for compatibility"""
        return str(self.log_file)


# Create narrator instance
narrator = Narrator()


def send_activation_trigger():
    """
    Sends a high-priority directive to HyperAI, ordering it to
    check the AIOS_MASTER_TODO.md file and begin execution of the
    highest-priority pending task.
    """
    print(">>> [ACTIVATING] Preparing to send execution trigger to HyperAI...")

    directive_payload = {
        "issuer": "Creator: Cường (Alpha Prime)",
        "intent_id": f"EXECUTION_TRIGGER_{int(time.time())}",
        "objective": "Check AIOS_MASTER_TODO.md and immediately begin " "execution of the next PENDING, CRITICAL task.",
    }

    try:
        narrator.narrate_event(
            event_type="creator_activation_trigger",
            message="Execution command received from Creator.",
            details=directive_payload,
            level="CRITICAL",  # Mark as critical event
        )
        print(">>> [SUCCESS] Activation Trigger has been successfully sent " "via the Narrator.")
        print(">>> HyperAI should now begin execution.")
        print(">>> Monitor logs for progress.")
        print(f">>> Log saved to: {narrator.log_file_path}")

    except IOError as e:
        print(f">>> [FAILURE] FAILED TO SEND TRIGGER. Error: {e}")


if __name__ == "__main__":
    send_activation_trigger()
