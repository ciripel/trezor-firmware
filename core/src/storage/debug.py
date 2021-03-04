from trezorutils import halt

if not __debug__:
    halt("Debugging is disabled")

if __debug__:
    save_screen = False
    save_screen_directory = "."

    current_content: list[str] = []
    watch_layout_changes = False

    reset_internal_entropy: bytes = b""
