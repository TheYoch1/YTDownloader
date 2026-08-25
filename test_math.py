def check_index(offset, cycle_size, items):
    item_w = cycle_size / items
    center_pos = (offset + item_w / 2) % cycle_size
    return int(center_pos / item_w)

for x in range(0, 100, 10):
    print(f"offset {x}, index {check_index(x, 100, 10)}")
