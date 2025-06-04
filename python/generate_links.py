import json
import sys
from collections import defaultdict

def build_links(nodes):
    potential_links = []
    # Create a quick lookup for nodes by ID
    node_id_map = {node["id"]: node for node in nodes}

    # Step 1: Generate all potential links with their weights
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            source_node = nodes[i]
            target_node = nodes[j]
            weight = 0

            # +5 weight if main_keyword matches
            if source_node.get("main_keyword") == target_node.get("main_keyword"):
                weight += 5

            # +1 per shared keyword
            source_keywords = set(source_node.get("keyword", []))
            target_keywords = set(target_node.get("keyword", []))
            shared_keywords = source_keywords.intersection(target_keywords)
            weight += len(shared_keywords)

            if weight > 0:
                potential_links.append({
                    "source": source_node["id"],
                    "target": target_node["id"],
                    "weight": weight
                })

    # Step 2: Prioritize keeping nodes connected
    # Build an adjacency list to easily count existing links for each node
    adj_list = defaultdict(list)
    for link in potential_links:
        adj_list[link["source"]].append(link)
        adj_list[link["target"]].append(link) # Store the link object itself or just id

    # Determine which links to keep. We'll iterate and make decisions.
    final_links = []
    links_to_consider_for_removal = set() # Use a set to track links by (source, target) tuple

    # Identify links with weight 1 that are candidates for removal
    for link in potential_links:
        if link["weight"] == 1:
            # Store a canonical representation (e.g., sorted tuple) for easy lookup in a set
            s_id, t_id = sorted((link["source"], link["target"]))
            links_to_consider_for_removal.add((s_id, t_id))

    # Iterate through potential links and decide whether to keep or remove
    for link in potential_links:
        s_id = link["source"]
        t_id = link["target"]
        link_weight = link["weight"]

        # Canonical representation for the current link
        current_link_tuple = tuple(sorted((s_id, t_id)))

        # Rule 1: Always keep links with weight > 1
        if link_weight > 1:
            final_links.append(link)
        else: # Link weight is 1
            # Check if this link is a candidate for removal
            if current_link_tuple in links_to_consider_for_removal:
                # Count how many links each node would have *if this specific link were removed*
                # We need to consider other links, not just the initial count
                source_other_links_count = sum(1 for l in adj_list[s_id] if tuple(sorted((l["source"], l["target"]))) != current_link_tuple)
                target_other_links_count = sum(1 for l in adj_list[t_id] if tuple(sorted((l["source"], l["target"]))) != current_link_tuple)

                # Rule 2: Remove a weight 1 link ONLY if both source AND target nodes
                # would still have at least one other connection (from a link of any weight)
                # AFTER this link is removed.
                if source_other_links_count >= 1 and target_other_links_count >= 1:
                    # This link can be removed because both nodes are still connected elsewhere
                    continue # Skip adding this link to final_links
                else:
                    # Keep this link because at least one node would become isolated if removed
                    final_links.append(link)
            else:
                # This case should ideally not be hit if links_to_consider_for_removal
                # correctly contains all weight 1 links. Added for safety.
                final_links.append(link)

    # Sanity check: Ensure no node that had any potential links ends up with zero final links
    # (unless it genuinely had no main_keyword or shared keywords with anyone)
    # This is a post-processing step to re-add links if absolutely necessary
    node_has_links_in_final = defaultdict(bool)
    for link in final_links:
        node_has_links_in_final[link["source"]] = True
        node_has_links_in_final[link["target"]] = True

    # Check for nodes that originally had potential links but lost them all
    for node_id in node_id_map.keys():
        if not node_has_links_in_final[node_id] and len(adj_list[node_id]) > 0:
            # This node had links, but now has none. Try to add back its strongest missing link.
            # Find the strongest link that involved this node and was removed
            strongest_missing_link = None
            max_weight = 0
            for link in potential_links:
                s_id, t_id = sorted((link["source"], link["target"]))
                if (link["source"] == node_id or link["target"] == node_id) and \
                   tuple(sorted((link["source"], link["target"]))) not in [(fl["source"], fl["target"]) for fl in final_links]: # Check if not already in final_links
                    if link["weight"] > max_weight:
                        max_weight = link["weight"]
                        strongest_missing_link = link
            if strongest_missing_link:
                # Only add if it's not already there
                if not any(sl["source"] == strongest_missing_link["source"] and sl["target"] == strongest_missing_link["target"] for sl in final_links):
                    final_links.append(strongest_missing_link)
                    node_has_links_in_final[strongest_missing_link["source"]] = True
                    node_has_links_in_final[strongest_missing_link["target"]] = True


    return final_links

def main():
    if len(sys.argv) != 3:
        print("Usage: python generate_links.py nodes.json links.json")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    try:
        with open(input_path, "r", encoding="utf-8") as f:
            nodes = json.load(f)
    except FileNotFoundError:
        print(f"Error: nodes.json not found at {input_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {input_path}. Check file format.")
        sys.exit(1)
    except UnicodeDecodeError as e:
        print(f"Error: UnicodeDecodeError when reading {input_path}. Ensure it's UTF-8 encoded. Details: {e}")
        sys.exit(1)


    links = build_links(nodes)

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(links, f, indent=2)
    except Exception as e:
        print(f"Error writing links.json to {output_path}: {e}")
        sys.exit(1)

    print(f"Generated {len(links)} links and saved to {output_path}")

if __name__ == "__main__":
    main()