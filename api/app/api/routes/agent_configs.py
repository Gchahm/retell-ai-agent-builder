from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.api.deps import SessionDep
from app.models import AgentConfig
from app.schemas import AgentConfigCreate, AgentConfigResponse, AgentConfigUpdate

router = APIRouter(prefix="/api/agent-configs", tags=["agent-configs"])


@router.post("", response_model=AgentConfigResponse, status_code=201)
def create_agent_config(config: AgentConfigCreate, session: SessionDep):
    """Create a new agent configuration."""
    db_config = AgentConfig.model_validate(config)
    session.add(db_config)
    session.commit()
    session.refresh(db_config)
    return db_config


@router.get("", response_model=list[AgentConfigResponse])
def list_agent_configs(session: SessionDep):
    """List all agent configurations."""
    configs = session.exec(select(AgentConfig)).all()
    return configs


@router.get("/{config_id}", response_model=AgentConfigResponse)
def get_agent_config(config_id: int, session: SessionDep):
    """Get a specific agent configuration."""
    config = session.get(AgentConfig, config_id)
    if not config:
        raise HTTPException(status_code=404, detail="Agent configuration not found")
    return config


@router.patch("/{config_id}", response_model=AgentConfigResponse)
def update_agent_config(config_id: int, updates: AgentConfigUpdate, session: SessionDep):
    """Update an agent configuration."""
    config = session.get(AgentConfig, config_id)
    if not config:
        raise HTTPException(status_code=404, detail="Agent configuration not found")

    update_data = updates.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(config, key, value)

    session.add(config)
    session.commit()
    session.refresh(config)
    return config


@router.delete("/{config_id}", status_code=204)
def delete_agent_config(config_id: int, session: SessionDep):
    """Delete an agent configuration."""
    config = session.get(AgentConfig, config_id)
    if not config:
        raise HTTPException(status_code=404, detail="Agent configuration not found")

    session.delete(config)
    session.commit()
    return None
