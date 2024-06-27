from typing import List, Union, Any

from openai.types.chat.chat_completion_message_tool_call import (
    ChatCompletionMessageToolCall,
)
from pydantic import BaseModel
from pydantic_core import from_json
from rich.console import Console

from getting_started_with_ai_agents.llm import (
    SystemMessage,
    UserMessage,
    AssistantMessage,
    LLMModel,
)

console = Console()


class Agent(BaseModel):
    context: List[Union[SystemMessage, UserMessage, AssistantMessage]] = []
    percept_seq: List[Union[SystemMessage, UserMessage, AssistantMessage]] = []
    model: LLMModel = LLMModel.GPT4_Omni
    client: Any
    toolbox: List[Any]
    stateful: bool = False

    def add_percept(self, percept: Union[SystemMessage, UserMessage, AssistantMessage]):
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

    def process(self, percept: Union[SystemMessage, UserMessage, AssistantMessage]):
        self.add_percept(percept)
        messages = [p.dict() for p in [*self.context, *self.percept_seq]]
        tools = [
            dict(type="function", function=tool.openai_schema) for tool in self.toolbox
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
