
import sys

try:
    import win32con
    import win32gui
except ImportError:
    sys.exit('Error: pywin32 package missing. Install it from\n'
        'http://sourceforge.net/projects/pywin32/files/')

try:
    # python 3
    import winreg
    from winreg import (
        HKEY_CURRENT_USER, HKEY_LOCAL_MACHINE,
        KEY_ALL_ACCESS, KEY_READ, REG_EXPAND_SZ,
    )
except ImportError:
    # python 2
    import _winreg as winreg
    from _winreg import (
        HKEY_CURRENT_USER, HKEY_LOCAL_MACHINE,
        KEY_ALL_ACCESS, KEY_READ, REG_EXPAND_SZ,
    )


# Registry key where environment variables are stored
# False=machine, True=user
REG_KEY = {
    False:
        (HKEY_LOCAL_MACHINE,
        r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment'),
    True:
        (HKEY_CURRENT_USER,
        'Environment'),
}


def get_env_registry(name, user=True):
    root, subkey = REG_KEY[user]
    key = winreg.OpenKey(root, subkey, 0, KEY_READ)
    try:
        value, _ = winreg.QueryValueEx(key, name)
    except WindowsError:
        return None
    return value


def set_env_registry(name, value, user=True):
    '''
    Set environment variable name=value, in the registry so it is persisted.
    'user' determines whether it is set machine-wide, or for current user.
    SendMessage broadcasts the change to windows taskbar (and other interested
    processes) so that it knows about the change, and launches any new
    processes with the new values. New processes will see the change, existing
    ones (including the shell that started this python script) will not.
    Set value==None to delete the variable.
    '''
    root, subkey = REG_KEY[user]
    key = winreg.OpenKey(root, subkey, 0, KEY_ALL_ACCESS)
    if value is not None:
        winreg.SetValueEx(key, name, 0, REG_EXPAND_SZ, value)
    else:
        try:
            winreg.DeleteValue(key, name)
        except WindowsError:
            pass # name did not exist
    winreg.CloseKey(key)
    win32gui.SendMessage(
        win32con.HWND_BROADCAST, win32con.WM_SETTINGCHANGE, 0, 'Environment')

