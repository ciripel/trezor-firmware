# This file is part of the Trezor project.
#
# Copyright (C) 2012-2018 SatoshiLabs and contributors
#
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version 3
# as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the License along with this library.
# If not, see <https://www.gnu.org/licenses/lgpl-3.0.html>.

from binascii import hexlify

import pytest

from trezorlib import messages, stellar
from trezorlib.tools import CallException, parse_path

from .common import TrezorTest
from .conftest import TREZOR_VERSION


@pytest.mark.stellar
class TestMsgStellarGetPublicKey(TrezorTest):
    def test_stellar_get_public_key(self):
        self.setup_mnemonic_nopin_nopassphrase()

        # GAK5MSF74TJW6GLM7NLTL76YZJKM2S4CGP3UH4REJHPHZ4YBZW2GSBPW
        response = stellar.get_public_key(
            self.client, parse_path(stellar.DEFAULT_BIP32_PATH), show_display=True
        )
        assert (
            hexlify(response)
            == b"15d648bfe4d36f196cfb5735ffd8ca54cd4b8233f743f22449de7cf301cdb469"
        )
        assert (
            stellar.address_from_public_key(response)
            == "GAK5MSF74TJW6GLM7NLTL76YZJKM2S4CGP3UH4REJHPHZ4YBZW2GSBPW"
        )

    def test_stellar_get_public_key_fail(self):
        self.setup_mnemonic_nopin_nopassphrase()

        with pytest.raises(CallException) as exc:
            stellar.get_public_key(self.client, parse_path("m/0/1"))

        if TREZOR_VERSION == 1:
            assert exc.value.args[0] == messages.FailureType.ProcessError
            assert exc.value.args[1].endswith("Failed to derive private key")
        else:
            assert exc.value.args[0] == messages.FailureType.FirmwareError
            assert exc.value.args[1].endswith("Firmware error")
