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

import time

import pytest
from mnemonic import Mnemonic

from trezorlib import device, messages as proto

from .common import TrezorTest, generate_entropy


@pytest.mark.skip_t1
class TestMsgResetDeviceT2(TrezorTest):
    def test_reset_device(self):

        # No PIN, no passphrase, don't display random
        external_entropy = b"zlutoucky kun upel divoke ody" * 2
        strength = 128
        ret = self.client.call_raw(
            proto.ResetDevice(
                display_random=False,
                strength=strength,
                passphrase_protection=False,
                pin_protection=False,
                label="test",
            )
        )

        # Provide entropy
        assert isinstance(ret, proto.EntropyRequest)
        internal_entropy = self.client.debug.read_reset_entropy()
        ret = self.client.call_raw(proto.EntropyAck(entropy=external_entropy))

        # Generate mnemonic locally
        entropy = generate_entropy(strength, internal_entropy, external_entropy)
        expected_mnemonic = Mnemonic("english").to_mnemonic(entropy)

        # Safety warning
        assert isinstance(ret, proto.ButtonRequest)
        self.client.debug.press_yes()
        ret = self.client.call_raw(proto.ButtonAck())

        # List through mnemonic pages
        assert isinstance(ret, proto.ButtonRequest)
        self.client.transport.write(proto.ButtonAck())
        self.client.debug.press_yes()
        words = []
        time.sleep(1)
        words.extend(self.client.debug.read_reset_word().split())
        self.client.debug.swipe_down()
        time.sleep(1)
        words.extend(self.client.debug.read_reset_word().split())
        self.client.debug.swipe_down()
        time.sleep(1)
        words.extend(self.client.debug.read_reset_word().split())

        # Compare that device generated proper mnemonic for given entropies
        assert " ".join(words) == expected_mnemonic

        # Confirm the mnemonic
        self.client.debug.press_yes()

        # Check mnemonic words
        time.sleep(1)
        index = self.client.debug.read_reset_word_pos()
        self.client.debug.input(words[index])
        time.sleep(1)
        index = self.client.debug.read_reset_word_pos()
        self.client.debug.input(words[index])
        ret = self.client.transport.read()

        # Safety warning
        assert isinstance(ret, proto.ButtonRequest)
        self.client.debug.press_yes()
        ret = self.client.call_raw(proto.ButtonAck())
        assert isinstance(ret, proto.Success)

        # Check if device is properly initialized
        resp = self.client.call_raw(proto.Initialize())
        assert resp.initialized is True
        assert resp.needs_backup is False
        assert resp.pin_protection is False
        assert resp.passphrase_protection is False

    def test_reset_device_pin(self):

        # PIN, passphrase, display random
        external_entropy = b"zlutoucky kun upel divoke ody" * 2
        strength = 128
        ret = self.client.call_raw(
            proto.ResetDevice(
                display_random=True,
                strength=strength,
                passphrase_protection=True,
                pin_protection=True,
                label="test",
            )
        )

        # Enter PIN for first time
        assert isinstance(ret, proto.ButtonRequest)
        self.client.debug.input("654")
        ret = self.client.call_raw(proto.ButtonAck())

        # Enter PIN for second time
        assert isinstance(ret, proto.ButtonRequest)
        self.client.debug.input("654")
        ret = self.client.call_raw(proto.ButtonAck())

        # Confirm entropy
        assert isinstance(ret, proto.ButtonRequest)
        self.client.debug.press_yes()
        ret = self.client.call_raw(proto.ButtonAck())

        # Provide entropy
        assert isinstance(ret, proto.EntropyRequest)
        internal_entropy = self.client.debug.read_reset_entropy()
        ret = self.client.call_raw(proto.EntropyAck(entropy=external_entropy))

        # Generate mnemonic locally
        entropy = generate_entropy(strength, internal_entropy, external_entropy)
        expected_mnemonic = Mnemonic("english").to_mnemonic(entropy)

        # Safety warning
        assert isinstance(ret, proto.ButtonRequest)
        self.client.debug.press_yes()
        ret = self.client.call_raw(proto.ButtonAck())

        # List through mnemonic pages
        assert isinstance(ret, proto.ButtonRequest)
        self.client.transport.write(proto.ButtonAck())
        self.client.debug.press_yes()
        words = []
        time.sleep(1)
        words.extend(self.client.debug.read_reset_word().split())
        self.client.debug.swipe_down()
        time.sleep(1)
        words.extend(self.client.debug.read_reset_word().split())
        self.client.debug.swipe_down()
        time.sleep(1)
        words.extend(self.client.debug.read_reset_word().split())

        # Compare that device generated proper mnemonic for given entropies
        assert " ".join(words) == expected_mnemonic

        # Confirm the mnemonic
        self.client.debug.press_yes()

        # Check mnemonic words
        time.sleep(1)
        index = self.client.debug.read_reset_word_pos()
        self.client.debug.input(words[index])
        time.sleep(1)
        index = self.client.debug.read_reset_word_pos()
        self.client.debug.input(words[index])
        ret = self.client.transport.read()

        # Safety warning
        assert isinstance(ret, proto.ButtonRequest)
        self.client.debug.press_yes()
        ret = self.client.call_raw(proto.ButtonAck())
        assert isinstance(ret, proto.Success)

        # Check if device is properly initialized
        resp = self.client.call_raw(proto.Initialize())
        assert resp.initialized is True
        assert resp.needs_backup is False
        assert resp.pin_protection is True
        assert resp.passphrase_protection is True

    def test_failed_pin(self):
        # external_entropy = b'zlutoucky kun upel divoke ody' * 2
        strength = 128
        ret = self.client.call_raw(
            proto.ResetDevice(strength=strength, pin_protection=True, label="test")
        )

        # Enter PIN for first time
        assert isinstance(ret, proto.ButtonRequest)
        self.client.debug.input("654")
        ret = self.client.call_raw(proto.ButtonAck())

        # Enter PIN for second time
        assert isinstance(ret, proto.ButtonRequest)
        self.client.debug.input("456")
        ret = self.client.call_raw(proto.ButtonAck())

        assert isinstance(ret, proto.ButtonRequest)

    def test_already_initialized(self):
        self.setup_mnemonic_nopin_nopassphrase()
        with pytest.raises(Exception):
            device.reset(self.client, False, 128, True, True, "label", "english")
