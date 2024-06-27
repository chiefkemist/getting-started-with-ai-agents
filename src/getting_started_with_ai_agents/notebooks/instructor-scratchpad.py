import marimo

__generated_with = "0.6.23"
app = marimo.App(width="medium", app_title="Instructor Scratch Pad")


@app.cell
def __():
    import marimo as mo

    return (mo,)


@app.cell
def __():
    import os
    import json

    from typing import Optional
    from uuid import uuid4

    import instructor

    from instructor import Instructor, AsyncInstructor
    from instructor import OpenAISchema, llm_validator

    # from anthropic import Anthropic, AsyncAnthropic
    # from groq import Groq, AsyncGroq
    from openai import OpenAI, AsyncOpenAI
    from openai.types.chat.chat_completion_message_tool_call import (
        ChatCompletionMessageToolCall,
    )
    from pydantic import BaseModel, Field
    from pydantic import BeforeValidator, AfterValidator
    from pydantic_core import from_json

    from rich.console import Console

    console = Console()
    return (
        AfterValidator,
        AsyncInstructor,
        AsyncOpenAI,
        BaseModel,
        BeforeValidator,
        ChatCompletionMessageToolCall,
        Console,
        Field,
        Instructor,
        OpenAI,
        OpenAISchema,
        Optional,
        console,
        from_json,
        instructor,
        json,
        llm_validator,
        os,
        uuid4,
    )


@app.cell
def __(os):
    # from getpass import getpass
    # OPENAI_API_KEY = getpass('Paste your OpenAI API Key: ')
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    return (OPENAI_API_KEY,)


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
    mo.md(
        """
        * Basic Data Extraction

          The `response_model` field is used to obtain structured data from the LLM completions
        """
    )
    return


@app.cell
def __(BaseModel):
    class UserDetail(BaseModel):
        """
        Extract User Data
        """

        name: str
        age: int

    return (UserDetail,)


@app.cell
def __(LLMModel, UserDetail, client_gpt35turbo):
    user: UserDetail = client_gpt35turbo.chat.completions.create(
        model=LLMModel.GPT35_Turbo,
        response_model=UserDetail,
        messages=[
            {
                "role": "user",
                "content": "Hi, my name is Lambert, and I am 24 years old.",
            }
        ],
    )
    return (user,)


@app.cell
def __(user):
    user.name
    return


@app.cell
def __(user):
    user.age
    return


@app.cell
def __(mo):
    mo.md(
        """
        * Fields

          The `pydantic.Field` is used to add and customize the metada of the [Pydantic](https://docs.pydantic.dev/latest/) models.
        """
    )
    return


@app.cell
def __(BaseModel, Field, Optional, uuid4):
    class User(BaseModel):
        id: str = Field(default_factory=lambda: str(uuid4().hex))
        id2: Optional[str]

    return (User,)


@app.cell
def __(mo):
    mo.md(
        """
        * Converting to `OpenAI Schema`

          Convert your Pydantic model into an OpenAI function by simply extending `OpenAISchema`
        """
    )
    return


@app.cell
def __(OpenAISchema):
    class UserFunc(OpenAISchema):
        name: str
        age: int

        def run(self):
            msg = f"UserFunc->run: User's name is {self.name} and age is {self.age}"
            return msg

    return (UserFunc,)


@app.cell
def __(UserFunc):
    UserFunc.openai_schema
    return


@app.cell
def __(UserFunc):
    UserFunc.openai_schema["name"]
    return


@app.cell
def __(LLMModel, UserFunc, client_gpt35turbo):
    user_completion = client_gpt35turbo.chat.completions.create(
        model=LLMModel.GPT35_Turbo,
        messages=[
            {
                "role": "user",
                "content": "Hi, my name is Lambert, and I am 24 years old.",
            }
        ],
        tools=[
            {
                "type": "function",
                "function": UserFunc.openai_schema,  # add your function
            }
        ],
        tool_choice={
            "type": "function",
            "function": {
                "name": UserFunc.openai_schema["name"],
            },
        },
    )
    return (user_completion,)


@app.cell
def __(user_completion):
    user_completion
    return


@app.cell
def __(user_completion):
    user_completion.choices
    return


@app.cell
def __(user_completion):
    user_completion.choices[0]
    return


@app.cell
def __(mo):
    mo.md("* Tool Execution")
    return


@app.cell
def __(
    ChatCompletionMessageToolCall,
    List,
    OpenAISchema,
    console,
    from_json,
):
    def execute_tool(
        tool_call: ChatCompletionMessageToolCall, funcs: List[OpenAISchema]
    ):
        Func = next(
            iter([func for func in funcs if func.__name__ == tool_call.function.name])
        )

        if not Func:
            available_function_names = [func.__name__ for func in funcs]
            return f"Error: Function {tool_call.function.name} not found. Available functions: {available_function_names}"

        try:
            console.log(
                f"Tool Call -> {tool_call.function.name} ->with {tool_call.function.arguments} of type {type(tool_call.function.arguments)}",
                style="bold blue",
            )
            # func = Func(**eval(tool_call.function.arguments))
            # args = json.loads(tool_call.function.arguments)
            # func = Func(**args)
            args = from_json(tool_call.function.arguments)
            console.log(f"Args -> {args} of type {type(args)}", style="bold blue")
            func = Func.model_validate(args)
            console.log(f"Func -> {repr(func)}", style="bold blue")
            output = func.run()
            return output
        except Exception as e:
            return f"Error: {e}"

    return (execute_tool,)


@app.cell
def __(UserFunc):
    FUNCS = [UserFunc]  # Available Functions
    return (FUNCS,)


@app.cell
def __(user_completion):
    first_user_completion_tool_choice = user_completion.choices[0]
    return (first_user_completion_tool_choice,)


@app.cell
def __(FUNCS, console, execute_tool, first_user_completion_tool_choice):
    for tool_call in first_user_completion_tool_choice.message.tool_calls:
        output = execute_tool(tool_call, FUNCS)
        console.log(output, style="bold green")
    return output, tool_call


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
