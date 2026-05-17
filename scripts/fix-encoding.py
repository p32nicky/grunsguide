import os

folder = r"C:\grunssite\content\articles"

replacements = [
    (b"\xc3\xa2\xe2\x80\xa0\xe2\x80\x99", b"\xe2\x86\x92"),  # â†' -> →
    (b"\xc3\xa2\xe2\x82\xac\xe2\x80\x9d", b"\xe2\x80\x94"),  # â€" -> —
    (b"\xc3\xa2\xe2\x82\xac\xe2\x80\x9c", b"\xe2\x80\x93"),  # â€" -> –
    (b"\xc3\x83\xc2\xbc", b"\xc3\xbc"),  # Ã¼ -> ü
    (b"\xc3\x83\xc2\xbc", b"\xc3\xbc"),
]

fixed = 0
for fname in os.listdir(folder):
    if not fname.endswith(".json"):
        continue
    path = os.path.join(folder, fname)
    with open(path, "rb") as f:
        data = f.read()
    new_data = data
    for bad, good in replacements:
        new_data = new_data.replace(bad, good)
    if new_data != data:
        with open(path, "wb") as f:
            f.write(new_data)
        fixed += 1

print(f"Fixed {fixed} files")
