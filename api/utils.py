import re

def correct_references(answer, references):
    index_to_url = {}
    url_to_index = {}
    for index, url in references.items():
        if url not in url_to_index:
            url_to_index[url] = len(url_to_index.values()) + 1
            index_to_url[len(url_to_index)] = url
    print("index_to_url: ", index_to_url)
    print("url_to_index: ", url_to_index)

    left_bracket_index = [idx for idx, char in enumerate(answer) if char == "["]
    right_bracket_index = [idx for idx, char in enumerate(answer) if char == "]"]
    answer_list = list(answer)
    for i in range(len(left_bracket_index)):
        l, r = left_bracket_index[i], right_bracket_index[i]
        curr = answer[l+1:r]
        if "," in curr:
            curr = curr.replace(" ", "").split(",")
            print("before curr: ", curr)
            updated_curr = []
            for j,c in enumerate(curr):
                updated_index = url_to_index[references[int(c)]]
                if str(updated_index) not in updated_curr:
                    updated_curr.append(c)
            print("after curr: ", updated_curr)
            curr = ",".join(updated_curr)
        else:
            curr = str(url_to_index[references[int(curr)]])
        for k in range(1, r-l):
            answer_list[l+k] = curr[k-1] if k <= len(curr) else ""
    answer = "".join(answer_list)
    return answer, index_to_url


def correct_references2(answer, references):
    unique_references = {}
    updated_answer = answer

    # Find all reference patterns in the answer, such as [1], [2,3], etc.
    reference_patterns = re.findall(r'\[\d+(?:,\d+)*\]', answer)

    for pattern in reference_patterns:
        old_indices = [int(index) for index in re.findall(r'\d+', pattern)]
        urls = [references.get(old_index) for old_index in old_indices]

        new_indices = []

        for url in urls:
            if url and url not in unique_references.values():
                new_index = len(unique_references) + 1
                unique_references[new_index] = url
                new_indices.append(new_index)

        if new_indices:
            new_pattern = "[" + ",".join(map(str, new_indices)) + "]"
            updated_answer = updated_answer.replace(pattern, new_pattern)

    return updated_answer, unique_references

# Your original data
answer = "wire [2,3] fraud counts tied [2] to specific [1,2] investors [1,2,3]."
answer = "wire [1,1,2,3,1] fraud counts tied [2,2,4,2] to specific [1,2] investors [1][2][3][4]."
# wire [1,2] fraud counts tied [1] to specific [1] investors [1,2].
references = {
    1: 'https://www.cnn.com/2022/01/03/tech/elizabeth-holmes-verdict/index.html',
    2: 'https://www.cnn.com/2022/01/03/tech/elizabeth-holmes-verdict/index.html',
    3: 'https://www.cnn.com/2022/01/04/tech/elizabeth-holmes-rise-and-fall/index.html',
    4: 'https://www.cnn.com/2022/01/05/tech/elizabeth-holmes-rise-and-fall/index.html'
}

updated_answer, unique_references = correct_references(answer, references)

print("Original Answer:", answer)
print("Updated Answer:", updated_answer)
print("Unique References:", unique_references)
