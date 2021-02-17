# isort:skip_file

from trezor import loop, utils, wire, workflow

unimport_manager = utils.unimport()

# unlock the device
with unimport_manager:
    import boot

    del boot

# prepare the USB interfaces, but do not connect to the host yet
import usb

# start the USB
usb.bus.open()


def _boot_apps() -> None:
    # load applications
    import apps.base

    apps.base.boot()

    if not utils.BITCOIN_ONLY:
        import apps.webauthn

        apps.webauthn.boot()

    if __debug__:
        import apps.debug

        apps.debug.boot()

    with unimport_manager:
        import register_messages

        del register_messages

    # run main event loop and specify which screen is the default
    apps.base.set_homescreen()
    workflow.start_default()


_boot_apps()

# initialize the wire codec
wire.setup(usb.iface_wire)
if __debug__:
    wire.setup(usb.iface_debug, use_workflow=False)

loop.run()

# loop is empty. That should not happen
utils.halt("All tasks have died.")
