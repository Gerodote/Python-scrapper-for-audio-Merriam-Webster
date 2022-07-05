import json
import re

import requests
from bs4 import BeautifulSoup as bs


def remove(string):
    pattern = re.compile("\s+")
    return re.sub(pattern, '', string).replace(r'\n', '').replace(r'\t', '').replace(r"\'", '').replace(r"'", '')


def get_audio_url_of_word(word):
    base_url = "https://www.merriam-webster.com/dictionary/"
    url = base_url + word
    site_connection = requests.get(url)
    html_code = site_connection.content
    if not b"isn't in the dictionary" in html_code:
        soup = bs(html_code, features="html.parser")
        script_bs4 = soup.find("script", attrs={"type": "application/ld+json"})
        script = script_bs4.contents
        script_without_whitespaces = remove(str(script))
        json_of_script = json.loads(script_without_whitespaces)
        name_of_needed_key = "contentURL"
        needed_value = None
        for a_dict in json_of_script[0]:
            if name_of_needed_key in a_dict:
                needed_value = a_dict[name_of_needed_key]

        return needed_value

    else:
        raise KeyError("There's no such word in Merriam-Webster dictionary.")


def main():
    word = input("Enter a word:")
    try:
        print(get_audio_url_of_word(word))
    except KeyError:
        print("There's no such word. ")


if __name__ == '__main__':
    main()
