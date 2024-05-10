import re, requests, dotenv, os
from bs4 import BeautifulSoup

dotenv.load_dotenv()

import anthropic
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL_NAME = "claude-3-opus-20240229"
CLIENT = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# Récupérer la remove_floating_variables_prompt dans le fichier txt "data/remove_floating_variables_prompt.txt"
remove_floating_variables_prompt = open("data/remove_floating_variables_prompt.txt", "r").read()

def pretty_print(message):
    print('\n\n'.join('\n'.join(line.strip() for line in re.findall(r'.{1,100}(?:\s+|$)', paragraph.strip('\n'))) for paragraph in re.split(r'\n\n+', message)))

def extract_between_tags(tag: str, string: str, strip: bool = False) -> list[str]:
    ext_list = re.findall(f"<{tag}>(.+?)</{tag}>", string, re.DOTALL)
    if strip:
        ext_list = [e.strip() for e in ext_list]
    return ext_list

def remove_empty_tags(text):
    return re.sub(r'\n<(\w+)>\s*</\1>\n', '', text, flags=re.DOTALL)

def extract_prompt(metaprompt_response):
    between_tags = extract_between_tags("Instructions", metaprompt_response)[0]
    return between_tags[:1000] + remove_empty_tags(remove_empty_tags(between_tags[1000:]).strip()).strip()

def extract_variables(prompt):
    pattern = r'{([^}]+)}'
    variables = re.findall(pattern, prompt)
    return set(variables)

def remove_inapt_floating_variables(prompt):
    message = CLIENT.messages.create(
        model=MODEL_NAME,
        # model="claude-3-sonnet-20240229",
        # model="claude-3-haiku-20240307",
        messages=[{'role': "user", "content": remove_floating_variables_prompt.replace("{$PROMPT}", prompt)}],
        max_tokens=4096,
        temperature=0
    ).content[0].text
    return extract_between_tags("rewritten_prompt", message)[0]

def find_free_floating_variables(prompt):
    variable_usages = re.findall(r'\{\$[A-Z0-9_]+\}', prompt)

    free_floating_variables = []
    for variable in variable_usages:
        preceding_text = prompt[:prompt.index(variable)]
        open_tags = set()

        i = 0
        while i < len(preceding_text):
            if preceding_text[i] == '<':
                if i + 1 < len(preceding_text) and preceding_text[i + 1] == '/':
                    closing_tag = preceding_text[i + 2:].split('>', 1)[0]
                    open_tags.discard(closing_tag)
                    i += len(closing_tag) + 3
                else:
                    opening_tag = preceding_text[i + 1:].split('>', 1)[0]
                    open_tags.add(opening_tag)
                    i += len(opening_tag) + 2
            else:
                i += 1

        if not open_tags:
            free_floating_variables.append(variable)

    return free_floating_variables

def get_abstract(doi):
    if doi is None:
        return "DOI non trouvé."

    # On essaie d'abord avec l'API Crossref
    base_url = "https://api.crossref.org/works/"
    try:
        response = requests.get(base_url + doi)
        if response.status_code == 200:
            data = response.json()
            abstract = data["message"].get("abstract")
            if abstract:
                clean_abstract = " ".join(abstract.split())
                clean_abstract = clean_abstract.replace("<jats:title>", "").replace("</jats:title>", "")
                clean_abstract = clean_abstract.replace("<jats:italic>", "").replace("</jats:italic>", "")
                clean_abstract = clean_abstract.replace("<jats:bold>", "").replace("</jats:bold>", "")
                clean_abstract = clean_abstract.replace("<jats:underline>", "").replace("</jats:underline>", "")
                clean_abstract = clean_abstract.replace("<jats:sub>", "").replace("</jats:sub>", "")
                clean_abstract = clean_abstract.replace("<jats:sec>", "").replace("</jats:sec>", "")
                clean_abstract = clean_abstract.replace("<jats:p>", "").replace("</jats:p>", "")
                return clean_abstract
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête à l'API Crossref: {str(e)}")

    # Si l'abstract n'est pas trouvé avec le Crossref API, on essaie avec le PubMed Central API
    base_url = "https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/"
    try:
        response = requests.get(base_url, params={"ids": doi, "format": "json"})
        if response.status_code == 200:
            data = response.json()
            pmc_id = data["records"][0].get("pmcid")
            if pmc_id:
                article_url = f"https://www.ncbi.nlm.nih.gov/pmc/articles/{pmc_id}/"
                article_response = requests.get(article_url)
                if article_response.status_code == 200:
                    soup = BeautifulSoup(article_response.text, "html.parser")
                    abstract_element = soup.find("div", class_="abstract")
                    if abstract_element:
                        abstract_text = abstract_element.get_text(strip=True)
                        return abstract_text
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête à l'API PubMed Central: {str(e)}")

    return "Abstract not found."