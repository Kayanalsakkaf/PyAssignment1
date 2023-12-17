def preprocess(lines):
    # Return a list of lists, where each inner list contains the words from a line.
    objects = []
    for line in lines:
        line = line.upper()
        words = []
        word = '' #Current
        for characters in line:
            if ord(characters) == 39:
                continue
            elif characters.isalpha():
                word = word + characters
            else:
                if len(word) > 0:
                    words.append(word)
                    word = ''
        objects.append(words)
    return objects
def extract_abbreviations(obj):
    #Identify potential abbreviations from list of words.
    def find_pos(position):
        for index in range(len(lengths)):
            if lengths[index] > position:
                break
            position -= lengths[index]
        if position == 0: # calculate score
            score = 0
        elif position == lengths[index] - 1:
            if obj[index][position] == 'E':
                score = 20
            else:
                score = 6
        else:
            score = position + common_score[obj[index][position]]
        return index, position, score
    result = {}
    common_score = {'A': 25, 'B': 8, 'C': 8, 'D': 9, 'E': 35, 'F': 7,
                    'G': 9, 'H': 7, 'I': 25, 'J': 3, 'K': 6, 'L': 15,
                    'M': 8, 'N': 15, 'O': 20, 'P': 8, 'Q': 1, 'R': 15,
                    'S': 15, 'T': 15, 'U': 20, 'V': 7, 'W': 7, 'X': 3, 'Y': 7, 'Z': 1}
    lengths = [len(word) for word in obj]
    sums = sum(lengths)
    for character_position in range(1, sums): #Entering a nested loop structure.
        index, position, score = find_pos(character_position)
        abbreva = obj[0][0] + obj[index][position] 
        score_a = score
        for letter_position in range(character_position + 1, sums):
            index, position, score = find_pos(letter_position)
            abbrevb = abbreva + obj[index][position]
            score = score_a + score
            val = result.get(abbrevb, float('inf'))
            if score < val:
                result[abbrevb] = score
    return result
def remove_duplicates(abbrevs):
    indices = {}
    for abbrevb in abbrevs: 
        for key, val in abbrevb.items():
            if key in indices:
                indices[key].append(val)
            else:
                indices[key] = [val]
    unique_keys = [key for key in indices if len(indices[key]) == 1]
    filtered = []
    for abbrevb in abbrevs:
        result = {}
        for key, val in abbrevb.items():
            if key in unique_keys:
                result[key] = val
        filtered.append(result)
    return filtered
def find_lowest_scores(abbrevb):
    if len(abbrevb) == 0:
        return []
    val = min(abbrevb.values())
    return [key for key in abbrevb if abbrevb[key] == val]

def main(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
    objects = preprocess(lines)
    abbrevs = [extract_abbreviations(obj) for obj in objects]
    filtered = remove_duplicates(abbrevs)
    out_path = 'alsakkaf_' + file_name[:-4] + '_abbrevs.txt' #surname + filename + _abbrevs.txt
    with open(out_path, 'w') as file:
        for line, abbrevb in zip(lines, filtered):
            result = find_lowest_scores(abbrevb)
            file.write(line)
            file.write(' '.join(result) + '\n')
if __name__ == '__main__':
    main('trees.txt')
    main('sample.txt')