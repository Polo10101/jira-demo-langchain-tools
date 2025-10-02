
"""This function let us parse the json in way that we can obtain the text from the comments or description and summary in the issue. (Could be
used for other actions)."""

def extrat_text_fields(adf_json):
    text = []
    def extract_content(content):
        for item in content:
            if item.get("type") == "text":
                text.append(item.get("text", ""))
            elif "content" in item:
                extract_content(item["content"])
    if isinstance(adf_json, dict):
        extract_content(adf_json.get("content", []))
    return "\n\n".join(text)