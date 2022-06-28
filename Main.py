# By Yash Mishra

import time
from termcolor import colored


# generates one truth table
def generate_truth_table():
    props = get_props()  # gets proposition names from user and the number of table columns so far

    num_rows = 2 ** len(props)  # each value is either T or F, so number of rows will be 2 ** number of propositions
    num_cols = len(props)

    operators = ['~', '&', '|', '#', '->', '<->']

    calculated_props = get_calculated_props(props, len(props) + 1, operators)  # gets calculated propositions from user
    num_cols += len(calculated_props)  # increments the number of columns by the number of propositions to calculate

    combination = props + calculated_props  # list of all propositions (including calculated ones)

    positions = {}
    for i in range(len(combination)):
        positions[combination[i]] = i  # maps each proposition to its index in the combination list

    table = [[None for _ in range(num_cols)] for _ in range(num_rows)]  # initializes the Table
    formatted_combination = props.copy()

    start = time.time()

    generate_true_false_combinations(table, len(props))  # generates all T/F combinations for the props
    compute(table, props, combination, formatted_combination, positions)  # computes calculated propositions

    end = time.time()

    elapsed_time = end - start
    elapsed_time_in_ms = elapsed_time * 1000

    print(colored(f"Truth Table Generation and Requested Computations successfully "
                  f"completed in {elapsed_time_in_ms} milliseconds.", "blue"))

    number_format_requested = print_format_is_numbers()  # true if user wants 1/0 format, false for T/F format

    print_table(table, formatted_combination, num_rows, num_cols, number_format_requested)  # prints the table


# gets props from the user and does input validation
def get_props():
    print("Enter proposition names. Each should be one character, and no character can be repeated. When you are done "
          "inputting characters, hit enter.")
    props = []
    i = 1
    while True:
        prop_input = input(f"Proposition {i} (Table Column {i}): ")
        if len(prop_input) < 1:
            print("\n")
            return props
        elif len(prop_input) > 1:
            print(colored("\tProposition names can only be one character. Please try again.", "red"))
        elif not prop_input.isalpha():
            print(colored("\tProposition names can only be alphabetic characters. Please try again.", "red"))
        elif prop_input.lower() in props:
            print(colored("\tYou may not enter the same proposition name twice. Please try again.", "red"))
        else:
            lowercase_prop_input = prop_input.lower()
            print(colored(f"\tTable Column {i} set to " + lowercase_prop_input, "green"))
            props.append(lowercase_prop_input)
            i += 1


# gets calculated props from the user and does input validation
def get_calculated_props(props, current_column, operators):
    print("Enter propositions to compute. Separate each with a single space. Use '~' for negation, '&' for 'and', '|' "
          "for 'or', '#' for exclusive or, '->' for implication, or '<->' for biconditional.")
    print("Each expression must have one operator and a term before and after (like p->q). However, for doing negation,"
          " use only one term after the '~' and nothing before (like ~p).")
    print("If you would like to have one of the terms be a previous computed expression, then use its column "
          "number in the table.")
    print("When you are done inputting propositions to compute, hit enter.\n")
    print("For example, let's say you inputted propositions p, q, and r. Those correspond to columns 1, 2, "
          "and 3 respectively. Below is one way to compute (~r)|(p&(q->r)).")
    print("First, enter ~r. That now corresponds to column 4.")
    print("Then, enter q->r. That now corresponds to column 5.")
    print("Then, enter p&5 to compute p&(q->r) (because column 5 has q->r). That now corresponds to column 6.")
    print("Then, enter 4|6 to compute (~r)|(p&(q->r). That now corresponds to column 7.")
    print("Finally, hit enter to move on.\n")

    calculated_props = []

    valid_symbols = props + [str((i + 1)) for i in range(len(props))]  # column numbers start at 1

    while True:
        print(colored("Valid Symbols to use in your expression: ", "yellow"), colored(valid_symbols, "yellow"))
        print(colored("Valid Operators to use in your expression: ", "yellow"), colored(operators, "yellow"))
        input_is_valid = True
        left_term = ""
        right_term = ""
        i = 0
        calculated_prop_input = input(f"Calculated Proposition {current_column - len(props)} (Table Column "
                                      f"{current_column}): ").lower()

        if len(calculated_prop_input) < 1:
            return calculated_props

        if calculated_prop_input in calculated_props:
            print(colored("\tYou may not request the same computation twice. Please try again", "red"))
            continue
        operator_has_been_used = False
        while i in range(len(calculated_prop_input)):
            char = calculated_prop_input[i]
            if char.isdigit():  # if digit, concatenate with the following digits
                while (i + 1) < len(calculated_prop_input) and calculated_prop_input[i + 1].isdigit():
                    char += calculated_prop_input[i + 1]
                    i += 1

            implication_detected = i < len(calculated_prop_input) - 1 and char == '-' \
                                   and calculated_prop_input[i + 1] == ">"
            biconditional_detected = i < len(calculated_prop_input) - 2 and char == '<' \
                                     and calculated_prop_input[i + 1] == "-" and \
                                     calculated_prop_input[i + 2] == ">"

            if char in operators or implication_detected or biconditional_detected:
                if operator_has_been_used:
                    input_is_valid = False
                    print(colored("\tYou cannot use an operator more than once in one expression. Use column numbers to"
                                  " simplify operations. Please try again.", "red"))
                else:
                    operator_has_been_used = True
            else:
                if operator_has_been_used:
                    right_term += char
                else:
                    left_term += char

            if implication_detected:
                i += 2
                continue
            elif biconditional_detected:
                i += 3
                continue

            if char not in valid_symbols and char not in operators:
                input_is_valid = False
                print(colored("\tYour input contains an invalid character. You may only enter proposition names, "
                              "an operator, or an already created column number. Please try again.", "red"))
            i += 1

        if operator_has_been_used:  # only validate left and right terms if an operator has been detected
            if len(left_term) == 0:
                if '~' not in calculated_prop_input:
                    print(colored("\tYou must have a left term before the operator unless your operator is '~'. "
                                  "Please try again.", "red"))
                    input_is_valid = False
            elif len(left_term) > 1:
                if '~' in calculated_prop_input:
                    print(colored("\tIf your operator is '~' you may not have a left term. Please try again.", "red"))
                    input_is_valid = False
                else:
                    if not left_term.isnumeric():
                        print(colored("\tThe length of the left term must be one. Please try again.", "red"))
                        input_is_valid = False
            else:
                if '~' in calculated_prop_input:
                    print(colored("\tIf your operator is '~' you may not have a left term. Please try again.", "red"))
                    input_is_valid = False

            if len(right_term) == 0:
                print(colored("\tYou must have a right term after the operator. Please try again.", "red"))
                input_is_valid = False
            elif len(right_term) > 1:
                if not right_term.isnumeric():
                    print(colored("\tThe length of the right term must be one. Please try again.", "red"))
                    input_is_valid = False
        else:
            print(colored("\tYou must have one operator in your expression. Please try again.", "red"))
            input_is_valid = False

        if input_is_valid:
            print(colored(f"\tTable Column {current_column} set to {calculated_prop_input}", "green"))
            valid_symbols.append(str(current_column))
            calculated_props.append(calculated_prop_input)
            i += 1
            current_column += 1
        else:
            continue


# adds true false combinations for the propositions in the following pattern:
# T     T     T
# T     T     F
# T     F     T
# T     F     F
# F     T     T
# F     T     F
# F     F     T
# F     F     F
# algorithm time complexity is O(columns * rows), and goes column-by-column
def generate_true_false_combinations(table, num_props_columns):
    for j in range(num_props_columns):
        original_switch = len(table) // (2 ** (j + 1))
        switch = original_switch
        populate_value = True
        for i in range(len(table)):
            if i == switch:
                populate_value = not populate_value
                switch += original_switch
            table[i][j] = populate_value


# returns index of first digit in expression, or returns -1 if no digit is found in the expression
def first_digit_index(expression):
    for i in range(len(expression)):
        if expression[i].isdigit():
            return i
    return -1


# converts an expression into a formatted list
def generate_formatted_list(expression):
    formatted_list = []
    i = 0
    while i in range(len(expression)):
        if expression[i].isdigit():  # if digit, concatenate with the following digits, then append it to the list
            to_append = expression[i]
            i += 1
            while i < len(expression) and expression[i].isdigit():
                to_append += expression[i]
                i += 1
            formatted_list.append(to_append)
        else:  # if not digit, append it to the list
            formatted_list.append(expression[i])
        i += 1
    return formatted_list


# computes the calculated propositions and adds them to the table
def compute(table, props, combination, formatted_combination, positions):
    for j in range(len(props), len(combination)):
        expression = combination[j]
        left_term = ""
        operator = ""
        right_term = ""
        before_operator = True
        i = 0
        while i in range(len(expression)):
            char = expression[i]
            if char.isalpha() or char.isnumeric():
                if before_operator:
                    left_term += char  # build the left term
                else:
                    right_term += char  # build the right term
                i += 1
            else:
                before_operator = False
                while not (expression[i].isalpha() or expression[i].isnumeric()):  # build the operator
                    operator += expression[i]
                    i += 1

        formatted_left_term = generate_formatted_list(left_term)
        formatted_right_term = generate_formatted_list(right_term)

        while first_digit_index(formatted_left_term) != -1:  # converts column numbers to corresponding propositions
            temp = first_digit_index(formatted_left_term)
            formatted_left_term[temp] = formatted_combination[int(formatted_left_term[temp]) - 1]
        while first_digit_index(formatted_right_term) != -1:  # converts column numbers to corresponding propositions
            temp = first_digit_index(formatted_right_term)
            formatted_right_term[temp] = formatted_combination[int(formatted_right_term[temp]) - 1]

        if left_term.isnumeric():
            left_term = combination[int(left_term) - 1]
        if right_term.isnumeric():
            right_term = combination[int(right_term) - 1]

        left_string = ''.join(formatted_left_term)
        right_string = ''.join(formatted_right_term)

        if len(left_term) > 1:
            left_string = "(" + left_string + ")"
        if (len(right_term)) > 1:
            right_string = "(" + right_string + ")"

        formatted_combination.append(left_string + operator + right_string)

        for i in range(len(table)):
            if operator == "~":
                table[i][j] = not table[i][
                    positions[right_term]]
            elif operator == "&":
                table[i][j] = table[i][positions[left_term]] and table[i][positions[right_term]]
            elif operator == "|":
                table[i][j] = table[i][positions[left_term]] or table[i][positions[right_term]]
            elif operator == "#":
                table[i][j] = (table[i][positions[left_term]] and not table[i][positions[right_term]]) or \
                              (not table[i][positions[left_term]] and table[i][positions[right_term]])
            elif operator == "->":
                table[i][j] = (not table[i][positions[left_term]]) or table[i][positions[right_term]]
            elif operator == "<->":
                table[i][j] = table[i][positions[left_term]] == table[i][positions[right_term]]
            else:
                print(colored("\tSomething was wrong with your input. Please try again.", "red"))
                return


# returns true if user wants 1/0 format, returns false if user wants T/F format
def print_format_is_numbers():
    print_format_response = input("Would you like your results to be printed as 1/0 or T/F? Type 1 for 1/0 or "
                                  "anything else for T/F: ")
    return print_format_response == "1"


# prints out the table in the format requested by the user
def print_table(table, formatted_combination, num_rows, num_cols,
                number_format_requested):
    with open('output.txt', 'w') as f:
        longest_length = 0
        for i in range(len(formatted_combination) - 1):  # excludes the last proposition
            length = len(formatted_combination[i])
            if length > longest_length:
                longest_length = length

        spacing = " " * longest_length + "   "  # spacing of the table is based on length of longest proposition

        for i in range(num_cols):
            print(i + 1, end=spacing[len(str(i))::])  # print column numbers starting at 1
            f.write(str(i + 1) + spacing[len(str(i))::])
        print()
        f.write("\n")
        for prop_or_calculated_prop in formatted_combination:
            print(prop_or_calculated_prop, end=spacing[len(prop_or_calculated_prop)::])  # print all props
            f.write(prop_or_calculated_prop + spacing[len(prop_or_calculated_prop)::])
        print("\n")
        f.write("\n\n")
        for i in range(num_rows):
            for j in range(num_cols):
                if number_format_requested:
                    f.write(str(int(table[i][j])) + spacing[1::])
                    if table[i][j]:
                        print(colored(int(table[i][j]), "green"), end=spacing[1::])  # print 1 in green
                    else:
                        print(colored(int(table[i][j]), "red"), end=spacing[1::])  # print 0 in red
                else:
                    f.write(str(table[i][j])[0] + spacing[1::])
                    if table[i][j]:
                        print(colored(str(table[i][j])[0], "green"), end=spacing[1::])  # print T in green
                    else:
                        print(colored(str(table[i][j])[0], "red"), end=spacing[1::])  # print F in red
            print("\n")
            f.write("\n")
        print("Open output.txt to see results. Expand the window if lines are pushed together.\n")


while True:
    generate_truth_table()
