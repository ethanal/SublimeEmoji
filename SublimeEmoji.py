# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sublime
import sublime_plugin
import re


def load_emoji():
    f = sublime.load_binary_resource("/".join(("Packages", __package__, "emoji-test.txt")))
    lines = f.decode("utf-8").strip().split("\n")
    data = []
    names = {}

    for line in lines:
        if not line or line[0] == "#":
            continue

        code = line.split(';')[0].strip()
        emoji = line.split('#')[1].strip().split(' ')[0]
        name = ' '.join((line.split('#')[1].strip().split(' ')[1:999]))
        names[code] = name
        name = name.title()
        data.append([code, emoji, name, "{} {} ({})".format(emoji, name, code)])

    return sorted(data, key=lambda x: names[x[0]])


class SelectEmojiCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        window = self.view.window()
        data = load_emoji()
        items = [t[-1] for t in data]

        def callback(selection):
            if selection >= 0:
                emoji = data[selection][1]
                self.view.run_command("insert", {"characters": emoji})

        window.show_quick_panel(items, callback)
