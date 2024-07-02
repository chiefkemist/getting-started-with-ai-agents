import marimo

__generated_with = "0.6.23"
app = marimo.App(width="medium", app_title="Agents Scratchpad")


@app.cell
def __():
    import marimo as mo
    return mo,


@app.cell
def __():
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

    from rich.console import Console

    console = Console()
    return (
        AfterValidator,
        Any,
        AsyncInstructor,
        AsyncOpenAI,
        BaseModel,
        BeforeValidator,
        ChatCompletionMessage,
        ChatCompletionMessageToolCall,
        ConfigDict,
        Console,
        Dict,
        Field,
        Function,
        Instructor,
        InstructorChatCompletionCreate,
        List,
        Literal,
        OpenAI,
        OpenAISchema,
        Optional,
        TypeAdapter,
        Union,
        console,
        from_json,
        instructor,
        json,
        llm_validator,
        os,
        parse_obj_as,
        uuid4,
    )


@app.cell
def __(os):
    # from getpass import getpass
    # OPENAI_API_KEY = getpass('Paste your OpenAI API Key: ')
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    return OPENAI_API_KEY,


@app.cell
def __():
    from enum import Enum, auto

    class LLMModel(str, Enum):
        Claude3 = "claude-3-opus-20240229"
        GPT4_Omni = "gpt-4o"
        GPT35_Turbo = "gpt-3.5-turbo"
        LLAMA3 = "llama3-70b-8192"
    return Enum, LLMModel, auto


@app.cell
def __(mo):
    mo.md(
        rf"""
        * Patch the client

          The LLM's capability are enhanced
        """
    )
    return


@app.cell
def __(
    AsyncInstructor,
    AsyncOpenAI,
    Instructor,
    LLMModel,
    OpenAI,
    instructor,
):
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
    return gen_async_client, gen_client


@app.cell
def __(mo):
    mo.md("* Setup clients")
    return


@app.cell
def __(LLMModel, gen_async_client, gen_client):
    client = gen_client()
    aclient = gen_async_client()

    client_gpt35turbo = gen_client(model=LLMModel.GPT35_Turbo)
    aclient_gpt35turbo = gen_async_client(model=LLMModel.GPT35_Turbo)
    return aclient, aclient_gpt35turbo, client, client_gpt35turbo


@app.cell
def __(mo):
    mo.md("* Agents")
    return


@app.cell
def __(Any, BaseModel, Dict, Literal):
    class SystemMessage(BaseModel):
        role: Literal["system"] = "system"
        content: str

    class UserMessage(BaseModel):
        role: Literal["user"] = "user"
        content: str

    class AssistantMessage(BaseModel):
        role: Literal["assistant"] = "assistant"
        content: str

    class FuncNameArgs(BaseModel):
        arguments: Dict[str, Any]
        name: str
    return AssistantMessage, FuncNameArgs, SystemMessage, UserMessage


@app.cell
def __(SystemMessage):
    sys_msg = SystemMessage(content="Greet")
    sys_msg
    return sys_msg,


@app.cell
def __(UserMessage):
    user_msg = UserMessage(content="Hi")
    user_msg
    return user_msg,


@app.cell
def __(
    AssistantMessage,
    List,
    SystemMessage,
    Union,
    UserMessage,
    sys_msg,
    user_msg,
):
    msg_lst: List[Union[SystemMessage, UserMessage, AssistantMessage]] = [
        sys_msg,
        user_msg,
    ]
    msg_lst
    return msg_lst,


@app.cell
def __(msg_lst):
    [m.dict() for m in msg_lst]
    return


@app.cell
def __(AssistantMessage):
    assistant_msg = AssistantMessage(content="Hello")
    assistant_msg
    return assistant_msg,


@app.cell
def __(AssistantMessage, SystemMessage, TypeAdapter, Union, UserMessage):
    MsgLst = TypeAdapter(Union[SystemMessage, UserMessage, AssistantMessage])
    MsgLst
    return MsgLst,


@app.cell
def __(MsgLst):
    lb = MsgLst.validate_python({"type": "user", "content": "d"})
    lb
    return lb,


@app.cell
def __(OpenAISchema):
    class UserFunc(OpenAISchema):
        name: str
        age: int

        def run(self):
            msg = f"UserFunc->run: User's name is {self.name} and age is {self.age}"
            return msg
    return UserFunc,


@app.cell
def __(OpenAISchema):
    class DefaultFunc(OpenAISchema):
        response: str

        def run(self):
            msg = f"DefaultFunc->run: {self.response}"
            return msg
    return DefaultFunc,


@app.cell
def __(
    Any,
    AssistantMessage,
    BaseModel,
    ChatCompletionMessageToolCall,
    LLMModel,
    List,
    SystemMessage,
    Union,
    UserMessage,
    console,
    from_json,
):
    class Agent(BaseModel):
        context: List[Union[SystemMessage, UserMessage, AssistantMessage]] = []
        percept_seq: List[Union[SystemMessage, UserMessage, AssistantMessage]] = []
        model: LLMModel = LLMModel.GPT4_Omni
        client: Any
        toolbox: List[Any]
        stateful: bool = False

        def add_percept(
            self, percept: Union[SystemMessage, UserMessage, AssistantMessage]
        ):
            self.percept_seq.append(percept)

        def actuate(self, tool_call: ChatCompletionMessageToolCall):
            Func = next(
                iter(
                    [
                        func
                        for func in self.toolbox
                        if func.__name__ == tool_call.function.name
                    ]
                )
            )

            if not Func:
                available_function_names = [func.__name__ for func in self.toolbox]
                err_msg = f"Error: Function {tool_call.function.name} not found. Available functions: {available_function_names}"
                console.error(err_msg)
                return err_msg

            try:
                console.log(
                    f"Tool Call -> {tool_call.function.name} ->with {tool_call.function.arguments} of type {type(tool_call.function.arguments)}",
                    style="bold blue",
                )
                args = from_json(tool_call.function.arguments)
                console.log(f"Args -> {args} of type {type(args)}", style="bold blue")
                func = Func.model_validate(args)
                console.log(f"Func -> {repr(func)}", style="bold blue")
                output = func.run()
                return output
            except Exception as e:
                return f"Error: {e}"

        def run(self, percept: Union[SystemMessage, UserMessage, AssistantMessage]):
            self.add_percept(percept)
            messages = [p.dict() for p in [*self.context, *self.percept_seq]]
            tools = [
                dict(type="function", function=tool.openai_schema)
                for tool in self.toolbox
            ]
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools,
            )
            # console.log(completion)
            first_message = completion.choices[0].message
            if first_message.content is None:
                tool_calls = first_message.tool_calls
                results = []
                for tool_call in tool_calls:
                    output = self.actuate(tool_call)
                    results.append(output)
                return results
            else:
                content = first_message.content.replace("\\", "")
                console.log(content)
                return content
    return Agent,


@app.cell
def __(Agent, DefaultFunc, SystemMessage, UserFunc, client):
    person_details_agent = Agent(
        context=[
            SystemMessage(
                content="You will collect the personal details of any person mentioned, otherwise just answer the question."
            )
        ],
        client=client,
        toolbox=[DefaultFunc, UserFunc],
    )
    return person_details_agent,


@app.cell
def __(UserMessage, person_details_agent):
    responses_msg = person_details_agent.run(
        UserMessage(
            content="Hi, my name is Lambert, and I am 24 years old and Rigobertine is 22 years old."
        )
    )
    # [Function.validate(response_msg).dict() for response_msg in responses_msg]
    responses_msg
    return responses_msg,


@app.cell
def __(UserMessage, person_details_agent):
    weather_conversion_msg = person_details_agent.run(
        UserMessage(content="How do we convert Fahrenheit to Celcius?")
    )
    weather_conversion_msg
    return weather_conversion_msg,


@app.cell
def __():
    return


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
