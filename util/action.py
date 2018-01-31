from enum import Enum


class Action(Enum):
    """
    An enumeration of actions a user may perform with this API.
    """

    UPDATE_TIME_ALLOCATIONS = 1
    VIEW_PARTNER_PROPOSALS = 2
    UPDATE_TAC_COMMENTS = 3
    UPDATE_TECHNICAL_REPORT = 4
    UPDATE_LIAISON_ASTRONOMER = 5
    VIEW_PROPOSAL = 6
    UPDATE_REVIEWER = 7
