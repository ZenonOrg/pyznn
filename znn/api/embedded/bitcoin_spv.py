from znn.client.websocket import get_default_client
from znn.embedded.definitions import BITCOIN_SPV_ABI
from znn.model.nom.account_block import AccountBlock
from znn.model.primitives.address import BITCOIN_SPV_ADDRESS
from znn.model.primitives.token_standard import ZNN_ZTS


class BitcoinSpvApi:
    """Bitcoin SPV contract API.

    Note: No RPC query methods yet - the node does not expose
    embedded.bitcoinSpv.* endpoints.
    """

    def __init__(self, ws_client=None):
        self.ws_client = ws_client

        if self.ws_client is None:
            self.ws_client = get_default_client()

    def submit_headers(self, headers: bytes):
        return AccountBlock.contract_call(
            BITCOIN_SPV_ADDRESS,
            ZNN_ZTS,
            0,
            BITCOIN_SPV_ABI.encode("SubmitHeaders", [headers]),
        )

    def verify_transaction(
        self,
        tx_hash: bytes,
        block_height: int,
        merkle_proof: bytes,
        tx_index: int,
    ):
        return AccountBlock.contract_call(
            BITCOIN_SPV_ADDRESS,
            ZNN_ZTS,
            0,
            BITCOIN_SPV_ABI.encode(
                "VerifyTransaction",
                [tx_hash, block_height, merkle_proof, tx_index],
            ),
        )
