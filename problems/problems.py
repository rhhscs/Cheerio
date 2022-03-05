"""
Contains functions relating to problem data

Function:
    get_all_problems() -> list
    get_problem_info(int) -> map
    parse_html(int) -> str
"""

import markdown
import os
import yaml

def get_all_problems() -> list:
    """
    Gets all the problems

    Returns:
        list: list of all the problems that exist here
    """
    return [x for x in os.listdir("./problems") if x.endswith(".yml")]

def get_problem_info(problem_id: int) -> map:
    """
    Gets the data for a problem

    Args:
        problem_id (int): the id of the problem, also the name of the problem file

    Returns:
        map: a map containing all information on the problem
    """
    for problem in get_all_problems():
        with open(f"./problems/{problem}", "r") as stream:
            try:
                problem_data = yaml.safe_load(stream)
                if problem_data["id"] == problem_id:
                    return problem_data
            except yaml.YAMLError as exc:
                print(exc)
    return None

def parse_html(problem_id: int) -> str:
    """
    Parses the markdown description to HTML

    Args:
        problem_id (int): the id of the problem

    Returns:
        str: the HTML string of the problem description
    """
    problem_data = get_problem_info(problem_id)
    return markdown.markdown(problem_data["description"])

