import uuid
import sqlite3
from datetime import datetime

# connect the database
conn = sqlite3.connect("database/app.db")
cursor = conn.cursor()





Word_Ladder_Path_Finder = "48461c57-b266-468c-b1be-bc83f86024d3"

word_ladder_solutions = [
    {
        "language": "Python",
        "code": """```python
# Word Ladder using BFS
from collections import deque

def word_ladder(beginWord, endWord, wordList):
    wordSet = set(wordList)
    queue = deque([(beginWord, 1)])
    while queue:
        word, steps = queue.popleft()
        if word == endWord:
            return steps
        for i in range(len(word)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                next_word = word[:i] + c + word[i+1:]
                if next_word in wordSet:
                    wordSet.remove(next_word)
                    queue.append((next_word, steps + 1))
    return 0
```"""
    },
    {
        "language": "JavaScript",
        "code": """```javascript
// Word Ladder using BFS
function wordLadder(beginWord, endWord, wordList) {
    const wordSet = new Set(wordList);
    const queue = [[beginWord, 1]];
    while (queue.length > 0) {
        const [word, steps] = queue.shift();
        if (word === endWord) return steps;
        for (let i = 0; i < word.length; i++) {
            for (let c of 'abcdefghijklmnopqrstuvwxyz') {
                const nextWord = word.slice(0, i) + c + word.slice(i + 1);
                if (wordSet.has(nextWord)) {
                    wordSet.delete(nextWord);
                    queue.push([nextWord, steps + 1]);
                }
            }
        }
    }
    return 0;
}
```"""
    },
    {
        "language": "TypeScript",
        "code": """```typescript
// Word Ladder using BFS
function wordLadder(beginWord: string, endWord: string, wordList: string[]): number {
    const wordSet = new Set(wordList);
    const queue: [string, number][] = [[beginWord, 1]];
    while (queue.length > 0) {
        const [word, steps] = queue.shift()!;
        if (word === endWord) return steps;
        for (let i = 0; i < word.length; i++) {
            for (let c of 'abcdefghijklmnopqrstuvwxyz') {
                const nextWord = word.slice(0, i) + c + word.slice(i + 1);
                if (wordSet.has(nextWord)) {
                    wordSet.delete(nextWord);
                    queue.push([nextWord, steps + 1]);
                }
            }
        }
    }
    return 0;
}
```"""
    },
    {
        "language": "Java",
        "code": """```java
// Word Ladder using BFS
import java.util.*;

public class Main {
    public static int wordLadder(String beginWord, String endWord, List<String> wordList) {
        Set<String> wordSet = new HashSet<>(wordList);
        Queue<String> queue = new LinkedList<>();
        queue.offer(beginWord);
        int steps = 1;

        while (!queue.isEmpty()) {
            int size = queue.size();
            for (int s = 0; s < size; s++) {
                String word = queue.poll();
                if (word.equals(endWord)) return steps;
                char[] chars = word.toCharArray();
                for (int i = 0; i < chars.length; i++) {
                    char old = chars[i];
                    for (char c = 'a'; c <= 'z'; c++) {
                        chars[i] = c;
                        String nextWord = new String(chars);
                        if (wordSet.contains(nextWord)) {
                            wordSet.remove(nextWord);
                            queue.offer(nextWord);
                        }
                    }
                    chars[i] = old;
                }
            }
            steps++;
        }
        return 0;
    }
}
```"""
    },
    {
        "language": "C++",
        "code": """```cpp
// Word Ladder using BFS
#include <iostream>
#include <unordered_set>
#include <queue>
using namespace std;

int wordLadder(string beginWord, string endWord, vector<string>& wordList) {
    unordered_set<string> wordSet(wordList.begin(), wordList.end());
    queue<pair<string, int>> q;
    q.push({beginWord, 1});

    while (!q.empty()) {
        auto [word, steps] = q.front();
        q.pop();
        if (word == endWord) return steps;

        for (size_t i = 0; i < word.size(); ++i) {
            string temp = word;
            for (char c = 'a'; c <= 'z'; ++c) {
                temp[i] = c;
                if (wordSet.count(temp)) {
                    wordSet.erase(temp);
                    q.push({temp, steps + 1});
                }
            }
        }
    }
    return 0;
}
```"""
    }
]


for solution in word_ladder_solutions:
    solution_id = str(uuid.uuid4())
    cursor.execute(
        """
INSERT INTO Solution (solution_id, challenge_id, answer, language) VALUES (?, ?, ?, ?)
""",
        (
            solution_id,
            Word_Ladder_Path_Finder,
            solution["code"],
            solution["language"],
        ),
    )
    conn.commit()

print("done")
