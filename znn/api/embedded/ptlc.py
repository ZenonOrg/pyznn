from znn.client.websocket import get_default_client
from znn.embedded.definitions import PTLC_ABI
from znn.model.nom.account_block import AccountBlock
from znn.model.primitives.address import Address
from znn.model.primitives.address import PTLC_ADDRESS
from znn.model.primitives.hash import Hash
from znn.model.primitives.token_standard import ZNN_ZTS


class PtlcApi:
    def __init__(self, ws_client=None):
        self.ws_client = ws_client

        if self.ws_client is None:
            self.ws_client = get_default_client()

    # RPC queries

    async def get_by_id(self, id: Hash):
        return await self.ws_client.send_request(
            "embedded.ptlc.getById", [str(id)]
        )

    async def get_proxy_unlock_status(self, address: Address):
        return await self.ws_client.send_request(
            "embedded.ptlc.getProxyUnlockStatus", [str(address)]
        )

    # Contract methods

    def create(
        self,
        token_standard,
        amount: int,
        point_locked: Address,
        expiration_time: int,
        point_lock: bytes,
    ):
        return AccountBlock.contract_call(
            PTLC_ADDRESS,
            token_standard,
            amount,
            PTLC_ABI.encode("Create", [point_locked, expiration_time, point_lock]),
        )

    def reclaim(self, id: Hash):
        return AccountBlock.contract_call(
            PTLC_ADDRESS,
            ZNN_ZTS,
            0,
            PTLC_ABI.encode("Reclaim", [id]),
        )

    def unlock(self, id: Hash, scalar: bytes):
        return AccountBlock.contract_call(
            PTLC_ADDRESS,
            ZNN_ZTS,
            0,
            PTLC_ABI.encode("Unlock", [id, scalar]),
        )

    def deny_proxy_unlock(self):
        return AccountBlock.contract_call(
            PTLC_ADDRESS,
            ZNN_ZTS,
            0,
            PTLC_ABI.encode("DenyProxyUnlock", []),
        )

    def allow_proxy_unlock(self):
        return AccountBlock.contract_call(
            PTLC_ADDRESS,
            ZNN_ZTS,
            0,
            PTLC_ABI.encode("AllowProxyUnlock", []),
        )
