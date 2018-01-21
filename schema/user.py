from graphene import Enum, ObjectType, String, List, Field
from util.action import Action
from data.proposal import liaison_astronomer

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
                    current_liaison is None and
                    assigned_liaison == g.user.username)

        if action == Action.UPDATE_TECHNICAL_REPORT:
            return self.has_role(RoleType.ADMINISTRATOR, partner) or \
                   self.has_role(RoleType.SALT_ASTRONOMER, partner)

        return False

    def __str__(self):
        return "username: {username}, role: {role}".format(username=self.username, role=self.role)
