from ortools.sat.python import cp_model
from src.types import Box


class ThreeDimPacking:
    def __init__(
        self,
        box: Box,
        items: list[Box]
    ):
        # list of [width, height, length]
        self.items: list[tuple[int, int, int]]
        self.items = [item.get_dimensions() for item in items]
        # [width, height, length]
        self.W, self.H, self.L = box.get_dimensions()
        self.box_volume = self.W * self.H * self.L
        self.n = len(items)

        self.model: cp_model.CpModel
        # Variable types
        self.placed: list[cp_model.BoolVar]
        self.x: list[cp_model.IntVar]
        self.y: list[cp_model.IntVar]
        self.z: list[cp_model.IntVar]
        self.item_volumes: list[cp_model.BoolVar]
        self.solver: cp_model.CpSolver
        self.status: cp_model.CpSolver.StatusName
        self.positions: list[tuple[int, int, int]]

    def _init_model(self):
        self.model = cp_model.CpModel()

    def _add_variables(self):
        self.placed = [
            self.model.NewBoolVar(f'placed_{i}')
            for i in range(self.n)]
        self.x = [
            self.model.NewIntVar(0, self.W, f'x_{i}')
            for i in range(self.n)]
        self.y = [
            self.model.NewIntVar(0, self.H, f'y_{i}')
            for i in range(self.n)]
        self.z = [
            self.model.NewIntVar(0, self.L, f'z_{i}')
            for i in range(self.n)]
        self.item_volumes = [
            self.model.NewIntVar(0, self.box_volume, f'vol_{i}')
            for i in range(self.n)]

    def _add_boundary_constraints(self, i: int):
        wi, hi, li = self.items[i]
        self.model.Add(self.x[i] + wi <= self.W).OnlyEnforceIf(self.placed[i])
        self.model.Add(self.y[i] + hi <= self.H).OnlyEnforceIf(self.placed[i])
        self.model.Add(self.z[i] + li <= self.L).OnlyEnforceIf(self.placed[i])

    def _add_item_volume_constraints(self, i: int):
        wi, hi, li = self.items[i]
        item_volume = wi * hi * li
        self.model.Add(self.item_volumes[i] == item_volume)\
            .OnlyEnforceIf(self.placed[i])
        self.model.Add(self.item_volumes[i] == 0)\
            .OnlyEnforceIf(self.placed[i].Not())

    def _add_no_overlap_constraints(self, i: int, j: int):
        wi, hi, li = self.items[i]
        wj, hj, lj = self.items[j]
        left = self.model.NewBoolVar(f'left_{i}_{j}')
        right = self.model.NewBoolVar(f'right_{i}_{j}')
        above = self.model.NewBoolVar(f'above_{i}_{j}')
        below = self.model.NewBoolVar(f'below_{i}_{j}')
        front = self.model.NewBoolVar(f'front_{i}_{j}')
        behind = self.model.NewBoolVar(f'behind_{i}_{j}')

        self.model.Add(self.x[i] + wi <= self.x[j]).OnlyEnforceIf(left)
        self.model.Add(self.x[j] + wj <= self.x[i]).OnlyEnforceIf(right)
        self.model.Add(self.y[i] + hi <= self.y[j]).OnlyEnforceIf(above)
        self.model.Add(self.y[j] + hj <= self.y[i]).OnlyEnforceIf(below)
        self.model.Add(self.z[i] + li <= self.z[j]).OnlyEnforceIf(front)
        self.model.Add(self.z[j] + lj <= self.z[i]).OnlyEnforceIf(behind)

        self.model.AddBoolOr([left, right, above, below, front, behind])

    def _add_constraints(self):
        # TODO: Add posiibility to rotate items
        for i in range(self.n):
            self._add_boundary_constraints(i)
            self._add_item_volume_constraints(i)

            for j in range(i + 1, self.n):
                self._add_no_overlap_constraints(i, j)

    def _add_objective(self):
        # TODO: Add goal to maximize total used volume
        # Maximize number of items placed
        self.model.Maximize(sum(self.placed))

    def _solve(self):
        self.solver = cp_model.CpSolver()
        self.solver.parameters.log_search_progress = True
        self.status = self.solver.Solve(self.model)
        self.status_name = self.solver.StatusName(self.status)
        return self.status

    def solve(self):
        self._init_model()
        self._add_variables()
        self._add_constraints()
        self._add_objective()
        self._solve()
        print(f'Solution status: {self.status_name}')

    def get_result(self) -> list[list[int]]:
        if self.status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            self.positions = [[
                self.solver.Value(self.x[i]),
                self.solver.Value(self.y[i]),
                self.solver.Value(self.z[i])]
                if self.solver.Value(self.placed[i]) == 1 else (-1, -1, -1)
                for i in range(self.n)
            ]
            return self.positions
        else:
            print('Solution status: %s. Cann\'t get the results.' % (
                self.status_name, ))
            return []
