# isort:skip_file
import storage
import storage.device
if __debug__:
    import storage.debug

# Import always-active modules
from trezor import config, pin, utils

# Prepare the USB interfaces first. Do not connect to the host yet.
import usb
#from trezor import pin, utils

unimport_manager = utils.unimport()

# unlock the device, unload the boot module afterwards
with unimport_manager:
    import boot

    del boot

# start the USB
usb.bus.open(storage.device.get_device_id())

while True:
    with unimport_manager:
        import session

        del session

    print("reboot")
    #utils.mem_dump("reboot.json")
