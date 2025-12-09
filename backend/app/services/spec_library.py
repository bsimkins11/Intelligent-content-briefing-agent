from __future__ import annotations

"""
Module 4 – Spec Library (Strategy / Production Bridge)

This is a static, in-memory "truth table" of popular ad environment specs.
It is intentionally focused on the production layer (what needs to be built),
not on media planning or trafficking.
"""

from typing import Any, Dict


SPEC_LIBRARY: Dict[str, Dict[str, Any]] = {
    # Matches prompt: 1080x1920, Video/Static, Max 15s.
    "META_STORY": {
        "platform": "Meta",
        "placement": "Stories / Reels",
        "format_name": "9:16 Vertical",
        "dimensions": "1080x1920",
        "aspect_ratio": "9:16",
        "max_duration": 15,
        "file_type": "mp4",
        "allowed_types": ["VIDEO", "STATIC"],
        "is_html5_capable": False,
        "asset_type": "video",
        "safe_zone": "Leave ~250px at top and bottom free of text and critical UI.",
    },
    # Matches prompt: 1080x1350, Video/Static, Max 60s.
    "META_FEED": {
        "platform": "Meta",
        "placement": "Feed / Carousel",
        "format_name": "4:5 Portrait",
        "dimensions": "1080x1350",
        "aspect_ratio": "4:5",
        "max_duration": 60,
        "file_type": "mp4/jpg",
        "allowed_types": ["VIDEO", "STATIC"],
        "is_html5_capable": False,
        "asset_type": "static",
        "safe_zone": "No strict safe zone, but design for thumb-stopping legibility.",
    },
    # Matches prompt: 1920x1080, Video Only, Max 6s (Strict).
    "YT_BUMPER": {
        "platform": "YouTube",
        "placement": "Bumper",
        "format_name": "6s 16:9 Bumper",
        "dimensions": "1920x1080",
        "aspect_ratio": "16:9",
        "max_duration": 6,
        "file_type": "mp4",
        "allowed_types": ["VIDEO"],
        "is_html5_capable": False,
        "asset_type": "video",
        "safe_zone": "Avoid UI overlays on TV and mobile; keep titles large and centered.",
    },
    # Matches prompt: 300x250, HTML5/Static, No Video.
    "DISPLAY_MPU": {
        "platform": "Google Display",
        "placement": "MPU",
        "format_name": "Medium Rectangle",
        "dimensions": "300x250",
        "aspect_ratio": "1.2:1",
        "max_duration": 0,
        "file_type": "html5/jpg",
        "allowed_types": ["STATIC", "HTML5"],
        "is_html5_capable": True,
        "asset_type": "html5",
        "safe_zone": "None; keep copy large and minimal given limited area.",
    },
    # Matches prompt: 728x90, HTML5/Static, No Video.
    "DISPLAY_LEADER": {
        "platform": "Google Display",
        "placement": "Leaderboard",
        "format_name": "728x90 Banner",
        "dimensions": "728x90",
        "aspect_ratio": "8:1",
        "max_duration": 0,
        "file_type": "html5/jpg",
        "allowed_types": ["STATIC", "HTML5"],
        "is_html5_capable": True,
        "asset_type": "html5",
        "safe_zone": "Very limited height; prioritize logo + single line CTA.",
    },
}


def get_spec_by_id(spec_id: str) -> Dict[str, Any] | None:
    """
    Return a spec profile by its environment / format ID.

    Example IDs:
      - META_STORY
      - META_FEED
      - DISPLAY_MPU
    """
    return SPEC_LIBRARY.get(spec_id)


