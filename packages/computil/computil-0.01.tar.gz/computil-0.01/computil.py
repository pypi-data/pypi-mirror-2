import time

def track(sequence, time_quant=2):
    t_0 = t_last = time.time()
    for i, element in enumerate(sequence):
        now = time.time()
        if now - t_last > time_quant:
            so_far = now - t_0
            speed = float(so_far) / (i + 1)
            estimated_all = len(sequence) * speed
            minutes_left = (estimated_all - so_far) / 60
            print "%s/%s (estimated %.2fmins left)" % (i + 1, len(sequence), minutes_left)
        yield element
