from psychopy import logging, visual, event
from collections import OrderedDict


def get_screen_res():
    """
    Funcion that check current screen resolution. Raise OSError if can't recognise OS!
    * :return: (width, height) tuple with screen resolution.
    """
    import platform

    system = platform.system()
    if 'Linux' in system:
        width, height = [int(x) for x in "b'1920x1080\n'".split('\'')[1].split('\n')[0].split('x')]
    elif 'Windows' in system:
        from win32api import GetSystemMetrics

        width = int(GetSystemMetrics(0))
        height = int(GetSystemMetrics(1))
    else:  # can't recognise OS
        logging.ERROR('OS ERROR - no way of determine screen res')
        raise OSError("get_screen_res function can't recognise your OS")
    logging.info('Screen res set as: {}x{}'.format(width, height))

    return [width, height]


def get_frame_rate(win, legal_frame_rates=(60, 30)):
    frame_rate = 60  # int(round(win.getActualFrameRate(nIdentical=30, nMaxFrames=200)))
    logging.info("Detected framerate: {} frames per sec.".format(frame_rate))
    assert frame_rate in legal_frame_rates, 'Illegal frame rate.'
    return frame_rate


def create_win(screen_color):
    """
    zwraca ekran na ktorym bedzie wszystko wyswietlane
    wylacza myszke
    :param screen_color: kolor tla
    :return: zwraca ekran na ktorym bedzie wszystko wyswietlane
    """
    screen_res = get_screen_res()
    win = visual.Window(screen_res, fullscr=True, monitor='TestMonitor',
                        units='pix', screen=0, color=screen_color)
    event.Mouse(visible=False, newPos=None, win=win)
    win.flip()
    frames_per_sec = get_frame_rate(win=win)
    return win, screen_res, frames_per_sec
