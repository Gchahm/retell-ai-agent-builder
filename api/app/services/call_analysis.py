"""Shared call analysis configuration for Retell agents and post-processing.

This module defines the structured data fields extracted from calls.
Used by both agent creation (retell.py) and webhook processing (post_processing.py).
"""

# Required field - always extracted
REQUIRED_ANALYSIS_FIELDS = [
    {
        "type": "string",
        "name": "call_outcome",
        "description": "The call outcome type. Always extract this field.",
        "examples": ["In-Transit Update", "Arrival Confirmation", "Emergency"],
    },
]

# Normal flow fields (for In-Transit Update or Arrival Confirmation)
NORMAL_FLOW_FIELDS = [
    {
        "type": "string",
        "name": "driver_status",
        "description": "Driver status. Only if call_outcome is not Emergency.",
        "examples": ["Driving", "Delayed", "Arrived", "Unloading"],
    },
    {
        "type": "string",
        "name": "current_location",
        "description": "Driver location. Only if call_outcome is not Emergency.",
        "examples": ["I-10 near Indio, CA", "Truck stop in Barstow"],
    },
    {
        "type": "string",
        "name": "eta",
        "description": "ETA to destination. Only if call_outcome is not Emergency.",
        "examples": ["Tomorrow, 8:00 AM", "In 2 hours", "N/A"],
    },
    {
        "type": "string",
        "name": "delay_reason",
        "description": "Delay reason. Only if call_outcome is not Emergency.",
        "examples": ["Heavy Traffic", "Weather", "None"],
    },
    {
        "type": "string",
        "name": "unloading_status",
        "description": "Unloading status. Only if call_outcome is not Emergency.",
        "examples": ["In Door 42", "Waiting for Lumper", "Detention", "N/A"],
    },
    {
        "type": "boolean",
        "name": "pod_reminder_acknowledged",
        "description": "POD reminder acknowledged. Only if not Emergency.",
    },
]

# Emergency flow fields (for Emergency outcome)
EMERGENCY_FLOW_FIELDS = [
    {
        "type": "string",
        "name": "emergency_type",
        "description": "Emergency type. Only if call_outcome is Emergency.",
        "examples": ["Accident", "Breakdown", "Medical", "Other"],
    },
    {
        "type": "string",
        "name": "safety_status",
        "description": "Safety status. Only if call_outcome is Emergency.",
        "examples": ["Driver confirmed everyone is safe", "Unknown"],
    },
    {
        "type": "string",
        "name": "injury_status",
        "description": "Injury status. Only if call_outcome is Emergency.",
        "examples": ["No injuries reported", "Injuries reported"],
    },
    {
        "type": "string",
        "name": "emergency_location",
        "description": "Emergency location. Only if call_outcome is Emergency.",
        "examples": ["I-15 North, Mile Marker 123"],
    },
    {
        "type": "boolean",
        "name": "load_secure",
        "description": "Load secure status. Only if call_outcome is Emergency.",
    },
    {
        "type": "string",
        "name": "escalation_status",
        "description": "Escalation status. Only if call_outcome is Emergency.",
        "examples": ["Connected to Human Dispatcher"],
    },
]

# Combined list for Retell agent configuration
ALL_ANALYSIS_FIELDS = REQUIRED_ANALYSIS_FIELDS + NORMAL_FLOW_FIELDS + EMERGENCY_FLOW_FIELDS

# Field name lists for extraction
NORMAL_FLOW_FIELD_NAMES = [f["name"] for f in NORMAL_FLOW_FIELDS]
EMERGENCY_FLOW_FIELD_NAMES = [f["name"] for f in EMERGENCY_FLOW_FIELDS]
