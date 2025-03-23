from copy import deepcopy


class Flattener:
    def __init__(self):
        pass

    def cross_join(self, left, right):
        if len(right) == len(left):
            return [
                dict(list(left[i].items()) + list(right[i].items()))
                for i in range(len(left))
            ]
        new_rows = [] if right else left
        for left_row in left:
            for right_row in right:
                temp_row = deepcopy(left_row)
                for key, value in right_row.items():
                    temp_row[key] = value
                new_rows.append(deepcopy(temp_row))
        return new_rows

    def flatten_list(self, data):
        for elem in data:
            if isinstance(elem, list):
                yield from self.flatten_list(elem)
            else:
                yield elem

    def flatten_json(self, data_in):
        def realize(data, prev_heading=""):
            if isinstance(data, dict):
                rows = [{}]
                for key, value in data.items():
                    rows = self.cross_join(
                        rows, realize(value, prev_heading + "_" + key)
                    )
            elif isinstance(data, list):
                rows = []
                for item in data:
                    [
                        rows.append(elem)
                        for elem in self.flatten_list(realize(item, prev_heading))
                    ]
            else:
                rows = [{prev_heading[1:]: data}]
            return rows

        return realize(data_in)
