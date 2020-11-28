from typing import Any, Dict, List, TYPE_CHECKING

if TYPE_CHECKING:
    from poetry.core.packages import ProjectPackage
    from poetry.puzzle.provider import Provider
    from poetry.core.packages import Package
else:
    ProjectPackage = Any
    Provider = Any
    Package = Any

try:
    from ._pubgrub import PubGrubVersionSolver as VersionSolver
    print(">>> use rust versionsolver")
except ImportError:
    from .version_solver import VersionSolver
    print(">>> use python versionsolver")


def resolve_version(root: ProjectPackage, provider: Provider, locked: Dict[str, Package] = None, use_latest: List[str] = None):
    solver = VersionSolver(root, provider, locked=locked, use_latest=use_latest)
    return solver.solve()
