import csv
import sys

import util
from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    # TODO
    nodes = util.QueueFrontier()
    visited = []
    target_reached = False

    # If the source and target are the same end the program
    if (source == target):
        return visited

    # Gets the starting layer (first connecting actors to source actor)
    pairs = neighbors_for_person(source)
    for pair in pairs:
        if pair[1] != source:
            nodes.add(Node(pair, None, 1))
            # If target is in the first layer skip straight to the output
            if pair[1] == target:
                target_reached = True
                break

    # Checks actors using Breath first search until the target actor is found or there is no link between the source and target actor
    while not target_reached:
        if nodes.empty():
            return None

        parent = nodes.remove()
        not_visited = True
        # Check if the parent has already been visited
        for node in visited:
            if parent.state[0] == node.state[0] and parent.state[1] == node.state[1]:
                not_visited = False
                break

        # If the parent has already been checked ignore them
        if not_visited:
            visited.append(parent)
            # Add the child nodes to the frontier
            for actor in neighbors_for_person(parent.state[1]):
                # If actor is not the starting actor or the parent actor then add the actor to the frontier as a node
                if actor[1] != parent.state[1] and actor[1] != source:
                    nodes.add(Node(actor, parent, parent.action + 1))
                    if actor[1] == target:
                        target_reached = True
                        break

    quickest_path = []
    current_node = nodes.frontier[len(nodes.frontier) - 1]
    # Adds the target node to path
    quickest_path.append(current_node.state)

    # Reverses through the targets connecting pairs to find the quickest path
    if current_node.parent is not None:
        while True:
            parent_node = current_node.parent

            quickest_path.append(parent_node.state)

            if parent_node.parent is None:
                break

            else:
                current_node = parent_node

    quickest_path.reverse()
    return quickest_path


def create_layer(source):
    layer = []
    pairs = neighbors_for_person(source)
    for pair in pairs:
        if pair[1] == source:
            layer.append(pair)    


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
