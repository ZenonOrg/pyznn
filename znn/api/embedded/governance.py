from znn.client.websocket import get_default_client
from znn.embedded.definitions import GOVERNANCE_ABI
from znn.model.nom.account_block import AccountBlock
from znn.model.primitives.address import GOVERNANCE_ADDRESS
from znn.model.primitives.hash import Hash
from znn.model.primitives.token_standard import ZNN_ZTS


class GovernanceApi:
    """Governance contract API.

    Note: No RPC query methods yet - the node does not expose
    embedded.governance.* endpoints.
    """

    def __init__(self, ws_client=None):
        self.ws_client = ws_client

        if self.ws_client is None:
            self.ws_client = get_default_client()

    def create_proposal(
        self,
        title: str,
        description: str,
        url: str,
        voting_period: int,
    ):
        return AccountBlock.contract_call(
            GOVERNANCE_ADDRESS,
            ZNN_ZTS,
            0,
            GOVERNANCE_ABI.encode(
                "CreateProposal", [title, description, url, voting_period]
            ),
        )

    def cast_vote(self, id: Hash, vote: int):
        return AccountBlock.contract_call(
            GOVERNANCE_ADDRESS,
            ZNN_ZTS,
            0,
            GOVERNANCE_ABI.encode("CastVote", [id, vote]),
        )

    def execute(self, id: Hash):
        return AccountBlock.contract_call(
            GOVERNANCE_ADDRESS,
            ZNN_ZTS,
            0,
            GOVERNANCE_ABI.encode("Execute", [id]),
        )
