from typing import List, Dict, Any


def _normalise_key(name: str) -> str:
    """Return a lowercase, underscore variant of a column name for fuzzy matching."""
    return name.strip().lower().replace(" ", "_")


def generate_dco_feed(
    audience_strategy: List[Dict[str, Any]],
    asset_list: List[Dict[str, Any]],
    media_plan_rows: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Generate a simple DCO feed that connects strategy + concepts + media.

    This deliberately stays schema-light so we can evolve the upstream data
    structures (AudienceStrategy, AssetList, MediaPlanRows) without having to
    constantly rework the core loop.

    Expected (but not strictly required) shapes:
      - audience_strategy: [{ "audience": "Prospects", "headline": "..." }, ...]
      - asset_list:       [{ "audience": "Prospects", "image_url": "...", "exit_url": "..." }, ...]
      - media_plan_rows:  [{ "Placement ID": "123", "Target Audience": "Prospects", ... }, ...]

    The function:
      - walks each media row
      - finds a matching strategy row by audience -> headline
      - finds a matching asset row by audience -> image_url / exit_url
      - returns rows shaped like the Toyota-style feed:
          { "Unique_ID", "Headline", "Image_URL", "Exit_URL" }
    """

    # Build simple lookup tables keyed by normalised audience name
    strategy_by_audience: Dict[str, Dict[str, Any]] = {}
    for s in audience_strategy:
        audience = s.get("audience") or s.get("Audience") or s.get("target_audience")
        if not isinstance(audience, str):
            continue
        strategy_by_audience[_normalise_key(audience)] = s

    assets_by_audience: Dict[str, Dict[str, Any]] = {}
    for a in asset_list:
        audience = a.get("audience") or a.get("Audience") or a.get("target_audience")
        if not isinstance(audience, str):
            continue
        assets_by_audience[_normalise_key(audience)] = a

    feed: List[Dict[str, Any]] = []

    for idx, row in enumerate(media_plan_rows):
        # Try a couple of common audience column names
        audience = (
            row.get("Target Audience")
            or row.get("Audience")
            or row.get("audience")
            or row.get("Segment")
            or row.get("segment")
        )

        norm_aud = _normalise_key(audience) if isinstance(audience, str) else ""

        strategy = strategy_by_audience.get(norm_aud, {})
        asset = assets_by_audience.get(norm_aud, {})

        headline = (
            strategy.get("headline")
            or strategy.get("Headline")
            or strategy.get("message")
            or strategy.get("Message")
            or ""
        )

        image_url = (
            asset.get("image_url")
            or asset.get("Image_URL")
            or asset.get("asset_url")
            or asset.get("Asset_URL")
            or ""
        )

        exit_url = (
            asset.get("exit_url")
            or asset.get("Exit_URL")
            or asset.get("click_url")
            or asset.get("Click_URL")
            or ""
        )

        unique_id = (
            row.get("Unique_ID")
            or row.get("Placement ID")
            or row.get("placement_id")
            or f"ROW-{idx+1}"
        )

        feed.append(
            {
                "Unique_ID": str(unique_id),
                "Headline": str(headline) if headline is not None else "",
                "Image_URL": str(image_url) if image_url is not None else "",
                "Exit_URL": str(exit_url) if exit_url is not None else "",
            }
        )

    return feed


