default_prompt_template = '''
        Generate an answer (no more than 50 words) for a given question based solely on the given documents. 
        Cite the documents using numeric references in the text. 
        If multiple documents contain the answer, cite those documents like [1,2] at the end of the sentence in the answer. 
        If the documents do not contain the answer to the question, say that 'answering is not possible given the available information.'

        {join(documents, delimiter=new_line, pattern=new_line+'Document[$idx]: $content', str_replace={new_line: ' ', '[': '(', ']': ')'})}

        Question: {query}; Answer:
    '''

long_prompt_template = '''
        Generate a detailed and informative answer (up to 100 words) for a given question based solely on the given documents. 
        Cite the documents using numeric references in the text. 
        If multiple documents contain the answer, cite those documents like [1,2] at the end of the sentence in the answer. 
        If the documents do not contain the answer to the question, say that 'answering is not possible given the available information.'

        {join(documents, delimiter=new_line, pattern=new_line+'Document[$idx]: $content', str_replace={new_line: ' ', '[': '(', ']': ')'})}

        Question: {query}; Answer:
    '''

short_prompt_template = '''
        Generate a concise answer (as short as possible) for a given question based solely on the given documents. 
        Cite the documents using numeric references in the text. 
        If multiple documents contain the answer, cite those documents like [1,2] at the end of the sentence in the answer. 
        If the documents do not contain the answer to the question, say that 'answering is not possible given the available information.'

        {join(documents, delimiter=new_line, pattern=new_line+'Document[$idx]: $content', str_replace={new_line: ' ', '[': '(', ']': ')'})}

        Question: {query}; Answer:
    '''

temperature_prompt_template = '''
        Answer the given question based solely on the given documents. 
        You can include as much or as little relevant information in the answer, but the answer should not be more than 100 words.
        Cite the documents using numeric references in the text. 
        If multiple documents contain the answer, cite those documents like [1,2] at the end of the sentence in the answer. 
        If the documents do not contain the answer to the question, say that 'answering is not possible given the available information.'

        {join(documents, delimiter=new_line, pattern=new_line+'Document[$idx]: $content', str_replace={new_line: ' ', '[': '(', ']': ')'})}

        Question: {query}; Answer:
    '''


questions = [
    # 0-5
    "Can pig hearts be used for human transplants? Is it safe?",
    "Why did the man receive a pig heart transplant?",
    "Why is Elizabeth Holmes on trial?",
    "Is Elizabeth Holmes guilty?",
    "What was the Supreme Court's ruling on the Biden administration's vaccine mandate for large employers?",
    # 6-10
    "What companies took action against Russia?",
    "What is the US's stance on the Ukraine crisis?",
    "What is China's stance on the Ukraine crisis?",
    "Did the US send troops to Ukraine?",
    "Why are companies are moving out of Russia?",
    # 11-15
    "Who's nominated for best supporting actress?",
    "Who is Ketanji Jackson?",
    "What's the controversy surrounding Eileen Gu",
    "Who is Eileen Gu?",
    "What images did James Webb Telescope capture?"
]