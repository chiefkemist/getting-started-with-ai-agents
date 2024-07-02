from pydantic import BaseModel

from rich.console import Console

from getting_started_with_ai_agents.agents.base import Agent
from getting_started_with_ai_agents.llm import UserMessage

console = Console()


class Person(BaseModel):
    name: str  # name of the person
    age: int  # age of the person
    cash: float  # amount of cash the person has
    is_on_guest_list: bool = False  # whether the person is on the guest list


class Guest(Person):
    has_ticket: bool = False  # whether the person has a ticket
    is_on_guest_list: bool = False  # whether the person is on the guest list
    is_vip: bool = False  # whether the person is a VIP


class Club(BaseModel):
    capacity: int
    table_count: int


class ClubBouncer(Agent):
    """An agent that decides who can enter a club."""

    capacity: int
    table_count: int

    def check_person(self, person: Person):
        console.log(f"Checking the {person.name}'s details...")
        if person.age >= 21 and person.cash >= 20:
            if person.cash >= 1000:
                if self.table_count > 0:
                    guest_details = UserMessage(
                        f"The person is {person.name} and is {person.age} years old with ${person.cash} in cash. As a VIP they want table service."
                    )
                else:
                    guest_details = UserMessage(
                        f"The person is {person.name} and is {person.age} years old with ${person.cash} in cash. As a VIP they want table service but there are no tables available."
                    )
            elif person.is_on_guest_list:
                guest_details = UserMessage(
                    f"The person is {person.name} and is {person.age} years old with ${person.cash} in cash. They are on the guest list."
                )
            else:
                guest_details = UserMessage(
                    f"The person is {person.name} and is {person.age} years old with ${person.cash} in cash to purchase a ticket."
                )
            console.log(guest_details.content)
            self.manage_line(guest_details)
        else:
            console.log(f"Sorry {person.name}, you can't enter the club.")

    def check_guest(self, guest: Guest):
        console.log(f"Checking the {guest.name}'s guest details...")
        if guest.has_ticket:
            console.log("Welcome to the club! Please proceed.")
            self.capacity -= 1  # decrement the capacity
        elif guest.is_on_guest_list:
            console.log(
                f"Welcome to the club {guest.name}! You are on the guest list and do not need a ticket. Please proceed."
            )
            self.capacity -= 1  # decrement the capacity
        elif guest.is_vip:
            console.log(
                f"Welcome to the club {guest.name}! You are a VIP and do not need a ticket. Please proceed."
            )
            self.capacity -= 1  # decrement the capacity
            self.table_count -= 1  # decrement the table count
        else:
            console.log(f"Sorry {guest.name}, you can't enter the club.")

    def manage_line(self, next_in_line_details: UserMessage):
        """Decide who can enter the club."""
        outcome = self.process(next_in_line_details)
        console.log(outcome)
        if isinstance(outcome, Person):  # outcome indicates the person details
            self.check_person(outcome)
        elif isinstance(outcome, Guest):  # outcome indicates the guest details
            self.check_guest(outcome)
        elif isinstance(outcome, list):
            for otcm in outcome:
                if isinstance(outcome, Person):  # outcome indicates the person details
                    self.check_person(otcm)
                elif isinstance(otcm, Guest):  # outcome indicates the guest details
                    self.check_guest(otcm)
                elif isinstance(otcm, str):  # outcome indicates a message
                    console.log(otcm)
                else:
                    console.log("Sorry, you can't enter the club.")
        elif isinstance(outcome, str):  # outcome indicates a message
            console.log(outcome)
        else:
            console.log("Sorry, you can't enter the club.")
