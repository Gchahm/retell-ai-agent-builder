from retell import Retell
from retell.types import AgentListResponse, AgentResponse

from app.config import get_settings

settings = get_settings()

# Default configuration for our agents
DEFAULT_VOICE_ID = "11labs-Adrian"  # Professional male voice
DEFAULT_VOICE_MODEL = "eleven_turbo_v2"  # Fast, high-quality
DEFAULT_LANGUAGE = "en-US"
DEFAULT_START_SPEAKER = "user"  # User initiates the conversation


class RetellService:
    """Service for interacting with Retell AI API."""

    def __init__(self):
        self.client = Retell(api_key=settings.retell_api_key)

    def create_agent(self, prompt: str, agent_name: str | None = None) -> AgentResponse:
        """
        Create a new agent with the specified prompt.

        This is a light wrapper around the Retell SDK that:
        1. Creates an LLM with the provided prompt
        2. Creates an agent using that LLM with sensible defaults

        Args:
            prompt: The system prompt defining agent behavior
            agent_name: Optional name for the agent (for internal reference)

        Returns:
            AgentResponse: The created agent from Retell SDK
        """
        # Step 1: Create the LLM with the user's prompt
        llm = self.client.llm.create(
            general_prompt=prompt,
            start_speaker=DEFAULT_START_SPEAKER,
            # Optional but good defaults
            model="gpt-4o-mini",  # Fast and cost-effective
            begin_message=None,  # Let LLM generate dynamic greeting
        )

        # Step 2: Create the agent using the LLM
        agent = self.client.agent.create(
            agent_name=agent_name,
            voice_id=DEFAULT_VOICE_ID,
            voice_model=DEFAULT_VOICE_MODEL,
            language=DEFAULT_LANGUAGE,
            response_engine={"type": "retell-llm", "llm_id": llm.llm_id},
            # Good defaults for responsiveness
            responsiveness=0.7,
            interruption_sensitivity=0.5,
            enable_backchannel=True,
            backchannel_frequency=0.3,
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

        Args:
            agent_id: The ID of the agent to update
            prompt: New system prompt (optional, creates new LLM if provided)
            agent_name: New agent name (optional)

        Returns:
            AgentResponse: The updated agent from Retell SDK
        """
        update_data = {}

        # If prompt is provided, create a new LLM and update response_engine
        if prompt is not None:
            llm = self.client.llm.create(
                general_prompt=prompt,
                start_speaker=DEFAULT_START_SPEAKER,
                model="gpt-4o-mini",
                begin_message=None,
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
