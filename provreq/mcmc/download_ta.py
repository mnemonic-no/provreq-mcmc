import json
import re
import unicodedata

from attampck import data, matrices, stixmap


def slugify(value: str, allow_unicode: bool = False) -> str:
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")


d = data.Attampck()

for g in d.iterate(matrices.ENTERPRISE, stixmap.GROUP):
    res = {"agents": [], "tool_agents": []}
    for ref in d.enterprise_memorystore.relationships(
        g, source_only=True, relationship_type="uses"
    ):
        target_object = d.enterprise.get(ref.target_ref)
        if target_object and target_object[0]["type"] == stixmap.TECHNIQUE:
            res["agents"].append(data.resolve_mitre_id(target_object[0]))
        elif target_object and target_object[0]["type"] == stixmap.TOOL:
            for tref in d.enterprise_memorystore.relationships(
                target_object[0], source_only=True, relationship_type="uses"
            ):
                target_object = d.enterprise.get(tref.target_ref)
                if target_object and target_object[0]["type"] == stixmap.TECHNIQUE:
                    res["tool_agents"].append(
                        data.resolve_mitre_id(target_object[0])
                    )
    with open(slugify(g["name"]) + ".json", "w", encoding="utf-8") as f:
        print("Writing ", slugify(g["name"]) + ".json")
        f.write(json.dumps(res))
