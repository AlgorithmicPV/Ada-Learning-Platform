import uuid
import sqlite3

challenge_id = '17b09d10-9c7b-466c-be77-9903aff91464'

count_occurrences_solutions = [
    {
        "language": "python",
        "code": """```python
# Counts how many times a specific character appears in a string
def count_occurrences(s, ch):
    # Use the count() method which returns the number of occurrences
    return s.count(ch)

print(count_occurrences("hello world", "l"))  # Output: 3
```"""
    },
    {
        "language": "javascript",
        "code": """```javascript
// Counts how many times a specific character appears in a string
function countOccurrences(s, ch) {
  // Split the string into characters and filter by the target character
  return [...s].filter(c => c === ch).length;
}

console.log(countOccurrences("hello world", "l"));  // Output: 3
```"""
    },
    {
        "language": "typescript",
        "code": """```typescript
// Type-safe way to count character occurrences in a string
function countOccurrences(s: string, ch: string): number {
  // Loop through the string and count matching characters
  let count = 0;
  for (let c of s) {
    if (c === ch) count++;
  }
  return count;
}

console.log(countOccurrences("hello world", "l"));  // Output: 3
```"""
    },
    {
        "language": "java",
        "code": """```java
// Counts how many times a specific character appears in a string
public class Main {
    public static int countOccurrences(String s, char ch) {
        int count = 0;
        for (char c : s.toCharArray()) {
            if (c == ch) count++;
        }
        return count;
    }

    public static void main(String[] args) {
        System.out.println(countOccurrences("hello world", 'l'));  // Output: 3
    }
}
```"""
    },
    {
        "language": "c++",
        "code": """```cpp
// Counts how many times a specific character appears in a string
#include <iostream>
#include <string>
using namespace std;

int countOccurrences(string s, char ch) {
    int count = 0;
    for (char c : s) {
        if (c == ch) count++;
    }
    return count;
}

int main() {
    cout << countOccurrences("hello world", 'l') << endl;  // Output: 3
}
```"""
    }
]


conn = sqlite3.connect("app.db")
cursor = conn.cursor()

for sol in count_occurrences_solutions:
    id = str(uuid.uuid4())
    cursor.execute(
        """
            INSERT INTO Solution (solution_id, challenge_id, answer, language)
            VALUES (? , ?, ?, ?)
        """, (id, challenge_id, sol['code'], sol['language']))
    conn.commit()
print("done")
