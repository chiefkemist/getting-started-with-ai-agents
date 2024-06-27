import os
import json

from typing import List, Optional, Union, Dict, Any
from typing_extensions import Literal
from uuid import uuid4

import instructor

from instructor import Instructor, AsyncInstructor
from instructor import OpenAISchema, llm_validator
from instructor.patch import InstructorChatCompletionCreate

# from anthropic import Anthropic, AsyncAnthropic
# from groq import Groq, AsyncGroq
from openai import OpenAI, AsyncOpenAI
from openai.types.chat.chat_completion_message_tool_call import (
    ChatCompletionMessageToolCall,
    Function,
)
from openai.types.chat.chat_completion_message import ChatCompletionMessage
from pydantic import BaseModel, Field, ConfigDict, parse_obj_as
from pydantic import BeforeValidator, AfterValidator, TypeAdapter
from pydantic_core import from_json

from enum import Enum, auto


class LLMModel(str, Enum):
    Claude3 = "claude-3-opus-20240229"
    GPT4_Omni = "gpt-4o"
    GPT35_Turbo = "gpt-3.5-turbo"
    LLAMA3 = "llama3-70b-8192"


def gen_client(model=LLMModel.GPT4_Omni) -> Instructor:
    match model:
        # case LLMModel.Claude3:
        #     client = instructor.from_anthropic(Anthropic())
        case LLMModel.GPT4_Omni | LLMModel.GPT35_Turbo:
            client = instructor.patch(OpenAI())
        # case LLMModel.LLAMA3:
        #     client = instructor.patch(Groq())
    return client


def gen_async_client(model=LLMModel.GPT4_Omni) -> AsyncInstructor:
    match model:
        # case LLMModel.Claude3:
        #     client = instructor.from_anthropic(AsyncAnthropic())
        case LLMModel.GPT4_Omni | LLMModel.GPT35_Turbo:
            client = instructor.patch(AsyncOpenAI())
        # case LLMModel.LLAMA3:
        #     client = instructor.patch(AsyncGroq())
    return client


class SystemMessage(BaseModel):
    role: Literal["system"] = "system"
    content: str


class UserMessage(BaseModel):
    role: Literal["user"] = "user"
    content: str


class AssistantMessage(BaseModel):
    role: Literal["assistant"] = "assistant"
    content: str


MsgLst = TypeAdapter(Union[SystemMessage, UserMessage, AssistantMessage])
