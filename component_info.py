"""
component_info.py

A simple Python dictionary holding beginner-friendly explanations for each
PC part. This is imported into app.py.

Why a separate file? It keeps app.py shorter and teaches how one Python
file can import from another.
"""

COMPONENT_INFO = {
    "CPU": {
        "emoji": "🧠",
        "summary": "The CPU is the 'brain' of the computer. It does the thinking "
                    "and math needed to run every program and game.",
        "tip": "More cores = more things it can do at once. Higher GHz = it "
               "thinks faster.",
    },
    "GPU": {
        "emoji": "🎮",
        "summary": "The GPU draws everything you see on screen — games, videos, "
                    "and photo/video effects.",
        "tip": "This matters most for gaming and video editing. For basic "
               "browsing, you often don't need a fancy one.",
    },
    "RAM": {
        "emoji": "📋",
        "summary": "RAM is short-term memory. It holds what your computer is "
                    "actively working on right now.",
        "tip": "Think of RAM like a desk — the bigger it is, the more you can "
               "have open at once without things slowing down.",
    },
    "Motherboard": {
        "emoji": "🔌",
        "summary": "The motherboard connects every other part together — it's "
                    "the foundation everything plugs into.",
        "tip": "It must match your CPU's 'socket' type, or the CPU won't "
               "physically fit.",
    },
    "Storage": {
        "emoji": "💾",
        "summary": "Storage is where your files, games, and programs live "
                    "permanently, even when the PC is off.",
        "tip": "SSDs are fast, HDDs are slow but cheap. Always get an SSD if "
               "you can.",
    },
    "PSU": {
        "emoji": "⚡",
        "summary": "The PSU (Power Supply Unit) takes power from the wall and "
                    "sends the right amount to every part.",
        "tip": "Never buy a cheap PSU — a bad one can damage your other parts.",
    },
    "Case": {
        "emoji": "🖥️",
        "summary": "The case is the box that holds and protects everything, "
                    "while helping keep it cool.",
        "tip": "Good airflow matters more than looks when you're starting out.",
    },
}
