import json

def parse_coverage(file="coverage.json"):
    with open(file) as f:
        data = json.load(f)

    results = []
    for filename, metrics in data["files"].items():
        results.append({
            "file": filename,
            "coverage": metrics["summary"]["percent_covered"]
        })
    return results

if __name__ == "__main__":
    print(parse_coverage())
