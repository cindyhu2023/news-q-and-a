
'''
remove duplicate references and fix the numbering in the answer

original answer and reference:
"answer": "Elizabeth Holmes is on trial for defrauding investors [1,4], as well as three wire fraud counts tied to specific investors [2,3]. She faces up to 20 years in prison and a fine of $250,000 plus restitution for each count [4].",
"reference": {
    "1": "https://www.cnn.com/2022/01/03/tech/elizabeth-holmes-verdict/index.html",
    "2": "https://www.cnn.com/2022/01/04/tech/elizabeth-holmes-rise-and-fall/index.html",
    "3": "https://www.cnn.com/2022/01/03/tech/elizabeth-holmes-verdict/index.html",
    "4": "https://www.cnn.com/2022/01/03/tech/elizabeth-holmes-verdict/index.html",
    "5": "https://www.cnn.com/2022/01/03/tech/elizabeth-holmes-verdict/index.html"
}

corrected answer and reference:
"answer": "Elizabeth Holmes is on trial for defrauding investors [1], as well as three wire fraud counts tied to specific investors [1,2]. She faces up to 20 years in prison and a fine of $250,000 plus restitution for each count [1].",
"reference": {
    "1": "https://www.cnn.com/2022/01/03/tech/elizabeth-holmes-verdict/index.html",
    "2": "https://www.cnn.com/2022/01/04/tech/elizabeth-holmes-rise-and-fall/index.html",
}

'''

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
                    
