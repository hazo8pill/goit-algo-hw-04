import random
import timeit


def insertion_sort(arr):
    a = list(arr)
    for i in range(1, len(a)):
        key, j = a[i], i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


def merge_sort(arr):
    if len(arr) <= 1:
        return list(arr)
    mid = len(arr) // 2
    left, right = merge_sort(arr[:mid]), merge_sort(arr[mid:])
    merged, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


ALGORITHMS = {"insertion": insertion_sort, "merge": merge_sort, "timsort": sorted}


def make_datasets(n, seed=42):
    rng = random.Random(seed)
    data = [rng.randint(0, n) for _ in range(n)]
    ordered = sorted(data)
    nearly = ordered.copy()
    for _ in range(max(1, n // 100)):
        i, j = rng.randrange(n), rng.randrange(n)
        nearly[i], nearly[j] = nearly[j], nearly[i]
    return {
        "random": data,
        "sorted": ordered,
        "reversed": ordered[::-1],
        "nearly_sorted": nearly,
    }


def benchmark(sizes, number=3):
    rows = []
    for n in sizes:
        for name, data in make_datasets(n).items():
            for algo, fn in ALGORITHMS.items():
                t = timeit.timeit(lambda: fn(data), number=number) / number
                rows.append({"algorithm": algo, "size": n, "dataset": name, "seconds": t})
    return rows


def to_markdown(rows):
    headers = ["Dataset", "N", *(f"{a.capitalize()}, s" for a in ALGORITHMS), "Merge/Timsort"]
    lines = ["| " + " | ".join(headers) + " |",
             "|---|" + "---:|" * (len(headers) - 1)]
    table = {}
    for r in rows:
        table.setdefault((r["dataset"], r["size"]), {})[r["algorithm"]] = r["seconds"]
    for (ds, n), t in sorted(table.items()):
        times = " | ".join(f"{t[a]:.6f}" for a in ALGORITHMS)
        lines.append(f"| {ds} | {n} | {times} | ×{t['merge'] / t['timsort']:.0f} |")
    return "\n".join(lines)


def main():
    print(to_markdown(benchmark([100, 1_000, 5_000, 10_000])))


if __name__ == "__main__":
    main()
