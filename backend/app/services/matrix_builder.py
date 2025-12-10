from __future__ import annotations

"""
Matrix Builder – Many-to-One ProductionJob grouper.

Given a set of selected specs and a creative concept, this service groups
redundant specs (same physical asset) into a single ProductionJob with
multiple DeliveryDestinations.
"""

from typing import Dict, List

from app.schemas.production_matrix import DeliveryDestination, ProductionJob


class MatrixBuilder:
    """
    Group flat spec selections into consolidated ProductionJob tickets.
    """

    def group_specs_by_creative(self, selected_specs: List[Dict], creative_concept: str) -> List[ProductionJob]:
        """
        Input: A list of selected spec dicts (from spec library or UI).

        Expected keys (best-effort, falls back when missing):
          - dimensions (e.g. "1080x1920") or width/height
          - file_type or media_type
          - aspect_ratio or orientation
          - platform_name or platform
          - id (spec identifier)
          - format_name or placement
          - safe_zone_notes or notes or safe_zone
          - max_duration (optional)
        """
        grouped_jobs: Dict[str, ProductionJob] = {}

        for idx, spec in enumerate(selected_specs):
            # Normalise raw spec fields to a common shape
            dimensions = spec.get("dimensions")
            if not dimensions:
                w = spec.get("width")
                h = spec.get("height")
                if w and h:
                    dimensions = f"{w}x{h}"

            file_type = spec.get("file_type") or spec.get("media_type") or "asset"
            aspect_ratio = spec.get("aspect_ratio") or spec.get("orientation") or ""

            platform_name = spec.get("platform_name") or spec.get("platform") or "Unknown"
            spec_id = spec.get("id") or spec.get("spec_id") or f"SPEC-{idx+1}"
            format_name = spec.get("format_name") or spec.get("placement") or ""

            safe_notes = (
                spec.get("safe_zone_notes")
                or spec.get("notes")
                or spec.get("safe_zone")
                or "Standard"
            )
            max_duration = spec.get("max_duration")

            # Group key: physical asset (dimensions + file_type) + concept
            key_dimensions = dimensions or "GENERIC"
            key_file = file_type or "asset"
            group_key = f"{key_dimensions}_{key_file}_{creative_concept}"

            if group_key not in grouped_jobs:
                tech_parts = [key_dimensions]
                if max_duration:
                    tech_parts.append(f"{max_duration}s")
                tech_parts.append(file_type.upper())
                technical_summary = ", ".join(tech_parts)

                grouped_jobs[group_key] = ProductionJob(
                    job_id=f"JOB-{len(grouped_jobs) + 1}",
                    creative_concept=creative_concept,
                    asset_type=f"{aspect_ratio or key_dimensions} {file_type}".strip(),
                    technical_summary=technical_summary,
                    destinations=[],
                )

            grouped_jobs[group_key].destinations.append(
                DeliveryDestination(
                    platform_name=platform_name,
                    spec_id=spec_id,
                    format_name=format_name or key_dimensions,
                    special_notes=safe_notes,
                )
            )

        return list(grouped_jobs.values())


