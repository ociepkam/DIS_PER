import atexit
import random
from psychopy import visual, event, core, logging

from os.path import join
import csv

from sources.experiment_info import experiment_info
from sources.load_data import load_config, load_words, load_trials, load_training_trials
from sources.screen import get_screen_res, get_frame_rate
from sources.run_trial import run_trial
from sources.show_info import show_info, show_image, read_text_from_file
from sources.create_trails import create_experiment_trials, create_training_trials

part_id, part_sex, part_age, date = experiment_info()
NAME = "{}_{}_{}".format(part_id, part_sex[:1], part_age)

RESULTS = list()
RESULTS.append(['NR', 'TRAINING', 'N_ANSWERS', 'ACC', 'RT', 'UPPER_WORDS', 'TRIAL_WITH_DISTRACTOR',
                "CHOSEN_ANSWER_WORD", "CHOSEN_ANSWER_LENGTH", "CHOSEN_ANSWER_CATEGORY",
                "TASK_WORD", "TASK_LENGTH", "TASK_CATEGORY",
                "DISTRACTOR_WORD", "DISTRACTOR_CATEGORY",
                'ANSWERS'])

RAND = str(random.randint(100, 999))

logging.LogFile(join('.', 'results', 'logging', NAME + '_' + RAND + '.log'), level=logging.INFO)


@atexit.register
def save_beh():
    logging.flush()
    with open(join('results', 'behavioral_data', 'beh_{}_{}.csv'.format(NAME, RAND)), 'w') as csvfile:
        beh_writer = csv.writer(csvfile)
        beh_writer.writerows(RESULTS)


def add_trail_to_results(i, training, t, acc, rt, chosen_answer):
    global RESULTS
    RESULTS.append([i, training, len(t.words), acc, rt, t.info["upper_words"], t.trial_with_distractor,
                    chosen_answer["word"], chosen_answer["length"], chosen_answer["category"],
                    t.info["task"]["word"], t.info["task"]["length"], t.info["task"]["category"],
                    t.info["distractor"]["word"], t.info["distractor"]["category"],
                    t.info["answers"]])


config = load_config()
word_bank = load_words()

SCREEN_RES = get_screen_res()
win = visual.Window(SCREEN_RES, fullscr=True, monitor='testMonitor', units='pix', color=config["BACKGROUND_COLOR"])
FRAMES_PER_SEC = get_frame_rate(win)

clock_image = visual.ImageStim(win=win, image=join('images', 'clock.png'), interpolate=True,
                               size=config['CLOCK_SIZE'], pos=config['CLOCK_POS'])

fixation = visual.TextStim(win=win, height=config['FIXATION_SIZE'], alignHoriz='center',
                           alignVert='center', font=u'Arial', pos=config["FIXATION_POS"],
                           text=config["FIXATION_SYMBOL"], color=config["FIXATION_COLOR"])

mouse = event.Mouse()

response_clock = core.Clock()

in_trial_instruction = None
if config["SHOW_IN_TRIAL_INSTRUCTION"]:
    in_trial_instruction = visual.TextStim(win=win, height=config['IN_TRIAL_INSTRUCTION_SIZE'], alignHoriz='center',
                                           alignVert='center', font=u'Arial', pos=config["IN_TRIAL_INSTRUCTION_POS"],
                                           text=read_text_from_file(join('.', 'messages', "in_trial_instruction.txt")),
                                           wrapWidth=win.size[0], color=config["IN_TRIAL_INSTRUCTION_COLOR"])

# TRAINING 1
# show_info(win, join('.', 'messages', "instruction1.txt"), text_size=config['TEXT_SIZE'], screen_width=SCREEN_RES[0])
show_image(win, "instruction_1.jpg", size=config["INSTRUCTION_SIZE_TRAINING_1"])
training = True
training_trials_info = load_training_trials("training_1_trials.yaml")
training_trials = create_training_trials(config, win, training_trials_info)
train_clock = clock_image if config["SHOW_CLOCK_IN_TRAINING_1"] else None
for i, t in enumerate(training_trials):
    chosen_answer, acc, rt = run_trial(trial=t, config=config, response_clock=response_clock, clock_image=train_clock,
                                       fixation=fixation, win=win, instruction=in_trial_instruction, training=training,
                                       training_trial_idx=i, mouse=mouse, stim_time=config["STIM_TIME_TRAINING_1"])
    add_trail_to_results(i, training, t, acc, rt, chosen_answer)

n_trails_training_1 = len(training_trials)

# TRAINING 2
# show_info(win, join('.', 'messages', "instruction1.txt"), text_size=config['TEXT_SIZE'], screen_width=SCREEN_RES[0])
show_image(win, "instruction_2.jpg", size=config["INSTRUCTION_SIZE_TRAINING_2"])
training = True
training_trials_info = load_training_trials("training_2_trials.yaml")
training_trials = create_training_trials(config, win, training_trials_info)
for i, t in enumerate(training_trials):
    chosen_answer, acc, rt = run_trial(trial=t, config=config, response_clock=response_clock, clock_image=clock_image,
                                       mouse=mouse, win=win, instruction=in_trial_instruction, training=training,
                                       training_trial_idx=i+n_trails_training_1, fixation=fixation,
                                       stim_time=config["STIM_TIME"])
    add_trail_to_results(i, training, t, acc, rt, chosen_answer)


# EXPERIMENT
# show_info(win, join('.', 'messages', "instruction2.txt"), text_size=config['TEXT_SIZE'], screen_width=SCREEN_RES[0])
show_image(win, "instruction_3.jpg", size=config["INSTRUCTION_SIZE_EXPERIMENT"])
training = False
trials_info = load_trials()

if config["SHUFFLE_TRIALS"]:
    random.shuffle(trials_info)
trials = create_experiment_trials(config=config, win=win, word_bank=word_bank, trials_info=trials_info)


for i, t in enumerate(trials):
    chosen_answer, acc, rt = run_trial(trial=t, config=config, response_clock=response_clock, clock_image=clock_image,
                                       mouse=mouse, win=win, instruction=in_trial_instruction, training=training,
                                       fixation=fixation, stim_time=config["STIM_TIME"])
    add_trail_to_results(i, training, t, acc, rt, chosen_answer)

show_info(win, join('.', 'messages', "end.txt"), text_size=config['TEXT_SIZE'], screen_width=SCREEN_RES[0])