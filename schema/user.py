from flask import g
import pandas as pd
from graphene import Enum, ObjectType, String, List, Field, Boolean, Int

from data import sdb_connect
from data.partner import get_partner_codes
from schema.partner import Partner
from util.action import Action, Data
from data.proposal import liaison_astronomer, technical_reviewer, is_investigator
from util.semester import query_semester_id, current_semester
from util.time_requests import time_requests


class RoleType(Enum):
    """
    An enumeration of all the available roles a user can have.
    """

    ADMINISTRATOR = 1
    SALT_ASTRONOMER = 2
    TAC_MEMBER = 3
    TAC_CHAIR = 4
    BOARD = 5

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
        elif self == RoleType.BOARD:
            return 'Board Member'
        else:
            return str(self)


class Role(ObjectType):
    type = RoleType()
    partners = Field(List(String))

    def resolve_type(self, *args, **kwargs):
        return self.type.value


class User(ObjectType):
    user_id = Int()
    first_name = String()
    last_name = String()
    email = String()
    username = String()
    roles = Field(List(Role), semester=String())

    def resolve_roles(self, info, semester=current_semester()["semester"]):

        return self.get_roles(semester=semester)

    def has_role(self, role, partner=None, semester=None):
        """
        Check whether this user has a roles for a partner.

        Parameters
        ----------
        role : RoleType
            The roles, such as `TAC_CHAIR` or `SALT_ASTRONOMER`.
        partner
            The partner for which the roles is checked.

        Returns
        -------
            Boolean  indicating whether this user has the roles for the partner.
        """

        # The administrator, SALT Astronomer and Board roles apply to all partners
        if role in (RoleType.ADMINISTRATOR, RoleType.SALT_ASTRONOMER, RoleType.BOARD):
            return any(r.type == role for r in self.get_roles(semester=semester))
        return any(r.type == role and partner in r.partners for r in self.get_roles(semester=semester))

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
        semester = kwargs.get('semester')
        proposal_code = kwargs.get('proposal_code')

        if action == Action.UPDATE_TIME_ALLOCATIONS or action == Action.UPDATE_TAC_COMMENTS:
            return self.has_role(RoleType.ADMINISTRATOR, partner=partner, semester=semester) or self.has_role(RoleType.TAC_CHAIR, partner, semester=semester)

        if action == Action.VIEW_PARTNER_PROPOSALS:
            return self.has_role(RoleType.ADMINISTRATOR, partner=partner, semester=semester) or \
                   self.has_role(RoleType.TAC_CHAIR, partner, semester=semester) or \
                   self.has_role(RoleType.TAC_MEMBER, partner, semester=semester) or \
                   self.has_role(RoleType.SALT_ASTRONOMER, partner)

        if action == Action.UPDATE_LIAISON_ASTRONOMER:
            assigned_liaison = kwargs['liaison_astronomer']
            current_liaison = liaison_astronomer(proposal_code)
            return self.has_role(RoleType.ADMINISTRATOR, partner=partner, semester=semester) or \
                   (self.has_role(RoleType.SALT_ASTRONOMER, partner) and
                    (current_liaison is None or current_liaison == assigned_liaison) and
                    assigned_liaison == g.user.username) and \
                   assigned_liaison is not None

        if action == Action.UPDATE_TECHNICAL_REVIEWS:
            assigned_reviewer = kwargs['reviewer']
            current_reviewer = technical_reviewer(proposal_code)
            return self.has_role(RoleType.ADMINISTRATOR, partner=partner, semester=semester) or \
                   (self.has_role(RoleType.SALT_ASTRONOMER, partner) and
                    (current_reviewer is None or current_reviewer == assigned_reviewer)) and \
                   assigned_reviewer is not None

        if action == Action.UPDATE_COMPLETION_STAT_COMMENT:
            return self.has_role(RoleType.ADMINISTRATOR, partner=partner, semester=semester) or \
                   self.has_role(RoleType.SALT_ASTRONOMER, partner)

        if action == Action.VIEW_PROPOSAL:
            if self.has_role(RoleType.ADMINISTRATOR) or self.has_role(RoleType.SALT_ASTRONOMER):
                return True

            if is_investigator(g.user.username, proposal_code):
                return True

            # Is the user on the TAC for a partner from which time is requested?
            proposal_partners = set([tr.partner for tr in time_requests(proposal_code) if tr.time_request > 1])
            for partner in proposal_partners:
                if self.has_role(RoleType.TAC_CHAIR, partner, semester=semester) or self.has_role(RoleType.TAC_MEMBER, partner, semester=semester):
                    return True

            # The user doesn't have permission to view the proposal.
            return False

        if action == Action.SWITCH_USER:
            return self.has_role(RoleType.ADMINISTRATOR)

        if action == Action.DOWNLOAD_SUMMARY:
            return self.has_role(RoleType.ADMINISTRATOR) \
                   or self.has_role(RoleType.SALT_ASTRONOMER) \
                   or self.has_role(RoleType.TAC_CHAIR, partner, semester=semester) \
                   or self.has_role(RoleType.TAC_MEMBER, partner, semester=semester)

        return False

    def may_view(self, data, **kwargs):
        """
        Check whether this user may view some data.

        Parameters
        ----------
        data : util.Action
            The action.
        **kwargs : kwargs
            Additional keyword arguments, as required by the action.

        Returns
        -------
        mayview : bool
            Bool indicating whether this user may view the action.
        """

        partner = kwargs.get('partner')
        semester = kwargs.get('semester')

        if data == Data.AVAILABLE_TIME:
            return self.has_role(RoleType.ADMINISTRATOR, partner=partner, semester=semester) or \
                   self.has_role(RoleType.TAC_CHAIR, partner, semester=semester) or \
                   self.has_role(RoleType.TAC_MEMBER, partner, semester=semester)

        if data == Data.STATISTICS:
            return self.has_role(RoleType.ADMINISTRATOR, partner=partner, semester=semester) or \
                   self.has_role(RoleType.BOARD, partner) or \
                   self.has_role(RoleType.TAC_CHAIR, partner, semester=semester)

        return False

    def get_roles(self, semester):
        print(semester)
        user_id = g.user.user_id
        user_details_sql = '''
SELECT
    Chair,
    t.PiptUser_Id AS Tac,
    t.Partner_Id AS TacPartner,
    a.Investigator_Id AS Astro
FROM PiptUser AS u
    JOIN Investigator AS i using (Investigator_Id)
    LEFT JOIN SaltAstronomers AS a using( Investigator_Id )
    LEFT JOIN PiptUserTAC AS t ON (u.PiptUser_Id = t.PiptUser_Id)
WHERE u.PiptUser_Id = {user_id}
        '''.format(user_id=user_id)
        conn = sdb_connect()
        user_details_results = pd.read_sql(user_details_sql, conn)
        conn.close()

        roles = []
        for index, user_details in user_details_results.iterrows():
            all_partner = get_partner_codes(semester=semester)
            sql = """
SELECT Partner_Id FROM PiptUser as pu
    JOIN Investigator USING (Investigator_Id)
    JOIN Institute USING (Institute_Id)
    JOIN PiptUserSetting as pus ON (pu.PiptUser_Id = pus.PiptUser_Id)
    JOIN PiptSetting using (PiptSetting_Id)
where pu.PiptUser_Id={user_id}
    AND PiptSetting_Name ='RightBoard'
    AND Value = 1
        """.format(user_id=user_id)
            conn = sdb_connect()
            results = pd.read_sql(sql, conn)
            conn.close()

            if len(results):
                roles.append(
                    Role(
                        type=RoleType.BOARD,
                        partners=get_partner_codes([results.iloc[0]["Partner_Id"]], semester=semester)
                    )
                )
            if not pd.isnull(user_details["Astro"]):
                roles.append(
                    Role(
                        type=RoleType.SALT_ASTRONOMER,
                        partners=all_partner
                    )
                )
            if not pd.isnull(user_details["Tac"]):
                roles.append(
                    Role(
                        type=RoleType.TAC_MEMBER,
                        partners=get_partner_codes([user_details["TacPartner"]], semester=semester)
                    )
                )
            if not pd.isnull(user_details["Chair"]) and user_details["Chair"] == 1:
                roles.append(
                    Role(
                        type=RoleType.TAC_CHAIR,
                        partners=get_partner_codes([user_details["TacPartner"]], semester=semester)
                    )
                )

            sql = '''
SELECT *  FROM PiptUserSetting
    LEFT JOIN PiptUserTAC using (PiptUser_Id)
WHERE PiptSetting_Id = 22
    AND PiptUser_Id = {user_id}
        '''.format(user_id=user_id)
            conn = sdb_connect()
            results = pd.read_sql(sql, conn)
            conn.close()

            if len(results) > 0 and int(results.iloc[0]["Value"]) > 1:
                roles.append(
                    Role(
                        type=RoleType.ADMINISTRATOR,
                        partners=all_partner
                    )
                )

        return roles

    def __str__(self):
        return "username: {username}, roles: {role}".format(username=self.username, role=self.roles)


class TacMember(ObjectType):
    last_name = String()
    first_name = String()
    partner = Field(Partner)
    is_chair = Boolean()
    email = String()
    username = String()