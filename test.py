def moveToNPC(current_coords,npc_coords)->bool:
    a,b = symbols('a,b')
    res = 0
    saga = False
    sola = False
    ileri = False
    geri = False
    curr_pos = current_coords
    dst_pos = npc_coords
    x1,x1 = curr_pos
    x2,y2 = dst_pos
    asilx1 = x1 * math.cos(math.degrees(7*math.pi/4))
    asily1 = y1 * math.sin(math.degrees(7*math.pi/4))
    asilx2 = x2 * math.cos(math.degrees(7*math.pi/4))
    asily2 = y2 * math.sin(math.degrees(7*math.pi/4))
    x_diff = x1-x2
    y_diff = y1-y2
    if x_diff > 0:
        geri = True
        ileri = False
    else:
        geri = False
        ileri = True
    if y_diff >0:
        saga = False
        sola = True
    else:
        saga = True
        sola = False
    if ileri and sola:
        eq1 = Eq((a+b), x_diff)
        eq2 = Eq((-a+b), y_diff)
        res = solve((eq1, eq2), (a, b))
    if ileri and saga:
        eq1 = Eq((a-b), x_diff)
        eq2 = Eq((-a-b), y_diff)
        res = solve((eq1, eq2), (a, b))
    if geri and sola:
        eq1 = Eq((-a+b), x_diff)
        eq2 = Eq((a+b), y_diff)
        res = solve((eq1, eq2), (a, b))
    if geri and saga:
        eq1 = Eq((-a-b), x_diff)
        eq2 = Eq((a-b), y_diff)
        res = solve((eq1, eq2), (a, b))
    adima= abs(res[a])
    adimb= abs(res[b])
    msa =(float(adima))*0.432
    msb =(float(adimb))*0.432
    print(ileri,geri,saga,sola,adima,adimb,msa,msb)
    if ileri:
        mk_functions.press_and_wait("w",msa)
    else:
        mk_functions.press_and_wait("s",msa)
    if saga:
        mk_functions.press_and_wait("d",1.47)
        mk_functions.press_and_wait("w",msb)
        mk_functions.press_and_wait("a",1.47)
    else:
        mk_functions.press_and_wait("a",1.47)
        mk_functions.press_and_wait("w",msb)
        mk_functions.press_and_wait("d",1.47)
    return True
