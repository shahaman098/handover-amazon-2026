"""Inspectable dependency graph: closure, topological order, cycle detection."""

from __future__ import annotations

from collections import deque
from typing import Dict, List, Set


class DependencyGraph:
    def __init__(self, assessment_deps: Dict[str, List[str]]) -> None:
        self.assessment_deps = {k: list(v) for k, v in assessment_deps.items()}

    def dependent_closure(self, start_ids: List[str]) -> Set[str]:
        """All assessments transitively depending on any of start_ids (assertion or assessment)."""
        affected: Set[str] = set()
        queue: deque[str] = deque(start_ids)
        seen: Set[str] = set(start_ids)

        while queue:
            node = queue.popleft()
            for aid, deps in self.assessment_deps.items():
                if aid in affected:
                    continue
                if any(d in seen or d in affected for d in deps):
                    affected.add(aid)
                    queue.append(aid)

        return affected

    def topological_order(self) -> List[str]:
        """Assessments in dependency order (assessment deps may reference other assessments)."""
        ids = list(self.assessment_deps.keys())
        in_degree = {i: 0 for i in ids}
        for aid, deps in self.assessment_deps.items():
            for d in deps:
                if d in in_degree:
                    in_degree[aid] += 1

        queue = deque([i for i in ids if in_degree[i] == 0])
        order: List[str] = []
        while queue:
            n = queue.popleft()
            order.append(n)
            for aid, deps in self.assessment_deps.items():
                if n in deps:
                    in_degree[aid] -= 1
                    if in_degree[aid] == 0:
                        queue.append(aid)

        if len(order) != len(ids):
            raise ValueError("Dependency cycle detected among assessments")
        return order

    def would_create_cycle(self, assessment_id: str, new_dep: str) -> bool:
        """If assessment_id added new_dep, would that create a cycle?"""
        trial = {k: list(v) for k, v in self.assessment_deps.items()}
        trial.setdefault(assessment_id, []).append(new_dep)
        try:
            DependencyGraph(trial).topological_order()
            return False
        except ValueError:
            return True
