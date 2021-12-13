from lxml import html
import json
import re

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
                subtopic = topic.xpath("./h4")[0]
                competences = []
                for competence_list in topic.findall(".//div[@class='thema_absch']"):
                    for competence in competence_list.findall(".//li"):
                        competences.append(competence.text_content().strip())
                    plan.setdefault(topic_name, []).append(
                        {
                            "name": subtopic.xpath("./a/span")[1].text_content().strip(),
                            "competences": competences
                        }
                    )
    graph = []
    next_id = 0
    for toplevel in plan:
        toplevel_id = next_id
        next_id += 1
        toplevel_parts = []
        for midlevel in plan[toplevel]:
            midlevel_id = next_id
            next_id += 1
            toplevel_parts.append(midlevel_id)
            midlevel_parts = []
            for child in midlevel["competences"]:
                child_id = next_id
                next_id += 1
                midlevel_parts.append(child_id)
                graph.append({
                    "id": child_id,
                    "name": None,
                    "description": child,
                    "numberOfHours": None,
                    "isPartOf": [midlevel_id],
                    "hasPart": []
                })
            topic, hours = split_hours(midlevel["name"])
            graph.append({
                "id": midlevel_id,
                "name": topic,
                "description": topic,
                "numberOfHours": hours,
                "isPartOf": [toplevel_id],
                "hasPart": midlevel_parts
            })
        topic, hours = split_hours(toplevel)
        graph.append({
            "id": toplevel_id,
            "name": topic,
            "description": topic,
            "numberOfHours": hours,
            "isPartOf": [],
            "hasPart": toplevel_parts
        })
    return {"graph": graph}

def split_hours(heading):
     m = re.fullmatch("(.+)\s\(ca\.\s([0-9]+)\sStd\.\)", heading)
     assert m is not None
     return m.groups()


if __name__ == "__main__":
    import sys
    plan = parseHTML(sys.argv[1])
    print(json.dumps(plan))
