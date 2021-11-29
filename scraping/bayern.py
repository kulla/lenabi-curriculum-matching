from lxml import html
import json

def parseHTML(path):

    with open(path) as fobj:
        f = fobj.read()

    root = html.fromstring(f)

    plan = {}
    for page in root.findall(".//div[@class='fachlehrplan ']"):
        for topic in page.findall("./div"):
            if topic.get("class") == "open toggable headline_lvl1 ":
                topic_name = topic.xpath("./h3/a/span")[1].text_content().strip()
            if topic.get("class") == "open toggable headline_lvl2 ":
                plan.setdefault(topic_name, []).append(
                    topic.xpath("./h4/a/span")[1].text_content().strip()
                )
    return plan

if __name__ == "__main__":
    import sys
    plan = parseHTML(sys.argv[1])
    print(json.dumps(plan))
