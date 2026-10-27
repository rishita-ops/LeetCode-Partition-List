# LeetCode — Partition List

A focused Python implementation of **LeetCode's Partition List (Medium)** that **rearranges a singly linked list so every node smaller than `x` comes before every node greater than or equal to `x`** by **walking the list once, sending each node to one of two dummy-headed lists, and then joining the two lists together**. Clean, minimal, and correct — this solution is the entry point to understanding the idea of a **dummy (sentinel) node**, the **tail pointer** technique, **stable partitioning**, and why a single missing line (`greater_tail.next = None`) can turn a correct-looking solution into an infinite loop.

🔗 **Problem link:** [leetcode.com/problems/partition-list](https://leetcode.com/problems/partition-list/)

---

## Problem Statement

You are given the `head` of a linked list and a value `x`.

**Partition** the list such that all nodes **less than** `x` come before nodes **greater than or equal to** `x`.

You should **preserve the original relative order** of the nodes in each of the two partitions.

**Example 1:**

```
Input:  head = [1,4,3,2,5,2], x = 3
Output: [1,2,2,4,3,5]
Explanation: Nodes 1, 2, 2 are less than 3 and keep their order.
Nodes 4, 3, 5 are greater than or equal to 3 and keep their order.
```

**Example 2:**

```
Input:  head = [2,1], x = 2
Output: [1,2]
Explanation: 1 is less than 2, so it moves in front of 2.
```

**Official Constraints:**

- The number of nodes in the list is in the range `[0, 200]`
- `-100 <= Node.val <= 100`
- `-200 <= x <= 200`

---

## The Code

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

head_str = input("Enter head list ): ")
x = int(input("Enter x: "))

clean_str = head_str.replace("[", "").replace("]", "").strip()
if clean_str:
    nodes = [int(i.strip()) for i in clean_str.split(",")]
else:
    nodes = []

head = None
tail = None
for val in nodes:
    new_node = ListNode(val)
    if not head:
        head = new_node
        tail = new_node
    else:
        tail.next = new_node
        tail = new_node

less_dummy = ListNode(0)
greater_dummy = ListNode(0)

less_tail = less_dummy
greater_tail = greater_dummy

current = head
while current:
    if current.val < x:
        less_tail.next = current
        less_tail = less_tail.next
    else:
        greater_tail.next = current
        greater_tail = greater_tail.next
    current = current.next

greater_tail.next = None
less_tail.next = greater_dummy.next

result_head = less_dummy.next
output_list = []
while result_head:
    output_list.append(result_head.val)
    result_head = result_head.next

print(output_list)
```

---

## The Critical Idea — Build Two Lists, Then Join Them

This is the most important thing to understand about this solution.

The program works in **three separate stages**, and no node is ever moved around inside the original list:

1. **Build.** Turn the typed input into a real linked list of `ListNode` objects.
2. **Split.** Walk the list **once**. Every node goes to the end of one of two new lists: the **less** list (`val < x`) or the **greater** list (`val >= x`).
3. **Join.** Attach the **greater** list to the tail of the **less** list, and read the answer from the start of the **less** list.

```
head = 1 → 4 → 3 → 2 → 5 → 2,   x = 3

walk the list once:
   1  →  less      less:    1
   4  →  greater   greater: 4
   3  →  greater   greater: 4 → 3
   2  →  less      less:    1 → 2
   5  →  greater   greater: 4 → 3 → 5
   2  →  less      less:    1 → 2 → 2

join:  less ──► greater
       1 → 2 → 2 → 4 → 3 → 5
```

Because every node is appended at the **tail** of its list in the order it is met, the original relative order inside each partition is preserved automatically. This is called a **stable partition**.

The two **dummy nodes** (`less_dummy` and `greater_dummy`) remove every special case about "is this the first node of the list?". Appending to an empty list and appending to a non-empty list become exactly the same operation.

| Stage    | What happens                                      | Code                                                  |
| -------- | ------------------------------------------------- | ----------------------------------------------------- |
| 1. Build | Create the linked list from the input numbers     | `new_node = ListNode(val)` and `tail.next = new_node` |
| 2. Split | Send each node to the less or greater list        | `if current.val < x:` … `else:`                       |
| 3. Seal  | Cut the end of the greater list                   | `greater_tail.next = None`                            |
| 4. Join  | Link the less list to the front of the greater    | `less_tail.next = greater_dummy.next`                 |
| 5. Read  | Walk from `less_dummy.next` and collect the values | `while result_head:` … `output_list.append(...)`      |

---

## How the Code Works

```python
clean_str = head_str.replace("[", "").replace("]", "").strip()
if clean_str:
    nodes = [int(i.strip()) for i in clean_str.split(",")]
else:
    nodes = []
```

- **Clean:** removes the square brackets and surrounding spaces from input such as `[1,4,3,2,5,2]`
- **Split and convert:** `split(",")` cuts the text at every comma, and `int(i.strip())` turns each piece into a number
- **Empty input:** if nothing is left after cleaning, `nodes` becomes an empty list

```python
head = None
tail = None
for val in nodes:
    new_node = ListNode(val)
    if not head:
        head = new_node
        tail = new_node
    else:
        tail.next = new_node
        tail = new_node
```

- **First node:** becomes both `head` and `tail`
- **Every other node:** is linked after `tail`, and `tail` moves forward
- **Result:** `head` points to a real linked list, which is what LeetCode would normally hand to the function

```python
less_dummy = ListNode(0)
greater_dummy = ListNode(0)

less_tail = less_dummy
greater_tail = greater_dummy
```

- **Dummy nodes:** placeholder heads with the throwaway value `0`; they are never part of the answer
- **Tail pointers:** always point to the **last** node of each list, so appending costs O(1)

```python
current = head
while current:
    if current.val < x:
        less_tail.next = current
        less_tail = less_tail.next
    else:
        greater_tail.next = current
        greater_tail = greater_tail.next
    current = current.next
```

- **Less:** the node is attached after `less_tail`, and `less_tail` moves onto it
- **Greater or equal:** the same, but on the greater list
- **Advance:** `current` moves to the next node of the **original** chain
- **Strict comparison:** `<` is used, so a node equal to `x` always goes to the **greater** side, exactly as the problem requires

```python
greater_tail.next = None
less_tail.next = greater_dummy.next
```

- **Seal the end:** the last node of the greater list may still point to some node from the original chain
- **Join:** the less list now continues into the first real node of the greater list
- **Answer:** `less_dummy.next`

> **Why `greater_tail.next = None` is mandatory:** the nodes are **reused**, not copied. Take the example above: the node `5` is the last node of the greater list, but in the original list it was followed by `2`, which now lives in the less list. Without `greater_tail.next = None`, the tail would still point at that `2`, and the result would loop `... → 5 → 2 → 4 → 3 → 5 → 2 → ...` forever.

> **Why the dummy value is `0`:** the dummy values are never read. Only `less_dummy.next` is returned, so any number would work.

---

## Algorithm (Pseudocode)

```
read head list and x
build a linked list from the numbers

less_dummy    = new node
greater_dummy = new node
less_tail     = less_dummy
greater_tail  = greater_dummy

current = head
while current is not null:
    if current.val < x:
        less_tail.next = current
        less_tail = current
    else:
        greater_tail.next = current
        greater_tail = current
    current = current.next

greater_tail.next = null
less_tail.next = greater_dummy.next

print values from less_dummy.next to the end
```

---

## Dry Run

**Input:** `head = [1,4,3,2,5,2]`, `x = 3`

**Stage 1 — build:** `1 → 4 → 3 → 2 → 5 → 2 → None`

**Stage 2 — split:**

| Step | `current.val` | Test `val < 3`   | Goes to     | `less` list | `greater` list  |
| ---- | ------------- | ---------------- | ----------- | ----------- | --------------- |
| 1    | 1             | `1 < 3` ✔        | less        | 1           | (empty)         |
| 2    | 4             | `4 < 3` ✘        | greater     | 1           | 4               |
| 3    | 3             | `3 < 3` ✘        | **greater** | 1           | 4 → 3           |
| 4    | 2             | `2 < 3` ✔        | less        | 1 → 2       | 4 → 3           |
| 5    | 5             | `5 < 3` ✘        | greater     | 1 → 2       | 4 → 3 → 5       |
| 6    | 2             | `2 < 3` ✔        | less        | 1 → 2 → 2   | 4 → 3 → 5       |

**Stage 3 — seal and join:**

```
greater_tail.next = None          # 5 → None   (cuts the old link to the last 2)
less_tail.next = greater head     # 2 → 4

1 → 2 → 2 → 4 → 3 → 5 → None
```

**Output:**

```
[1, 2, 2, 4, 3, 5]
```

The answer is `[1,2,2,4,3,5]` ✅, matching Example 1. Notice that `1, 2, 2` and `4, 3, 5` both keep their original order.

---

## Complexity Analysis

| Metric | Complexity                                                                                              |
| ------ | ------------------------------------------------------------------------------------------------------- |
| Time   | **O(n)** — each node is visited exactly once while partitioning, plus one pass to build and one to print |
| Space  | **O(1)** for the partition itself — only two dummy nodes and a few pointers; the nodes are relinked, not copied |

The script as a whole uses **O(n)** extra space because it stores the input numbers in a Python list and the output in another one, but that is scaffolding for typing input and printing the result. The **partitioning step** itself needs only constant extra space.

---

## Edge Cases

| Scenario                                    | Behavior                                                                          |
| ------------------------------------------- | --------------------------------------------------------------------------------- |
| Official Example 1 `[1,4,3,2,5,2], x = 3`   | Less `1,2,2`, greater `4,3,5` — output `[1,2,2,4,3,5]` ✅                         |
| Official Example 2 `[2,1], x = 2`           | `1` goes less, `2` goes greater — output `[1,2]` ✅                               |
| Empty list `[]`                             | Both lists stay empty, and the script prints `[]` ✅                              |
| Single node `[5], x = 3`                    | Goes to greater — output `[5]` ✅                                                 |
| Every node less than `x` `[1,2,3], x = 10`  | Greater list is empty, so `less_tail.next` becomes `None` — output unchanged ✅   |
| Every node greater or equal `[5,6,7], x = 1`| Less list is empty, so the answer starts at `greater_dummy.next` — unchanged ✅   |
| Nodes equal to `x` `[3,3,1], x = 3`         | Equal nodes go to the greater side in order — output `[1,3,3]` ✅                 |
| Negative values `[-1,-5,2], x = 0`          | Works the same — output `[-1,-5,2]` ✅                                            |
| Already partitioned `[1,2,4,5], x = 3`      | Output is identical to the input ✅                                               |
| Input without brackets `1,4,3`              | The bracket cleanup is harmless, so it still parses ✅                            |
| Non-numeric input such as `[a,b]`           | `int()` raises `ValueError` and the script crashes ⚠️                             |
| Removing `greater_tail.next = None`         | The result contains a cycle, and printing never finishes ⚠️                       |

---

## Code-Quality Notes

**This is a script, not a LeetCode submission.** The code reads the list as text with `input()`, builds the linked list itself, and prints a Python list at the end. LeetCode instead gives you a ready-made `head`, calls a method on a class, and expects the **new head** back, so this code will not run in the LeetCode editor as it is. The submittable version is in the next section.

**The output is a Python list, not a linked list.** The final loop walks the partitioned list and collects the values into `output_list`, which is exactly the format used in the problem's examples. This is a good way to **see** the result when practising locally.

**The first prompt has a stray bracket.** `"Enter head list ): "` contains a `)` with no matching `(`. It does not affect the logic, but `"Enter head list: "` would look cleaner.

**Nodes are reused, not copied.** The loop never calls `ListNode(...)` for the partition; it only changes `next` pointers. That is why the extra space is constant, and also why `greater_tail.next = None` is needed.

**`less_tail = less_tail.next` is the same as `less_tail = current`.** After `less_tail.next = current`, the next node of `less_tail` **is** `current`, so both lines move the tail to the same place.

**The dummy nodes are not part of the answer.** The result starts at `less_dummy.next`, so the two dummy nodes are discarded automatically.

---

## The Natural Extension — Submittable `class Solution`

LeetCode supplies `ListNode` and the input, so the submission only needs the partition logic inside the method:

```python
class Solution:
    def partition(self, head, x):
        less_dummy = ListNode(0)
        greater_dummy = ListNode(0)

        less_tail = less_dummy
        greater_tail = greater_dummy

        current = head
        while current:
            if current.val < x:
                less_tail.next = current
                less_tail = less_tail.next
            else:
                greater_tail.next = current
                greater_tail = greater_tail.next
            current = current.next

        greater_tail.next = None
        less_tail.next = greater_dummy.next

        return less_dummy.next
```

**Trace for several inputs:**

| `head`          | `x` | Less list | Greater list | Joined result       |
| --------------- | --- | --------- | ------------ | ------------------- |
| `[1,4,3,2,5,2]` | 3   | `1,2,2`   | `4,3,5`      | **`[1,2,2,4,3,5]`** ✅ |
| `[2,1]`         | 2   | `1`       | `2`          | **`[1,2]`** ✅      |
| `[]`            | 1   | empty     | empty        | **`[]`** ✅         |
| `[1,2,3]`       | 10  | `1,2,3`   | empty        | **`[1,2,3]`** ✅    |
| `[5,6,7]`       | 1   | empty     | `5,6,7`      | **`[5,6,7]`** ✅    |

The logic is the same as the script, with the input and output scaffolding removed.

**Where the same pattern goes next:**

- **Three-way partition** (less than, equal to, greater than `x`) by adding a third dummy list
- **Odd/even grouping** by sending nodes to two lists based on position instead of value
- **Partition by any rule** by replacing `current.val < x` with any condition
- **Quick sort on a linked list** by using this partition step around a pivot value

| Property                         | This script                              | `class Solution` version        |
| -------------------------------- | ---------------------------------------- | ------------------------------- |
| Time                             | O(n)                                     | **O(n)**                        |
| Extra space for the partition    | O(1)                                     | **O(1)**                        |
| Reads input and builds the list  | ✅ Yes                                   | ❌ No (LeetCode does it)        |
| Prints the result as a list      | ✅ Yes                                   | ❌ No (returns the new head)    |
| Works as a LeetCode submission   | ❌ No (script)                           | ✅ Yes                          |
| When to use                      | Learning and testing on your own machine | Interviews and LeetCode         |

> **A good testing habit:** after changing the code, try the empty list, a list where every node is smaller than `x`, and a list where every node is larger. These three cases are where a missing dummy node or a missing `None` shows up first.

---

## Repository Structure

```
LeetCode-Partition-List/
│
├── partition_list.py    # Main Python implementation
└── README.md            # Project documentation
```

---

## How to Compile and Run

**Prerequisites:** Python 3.8+

```bash
# Clone the repository
git clone https://github.com/rishita-ops/LeetCode-Partition-List.git
cd LeetCode-Partition-List

# Run
python3 partition_list.py
```

**On Windows:**

```bash
python partition_list.py
```

**Sample session:**

```
Enter head list ): [1,4,3,2,5,2]
Enter x: 3
[1, 2, 2, 4, 3, 5]
```

**Empty list:**

```
Enter head list ): []
Enter x: 3
[]
```

> Type the list as comma-separated integers, with or without square brackets.

---

## Key Concepts Covered

- **Singly linked list** — `ListNode` with `val` and `next`
- **Dummy (sentinel) node** — removes the special case for the first node
- **Tail pointer** — appends to the end of a list in O(1)
- **Stable partition** — the relative order inside each side is preserved
- **In-place relinking** — existing nodes are reused, not copied
- **Cycle prevention** — `greater_tail.next = None` cuts the old link
- **Single pass** — one traversal of the original list
- **Strict vs non-strict comparison** — `<` sends nodes equal to `x` to the greater side
- **Parsing text input** — bracket cleanup, `split(",")`, and `int()`

---

## Why This Problem Matters in DSA

The pattern of **splitting nodes into separate lists and stitching them back together** appears across a broad family of linked-list problems:

| Problem / Concept                                            | Connection                                                                       |
| ------------------------------------------------------------ | -------------------------------------------------------------------------------- |
| **Merge Two Sorted Lists** (LeetCode #21)                    | Same dummy-head and tail-pointer technique to build a new list                   |
| **Remove Linked List Elements** (LeetCode #203)              | A dummy head removes the special case for deleting the first node                |
| **Odd Even Linked List** (LeetCode #328)                     | Two interleaved lists built in one pass, then joined at the end                  |
| **Sort List** (LeetCode #148)                                | Merge sort on a linked list relies on splitting and relinking nodes              |
| **Remove Duplicates from Sorted List II** (LeetCode #82)     | Dummy node plus careful `next` pointer rewiring                                  |
| **Sort Colors** (LeetCode #75)                               | The same idea of partitioning by value, applied to an array                      |

Every problem that asks you to rearrange a linked list without creating new nodes starts from the habit introduced here: use a dummy node, keep a tail pointer, and always ask what the last node is still pointing to.

---

## Contributing

Contributions are welcome. Consider adding:

- The **`class Solution`** version as a separate, submittable file
- A **three-way partition** variant (less, equal, greater)
- A **test script** that checks the edge cases above
- A version that prints the result as a linked list (`1 → 2 → 2 → 4 → 3 → 5`)
- Input validation for non-numeric input
- Implementations in C++, Java, or JavaScript

```bash
git checkout -b feature/your-feature
git commit -m "Add: your feature description"
git push origin feature/your-feature
# Then open a Pull Request
```

---

## License

This project is open-source and available under the [MIT License](LICENSE).

---

_Part of a structured LeetCode practice series — fundamentals, done right._