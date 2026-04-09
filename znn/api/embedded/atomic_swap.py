from znn.client.websocket import get_default_client
from znn.embedded.definitions import ATOMIC_SWAP_ABI
from znn.model.nom.account_block import AccountBlock
from znn.model.primitives.address import Address
from znn.model.primitives.address import ATOMIC_SWAP_ADDRESS
from znn.model.primitives.hash import Hash
from znn.model.primitives.token_standard import ZNN_ZTS


class AtomicSwapApi:
    """Atomic Swap contract API.

    Note: No RPC query methods yet - the node does not expose
    embedded.atomicSwap.* endpoints.
    """

    def __init__(self, ws_client=None):
        self.ws_client = ws_client

        if self.ws_client is None:
            self.ws_client = get_default_client()

    def create_swap(
        self,
        token_standard,
        amount: int,
        counterparty: Address,
        btc_tx_hash: bytes,
        expiration_time: int,
    ):
        return AccountBlock.contract_call(
            ATOMIC_SWAP_ADDRESS,
            token_standard,
            amount,
            ATOMIC_SWAP_ABI.encode(
                "CreateSwap", [counterparty, btc_tx_hash, expiration_time]
            ),
        )

    def claim_swap(
        self,
        swap_id: Hash,
        block_header: bytes,
        merkle_proof: bytes,
        tx_index: int,
    ):
        return AccountBlock.contract_call(
            ATOMIC_SWAP_ADDRESS,
            ZNN_ZTS,
            0,
            ATOMIC_SWAP_ABI.encode(
                "ClaimSwap", [swap_id, block_header, merkle_proof, tx_index]
            ),
        )

    def reclaim_swap(self, swap_id: Hash):
        return AccountBlock.contract_call(
            ATOMIC_SWAP_ADDRESS,
            ZNN_ZTS,
            0,
            ATOMIC_SWAP_ABI.encode("ReclaimSwap", [swap_id]),
        )
