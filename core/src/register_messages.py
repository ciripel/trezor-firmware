from trezor import utils

# load applications
import apps.management
import apps.bitcoin
import apps.misc

if not utils.BITCOIN_ONLY:
    import apps.ethereum
    import apps.lisk
    import apps.monero
    import apps.nem
    import apps.stellar
    import apps.ripple
    import apps.cardano
    import apps.tezos
    import apps.eos
    import apps.binance

# boot applications
apps.management.boot()
apps.bitcoin.boot()
apps.misc.boot()
if not utils.BITCOIN_ONLY:
    apps.ethereum.boot()
    apps.lisk.boot()
    apps.monero.boot()
    apps.nem.boot()
    apps.stellar.boot()
    apps.ripple.boot()
    apps.cardano.boot()
    apps.tezos.boot()
    apps.eos.boot()
    apps.binance.boot()
