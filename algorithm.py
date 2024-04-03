def is_block(array, x, y):
    if array[x, y] == '0':
        return False
    else:
        return True


def edge(array, p1, p2):
    # 判断两个点是否都在边界上
    if (p1[0] == 0 or p1[0] == len(array) - 1) and (p2[0] == 0 or p2[0] == len(array) - 1):
        return True  # 如果两个点都在行边界上，则返回True
    if (p1[1] == 0 or p1[1] == len(array[0]) - 1) and (p2[1] == 0 or p2[1] == len(array[0]) - 1):
        return True  # 如果两个点都在列边界上，则返回True
    return False


def h(array, p1, p2):
    if p1[0] == p2[0] and p1[1] == p2[1]:
        return False
    if p1[0] != p2[0]:
        return False
    start_y = min(p1[1], p2[1])
    end_y = max(p1[1], p2[1])
    if start_y + 1 == end_y:
        return True
    for i in range(start_y + 1, end_y):
        if is_block(array, p1[0], i):
            return False
    return True


def v(array, p1, p2):
    if p1[0] == p2[0] and p1[1] == p2[1]:
        return False
    if p1[1] != p2[1]:
        return False
    start_x = min(p1[0], p2[0])
    end_x = max(p1[0], p2[0])
    if start_x + 1 == end_x:
        return True
    else:
        for i in range(start_x + 1, end_x):
            if is_block(array, i, p1[1]):
                return False
        return True


def turn_one(array, p1, p2):
    if p1[0] == p2[0] and p1[1] == p2[1]:
        return False
    x1, y1 = p1
    x2, y2 = p2
    start_x = min(p1[0], p2[0])
    end_x = max(p1[0], p2[0])
    start_y = min(p1[1], p2[1])
    end_y = max(p1[1], p2[1])
    if is_block(array, x1, y1) and is_block(array, x2, y2):
        if start_x + 1 == end_x:
            for i in range(start_y, end_y):
                if is_block(array, end_x, i):
                    return False
            for i in range(start_y, end_y):
                if is_block(array, start_x, i):
                    return False
        elif start_y + 1 == end_y:
            for i in range(start_x, end_x):
                if is_block(array, i, end_y):
                    return False
            for i in range(start_x, end_x):
                if is_block(array, i, start_y):
                    return False
        else:
            result1 = (h(array, p1, (x1, y2)) and v(array, (x1, y2), p2))
            result2 = (h(array, p1, (x2, y1)) and v(array, (x2, y1), p2))
            if result1 or result2:
                return True
    else:
        return False


def turn_two(array, p1, p2):
    if p1[0] == p2[0] and p1[1] == p2[1]:
        return False
    x1, y1 = p1
    x2, y2 = p2
    if is_block(array, x1, y1) and is_block(array, x2, y2):
        for y in range(0, 4):
            result1 = h(array, p1, (x1, y)) and turn_one(array, p2, (x1, y))
            if result1:
                return result1

        for x in range(0, 4):
            result2 = v(array, p1, (x, y1)) and turn_one(array, p2, (x, y1))
            if result2:
                return result2
    else:
        return False


def remove(array, p1, p2):
    if p1[0] == p2[0] and p1[1] == p2[1]:
        return False
    # p1 和 p2 都在边界，可以直接删除
    if (p1[0] == p2[0]) and (p1[0] == 0 or p1[0] == len(array) - 1):
        print('上下边界可以直接删除')
    elif (p1[1] == p2[1]) and (p1[1] == 0 or p1[1] == len(array[0]) - 1):
        print('上下边界可以直接删除')
    elif array[p1[0], p1[1]] == array[p2[0], p2[1]]:
        if h(array, p1, p2):
            print('水平可以消除')
        elif v(array, p1, p2):
            print('垂直可以消除')
        elif turn_one(array, p1, p2):
            print('一个拐可以消除')
        elif turn_two(array, p1, p2):
            print('二个拐可以消除')
    else:
        print('无法删除')


def can_remove(array, p1, p2):
    print('can_remove')
    if p1[0] == p2[0] and p1[1] == p2[1]:
        print('同一个点')
        return False
    elif array[p1[0], p1[1]] == array[p2[0], p2[1]]:
        # 边界
        if edge(array, p1, p2):
            print('边界')
            return True
        elif h(array, p1, p2):
            print('水平')
            return True
        elif v(array, p1, p2):
            print('竖直')
            return True
        elif turn_one(array, p1, p2):
            print('一个拐')
            return True
        elif turn_two(array, p1, p2):
            print('两个拐')
            return True
        else:
            print('匹配失败')
            return False
    else:
        print('无法匹配')
        return False
