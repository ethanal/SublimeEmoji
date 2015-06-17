# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sublime
import sublime_plugin
import re


def load_emoji():
    f = sublime.load_binary_resource("/".join(("Packages", __package__, "emoji-data.txt")))
    lines = f.decode("utf-8").strip().split("\n")
    data = []
    names = {}

    for line in lines:
        if line[0] == "#":
            continue
        code, emoji, name = re.findall("^([A-Z0-9 ]+) ;.+\((.+)\) (.+)", line)[0]
        names[code] = name
        name = name.title()
        data.append([code, emoji, name, "{} {} ({})".format(emoji, name, code)])

    return sorted(data, key=lambda x: names[x[0]])


class InsertEmojiCommand(sublime_plugin.TextCommand):

    def run(self, edit, emoji):
        for sel in self.view.sel():
            self.view.insert(edit, sel.begin(), emoji)


class SelectEmojiCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        window = self.view.window()
        data = load_emoji()
        items = [t[-1] for t in data]

        def callback(selection):
            if selection >= 0:
                emoji = data[selection][1]
                self.view.run_command("insert_emoji", {"emoji": emoji})

        window.show_quick_panel(items, callback)
