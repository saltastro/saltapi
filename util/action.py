from enum import Enum


class Action(Enum):
    """
    An enumeration of actions a user may perform with this API.
    """

    UPDATE_TIME_ALLOCATIONS = 1
    VIEW_PARTNER_PROPOSALS = 2
    UPDATE_TAC_COMMENTS = 3
    UPDATE_TECHNICAL_REVIEWS = 4
    UPDATE_LIAISON_ASTRONOMER = 5
    VIEW_PROPOSAL = 6
    SWITCH_USER = 7
    UPDATE_COMPLETION_STAT_COMMENT = 8
