from instructor import OpenAISchema

from getting_started_with_ai_agents.agents.club_bouncer import (
    ClubBouncer,
    Person,
    Guest,
)
from getting_started_with_ai_agents.llm import gen_client, SystemMessage, UserMessage

client = gen_client()


class ClubSecurity(OpenAISchema):
    """
    Security agent for Club UbuntuTechHive.
    Helps the bouncer manage the line and check the guest list following the club's rules.
    if the person is at least 21 years old and has at least $20 in cash, they can enter the club.
    if the person is on the guest list, they can enter the club.
    if the person is a VIP, they must have at least $1000 in cash to get table service.
    """

    name: str  # name of the person
    age: int  # age of the person
    cash: float  # amount of cash the person has
    is_on_guest_list: bool  # whether the person is on the guest list

    def run(self):
        person = Person(
            name=self.name,
            age=self.age,
            cash=self.cash,
            is_on_guest_list=self.is_on_guest_list,
        )
        return person


class ClubHost(OpenAISchema):
    """
    Hostess for Club UbuntuTechHive.
    Collects the cover charge and assigns tickets to guests.
    Checks the guest list and assigns guests to the VIP line.
    Manages the VIPs and table service.
    Accepts VIPs with at least $1000 in cash and table service requests.
    Accepts payment for table service and assigns tables to VIPs.
    if the person has money for a ticket, let them buy the ticket and mark them as having a ticket using a wristband.
    if guest is on the guest list, mark them as present on the club's copy of the guest list and let them in.
    if guest has $1000 in cash, they are a VIP, mark them as VIP, then lead them to a free table.
    """

    name: str  # name of the person
    age: int  # age of the person
    cash: float  # amount of cash the person has
    has_ticket: bool = False  # whether the person has a ticket
    is_on_guest_list: bool = False  # whether the person is on the guest list
    is_vip: bool = False  # whether the person is a VIP

    def run(self):
        guest = Guest(
            name=self.name,
            age=self.age,
            cash=self.cash,
            has_ticket=self.has_ticket,
            is_on_guest_list=self.is_on_guest_list,
            is_vip=self.is_vip,
        )
        return guest


bouncer = ClubBouncer(
    context=[
        SystemMessage(
            content="""
Welcome to Club UbuntuTechHive!
I am the Club Bouncer. I will be managing the line tonight for the club tonight.
I will be deciding who can enter the club. My decisions are based on the following criteria:
- The person must be at least 21 years old.
- The person must have at least $20 in cash.
- The person must have a ticket or be on the guest list.
- There will be a $20 cover charge for those without a ticket or not on the guest list.
- VIPs must have at least $1000 in cash to get table service.
- Table service is available for VIPs only if there are a limited number of tables available.
- When no tables are available, VIPs must wait on the VIP line for a table to become available.
            """
        )
    ],
    capacity=100,
    table_count=10,
    client=client,
    toolbox=[ClubSecurity, ClubHost],
)

if __name__ == "__main__":
    bouncer.manage_line(
        UserMessage(
            content="""
            The person is John Doe and is 25 years old with $50 in cash. They on the guest list.
            """
        )
    )

    bouncer.manage_line(
        UserMessage(
            content="""
                Lambert is 21 years old with $20 in cash. They want to purchase a ticket.
                """
        )
    )
