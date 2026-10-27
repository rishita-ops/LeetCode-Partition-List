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
