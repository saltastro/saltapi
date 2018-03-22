from flask import g
from graphene import Enum, ObjectType, String, List, Field, Boolean
from util.action import Action
from data.proposal import liaison_astronomer, technical_reviewer, is_investigator
from util.time_requests import time_requests


class RoleType(Enum):
    """
    An enumeration of all the available roles a user can have.
    """

    ADMINISTRATOR = 1
    SALT_ASTRONOMER = 2
    TAC_MEMBER = 3
    TAC_CHAIR = 4

    @property
    def description(self):
        if self == RoleType.ADMINISTRATOR:
            return 'Site administrator'
        elif self == RoleType.SALT_ASTRONOMER:
            return 'SALT Astronomer'
        elif self == RoleType.TAC_MEMBER:
            return 'Member of a Time Allocation Committee'
        elif self == RoleType.TAC_CHAIR:
            return 'Chair of a Time Allocation Committee'
        else:
            return str(self)


class Role(ObjectType):
    type = RoleType()
    partners = Field(List(String))

    def resolve_type(self, *args, **kwargs):
        return self.type.value


class UserModel(ObjectType):
    first_name = String()
    last_name = String()
    email = String()
    username = String()
    role = Field(List(Role))

    def has_role(self, role, partner=None):
        """
        Check whether this user has a role for a partner.

        Parameters
        ----------
        role : RoleType
            The role, such as `TAC_CHAIR` or `SALT_ASTRONOMER`.
        partner
            The partner for which the role is checked.

        Returns
        -------
        hasrole: bool
            Bool indicating whether this user has the role for the partner.
        """

        # the administrator and SALT Astronomer roles apply to all partners
        if role in (RoleType.ADMINISTRATOR, RoleType.SALT_ASTRONOMER):
            return any(r.type == role for r in self.role)
        return any(r.type == role and partner in r.partners for r in self.role)

    def may_perform(self, action, **kwargs):
        """
        Check whether this user may perform an action.

        Parameters
        ----------
        action : util.Action
            The action.
        **kwargs : kwargs
            Additional keyword arguments, as required by the action.

        Returns
        -------
        mayperform : bool
            Bool indicating whether this user may perform the action.
        """

        partner = kwargs.get('partner')
        proposal_code = kwargs.get('proposal_code')

        if action == Action.UPDATE_TIME_ALLOCATIONS or action == Action.UPDATE_TAC_COMMENTS:
            return self.has_role(RoleType.ADMINISTRATOR, partner) or self.has_role(RoleType.TAC_CHAIR, partner)

        if action == Action.VIEW_PARTNER_PROPOSALS:
            return self.has_role(RoleType.ADMINISTRATOR, partner) or \
                   self.has_role(RoleType.TAC_CHAIR, partner) or \
                   self.has_role(RoleType.TAC_MEMBER, partner) or \
                   self.has_role(RoleType.SALT_ASTRONOMER, partner)

        if action == Action.UPDATE_TAC_COMMENTS:
            return self.has_role(RoleType.ADMINISTRATOR, partner)

        if action == Action.UPDATE_LIAISON_ASTRONOMER:
            assigned_liaison = kwargs['liaison_astronomer']
            current_liaison = liaison_astronomer(proposal_code)
            return self.has_role(RoleType.ADMINISTRATOR, partner) or \
                   (self.has_role(RoleType.SALT_ASTRONOMER, partner) and
                    (current_liaison is None or current_liaison == assigned_liaison) and
                    assigned_liaison == g.user.username) and \
                   assigned_liaison is not None

        if action == Action.UPDATE_TECHNICAL_REVIEWS:
            assigned_reviewer = kwargs['reviewer']
            current_reviewer = technical_reviewer(proposal_code)
            return self.has_role(RoleType.ADMINISTRATOR, partner) or \
                   (self.has_role(RoleType.SALT_ASTRONOMER, partner) and
                    (current_reviewer is None or current_reviewer == assigned_reviewer)) and \
                   assigned_reviewer is not None

        if action == Action.VIEW_PROPOSAL:
            if self.has_role(RoleType.ADMINISTRATOR) or self.has_role(RoleType.SALT_ASTRONOMER):
                return True

            if is_investigator(g.user.username, proposal_code):
                return True

            # Is the user on the TAC for a partner from which time is requested?
            proposal_partners = set([tr.partner for tr in time_requests(proposal_code) if tr.time_request > 1])
            for partner in proposal_partners:
                if self.has_role(RoleType.TAC_CHAIR, partner) or self.has_role(RoleType.TAC_MEMBER, partner):
                    return True

            # The user doesn't have permission to view the proposal.
            return False

        if action == Action.SWITCH_USER:
            return self.has_role(RoleType.ADMINISTRATOR)

        return False

    def __str__(self):
        return "username: {username}, role: {role}".format(username=self.username, role=self.role)


class TacMember(ObjectType):
    last_name = String()
    first_name = String()
    partner_code = String()
    partner_name = String()
    is_chair = Boolean()
    email = String()
    username = String()