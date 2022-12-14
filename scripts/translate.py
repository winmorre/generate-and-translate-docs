from pathlib import Path

from googletrans import Translator

SERVICE_URLS = ["https://translate.googleapis.com/$discovery/rest?version=v3", "https://translate.googleapis.com"]

translator = Translator(service_urls=SERVICE_URLS)


def translation(text: str, dest_lng: str):
    return translator.translate(text=text, dest=dest_lng).text


def translate_file_content(output_path: Path, content: str, lng_code: str) -> None:
    content_lines = content.splitlines()
    skip = False

    translated_content = []

    for sentence in content_lines:
        sentence_strip = sentence.strip()

        if sentence_strip.startswith("```") and sentence_strip != "```":
            skip = True

        if skip:
            translated_content.append(sentence)

        if sentence_strip == "```":
            skip = False

        if "](" in sentence_strip:
            tokenize_i = sentence.split(" ")
            sub_sentence = ""

            for j in tokenize_i:
                if "](" not in j:
                    token_translate = translation(text=j, dest_lng=lng_code)
                    sub_sentence += f" {token_translate}"
                else:
                    j_split = j.split("](")
                    j_split_translate = translation(text=j_split[0] + "]", dest_lng=lng_code)
                    merge_i_trans = f" {j_split_translate}({j_split[1]}"
                    sub_sentence += merge_i_trans
            translated_content.append(sub_sentence)

        if not skip and sentence_strip != "```" and "](" not in sentence_strip:
            translated_sentence = translation(
                text=sentence,
                dest_lng=lng_code
            )

            translated_content.append(translated_sentence)

    merged_text = "\n".join(translated_content)
    output_path.write_text(merged_text, encoding="utf-8")

# supported languages link https://cloud.google.com/translate/docs/languages
