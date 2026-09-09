"""MCP Server for HyperLogLog Skill."""
import json
import sys
from client import HyperLogLog

def main():
    hll = HyperLogLog()
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            req_id = req.get("id")
            method = req.get("method")
            params = req.get("params", {})

            if method == "tools/list":
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "tools": [{
                            "name": "estimate_unique_elements",
                            "description": "Estimate distinct count of elements using HyperLogLog",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "items": {"type": "array", "items": {"type": "string"}}
                                },
                                "required": ["items"]
                            }
                        }]
                    }
                }
            elif method == "tools/call":
                args = params.get("arguments", {})
                tracker = HyperLogLog()
                for item in args["items"]:
                    tracker.add(item)
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"content": [{"type": "text", "text": json.dumps({"estimated_distinct_count": tracker.count()})}]}
                }
            else:
                res = {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}
            print(json.dumps(res), flush=True)
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32000, "message": str(e)}}
            print(json.dumps(err), flush=True)

if __name__ == "__main__":
    main()
