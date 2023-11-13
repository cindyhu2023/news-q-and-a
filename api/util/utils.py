
def remove_duplicate_references(answer, references):
    answer = answer.replace("[", "|")
    answer = answer.replace("]", "|")
    answer_list = answer.split("|")
    unique_references = {}
    url_to_index = {}
    next_index = 1
    res = ""
    for i, item in enumerate(answer_list):
        if i % 2 == 0:
            res += item
            continue
        else:
            refs = item.replace(" ", "").split(",")
            curr = []
            for ref in refs:
                if ref in curr:
                    continue
                elif references[int(ref)] not in url_to_index:
                    url_to_index[references[int(ref)]] = str(next_index)
                    unique_references[next_index] = references[int(ref)]
                    curr.append(str(next_index))
                    next_index += 1
                else:
                    new_ref = url_to_index[references[int(ref)]]
                    if new_ref not in curr:
                        curr.append(new_ref)
            new_item = ",".join(curr)
            res += "[" + new_item + "]" if new_item else ""


    return res, unique_references
                    
