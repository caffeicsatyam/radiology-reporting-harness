"""Visual diff generator comparing template content against the generated report.
Renders clean HTML/CSS components with field-level preservation badges and token highlighting.
"""

import html
import re
from .scorer import extract_report_sections, parse_labeled_fields, normalize_for_score


def generate_field_diff_html(template: str, report: str) -> str:
    """Generate an interactive, beautifully styled HTML card grid showing field-level changes."""
    tpl_f, tpl_i = extract_report_sections(template)
    rep_f, rep_i = extract_report_sections(report)

    tpl_fields = parse_labeled_fields(tpl_f)
    rep_fields = parse_labeled_fields(rep_f)

    all_fields = list(tpl_fields.keys())
    for f in rep_fields.keys():
        if f not in all_fields:
            all_fields.append(f)

    html_parts = [
        """
        <div class="diff-container" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
            <div style="display: flex; gap: 12px; margin-bottom: 16px; flex-wrap: wrap;">
                <span class="badge badge-preserved" style="background: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.3); padding: 4px 10px; border-radius: 9999px; font-size: 12px; font-weight: 600;">
                    ✓ Preserved Normal
                </span>
                <span class="badge badge-modified" style="background: rgba(59, 130, 246, 0.15); color: #3b82f6; border: 1px solid rgba(59, 130, 246, 0.3); padding: 4px 10px; border-radius: 9999px; font-size: 12px; font-weight: 600;">
                    ⚡ Dictation Incorporated
                </span>
                <span class="badge badge-invented" style="background: rgba(239, 68, 68, 0.15); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.3); padding: 4px 10px; border-radius: 9999px; font-size: 12px; font-weight: 600;">
                    ⚠️ Extra / Hallucinated Field
                </span>
            </div>
            <div class="fields-grid" style="display: flex; flex-direction: column; gap: 12px;">
        """
    ]

    for field in all_fields:
        tpl_val = tpl_fields.get(field, "")
        rep_val = rep_fields.get(field, "")

        if field not in tpl_fields:
            status = "invented"
            badge_text = "⚠️ Invented Field"
            border_color = "rgba(239, 68, 68, 0.4)"
            bg_color = "rgba(239, 68, 68, 0.05)"
        elif field not in rep_fields:
            status = "omitted"
            badge_text = "❌ Omitted Field"
            border_color = "rgba(245, 158, 11, 0.4)"
            bg_color = "rgba(245, 158, 11, 0.05)"
        elif normalize_for_score(tpl_val) == normalize_for_score(rep_val):
            status = "preserved"
            badge_text = "✓ Preserved Normal"
            border_color = "rgba(16, 185, 129, 0.3)"
            bg_color = "rgba(16, 185, 129, 0.04)"
        else:
            status = "modified"
            badge_text = "⚡ Finding Updated"
            border_color = "rgba(59, 130, 246, 0.4)"
            bg_color = "rgba(59, 130, 246, 0.06)"

        field_escaped = html.escape(field)
        tpl_escaped = html.escape(tpl_val) if tpl_val else "<span style='color: #6b7280; font-style: italic;'>None</span>"
        rep_escaped = html.escape(rep_val) if rep_val else "<span style='color: #ef4444; font-style: italic;'>Missing</span>"

        if status == "modified":
            content_html = f"""
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; font-size: 13px; line-height: 1.5;">
                    <div style="background: rgba(0,0,0,0.2); padding: 8px 12px; border-radius: 6px; border-left: 3px solid #ef4444;">
                        <div style="font-size: 11px; text-transform: uppercase; color: #9ca3af; font-weight: 600; margin-bottom: 4px;">Original Template Statement:</div>
                        <div style="color: #d1d5db; text-decoration: line-through; opacity: 0.85;">{tpl_escaped}</div>
                    </div>
                    <div style="background: rgba(0,0,0,0.2); padding: 8px 12px; border-radius: 6px; border-left: 3px solid #3b82f6;">
                        <div style="font-size: 11px; text-transform: uppercase; color: #60a5fa; font-weight: 600; margin-bottom: 4px;">Fine-Tuned Model Output:</div>
                        <div style="color: #ffffff; font-weight: 500;">{rep_escaped}</div>
                    </div>
                </div>
            """
        elif status == "preserved":
            content_html = f"""
                <div style="font-size: 13px; color: #9ca3af; padding: 4px 8px; line-height: 1.5;">
                    <span style="color: #d1d5db;">{rep_escaped}</span>
                </div>
            """
        else:
            content_html = f"""
                <div style="font-size: 13px; color: #ffffff; padding: 4px 8px; line-height: 1.5;">
                    {rep_escaped}
                </div>
            """

        card_html = f"""
            <div style="background: {bg_color}; border: 1px solid {border_color}; border-radius: 8px; padding: 12px 14px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="font-weight: 700; font-size: 13px; color: #f3f4f6; letter-spacing: 0.5px;">{field_escaped}</span>
                    <span style="font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 4px; background: rgba(0,0,0,0.3);">{badge_text}</span>
                </div>
                {content_html}
            </div>
        """
        html_parts.append(card_html)

    # Add IMPRESSION section card
    tpl_imp_escaped = html.escape(tpl_i) if tpl_i else "<span style='color: #6b7280; font-style: italic;'>None</span>"
    rep_imp_escaped = html.escape(rep_i) if rep_i else "<span style='color: #ef4444; font-style: italic;'>Missing</span>"

    html_parts.append(f"""
            <div style="margin-top: 10px; background: rgba(99, 102, 241, 0.08); border: 1px solid rgba(99, 102, 241, 0.4); border-radius: 8px; padding: 12px 14px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="font-weight: 700; font-size: 13px; color: #a5b4fc; letter-spacing: 0.5px;">CLINICAL IMPRESSION</span>
                    <span style="font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 4px; background: rgba(99, 102, 241, 0.2); color: #c7d2fe;">Synthesized Summary</span>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; font-size: 13px; line-height: 1.5;">
                    <div style="background: rgba(0,0,0,0.2); padding: 8px 12px; border-radius: 6px; border-left: 3px solid #6b7280;">
                        <div style="font-size: 11px; text-transform: uppercase; color: #9ca3af; font-weight: 600; margin-bottom: 4px;">Template Baseline:</div>
                        <div style="color: #9ca3af;">{tpl_imp_escaped}</div>
                    </div>
                    <div style="background: rgba(0,0,0,0.2); padding: 8px 12px; border-radius: 6px; border-left: 3px solid #818cf8;">
                        <div style="font-size: 11px; text-transform: uppercase; color: #a5b4fc; font-weight: 600; margin-bottom: 4px;">Generated Clinical Impression:</div>
                        <div style="color: #ffffff; font-weight: 600;">{rep_imp_escaped}</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """)

    return "".join(html_parts)
