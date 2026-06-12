from pydantic import BaseModel, ConfigDict, Field
from browser_use.tokens.views import UsageSummary

class Usage(BaseModel):
    task_name: str = Field(description="Nome da Task")
    summary: UsageSummary = Field(description="Resumo dos custos")

    model_config = ConfigDict(extra="forbid")