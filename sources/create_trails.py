from sources.trial import Trial


def get_used_words(trial):
    return [trial.info["task"]["word"]] + [elem["word"] for elem in trial.info["answers"]]


def update_used_words(used_words, trial, n_back=2):
    used_words.append(get_used_words(trial))
    if len(used_words) > n_back:
        used_words = used_words[1:]
    return used_words


def create_experiment_trials(config, win, word_bank, trials_info):
    trials = []
    used_words = []
    for trial in trials_info:
        t = Trial()
        t.prepare_info(word_bank=word_bank, n_answers=trial["N_ANSWERS"], task_length=trial["TASK_LENGTH"],
                       trial_with_distractor=trial["DISTRACTOR"], distractor_category=trial["DISTRACTOR_CATEGORY"],
                       task_category=trial["TASK_CATEGORY"], used_words=[y for x in used_words for y in x])
        used_words = update_used_words(used_words, t, config["N_BACK"])
        t.prepare_visualisation(config, win)
        trials.append(t)
    return trials


def create_training_trials(config, win, trials_description):
    trials = []
    for _, trial in trials_description.items():
        t = Trial()
        t.info = trial
        t.trial_with_distractor = trial["trial_with_distractor"]
        t.prepare_visualisation(config, win)
        trials.append(t)
    return trials
