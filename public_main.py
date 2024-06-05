from pywinauto import application
from pywinauto.timings import Timings
import time

# Constants
PASSCODE = "111111"
PASSAPP_EXE_PATH = r"C:\path\to\authentication\app.exe"
VPN_EXE_PATH = r"C:\path\to\vpnclient.exe"
PASSAPP_WINDOW_TITLE = "PASSAPP"
PASSAPP_ITEM_TEXT = "texty-text"
PASSAPP_COPY_BUTTON_TITLE = "Copy Passcode"
VPN_MAIN_WINDOW_TITLE = "VPN Client"
VPN_NEW_WINDOW_TITLE = "VPN Client .* - WEBZ"
VPN_ACCEPT_WINDOW_TITLE = "VPN Client"

# Set timings to be a bit more lenient
Timings.window_find_timeout = 20
Timings.window_find_retry = 2

# Start the PASSAPP application
pass_app = application.Application().start(PASSAPP_EXE_PATH)

# Wait for the PASSAPP window to appear
pass_window = pass_app.window(title_re=PASSAPP_WINDOW_TITLE)
pass_window.wait('visible', timeout=5)

# Interact with the ListView to find and click the item with the specified text
list_view = pass_window.child_window(class_name="SysListView32")
list_view.wait('visible', timeout=5)

# Find and click the item with the specified text
for item in list_view.items():
    if PASSAPP_ITEM_TEXT in item.text():
        item.click_input()
        break

# Wait for the new PASSAPP window to appear
new_pass_window = pass_app.window(title_re=PASSAPP_WINDOW_TITLE)
new_pass_window.wait('visible', timeout=5)

# Click on the "Copy Passcode" button
new_pass_window.child_window(title=PASSAPP_COPY_BUTTON_TITLE, class_name="Button").click()

# Close the PASSAPP application
pass_app.kill()

# Give it a moment to process
time.sleep(1)

# Start a new instance of the VPN client
vpn_app = application.Application().start(VPN_EXE_PATH)

# Wait for the main window to appear
vpn_window = vpn_app.window(title_re=VPN_MAIN_WINDOW_TITLE)
vpn_window.wait('visible', timeout=5)

# Click on the connect button
vpn_window.ConnectButton.click()

# Wait for the new window to appear
start_time = time.time()
new_window = None
while time.time() - start_time < 30:
    try:
        new_window = vpn_app.window(title_re=VPN_NEW_WINDOW_TITLE, class_name="#31787")
        if new_window.exists(timeout=1):
            break
    except Exception:
        time.sleep(1)

if new_window and new_window.exists():
    new_window.wait('visible', timeout=5)
    # Enter the passcode
    new_window.Edit2.set_edit_text(PASSCODE)

    # Paste the code from the clipboard
    new_window.Edit2.type_keys('^v')
    time.sleep(1)

    new_window.OK.click()

initial_window_count = len(vpn_app.windows())

# Do some fiti miti
start_time = time.time()
while time.time() - start_time < 30:  # Timeout after 30 seconds
    all_windows = vpn_app.windows()
    if len(all_windows) > initial_window_count:
        break
    time.sleep(1)

all_windows = vpn_app.windows()
accept_window = all_windows[0]

for button in accept_window.descendants():
    if "Accept" in button.window_text() and button.class_name() == "Button":
        button.click_input()
        break
