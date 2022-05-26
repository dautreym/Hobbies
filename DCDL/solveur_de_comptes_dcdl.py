"""
Yet another count solver for the french DCDL emission
(Des Chiffres et Des Lettres, hereafter DCDL)

Since I just did it quickly to kill time, it is designed
very simply with no hard optimization in mind
(yeah it's kinda bruteforce) though it is still efficient
due to the input values being limitated to 6 numbers
(as in DCDL count challenges)

To run this file, just use the  main function at its bottom
Modify total to reach as well as input values and run it as is !
"""


from itertools import product, permutations


def get_all_permutations_with_replacement_from_list(
    list_given,
    length_list_of_values,
    must_return_list_of_lists_instead=True,
    must_ignore_list_of_length_n=True,
):
    """
    This function's goal is to produce a list of
    possible permutations for a list of operators

    That's why we are ignoring lists of length n
    where n is the length of our input values
    (for 4 values in input, we would like to stop at lists
    of 3 operators)

    Since we would like to allow stuff like (+, +, +)
    we have to make a selection with replacement
    Also, we would like to differentiate the (+, *)
    tuple from the (*, +) tuple, which can lead to different results
    So we are looking for permutations instead of combinations
    Finally, itertools calls "product" the "permutations_with_replacement"
    feature, because yeah it can also be seen as a cartesian product
    However, to shuffle enumeration with algebra is confusing
    That's why the function is called like that
    """
    to_return = []
    range_to_take = (
        range(1, length_list_of_values)
        if must_ignore_list_of_length_n
        else range(1, length_list_of_values + 1)
    )

    for index_length in range_to_take:
        to_append = list(product(list_given, repeat=index_length))
        if must_return_list_of_lists_instead:
            to_return.append(to_append)
        else:
            to_return += to_append

    return to_return


def get_all_permutations_from_list(
    list_given,
    length_list_of_values,
    must_return_list_of_lists_instead=True,
    must_ignore_list_of_length_1=True,
):
    """
    This function's goal is to produce a list of
    possible permutations for a list of values

    Unlike previous function, we do no want to
    use twice the same input value
    (this is forbidden in DCDL rules)
    Also, we still would like to differentiate
    a (1, 2) tuple froam a (2, 1) tuple
    in order to be exhaustive
    So we are looking for permutations

    We start at second element because lists of
    values of length 1 have already been tested
    in the solve_total_to_reach function
    """
    to_return = []
    range_to_take = (
        range(2, length_list_of_values + 1)
        if must_ignore_list_of_length_1
        else range(1, length_list_of_values + 1)
    )

    for index_length in range_to_take:
        to_append = list(permutations(list_given, index_length))
        if must_return_list_of_lists_instead:
            to_return.append(to_append)
        else:
            to_return += to_append

    return to_return


def solve_total_to_reach(total_to_reach, list_of_values, is_debug_mode=False):
    """
    Solve a DCDL count challenge !
    Given a total_to_reach and a list of values to use,
    assuming we can use all four operators +, -, * and /,
    compute all possible permutations for operators and
    for values, then try them together by computing
    a temporary result
    If the total is reached, the list of operators and values
    that lead to the total are returned
    If the total is not reached, None is returned for
    both list_of_operators and list_of_values
    If a problem occurs, is_debug_mode can be turned to True
    """
    if total_to_reach in list_of_values:
        return [[], [total_to_reach]]
    else:
        list_of_operators = ["+", "-", "*", "/"]
        length_list_of_values = len(list_of_values)

        list_of_permutation_lists_for_operators_for_all_lengths = (
            get_all_permutations_with_replacement_from_list(
                list_of_operators, length_list_of_values
            )
        )

        list_of_permutation_lists_for_values_for_all_lengths = (
            get_all_permutations_from_list(list_of_values, length_list_of_values)
        )

        if is_debug_mode:
            print(
                "\nLEN list_of_permutation_lists_for_operators_for_all_lengths : ",
                len(list_of_permutation_lists_for_operators_for_all_lengths),
            )
            print(
                "LEN list_of_permutation_lists_for_values_for_all_lengths : ",
                len(list_of_permutation_lists_for_values_for_all_lengths),
            )

            print(
                "\nLEN list_of_permutation_lists_for_operators_for_all_lengths SUB : ",
                [
                    len(list_tmp)
                    for list_tmp in list_of_permutation_lists_for_operators_for_all_lengths
                ],
            )
            print(
                "LEN list_of_permutation_lists_for_values_for_all_lengths SUB : ",
                [
                    len(list_tmp)
                    for list_tmp in list_of_permutation_lists_for_values_for_all_lengths
                ],
            )

        for index_length in range(length_list_of_values - 1):
            if is_debug_mode:
                print(
                    "\nCURRENT INDEX LENGTH : ",
                    index_length,
                    " / ",
                    length_list_of_values - 1,
                )

            list_of_permutation_lists_for_operators = (
                list_of_permutation_lists_for_operators_for_all_lengths[index_length]
            )

            list_of_permutation_lists_for_values = (
                list_of_permutation_lists_for_values_for_all_lengths[index_length]
            )

            for list_of_operators in list_of_permutation_lists_for_operators:
                for list_of_values in list_of_permutation_lists_for_values:
                    list_of_operators_copy = [
                        operator_tmp for operator_tmp in list_of_operators
                    ]
                    list_of_values_copy = [value_tmp for value_tmp in list_of_values]

                    current_result = 0
                    while len(list_of_values_copy) > 1:
                        if list_of_operators_copy[0] == "/" and (
                            list_of_values_copy[1] == 0
                            or list_of_values_copy[0] / list_of_values_copy[1]
                            != list_of_values_copy[0] // list_of_values_copy[1]
                        ):
                            # change the operator for an arbitray + operator
                            current_result = compute_result(
                                "+",
                                list_of_values_copy[0],
                                list_of_values_copy[1],
                            )
                        else:
                            current_result = compute_result(
                                list_of_operators_copy[0],
                                list_of_values_copy[0],
                                list_of_values_copy[1],
                            )

                        list_of_operators_copy.pop(0)
                        list_of_values_copy.pop(0)
                        list_of_values_copy.pop(0)
                        list_of_values_copy = [current_result] + list_of_values_copy

                    if current_result == total_to_reach:
                        return [list(list_of_operators), list(list_of_values)]

        return [None, None]


def compute_result(operator, operand_1, operand_2):
    """
    Moved this function out to gain lisibility
    in the above function
    It is used by the solve_tota_l_to_reach to
    quickly compute a result
    """
    if operator == "+":
        to_return = operand_1 + operand_2
    elif operator == "-":
        to_return = operand_1 - operand_2
    elif operator == "*":
        to_return = operand_1 * operand_2
    elif operator == "/":
        assert operand_2 != 0
        to_return = operand_1 / operand_2
        assert to_return == operand_1 // operand_2
    else:
        to_return = None

    return to_return


def show_results(list_of_operators_found, list_of_values_found):
    """
    Functions that prints all steps done to reach the result
    and explain which values to use with which operators
    It basically prints a detailed solution
    for DCDL's count challenges
    """
    print("\nBEGINNING PRINTING RESULTS")
    print("\nList of operators found : ", list_of_operators_found)
    print("\nList of values found : ", list_of_values_found, "\n")
    if list_of_operators_found is None and list_of_values_found is None:
        print("\nGIVEN TOTAL IS NOT REACHABLE WITH THESE VALUES !!\n")
    elif list_of_operators_found == []:
        print(list_of_values_found[0])
    else:
        current_result = 0
        while len(list_of_values_found) > 1:
            current_result = compute_result(
                list_of_operators_found[0],
                list_of_values_found[0],
                list_of_values_found[1],
            )
            operator = list_of_operators_found.pop(0)
            operand_1 = list_of_values_found.pop(0)
            operand_2 = list_of_values_found.pop(0)
            list_of_values_found = [current_result] + list_of_values_found

            print(operand_1, operator, operand_2, " = ", current_result)

    print("\n")


def test():
    """
    Function to quickly test all above functions,
    also these test cases are a bit tricky
    They should not be modified
    To use the program, please modify the main function below
    """
    list_of_operators_found, list_of_values_found = solve_total_to_reach(
        629, [9, 7, 10, 1]
    )
    show_results(list_of_operators_found, list_of_values_found)
    print("\n\n")

    list_of_operators_found, list_of_values_found = solve_total_to_reach(
        4403, [7, 9, 7, 10, 1]
    )
    show_results(list_of_operators_found, list_of_values_found)
    print("\n\n")

    list_of_operators_found, list_of_values_found = solve_total_to_reach(
        977, [6, 3, 9, 6, 3, 2]
    )
    show_results(list_of_operators_found, list_of_values_found)
    print("\n\n")

    list_of_operators_found, list_of_values_found = solve_total_to_reach(
        100, [1, 1, 1, 1, 1, 1]
    )
    show_results(list_of_operators_found, list_of_values_found)
    print("\n\n")


def main():
    """
    Main function for our program
    Can be modified very quickly to directly
    solve DCDL's count challenges within the given 30s
    """
    list_of_operators_found, list_of_values_found = solve_total_to_reach(
        977, [6, 3, 9, 6, 3, 2]
    )
    show_results(list_of_operators_found, list_of_values_found)
    print("\n\n")


# test()
main()
