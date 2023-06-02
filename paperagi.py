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
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def append_message(messages, input_txt, role):
    messages.append({"role": role, "content": f"{input_txt}"})

def delete_message(messages):
    messages.pop()

def llmagent(message_array, llmmodel, temp):
    response = openai.ChatCompletion.create(
        model=llmmodel,
        temperature=temp,
        messages=message_array
    )
    print(response.choices[0].message.content)
    return response.choices[0].message.content



'''
ideas to write a phd writer. 

Steps: 

Get an imaginary arxiv pdf. Get imaginary authors, at a real institution. Get the abstract. Get the contents. Make an array of pages_summaries. Make an array of pages. Write a summary of each page and append summaries to array. Write each page based on summaries.


Generated variables:
{papner name, author name, institution, abstract, contents_page, pange_name-num, page summaries, pages}


V1 Steps:

1. Generate a paper name.
2. Generate an author name.
3. Generate an institution name.
4. Generate an abstract.
5. Generate a contents page.
6. Generate a page name.
7. Write a summary of each page and append summaries to array.
8. Write each page based on summaries.


V2 Steps:

1. Transform user prompt into research question + paper name.
2. Get research question + paper name, and generate imaginary author name + institution name.
3. Get research question, paper name, author name, and institution name, and generate abstract.
4. Get research question, paper name, author name, institution name, and abstract, and generate contents page.
5. Get page names from contents page, and append to page_name-num array.
6. Get research question, paper name, author name, institution name, abstract, and page_array, and generate page summaries, and append to page_summaries array.
7. Get research question, paper name, author name, institution name, abstract, contents page, page_name-num array, and page_summaries array, and generate pages.

'''



# prompt template for

# 1. Generate research question + paper name.

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
    template3 = f"""Generate a plausible research paper abstract based on the following research question: {research_question}, paper name: {paper_name}, institution name: {institution_name} and author name: {author_name}"""

    append_message(msg, template3, roles[2])

    abstract = llmagent(msg, gpt4, 0)

def generate_contents():
    msg = []
    global contents_page
    template4 = f"""Generate a plausible contents page based on the following research question: {research_question}, paper name: {paper_name}, author name: {author_name}, institution name: {institution_name}, and abstract: {abstract}."""

    append_message(msg, template4, roles[2])
    contents_page = llmagent(msg, gpt4, 0)

def generate_page_names():
    global contents_page
    global page_name_array
    msg = []

    template45 = f"""Generate a json dictionary of page names and page numbers based on the following contents page: {contents_page}."""

    append_message(msg, template45, roles[2])
    page_dictionary = llmagent(msg, gpt4, 0)

    page_dictionary = json.loads(page_dictionary).items()

    for i in page_dictionary:
        page_number, page_name = i
        page_name_and_numbers = f"{page_number}, {page_name}"
        page_name_array.append(page_name_and_numbers)

def generate_page_summaries():
    global page_summaries_array
    for page in page_name_array:
        msg = []
        template6 = f"""Generate a plausible page summary based on the following research question: {research_question}, paper name: {paper_name}, author name: {author_name}, institution name: {institution_name}, abstract: {abstract}, contents page: {contents_page}, and page name: {page}."""
        append_message(msg, template6, roles[2])
        page_summaries_array.append(llmagent(msg, gpt4, 0))

def generate_pages():
    global pages_array
    page_number = 0
    for page_summary in page_summaries_array:
        msg = []
        template7 = f"""Generate a plausible page based on the following research question: {research_question}, paper name: {paper_name}, author name: {author_name}, institution name: {institution_name}, abstract: {abstract}, contents page: {contents_page}, page name: {page_name_array[page_number]} page summary{page_summary}."""
        append_message(msg, template7, roles[2])
        pages_array.append(llmagent(msg, gpt4, 0))
        page_number += 1


# create a function to write a paper to txt file based on the above variables.

def write_paper():

    generate_name_and_question()
    generate_imaginary_authorname_and_institution()
    generate_abstract()
    generate_contents()
    generate_page_names()
    generate_page_summaries()
    generate_pages()

    # write paper based on variables.
    with open("paper.txt", "w") as f:
        f.write(f"Research Question: {research_question} \n")
        f.write(f"Paper Name: {paper_name} \n")
        f.write(f"Author Name: {author_name} \n")
        f.write(f"Institution Name: {institution_name} \n")
        f.write(f"Abstract: {abstract} \n")
        f.write(f"Contents Page: {contents_page} \n")
        f.write(f"Page Name Array: {page_name_array} \n")
        f.write(f"Page Summaries Array: {page_summaries_array} \n")
        f.write(f"Pages Array: {pages_array} \n")
        f.close()

'''
Using llms and robotics to create the perfect cup of tea on user voice commands.
'''

write_paper()
