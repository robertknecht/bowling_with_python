import time

def get_shot(shot_num, prev_score = False):
    int_to_str = {
        1: 'first',
        2: 'second',
        3: 'third'
    }
    score = input('Score for ' + int_to_str[shot_num] + ' throw: ')
    if not score.isdigit():
        print ('Numbers only, please.')
        return get_shot(shot_num, prev_score)
    score = int(score)
    if score > 10:
        print ('There are only 10 pins.')
        score = 'error'
    elif prev_score and score + prev_score > 10:
        print ('There are only 10 pins.')
        score = 'error'
    if score == 'error':
        return get_shot(shot_num, prev_score)
    return score

def calculate_score(throw_list, frame_num):
    total_score = 0
    for key, value in throw_list.items():
        turn = value['turn']
        score = value['score']
        total_score += score
        last_roll_spare = False
        last_roll_strike = False
        two_rolls_ago_strike = False
        if key > 1:
            last_roll = throw_list[key - 1]
            last_roll_strike = last_roll['turn'] == 1 and last_roll['score'] == 10
        if key > 2:
            two_rolls_ago = throw_list[key - 2]
            last_roll_spare = last_roll['turn'] == 2 and (last_roll['score'] + two_rolls_ago['score'] == 10)
            two_rolls_ago_strike = two_rolls_ago['turn'] == 1 and two_rolls_ago['score'] == 10
        if frame_num == 10:
            if last_roll_spare and turn == 1:
                total_score += score
            if last_roll_strike and turn == 1:
                total_score += score
            if two_rolls_ago_strike and (turn == 1 or turn == 2):
                total_score += score
        else:
            if last_roll_spare:
                total_score += score # score added to previous spare
            if last_roll_strike:
                total_score += score # score added to previous strike
            if two_rolls_ago_strike:
                total_score += score # score added to strike two turns ago
    return total_score

print ('Welcome to the bowling game!')

time.sleep(1)

print ('Record your score for each throw of each frame.')

time.sleep(2)

throw_count = 0
throw_list = {}
for frame_num in range(1, 11):
    print ('Frame ' + str(frame_num))
    throw1 = get_shot(1)
    throw_count += 1
    throw_list[throw_count] = {
        'turn': 1,
        'score': throw1
    }
    if (throw1 < 10 or frame_num == 10):
        throw1_holder = throw1
        if frame_num == 10:
            throw1_holder = False
        throw2 = get_shot(2, throw1_holder)
        throw_count += 1
        throw_list[throw_count] = {
            'turn': 2,
            'score': throw2
        }
    print 
    if (frame_num == 10 and (throw1 == 10 or throw1 + throw2 == 10)):
        throw3 = get_shot(3)
        throw_count += 1
        throw_list[throw_count] = {
            'turn': 3,
            'score': throw3
        }
    print ("Total Score: " + str(calculate_score(throw_list, frame_num)))

time.sleep(1)
print ("Congratulations! Your final score is " + str(calculate_score(throw_list, frame_num)) + "!")
