import json, sys
import parliament

def scan_file(path):
    try:
        with open(path) as f:
            content = f.read()
        result = parliament.analyze_policy_string(content, filepath=path, include_community_auditors=True)
    except Exception as e:
        return None, str(e)
    return result, None

if __name__ == "__main__":
    path = sys.argv[1]
    result, err = scan_file(path)
    if err or result is None:
        print(json.dumps({"valid": False, "error": err}))
        sys.exit(0)
    findings = []
    for f in result.findings:
        findings.append({
            "issue": f.issue,
            "detail": str(f.detail) if f.detail else "",
            "severity": str(f.severity) if hasattr(f, "severity") else "UNKNOWN",
            "location": str(f.location) if f.location else "",
        })
    print(json.dumps({"valid": True, "findings": findings}))
