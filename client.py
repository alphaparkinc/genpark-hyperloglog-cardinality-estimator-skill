"""HyperLogLog Cardinality Estimator.
100% Python Standard Library.
"""
import math
import hashlib
from typing import Dict, Any, List

class HyperLogLogCardinalityEstimator:
    """Pure Python 64-register HyperLogLog cardinality estimator."""
    def __init__(self, p: int = 6):
        self.p = p
        self.m = 1 << p
        self.registers: Dict[str, List[int]] = {}

        if self.m == 16:
            self.alpha = 0.673
        elif self.m == 32:
            self.alpha = 0.697
        elif self.m == 64:
            self.alpha = 0.709
        else:
            self.alpha = 0.7213 / (1.0 + 1.079 / self.m)

    def _get_registers(self, hll_id: str) -> List[int]:
        if hll_id not in self.registers:
            self.registers[hll_id] = [0] * self.m
        return self.registers[hll_id]

    def _hash(self, item: str) -> int:
        return int(hashlib.sha256(item.encode("utf-8")).hexdigest()[:16], 16)

    def add_item(self, hll_id: str, item: str) -> None:
        regs = self._get_registers(hll_id)
        x = self._hash(str(item))
        j = x & (self.m - 1)
        w = x >> self.p

        leading_zeros = 1
        while w > 0 and (w & 1) == 0:
            leading_zeros += 1
            w >>= 1

        regs[j] = max(regs[j], leading_zeros)

    def add_batch(self, hll_id: str, items: List[str]) -> Dict[str, Any]:
        for item in items:
            self.add_item(hll_id, item)
        return {"hll_id": hll_id, "items_added": len(items)}

    def estimate_cardinality(self, hll_id: str) -> Dict[str, Any]:
        regs = self._get_registers(hll_id)
        z = sum(2.0 ** (-reg) for reg in regs)
        raw_estimate = self.alpha * (self.m ** 2) / z

        if raw_estimate <= 2.5 * self.m:
            zeros = regs.count(0)
            if zeros != 0:
                cardinality = self.m * math.log(self.m / zeros)
            else:
                cardinality = raw_estimate
        else:
            cardinality = raw_estimate

        return {
            "hll_id": hll_id,
            "registers_count": self.m,
            "estimated_cardinality": int(round(cardinality))
        }

    def merge_hll(self, target_id: str, source_id: str) -> Dict[str, Any]:
        t_regs = self._get_registers(target_id)
        s_regs = self._get_registers(source_id)
        for i in range(self.m):
            t_regs[i] = max(t_regs[i], s_regs[i])
        return {"status": "merged", "target_id": target_id, "source_id": source_id}
