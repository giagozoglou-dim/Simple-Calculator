import PySimpleGUI as sg

from calculator import logic

FUNCTIONS = ("sin", "cos", "tan", "log", "ln")
OPERATORS = "+-*/√^"

def main_window(expanded_mode = False, saved_expression = ""):
    """
    Creates the main calculator window.
    """
    sg.theme('DarkBlue3')
    size = (4, 2)
    text = "Expand" if not expanded_mode else "Collapse"
    color = "orange" if not expanded_mode else "brown"
    layout = [
        [sg.Input(
            saved_expression, size=(35, 1), justification="right", key="-DISPLAY-",
            background_color="white", font=("Helvetica", 20),
            expand_x=True, enable_events=True
        )],
        [sg.Text("", size = (1, 4))],
            [
                sg.Button(text, key="-WIN_SIZE-", size=size, expand_x=True,
                          expand_y=True, button_color=color),
                sg.Button("AC", size=size, expand_x=True, expand_y=True,
                          button_color="red"),
                sg.Button("C", size=size, expand_x=True, expand_y=True,
                          button_color="red"),
                sg.Button("=", size=size, expand_x=True, expand_y=True,
                          button_color="purple", bind_return_key=True)
            ],
            [
                sg.Button("1", size=size, expand_x=True, expand_y=True,
                          button_color="blue"),
                sg.Button("2", size=size, expand_x=True, expand_y=True,
                          button_color="blue"),
                sg.Button("3", size=size, expand_x=True, expand_y=True,
                          button_color="blue"),
                sg.Button("+", size=size, expand_x=True, expand_y=True,
                          button_color="purple")
            ],
            [
                sg.Button("4", size=size, expand_x=True, expand_y=True,
                          button_color="blue"),
                sg.Button("5", size=size, expand_x=True, expand_y=True,
                          button_color="blue"),
                sg.Button("6", size=size, expand_x=True, expand_y=True,
                          button_color="blue"),
                sg.Button("-", size=size, expand_x=True, expand_y=True,
                          button_color="purple")
            ],
            [
                sg.Button("7", size=size, expand_x=True, expand_y=True,
                          button_color="blue"),
                sg.Button("8", size=size, expand_x=True, expand_y=True,
                          button_color="blue"),
                sg.Button("9", size=size, expand_x=True, expand_y=True,
                          button_color="blue"),
                sg.Button("*", size=size, expand_x=True, expand_y=True,
                          button_color="purple")
            ],
            [
                sg.Button(".", size=size, expand_x=True, expand_y=True,
                          button_color="blue"),
                sg.Button("0", size=size, expand_x=True, expand_y=True,
                          button_color="blue"),
                sg.Button("/", size=size, expand_x=True, expand_y=True,
                          button_color="purple")
            ]
    ]

    if expanded_mode:
        color = "green"
        layout.append([
            sg.Button("(", size=size, expand_x=True, expand_y=True,
                      button_color=color),
            sg.Button(")", size=size, expand_x=True, expand_y=True,
                      button_color=color),
            sg.Button("π", size=size, expand_x=True, expand_y=True,
                      button_color=color),
            sg.Button("e", size=size, expand_x=True, expand_y=True,
                      button_color=color)
        ])
        layout.append([
            sg.Button("sin", size=size, expand_x=True, expand_y=True,
                      button_color=color),
            sg.Button("cos", size=size, expand_x=True, expand_y=True,
                      button_color=color),
            sg.Button("tan", size=size, expand_x=True, expand_y=True,
                      button_color=color),
            sg.Button("^", size=size, expand_x=True, expand_y=True,
                      button_color=color)
        ])
        layout.append([
            sg.Button("log", size=size, expand_x=True, expand_y=True,
                      button_color=color),
            sg.Button("ln", size=size, expand_x=True, expand_y=True,
                      button_color=color),
            sg.Button("√", size=size, expand_x=True, expand_y=True,
                      button_color=color)
        ])

    new_window = sg.Window("Calculator", layout, size = (500, 500), resizable = True, finalize = True)
    return new_window

def update_display(window, text):
    """
    Updates the display of the calculator window.
    """
    display = window["-DISPLAY-"]
    assert display is not None
    display.update(value=text)

def main():
    """
    Main function to run the calculator application.
    """
    expanded_mode = False
    window = main_window()
    window.bind("<KP_Enter>", "NumpadEnter")
    window.set_min_size((500, 500))
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        saved_expression = values["-DISPLAY-"] if values else ""
        if event == "-WIN_SIZE-":
            window.close()
            expanded_mode = not expanded_mode
            window = main_window(expanded_mode=expanded_mode, saved_expression=saved_expression)
            if expanded_mode:
                window.set_min_size((500, 700))
            else:
                window.set_min_size((500, 500))
        elif event == "AC":
            update_display(window, "")
        elif event == "C":
            update_display(window, saved_expression[:-1])
        elif event == "-DISPLAY-":
            if not saved_expression:
                continue
            new_character = saved_expression[-1] if saved_expression else ""
            filtered_input = logic.filter_user_input(
                logic.ensure_proper_input(saved_expression[:-1], new_character))
            if "=" in filtered_input:
                filtered_input = filtered_input.replace("=", "")
                calculated_result = logic.calc_result(filtered_input)
                update_display(window, str(calculated_result))
            else:
                update_display(window, filtered_input)
        elif event in ("=", "NumpadEnter"):
            if saved_expression:
                calculated_result = logic.calc_result(saved_expression)
                update_display(window, str(calculated_result))
        else:
            new_expression = logic.ensure_proper_input(saved_expression, event)
            update_display(window, new_expression)
    window.close()
