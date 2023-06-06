################################################################################################
### prompts ###
################################################################################################
Eqline = "====================================== \n"
roles = ["user", "assistant", "system"]
gpt_model = ["gpt-3.5-turbo", "gpt-4"]

gpt35 = "gpt-3.5-turbo"
gpt4 = "gpt-4"
################################################################################################
import openai
import os
import json
import regex as re
import tiktoken


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
################################################################################################


############################################################
def append_message(messages, input_txt, role):
    messages.append({"role": role, "content": f"{input_txt}"})

def delete_message(messages):
    messages.pop()

def llmagent(message_array, llmmodel, temp):
    responsestr = ""
    while True:
        try:
            response = openai.ChatCompletion.create(
                model=llmmodel,
                temperature=temp,
                messages=message_array
            )
            print(response.choices[0].message.content)
            responsestr = response.choices[0].message.content
        except Exception as e:
            print("Error in LLM agent: ", e)
    
        if responsestr != "":
            return responsestr


template1 = "Given a user requirement for a research proposal, generate a research question and paper name. Return just a dictionary with the research question and the paper name."


# Function for research question + paper name.

research_question = ""
paper_name = ""

author_name = ""
institution_name = ""

abstract = ""

contents_page = ""

page_name_array = []
page_summaries_array = []
pages_array = []


def generate_name_and_question():
    msg = []
    global research_question
    global paper_name
    append_message(msg, template1, roles[2])

    print("Enter idea for research paper: ")
    user_input = input()
    append_message(msg, user_input, roles[0])

    json_response = llmagent(msg, gpt4, 0)
    loaded_json = json.loads(json_response).items()
    loaded_json = list(loaded_json)
    paper_name = loaded_json[0][1]
    research_question = loaded_json[1][1]

def generate_imaginary_authorname_and_institution():
    msg = []
    global author_name
    global institution_name
    template2 = f"""Create a fake researcher name, based on the following research question: {research_question}, and paper name: {paper_name}. Return just a dictionary with the author name and a plausible institution name."""

    append_message(msg, template2, roles[2])

    json_response = llmagent(msg, gpt4, 0)
    loaded_json = json.loads(json_response).items()
    loaded_json = list(loaded_json)
    author_name = loaded_json[0][1]
    institution_name = loaded_json[1][1]

def generate_abstract():
    msg = []
    global abstract
    template3 = f"""A research paper abstract based on the following research question: {research_question}, paper name: {paper_name}, institution name: {institution_name} and author name: {author_name}. Return just the abstract."""
    template0000 = "Write well written abstracts for research papers."
    append_message(msg, template0000, roles[2])
    append_message(msg, template3, roles[0])
    abstract = llmagent(msg, gpt4, 0)

def generate_contents():
    msg = []
    global contents_page
    template4 = f"""A plausible contents page based on the following research question: {research_question}, paper name: {paper_name}, author name: {author_name}, institution name: {institution_name}, abstract: {abstract}. Return just the contents page."""
    template000 = "Write a contents page for a research paper."
    append_message(msg, template000, roles[2])
    append_message(msg, template4, roles[0])
    contents_page = llmagent(msg, gpt4, 0)



def generate_page_names():
    global contents_page
    global page_name_array
    msg = []
    pattern = re.compile("^\d\. .*$")

    template45 = f"""Output a simple list of page number and names based on a given contents page. Just return a list of page numbers and names with each page number and name written on a new line."""

    append_message(msg, template45, roles[2])
    append_message(msg, contents_page, roles[0])

    page_dictionary = llmagent(msg, gpt4, 0)

    page_dictionary = page_dictionary.split("\n")

    for i in page_dictionary:
        if i == "":
            continue

        if pattern.search(i) != None:
            continue
        
        else:
            page_name_array.append(i)

def generate_page_summaries():
    global page_summaries_array
    for page in page_name_array:
        msg = []
        template6 = f"""Generate a page summary of a given page from an academic paper."""
        template65 = f"""Research question: {research_question}, paper name: {paper_name}, author name: {author_name}, institution name: {institution_name}, abstract: {abstract}, contents page: {contents_page}. Page name: {page}. Page summary:"""
        append_message(msg, template6, roles[2])
        append_message(msg, template65, roles[0])
        page_summaries_array.append(llmagent(msg, gpt35, 0))

def generate_pages():
    global pages_array
    page_number = 0
    for page_summary in page_summaries_array:
        msg = []
        template7 = f"""Generate the given page of an academic paper. Generate just the page content."""
        template8 = f"""Research question: {research_question}, paper name: {paper_name}, author name: {author_name}, institution name: {institution_name}, abstract: {abstract}, contents page: {contents_page}. Page summary: {page_summary}. Page name: {page_name_array[page_number]}. Page:"""
        append_message(msg, template7, roles[2])
        append_message(msg, template8, roles[0])
        pages_array.append(llmagent(msg, gpt4, 0))
        page_number += 1

# create a function to write a paper to txt file based on the above variables.

def abbreviate_filename(paper_name, ext='txt'):
    # Remove special characters and spaces
    safe_name = re.sub('[\W_]+', '', paper_name)
    # Shorten to 12 characters
    short_name = safe_name[:12]
    # Add extension
    filename = f'{short_name}.{ext}'
    return filename


def write_paper():

    generate_name_and_question()
    generate_imaginary_authorname_and_institution()
    generate_abstract()
    generate_contents()
    generate_page_names()
    generate_page_summaries()
    generate_pages()

    paperabrev = paper_name.split(" ")
    paperabrev = "".join([i[0] for range(i)[8] in paperabrev])
    
    short_paper_name = abbreviate_filename(paper_name)

    # write paper based on variables.
    with open(f"{short_paper_name}.txt", "w") as f:
        f.write(f"Paper Name: {paper_name}\n\n")
        f.write(f"Institution Name: {institution_name}\n\n")
        f.write(f"Author Name: {author_name}\n\n")
        f.write(f"Research Question: {research_question}\n\n")
        f.write(f"Abstract: {abstract}\n\n")
        f.write(f"Contents Page: {contents_page}\n\n")
        page_num = 1
        for page in pages_array:
            f.write(f"\n\nPage: {page_num},\n\n{page}\n\n")
            page_num += 1
        f.close()

'''
Example paper:
Using llms and robotics to create the perfect cup of tea on user voice commands.
'''


# Update to:
# LaTex paper template !!! !!!!

write_paper()
