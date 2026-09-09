"""Example usage for HyperLogLog Skill."""
from client import HyperLogLog

def main():
    print("Executing HyperLogLog Cardinality Estimation...")
    hll = HyperLogLog(b=8)
    true_unique = 1500
    for i in range(true_unique):
        hll.add(f"unique_sensor_reading_{i}")
        # Insert duplicates
        if i % 2 == 0:
            hll.add(f"unique_sensor_reading_{i}")

    estimated = hll.count()
    print(f"True unique: {true_unique}, Estimated: {estimated}")
    error_ratio = abs(estimated - true_unique) / true_unique
    print(f"Relative error: {error_ratio:.2%}")
    assert error_ratio < 0.15, "HLL error exceeded margin"
    print("HyperLogLog verified successfully!")

if __name__ == "__main__":
    main()
