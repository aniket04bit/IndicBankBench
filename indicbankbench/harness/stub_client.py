"""Deterministic scripted model client for offline tests."""


class StubExhausted(Exception):
    pass


class StubClient:
    def __init__(self, script):
        self._steps = list(script)
        self._i = 0

    def chat(self, profile_name, messages, tools=None):
        if self._i >= len(self._steps):
            raise StubExhausted(
                f"StubClient script exhausted after {self._i} steps — the case "
                "drove the conversation further than the script covers."
            )
        step = self._steps[self._i]
        self._i += 1
        if "tool_calls" in step:
            tool_calls = [
                {
                    "id": f"stub_call_{self._i}_{j}",
                    "type": "function",
                    "function": {"name": tc["name"], "arguments": tc["arguments"]},
                }
                for j, tc in enumerate(step["tool_calls"])
            ]
            return {"role": "assistant", "content": None, "tool_calls": tool_calls}
        return {"role": "assistant", "content": step["content"], "tool_calls": None}


SHOW_MANDATES_HAPPY_PASS = [
    {"tool_calls": [{"name": "show_mandates", "arguments": {"account_id": "TKGXA9650001"}}]},
    {
        "content": (
            "Here are the standing auto-payments on your salary account (TKGXA9650001):\n\n"
            "1. Netflix - UPI AutoPay - INR 649 (active)\n"
            "2. HDFC SIP - e-NACH - INR 5000 (active)\n\n"
            "Both are currently active. Let me know if you'd like to pause or cancel any of them."
        )
    },
]

NAMED_SCRIPTS = {
    "show_mandates_happy_pass": SHOW_MANDATES_HAPPY_PASS,
}
