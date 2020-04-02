import random
from psychopy import visual
import copy


class Trial:
    def __init__(self):
        self.trial_with_distractor = None
        self.info = None
        self.upper_words = []
        self.words = []
        self.frames = []

    @staticmethod
    def __choice_word(word_bank, length, category, used_words):
        i = 0
        while True:
            word = random.choice(list(word_bank[word_bank["LENGTH"] == length][category]))
            if word not in used_words:
                return {"word": word, "length": length, "category": category}
            i += 1
            assert i < 100, "I can't find word in word_bank which was not used in last trials. Category: " + category

    def prepare_info(self, word_bank, n_answers, trial_with_distractor, task_length=None,
                     task_category=None, distractor_category=None, used_words=None):
        self.trial_with_distractor = trial_with_distractor
        if used_words is None:
            used_words = []
        all_categories = list(word_bank.columns)
        all_categories.remove("LENGTH")
        if task_category not in all_categories:
            task_category = random.choice(all_categories)
        all_categories.remove(task_category)
        if task_length is None:
            task_length = random.choice(list(set(word_bank["LENGTH"])))
        if distractor_category is None:
            distractor_category = random.choice(all_categories)
        all_categories.remove(distractor_category)

        task = self.__choice_word(word_bank, task_length, task_category, used_words)
        if trial_with_distractor == "TRUE":
            distractor = self.__choice_word(word_bank, task_length, distractor_category, used_words)
            answers = [task, distractor]
        else:
            distractor = copy.copy(task)
            answers = [task]
        upper_words = ["task", "distractor"]
        random.shuffle(upper_words)

        while len(answers) < n_answers and len(all_categories) > 0:
            answer_category = random.choice(all_categories)
            all_categories.remove(answer_category)
            answers.append(self.__choice_word(word_bank, task_length, answer_category, used_words))

        random.shuffle(answers)
        info = {"task": task,
                "distractor": distractor,
                "trial_with_distractor": trial_with_distractor,
                "upper_words": upper_words,
                "answers": answers}
        self.info = info
        print(info)

    def __calculate_extra_x_offsets(self, config, win):
        words_length = []
        for elem in self.info["answers"]:
            word = visual.TextStim(win=win, font=u'Arial', text=elem["word"], height=config["ANSWER_SIZE"])
            w, h = word.boundingBox
            words_length.append(w)
        extra_x_offsets = [0] * len(words_length)
        if len(words_length) % 2 == 0:
            extra_x_offsets[0] = words_length[0] / 2
            for i in range(int(len(words_length) / 2)):
                extra_x_offsets[0] -= words_length[i]
            for i in range(1, len(words_length)):
                extra_x_offsets[i] = extra_x_offsets[i - 1] + words_length[i - 1] / 2 + words_length[i] / 2
        elif len(words_length) % 2 == 1 and len(words_length) > 1:
            extra_x_offsets[0] = - words_length[0] / 2 - words_length[1] / 2
            for i in range(1, int((len(words_length) - 1) / 2)):
                extra_x_offsets[0] -= (words_length[i] / 2 + words_length[i + 1] / 2)
            for i in range(1, len(words_length)):
                extra_x_offsets[i] = extra_x_offsets[i - 1] + words_length[i - 1] / 2 + words_length[i] / 2
        return words_length, extra_x_offsets

    def prepare_visualisation(self, config, win):
        for i, elem in enumerate(self.info["upper_words"]):
            color = config["TASK_COLOR"] if elem == "task" else config["DISTRACTOR_COLOR"]
            word = visual.TextStim(win=win, font=u'Arial', text=self.info[elem]["word"], color=color,
                                   height=config["UPPER_WORDS_SIZE"], pos=config["UPPER_WORDS_POS_"+str(i+1)])
            self.upper_words.append(word)

        words_length, extra_x_offsets = self.__calculate_extra_x_offsets(config, win)
        for idx, elem in enumerate(self.info["answers"]):
            x = config["ANSWERS_POS"][0] - (((len(self.info["answers"]) - 1) / 2 - idx) * config["ANSWERS_OFFSET"][0]) \
                + extra_x_offsets[idx]
            y = config["ANSWERS_POS"][1] - (((len(self.info["answers"]) - 1) / 2 - idx) * config["ANSWERS_OFFSET"][1])
            word = visual.TextStim(win=win, font=u'Arial', text=elem["word"], height=config["ANSWER_SIZE"],
                                   color=config["ANSWER_COLOR"], pos=[x, y])

            frame = visual.Rect(win, width=words_length[idx] + 40, height=config["ANSWER_SIZE"] + 10,
                                pos=[x, y], lineColor=config["FRAME_COLOR"], lineWidth=config["FRAME_LINE"])
            self.words.append(word)
            self.frames.append(frame)

    def set_auto_draw(self, draw):
        for elem in self.upper_words:
            elem.setAutoDraw(draw)
        for elem in self.words:
            elem.setAutoDraw(draw)
        if not draw:
            for elem in self.frames:
                elem.setAutoDraw(draw)
