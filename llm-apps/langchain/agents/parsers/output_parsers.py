from langchain.output_parsers import PydanticOutputParser
from pydantic import Field, BaseModel
from typing import List, Dict, Any


class Summary(BaseModel):
    summary: str = Field(description="describes the summary of the person")
    facts: List[str] = Field(description="contains interesting facts about the person")

    def to_dict(self) -> Dict[str, Any]:
        return {"summary": self.summary, "facts": self.facts}


summary_parser = PydanticOutputParser(pydantic_object=Summary)
