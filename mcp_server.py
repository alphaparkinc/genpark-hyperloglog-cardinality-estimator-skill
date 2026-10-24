"""MCP Stdio Server for HyperLogLog Cardinality Estimator.
100% Python Standard Library.
"""
import sys
import json
from client import HyperLogLogCardinalityEstimator

estimator = HyperLogLogCardinalityEstimator()

def handle_rpc(line):
    try:
        req = json.loads(line)
    except Exception:
        return
    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        res = {
            "protocolVersion": "2024-11-05",
            "serverInfo": {"name": "genpark-hyperloglog-cardinality-estimator-skill", "version": "1.0.1"},
            "capabilities": {"tools": {}}
        }
        send_response(req_id, res)
    elif method == "tools/list":
        tools = [
            {
                "name": "add_item",
                "description": "Ingest a single element into the HyperLogLog register array",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "hll_id": {"type": "string"},
                        "item": {"type": "string"}
                    },
                    "required": ["hll_id", "item"]
                }
            },
            {
                "name": "add_batch",
                "description": "Batch ingest elements into HyperLogLog register array",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "hll_id": {"type": "string"},
                        "items": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["hll_id", "items"]
                }
            },
            {
                "name": "estimate_cardinality",
                "description": "Calculate estimated distinct cardinality count with small/large range corrections",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "hll_id": {"type": "string"}
                    },
                    "required": ["hll_id"]
                }
            },
            {
                "name": "merge_hll",
                "description": "Merge source HLL estimator into target HLL estimator",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "target_id": {"type": "string"},
                        "source_id": {"type": "string"}
                    },
                    "required": ["target_id", "source_id"]
                }
            }
        ]
        send_response(req_id, {"tools": tools})
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "add_item":
            estimator.add_item(args.get("hll_id", ""), args.get("item", ""))
            out = {"status": "item_added"}
        elif name == "add_batch":
            out = estimator.add_batch(args.get("hll_id", ""), args.get("items", []))
        elif name == "estimate_cardinality":
            out = estimator.estimate_cardinality(args.get("hll_id", ""))
        elif name == "merge_hll":
            out = estimator.merge_hll(args.get("target_id", ""), args.get("source_id", ""))
        else:
            send_error(req_id, -32601, f"Unknown tool: {name}")
            return
        send_response(req_id, {"content": [{"type": "text", "text": json.dumps(out, indent=2)}]})

def send_response(req_id, result):
    sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": req_id, "result": result}) + "\n")
    sys.stdout.flush()

def send_error(req_id, code, message):
    sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": req_id, "error": {"code": code, "message": message}}) + "\n")
    sys.stdout.flush()

def main():
    for line in sys.stdin:
        if line.strip():
            handle_rpc(line.strip())

if __name__ == "__main__":
    main()
