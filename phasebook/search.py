from flask import Blueprint, request
from typing import Optional

from .data.search_data import USERS


bp = Blueprint("search", __name__, url_prefix="/search")


@bp.route("")
def search():
    return search_users(request.args.to_dict()), 200


def search_users(args):
    """Search users database

    Parameters:
        args: a dictionary containing the following search parameters:
            id: string
            name: string
            age: string
            occupation: string

    Returns:
        a list of users that match the search parameters
    """

    # Implement search here!

    # Extract search parameters
    id = args.get("id")
    name = args.get("name")
    age = args.get("age")
    occupation = args.get("occupation")

    arguments = [id, name, age, occupation]

    if any(arguments):  # Check if at least one of search parameters is passed
        # Creates a list of matcher for id, name, age, and occupation
        matchers = [
            id_matcher,
            name_matcher,
            age_matcher,
            occupation_matcher,
        ]

        match_results = []

        for user in USERS:
            for priority, (arg, matcher) in enumerate(zip(arguments, matchers)):
                # Check if the argument matches on its respective matcher function
                if matcher(arg, user):
                    # Add user to the results that matched the search parameters
                    # Use the matcher's index as the priority value.
                    # The lower the value the higher the priority
                    match_results.append((user, priority))

                    # Break out of loop since it already found a match in search parameters,
                    # and to avoid result duplication
                    break

        # Sort the results based on its priority
        match_results.sort(key=lambda result: result[1])

        # Only extract the users from results
        users = list(map(lambda result: result[0], match_results))
    else:  # Return all users if there is no seach parameter
        users = USERS

    return users


def id_matcher(id: Optional[str], user) -> bool:
    if id is None:
        return False

    return user["id"] == id


def name_matcher(name: Optional[str], user) -> bool:
    if name is None:
        return False

    return name.lower() in user["name"].lower()


def age_matcher(age: Optional[str], user) -> bool:
    if age is None:
        return False

    return is_integer(age) and user["age"] - 1 <= int(age) <= user["age"] + 1


def occupation_matcher(occupation: Optional[str], user) -> bool:
    if occupation is None:
        return False

    return occupation.lower() in user["occupation"].lower()


def is_integer(str: str):
    try:
        int(str)
    except ValueError:
        return False
    else:
        return True
