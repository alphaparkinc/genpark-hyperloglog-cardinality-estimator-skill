"""Example usage for GenPark HyperLogLog Cardinality Estimator."""
from client import HyperLogLogCardinalityEstimator

def main():
    hll = HyperLogLogCardinalityEstimator(p=6)
    print("Ingesting 500 distinct query fingerprints into HLL...")
    queries = [f"prompt_query_{i}" for i in range(500)]
    hll.add_batch("stream_analytics", queries)

    est = hll.estimate_cardinality("stream_analytics")
    print("HyperLogLog Cardinality Estimate:")
    print(f" - True Distinct Count: 500")
    print(f" - HLL Estimate:        {est['estimated_cardinality']}")
    print(f" - Error Margin:        {round(abs(est['estimated_cardinality'] - 500) / 500 * 100, 2)}%")

if __name__ == "__main__":
    main()
