from retell import Retell
from retell.types import AgentListResponse, AgentResponse

from app.config import get_settings
from app.services.prompts import build_full_prompt

settings = get_settings()

# Default configuration for our agents
DEFAULT_VOICE_ID = "11labs-Adrian"  # Professional male voice
DEFAULT_VOICE_MODEL = "eleven_turbo_v2"  # Fast, high-quality
DEFAULT_LANGUAGE = "en-US"
DEFAULT_START_SPEAKER = "agent"  # Agent initiates the conversation

# Voice tuning
DEFAULT_VOICE_TEMPERATURE = 0.8  # Slightly expressive [0-2]
DEFAULT_VOICE_SPEED = 1.0  # Normal pace [0.5-2]

# Ambient sound for realism
DEFAULT_AMBIENT_SOUND = "call-center"
DEFAULT_AMBIENT_SOUND_VOLUME = 0.3  # Subtle background [0-2]

# Interaction behavior
DEFAULT_RESPONSIVENESS = 0.8  # Fast reactions [0-1]
DEFAULT_INTERRUPTION_SENSITIVITY = 0.6  # Moderately interruptible [0-1]
DEFAULT_BACKCHANNEL_FREQUENCY = 0.5  # Frequent active listening [0-1]
DEFAULT_BACKCHANNEL_WORDS = ["uh-huh", "got it", "okay", "right", "I see", "mm-hmm"]

# Reminder settings for unresponsive drivers
DEFAULT_REMINDER_TRIGGER_MS = 8000  # Prompt after 8s silence
DEFAULT_REMINDER_MAX_COUNT = 2  # Max reminders before giving up

# Call management
DEFAULT_MAX_CALL_DURATION_MS = 300000  # 5 minute max
DEFAULT_END_CALL_AFTER_SILENCE_MS = 15000  # End after 15s silence
DEFAULT_BEGIN_MESSAGE_DELAY_MS = 500  # Half-second natural delay

# Speech recognition - logistics vocabulary
DEFAULT_BOOSTED_KEYWORDS = [
    "POD", "BOL", "lumper", "detention", "ETA",
    "mile marker", "load number", "dispatch",
    "blowout", "breakdown", "accident",
]
DEFAULT_DENOISING_MODE = "noise-cancellation"  # For noisy truck environments


class RetellService:
    """Service for interacting with Retell AI API."""

    def __init__(self):
        self.client = Retell(api_key=settings.retell_api_key)

    def create_agent(self, prompt: str, agent_name: str | None = None) -> AgentResponse:
        """
        Create a new agent with the specified prompt.

        This is a light wrapper around the Retell SDK that:
        1. Creates an LLM with the provided prompt (plus system prefix)
        2. Creates an agent using that LLM with sensible defaults
        3. Configures structured data extraction for logistics tracking

        The prompt provided by the admin is automatically combined with
        system-level instructions for style, emergency handling, and
        difficult situation management.

        Args:
            prompt: The admin's custom prompt (identity and conversation flow)
            agent_name: Optional name for the agent (for internal reference)

        Returns:
            AgentResponse: The created agent from Retell SDK
        """
        # Combine system prompt prefix with admin's custom prompt
        full_prompt = build_full_prompt(prompt)

        # Step 1: Create the LLM with the full prompt
        llm = self.client.llm.create(
            general_prompt=full_prompt,
            start_speaker=DEFAULT_START_SPEAKER,
            # Optional but good defaults
            model="gpt-4o-mini",  # Fast and cost-effective
            begin_message=None,  # Let LLM generate dynamic greeting
            # Add end_call and transfer_call functions
            general_tools=[
                {
                    "type": "end_call",
                    "name": "end_call",
                    "description": (
                        "Use this tool when the user says goodbye, thanks, or indicates "
                        "they want to end the call. Also use this when the conversation "
                        "objective has been completed."
                    ),
                },
            ],
            # Configure structured data extraction for post-call analysis
        )

        # Step 2: Create the agent using the LLM
        agent = self.client.agent.create(
            agent_name=agent_name,
            response_engine={"type": "retell-llm", "llm_id": llm.llm_id},
            # Voice settings
            voice_id=DEFAULT_VOICE_ID,
            voice_model=DEFAULT_VOICE_MODEL,
            voice_temperature=DEFAULT_VOICE_TEMPERATURE,
            voice_speed=DEFAULT_VOICE_SPEED,
            # Ambient sound for realism
            ambient_sound=DEFAULT_AMBIENT_SOUND,
            ambient_sound_volume=DEFAULT_AMBIENT_SOUND_VOLUME,
            # Interaction behavior
            language=DEFAULT_LANGUAGE,
            responsiveness=DEFAULT_RESPONSIVENESS,
            interruption_sensitivity=DEFAULT_INTERRUPTION_SENSITIVITY,
            enable_backchannel=True,
            backchannel_frequency=DEFAULT_BACKCHANNEL_FREQUENCY,
            backchannel_words=DEFAULT_BACKCHANNEL_WORDS,
            # Reminder settings for unresponsive drivers
            reminder_trigger_ms=DEFAULT_REMINDER_TRIGGER_MS,
            reminder_max_count=DEFAULT_REMINDER_MAX_COUNT,
            # Call management
            max_call_duration_ms=DEFAULT_MAX_CALL_DURATION_MS,
            end_call_after_silence_ms=DEFAULT_END_CALL_AFTER_SILENCE_MS,
            begin_message_delay_ms=DEFAULT_BEGIN_MESSAGE_DELAY_MS,
            # Speech recognition
            boosted_keywords=DEFAULT_BOOSTED_KEYWORDS,
            denoising_mode=DEFAULT_DENOISING_MODE,
            # Webhook configuration
            webhook_url=settings.webhook_url,
            # Post-call analysis data extraction for logistics tracking
            post_call_analysis_data=[
                {
                    "type": "string",
                    "name": "call_outcome",
                    "description": "The type of call update provided by the driver.",
                    "examples": ["In-Transit Update", "Arrival Confirmation"],
                },
                {
                    "type": "string",
                    "name": "driver_status",
                    "description": "The current status of the driver.",
                    "examples": ["Driving", "Delayed", "Arrived", "Unloading"],
                },
                {
                    "type": "string",
                    "name": "current_location",
                    "description": "The driver's current location as described.",
                    "examples": ["I-10 near Indio, CA", "Truck stop in Barstow"],
                },
                {
                    "type": "string",
                    "name": "eta",
                    "description": "The estimated time of arrival provided by the driver.",
                    "examples": ["Tomorrow, 8:00 AM", "In 2 hours", "3:30 PM today"],
                },
                {
                    "type": "string",
                    "name": "delay_reason",
                    "description": "The reason for any delay, or None if no delay.",
                    "examples": ["Heavy Traffic", "Weather", "Mechanical Issue", "None"],
                },
                {
                    "type": "string",
                    "name": "unloading_status",
                    "description": "The unloading status at destination, or N/A if not applicable.",
                    "examples": ["In Door 42", "Waiting for Lumper", "Detention", "N/A"],
                },
                {
                    "type": "boolean",
                    "name": "pod_reminder_acknowledged",
                    "description": "Whether the driver acknowledged the POD reminder.",
                },
            ],
        )

        return agent

    def update_agent(
        self,
        agent_id: str,
        prompt: str | None = None,
        agent_name: str | None = None,
    ) -> AgentResponse:
        """
        Update an existing agent.

        This is a light wrapper that allows updating:
        - The prompt (creates a new LLM and updates the agent's response_engine)
        - The agent name

        The prompt provided by the admin is automatically combined with
        system-level instructions for style, emergency handling, and
        difficult situation management.

        Args:
            agent_id: The ID of the agent to update
            prompt: New custom prompt (optional, creates new LLM if provided)
            agent_name: New agent name (optional)

        Returns:
            AgentResponse: The updated agent from Retell SDK
        """
        update_data = {}

        # If prompt is provided, create a new LLM and update response_engine
        if prompt is not None:
            full_prompt = build_full_prompt(prompt)
            llm = self.client.llm.create(
                general_prompt=full_prompt,
                start_speaker=DEFAULT_START_SPEAKER,
                model="gpt-4o-mini",
                begin_message=None,
                # Add end_call and transfer_call functions
                general_tools=[
                    {
                        "type": "end_call",
                        "name": "end_call",
                        "description": (
                            "Use this tool when the user says goodbye, thanks, or indicates "
                            "they want to end the call. Also use this when the conversation "
                            "objective has been completed."
                        ),
                    },
                ],
            )
            update_data["response_engine"] = {"type": "retell-llm", "llm_id": llm.llm_id}

        # If agent_name is provided, update it
        if agent_name is not None:
            update_data["agent_name"] = agent_name

        # Call the Retell API to update the agent
        agent = self.client.agent.update(agent_id, **update_data)

        return agent

    def list_agents(
        self, limit: int = 1000, pagination_key: str | None = None
    ) -> AgentListResponse:
        """
        List all agents from Retell AI.

        Args:
            limit: Number of agents to return (1-1000, default 1000)
            pagination_key: Agent ID to continue fetching from (for pagination)

        Returns:
            AgentListResponse: List of AgentResponse objects from Retell SDK
        """
        params = {"limit": limit}
        if pagination_key:
            params["pagination_key"] = pagination_key

        return self.client.agent.list(**params)

    def get_agent(self, agent_id: str) -> dict:
        """
        Get a specific agent from Retell AI with its prompt.

        This fetches both the agent and its associated LLM to include the prompt
        in the response.

        Args:
            agent_id: The ID of the agent to retrieve

        Returns:
            Dictionary containing only agent_id, name, and prompt
        """
        # Get the agent
        agent = self.client.agent.retrieve(agent_id)

        # Extract the LLM ID from the response_engine
        response_engine = agent.response_engine
        llm_id = response_engine.llm_id if response_engine.type == "retell-llm" else None

        prompt = None
        if llm_id:
            try:
                llm = self.client.llm.retrieve(llm_id)
                prompt = llm.general_prompt if hasattr(llm, "general_prompt") else None
            except Exception:
                # If LLM fetch fails, continue without prompt
                pass

        # Return only the essential fields
        return {
            "agent_id": agent.agent_id,
            "name": agent.agent_name,
            "prompt": prompt,
        }

    def create_web_call(
        self,
        agent_id: str,
        metadata: dict | None = None,
        retell_llm_dynamic_variables: dict[str, str] | None = None,
    ):
        """
        Create a web call via Retell AI.

        Args:
            agent_id: Unique ID of agent used for the call
            metadata: Arbitrary key-value storage for internal use (e.g., customer IDs)
            retell_llm_dynamic_variables: Dynamic string variables to inject into prompt

        Returns:
            Call object from Retell SDK containing access_token for frontend
        """
        params = {"agent_id": agent_id}

        if metadata is not None:
            params["metadata"] = metadata

        if retell_llm_dynamic_variables is not None:
            params["retell_llm_dynamic_variables"] = retell_llm_dynamic_variables

        return self.client.call.create_web_call(**params)

    def create_call(self, phone_number: str, agent_config: dict):
        """
        Create a phone call via Retell AI.

        TODO: Implement using retell-sdk
        See: https://github.com/RetellAI/retell-python-sdk/blob/main/api.md
        """
        pass

    def get_call_details(self, call_id: str):
        """
        Get call details from Retell AI.

        TODO: Implement using retell-sdk
        """
        pass
