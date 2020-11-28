from poetry.core.packages import Package
from .version_solver import VersionSolver as PoetryVersionSolver
from .result import SolverResult
from poetry._poetry_ext import resolve_pywrapper


class PubGrubVersionSolver(PoetryVersionSolver):
    def solve(self):
        requires = [(d.name, str(d.constraint)) for d in self._root.requires]
        dev_requires = [(d.name, str(d.constraint)) for d in self._root.dev_requires]
        pkgs = resolve_pywrapper(self._root.name, str(self._root.version), requires, dev_requires)
        packages = [Package(name, version) for (name, version) in pkgs]
        return SolverResult(self._root, packages, 1)
