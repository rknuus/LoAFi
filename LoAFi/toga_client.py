# Copyright (C) 2021 R. Knaus

import toga


def button_handler(widget):
    print("hello")


def build(app):
    box = toga.Box()

    raw_log_view = toga.MultilineTextInput(id='raw_log_view', readonly=True)
    raw_log_view.style.flex = 1
    raw_log_view.style.padding = 5
    box.add(raw_log_view)

    with open('/home/users/knausr/tmp/support-NewGen-IM-IC-connection-issue-losing-samples/logs-of-reproduced-case-with-extra-sniffing/logs/combined-syslog') as file:
        raw_log_view.value = file.read()

    filtered_log_view = toga.MultilineTextInput(id='filtered_log_view',
                                                readonly=True)
    filtered_log_view.style.flex = 1
    filtered_log_view.style.padding = 5
    box.add(filtered_log_view)

    return box


def main():
    return toga.App('LoAFi', 'com.github.rknuus',
                    startup=build)


if __name__ == '__main__':
    main().main_loop()
