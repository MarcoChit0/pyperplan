"""
Action Landmarks Heuristic
"""

from collections import defaultdict
import copy

from .heuristic_base import Heuristic


def _get_relaxed_task(task):
    """
    Removes the delete effects of every operator in task
    """
    relaxed_task = copy.deepcopy(task)
    for op in relaxed_task.operators:
        op.del_effects = set()
    return relaxed_task


def get_action_landmarks(task):
    action_landmarks = []
    task = _get_relaxed_task(task)
    for op in task.operators:
        current_state = task.initial_state
        goal_reached = current_state >= task.goals

        while not goal_reached:
            previous_state = current_state
            for _op in task.operators:
                if op != _op and _op.applicable(current_state):
                    current_state = _op.apply(current_state)
                    if current_state >= task.goals:
                        break
            if previous_state == current_state and not current_state >= task.goals:
                action_landmarks.append(op)
                break

            goal_reached = current_state >= task.goals
    return action_landmarks

class ActionLandmarkHeuristic(Heuristic):
    def __init__(self, task):
        self.task = task
        self.action_landmarks = get_action_landmarks(task)
        print("<action_landmarks>")
        for op in self.action_landmarks:
            print(f"{op.name}")
        print("</action_landmarks>")
        exit(1)


    def __call__(self, node):
        # 0 : goal reached
        # N : number of actions in the problem
        # n : N minus the number of action landmarks applicable in the current state
        # closer to 0 is better
        if all(fact in node.state for fact in self.task.goals):
            return 0
        applicable_landmarks = [op for op in self.action_landmarks if op.applicable(node.state)]
        if not applicable_landmarks:
            return len(self.task.operators)
        return len(self.task.operators) - len(applicable_landmarks)