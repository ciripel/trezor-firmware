from . import messages as proto
from .tools import CallException, expect, normalize_nfc, session


def int_to_big_endian(value):
    return value.to_bytes((value.bit_length() + 7) // 8, "big")


# ====== Client functions ====== #


@expect(proto.EthereumAddress, field="address")
def get_address(client, n, show_display=False, multisig=None):
    return client.call(proto.EthereumGetAddress(address_n=n, show_display=show_display))


@session
def sign_tx(
    client,
    n,
    nonce,
    gas_price,
    gas_limit,
    to,
    value,
    data=None,
    chain_id=None,
    tx_type=None,
):
    msg = proto.EthereumSignTx(
        address_n=n,
        nonce=int_to_big_endian(nonce),
        gas_price=int_to_big_endian(gas_price),
        gas_limit=int_to_big_endian(gas_limit),
        value=int_to_big_endian(value),
    )

    if to:
        msg.to = to

    if data:
        msg.data_length = len(data)
        data, chunk = data[1024:], data[:1024]
        msg.data_initial_chunk = chunk

    if chain_id:
        msg.chain_id = chain_id

    if tx_type is not None:
        msg.tx_type = tx_type

    response = client.call(msg)

    while response.data_length is not None:
        data_length = response.data_length
        data, chunk = data[data_length:], data[:data_length]
        response = client.call(proto.EthereumTxAck(data_chunk=chunk))

    return response.signature_v, response.signature_r, response.signature_s


@expect(proto.EthereumMessageSignature)
def sign_message(client, n, message):
    message = normalize_nfc(message)
    return client.call(proto.EthereumSignMessage(address_n=n, message=message))


def verify_message(client, address, signature, message):
    message = normalize_nfc(message)
    try:
        resp = client.call(
            proto.EthereumVerifyMessage(
                address=address, signature=signature, message=message
            )
        )
    except CallException as e:
        resp = e
    if isinstance(resp, proto.Success):
        return True
    return False
