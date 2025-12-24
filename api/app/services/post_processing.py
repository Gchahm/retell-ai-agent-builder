from app.services.call_analysis import (
    EMERGENCY_FLOW_FIELD_NAMES,
    NORMAL_FLOW_FIELD_NAMES,
)


class PostProcessingService:
    """Service for extracting structured data from Retell call analysis."""

    def __init__(self):
        pass

    def extract_structured_data(self, call_data: dict) -> dict:
        """
        Extract structured data from Retell's call analysis.

        Returns different fields based on call_outcome:
        - "In-Transit Update" or "Arrival Confirmation": Normal flow fields
        - "Emergency": Emergency flow fields

        Args:
            call_data: The call data from Retell webhook

        Returns:
            Dictionary with structured data based on outcome type
        """
        call_analysis = call_data.get("call_analysis", {})
        custom_data = call_analysis.get("custom_analysis_data", {})

        # Always include Retell's built-in analysis and the required call_outcome
        call_outcome = custom_data.get("call_outcome")

        result = {
            # Retell's built-in analysis fields
            "call_summary": call_analysis.get("call_summary"),
            "call_successful": call_analysis.get("call_successful"),
            "user_sentiment": call_analysis.get("user_sentiment"),
            "in_voicemail": call_analysis.get("in_voicemail"),
            # Required field
            "call_outcome": call_outcome,
        }

        # Add fields based on outcome type using shared field names
        if call_outcome == "Emergency":
            for field_name in EMERGENCY_FLOW_FIELD_NAMES:
                result[field_name] = custom_data.get(field_name)
        else:
            for field_name in NORMAL_FLOW_FIELD_NAMES:
                result[field_name] = custom_data.get(field_name)

        return result
