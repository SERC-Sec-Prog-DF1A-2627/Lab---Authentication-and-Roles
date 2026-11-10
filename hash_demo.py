"""Run: python hash_demo.py. Uses a fictional password only."""
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
ph = PasswordHasher()
password = "Learning-Portal-2026!"
first, second = ph.hash(password), ph.hash(password)
print("First encoded hash:", first)
print("Second encoded hash:", second)
print("Different because salts differ:", first != second)
print("Correct password verifies:", ph.verify(first, password))
try:
    ph.verify(first, "incorrect-password")
except VerifyMismatchError:
    print("Wrong password raises VerifyMismatchError.")
print("Current parameters:", "memory KiB", ph.memory_cost, "passes", ph.time_cost, "parallelism", ph.parallelism)
