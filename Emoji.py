# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sublime
import sublime_plugin
import os
import codecs
import re


def load_emoji():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "emoji-data.txt")
    f = codecs.open(path, encoding="utf-8")
    data = []
    names = {}
    for line in f:
        if line[0] == "#":
            continue
        code, emoji, name = re.findall("^([A-Z0-9 ]+) ;.+\((.+)\) (.+)", line)[0]
        names[code] = name
        name = name.title()
        data.append([code, emoji, name, "{} {} ({})".format(emoji, name, code)])

    return sorted(data, key=lambda x: names[x[0]])


class InsertEmojiCommand(sublime_plugin.TextCommand):

    def run(self, edit, emoji):
        sublime.status_message("ran")
        for sel in self.view.sel():
            self.view.insert(edit, sel.begin(), emoji)


class SelectEmojiCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        window = sublime.active_window()
        data = load_emoji()
        items = [t[-1] for t in data]

        def callback(selection):
            emoji = data[selection][1]
            self.view.run_command("insert_emoji", {"emoji": emoji})

        window.show_quick_panel(items, callback)
