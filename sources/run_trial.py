from psychopy import event, visual
import time
import random
from sources.check_exit import check_exit
from sources.show_info import read_text_from_file
from os.path import join


def run_trial(trial, config, response_clock, clock_image, mouse, win, fixation, stim_time,
              instruction=None, training=False, training_trial_idx=None):
    win.callOnFlip(response_clock.reset)
    win.flip()
    while response_clock.getTime() < config["FIXATION_TIME"]:
        fixation.draw(win)
        win.flip()

    acc = -1
    chosen_answer = {"word": None, "length": None, "category": None}
    rt = None
    trial.set_auto_draw(True)
    if instruction is not None:
        instruction.setAutoDraw(True)
    clock_is_shown = False
    win.callOnFlip(response_clock.reset)
    win.flip()
    event.clearEvents()

    while response_clock.getTime() < stim_time and acc == -1:
        for idx, frame in enumerate(trial.frames):
            if frame.contains(mouse.getPos()) and config["SHOW_FRAMES"]:
                frame.draw()
            if mouse.isPressedIn(frame):
                chosen_answer = trial.info["answers"][idx]
                acc = chosen_answer == trial.info["task"]
                rt = response_clock.getTime()
                break

        if clock_image is not None and \
                not clock_is_shown and \
                config["STIM_TIME"] - response_clock.getTime() < config["SHOW_CLOCK"]:
            clock_image.setAutoDraw(True)
            clock_is_shown = True
            win.flip()

        check_exit()
        win.flip()
    if clock_image is not None:
        clock_image.setAutoDraw(False)
    if training:
        if acc == 1:
            feedback_file_name = "feedback_positive.txt"
        elif acc == -1:
            feedback_file_name = "feedback_no_answer.txt"
        else:
            feedback_file_name = "feedback_negative.txt"
        text = read_text_from_file(join('.', 'messages', feedback_file_name)) + \
               read_text_from_file(join('.', 'messages', "feedback_info_{}.txt".format(training_trial_idx + 1)))

        feedback = visual.TextStim(win=win, height=config['FEEDBACK_SIZE'], alignHoriz='center', alignVert='center',
                                   font=u'Arial', pos=config["FEEDBACK_POS"], text=text, wrapWidth=win.size[0],
                                   color=config["FEEDBACK_COLOR"])
        feedback.setAutoDraw(True)

        answer_idx = trial.info["answers"].index(trial.info["task"])
        trial.frames[answer_idx].lineColor = config["FRAME_COLOR_CORR"]
        trial.frames[answer_idx].setAutoDraw(True)
        if not acc:
            chosen_idx = trial.info["answers"].index(chosen_answer)
            trial.frames[chosen_idx].lineColor = config["FRAME_COLOR_WRONG"]
            trial.frames[chosen_idx].setAutoDraw(True)

        win.flip()
        event.waitKeys(keyList=['space'])
        feedback.setAutoDraw(False)

    trial.set_auto_draw(False)
    if instruction is not None:
        instruction.setAutoDraw(False)
    win.flip()
    time.sleep(config["WAIT_TIME"] + random.uniform(config["WAIT_JITTER"][0], config["WAIT_JITTER"][1]))

    return chosen_answer, acc, rt
