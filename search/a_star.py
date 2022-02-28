#
# This file is part of pyperplan.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
#

"""
Implements the A* (a-star) and weighted A* search algorithm.
"""

import heapq
import logging

from . import searchspace


def ordered_node_astar(node, h, node_tiebreaker):
    """
    Creates an ordered search node (basically, a tuple containing the node
    itself and an ordering) for A* search.

    @param node The node itself.
    @param heuristic A heuristic function to be applied.
    @param node_tiebreaker An increasing value to prefer the value first
                           inserted if the ordering is the same.
    @returns A tuple to be inserted into priority queues.
    """
    f = node.g + h
    return (f, h, node_tiebreaker, node)


def ordered_node_weighted_astar(weight):
    """
    Creates an ordered search node (basically, a tuple containing the node
    itself and an ordering) for weighted A* search (order: g+weight*h).

    @param weight The weight to be used for h
    @param node The node itself
    @param h The heuristic value
    @param node_tiebreaker An increasing value to prefer the value first
                           inserted if the ordering is the same
    @returns A tuple to be inserted into priority queues
    """
    """
    Calling ordered_node_weighted_astar(42) actually returns a function (a
    lambda expression) which is the *actual* generator for ordered nodes.
    Thus, a call like
        ordered_node_weighted_astar(42)(node, heuristic, tiebreaker)
    creates an ordered node with weighted A* ordering and a weight of 42.
    """
    return lambda node, h, node_tiebreaker: (
        node.g + weight * h,
        h,
        node_tiebreaker,
        node,
    )


def ordered_node_greedy_best_first(node, h, node_tiebreaker):
    """
    Creates an ordered search node (basically, a tuple containing the node
    itself and an ordering) for greedy best first search (the value with lowest
    heuristic value is used).

    @param node The node itself.
    @param h The heuristic value.
    @param node_tiebreaker An increasing value to prefer the value first
                           inserted if the ordering is the same.
    @returns A tuple to be inserted into priority queues.
    """
    f = h
    return (f, h, node_tiebreaker, node)


def greedy_best_first_search(task, heuristic, use_relaxed_plan=False):
    """
    Searches for a plan in the given task using greedy best first search.

    @param task The task to be solved.
    @param heuristic A heuristic callable which computes the estimated steps
                     from a search node to reach the goal.
    """
    return astar_search(
        task, heuristic, ordered_node_greedy_best_first, use_relaxed_plan
    )


def weighted_astar_search(task, heuristic, weight=5, use_relaxed_plan=False):
    """
    Searches for a plan in the given task using A* search.

    @param task The task to be solved.
    @param heuristic  A heuristic callable which computes the estimated steps.
                      from a search node to reach the goal.
    @param weight A weight to be applied to the heuristics value for each node.
    """
    return astar_search(
        task, heuristic, ordered_node_weighted_astar(weight), use_relaxed_plan
    )


def astar_search(
    task, heuristic, make_open_entry=ordered_node_astar, use_relaxed_plan=False
):
    """
    Searches for a plan in the given task using A* search.

    @param task The task to be solved
    @param heuristic  A heuristic callable which computes the estimated steps
                      from a search node to reach the goal.
    @param make_open_entry An optional parameter to change the bahavior of the
                           astar search. The callable should return a search
                           node, possible values are ordered_node_astar,
                           ordered_node_weighted_astar and
                           ordered_node_greedy_best_first with obvious
                           meanings.
    """
    # For the purpose of this Task, the argument use_relaxed_plan is always 
    # considered to be False
    use_relaxed_plan=False

    # Create the root node (i.e. the node that corresponds to the
    # initial state). The root node is a SearchNode instance with the following
    # attributes:
    # state: equals to the initial state of the task
    # parent (node): None
    # action (that produced the initial state): None
    # g (The path length of the root node in the count of applied operators): 0
    # See searchspace.py for more details.
    # SearchNode instances are the nodes to be visited during search.
    root = searchspace.make_root_node(task.initial_state)
    
    # The cost of reaching the initial state is 0
    state_cost = {task.initial_state: 0}

    # An increasing value to prefer the value first inserted in the list of nodes
    # if the cost of two or more nodes is the same
    node_tiebreaker = 0

    # Calculate the estimated movement cost to reach the goal state
    # from the initial state (i.e. from the state in root node)
    init_h = heuristic(root)

    # The nodes to be visited. Each node will be stored along with the 
    # 1) estimated heuristing values f and h for reaching the goal state from the 
    # state in node, and 2) the node_tiebreaker value
    open = []

    # Add the root node in the heap of nodes to be visited ("open").
    # The root node is stored along along with 1) the estimated heuristing values 
    # f and h for reaching the goal state from the state in node, and 2) the 
    # node_tiebreaker value. f is calculated based on the callable parameter
    # make_open_entry, i.e. based on the type of the A* search algorithm.
    #
    # The node is stored in a heap so that nodes are stored based on their 
    # estimated cost. See more here: https://pythontic.com/algorithms/heapq/heappush
    heapq.heappush(open, make_open_entry(root, init_h, node_tiebreaker))
    logging.info("Initial h value: %f" % init_h)

    # Initially, the best cost value is set to infinite
    besth = float("inf")

    counter = 0

    # Counter of the nodes that have been expanded
    expansions = 0

    # Iterate over the heap as long as the heap contains items to pop
    while open:
        # Step 1
        # Pop the next node from the heap (i.e. the next node with the lowest estimated cost)
        # This is the node that will be expanded in this round
        # HINT: Use the function heappop() of the heapq module: https://pythontic.com/algorithms/heapq/heappop
        (f, h, _tie, pop_node) = heapq.heappop(open)

        # Update the best cost value
        if h < besth:
            besth = h
            logging.debug("Found new best h: %d after %d expansions" % (besth, counter))

        # Get the state in the node to be expanded
        pop_state = pop_node.state

        # Get the cost g of the node to be expanded (i.e. the path length, i.e. the number of applied 
        # operators for reaching the state in node)
        pop_g = pop_node.g

        # Step 2 
        # Only expand the node if its associated cost (g value) is the lowest
        # cost known for this state. Otherwise we already found a cheaper
        # path after creating this node and hence can disregard it.
        # HINT 1: Compare the state cost of pop_state with pop_g. If they are
        #         equal, proceed to the next step. Else continue to a new round.
        # HINT 2: The state cost of pop_state can be retrieved from the 
        #         state_cost dictionary (see before loop)
        if state_cost[pop_state] == pop_node.g:
        
        # If the state cost of pop_state is equal to pop_g:
            # Step 3
            # Increase the expansions counter
            expansions += 1

            # Step 3
            # If the goal of the task has been reach in the state
            # of the node, then extract the solution and return it.
            # HINT 1: The variable pop_state holds the state in the node
            # HINT 2: Use a Task method that you implemented to check if
            #         the goal of the task has been reached at the the state 
            #         in the node
            # HINT 3: Use the SearchNode method extract_solution() to extract
            #         and return the solution to the task (in case the goal has
            #         been achieved)
            if task.goal_reached(pop_state):
                logging.info("Goal reached. Start extraction of solution.")
                logging.info("%d Nodes expanded" % expansions)
                return pop_node.extract_solution()

            rplan = None

            for op, succ_state in task.get_successor_states(pop_state):
                succ_node = searchspace.make_child_node(pop_node, op, succ_state)
                h = heuristic(succ_node)
                if h == float("inf"):
                    # don't bother with states that can't reach the goal anyway
                    continue
                old_succ_g = state_cost.get(succ_state, float("inf"))
                if succ_node.g < old_succ_g:
                    # We either never saw succ_state before, or we found a
                    # cheaper path to succ_state than previously.
                    node_tiebreaker += 1
                    heapq.heappush(open, make_open_entry(succ_node, h, node_tiebreaker))
                    state_cost[succ_state] = succ_node.g

        counter += 1
    logging.info("No operators left. Task unsolvable.")
    logging.info("%d Nodes expanded" % expansions)
    return None
