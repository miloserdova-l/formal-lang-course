from project.rsm import RSM


def minimize_rsm(rsm: RSM) -> RSM:
    boxes = dict()
    for var in rsm.boxes.keys():
        boxes[var] = rsm.boxes[var].minimize()
    new_rsm = RSM(rsm.start_symbol, boxes)
    return new_rsm
