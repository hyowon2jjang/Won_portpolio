import json
import sys

def build_links(nodes):
    links = []
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            source = nodes[i]
            target = nodes[j]
            weight = 0

            # +5 weight if main_keyword matches
            if source.get("main_keyword") == target.get("main_keyword"):
                weight += 5

            # +1 per shared keyword
            source_keywords = set(source.get("keyword", []))
            target_keywords = set(target.get("keyword", []))
            shared_keywords = source_keywords & target_keywords
            weight += len(shared_keywords)

            if weight > 0:
                links.append({
                    "source": source["id"],
                    "target": target["id"],
                    "weight": weight
                })
    return links

def main():
    if len(sys.argv) != 3:
        print("Usage: python generate_links.py nodes.json links.json")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    with open(input_path, "r") as f:
        nodes = json.load(f)

    links = build_links(nodes)

    with open(output_path, "w") as f:
        json.dump(links, f, indent=2)

    print(f"Generated {len(links)} links and saved to {output_path}")

if __name__ == "__main__":
    main()
