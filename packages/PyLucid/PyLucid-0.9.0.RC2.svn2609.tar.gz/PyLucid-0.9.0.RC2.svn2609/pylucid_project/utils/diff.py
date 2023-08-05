# -*- coding: utf-8 -*-
"""
    PyLucid.utils.diff
    ~~~~~~~~~~~~~~~~~~

    combine difflib.Differ() with pygments.

    Used request.render.highlight or request.render.get_hightlighted


    example-1::
        from PyLucid.tools.Diff import display_diff
        display_diff(file_content, db_content, self.request)

    example-2::
        from PyLucid.tools.Diff import get_diff
        html_diff_page = get_diff(file_content, db_content, self.request)
        self.response.write(html_diff_page)


    Last commit info:
    ~~~~~~~~~~~~~~~~~
    $LastChangedDate: 2009-12-08 11:17:22 +0100 (Di, 08. Dez 2009) $
    $Rev: 2477 $
    $Author: JensDiemer $

    :copyleft: 2007-2009 by the PyLucid team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""


import difflib

from pylucid_project.apps.pylucid.markup.hightlighter import pygmentize


def diff_lines(content1, content2):
    """
    Display a diff without pygments.
    """
    results = []
    diff = make_diff(content1, content2)

    def is_diff_line(line):
        for char in ("-", "+", "?"):
            if line.startswith(char):
                return True
        return False

    old_line = ""
    in_block = False
    old_lineno = lineno = 0
    for line in diff:
        if line.startswith(" ") or line.startswith("+"):
            lineno += 1

        if old_lineno == lineno:
            display_line = "%4s | %s" % ("", line.rstrip())
        else:
            display_line = "%4s | %s" % (lineno, line.rstrip())

        if is_diff_line(line):
            if not in_block:
                results.append("...")
                # Display previous line
                results.append(old_line)
                in_block = True

            results.append(display_line)
        else:
            if in_block:
                # Display the next line after a diff-block
                results.append(display_line)
            in_block = False

        old_line = display_line
        old_lineno = lineno
    results.append("...")

    return "\n".join(results)


def get_pygmentize_diff(content1, content2):
    """
    returns the HTML-Diff hightlighted with Pygments
    Note: the complete content will be returned and not only the "diff-lines".
    """
    diff = make_diff(content1, content2, mode="Differ")
    diff = "\n".join(diff)

    # hightlight with Pygments
    diff, _ = pygmentize(diff, source_type="diff")

    return diff


def make_diff(content1, content2, mode="Differ"):
    """
    returns the diff as a String, made with difflib.Differ.
    """
    def prepare(content):
        if isinstance(content, (list, tuple)):
            return content

        return content.splitlines()

    content1 = prepare(content1)
    content2 = prepare(content2)

    if mode == "Differ":
        diff = difflib.Differ().compare(content1, content2)
    elif mode == "HtmlDiff":
        diff = difflib.HtmlDiff(tabsize=4).make_table(content1, content2)

    return diff
