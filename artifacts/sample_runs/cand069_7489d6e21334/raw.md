# DeepSeek 输出

- repo: `/home/netro/Introduction-to-Software-Testing/commons-lang`
- A: `b3cd50b19e89792fa587bea3fa7d79709ab46c48`
- B: `7489d6e21334673dc56399de7decaaa00f11ebcf`
- test: `src/test/java/org/apache/commons/lang3/CharSetTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/CharSet.java']`
- old_test_mode: `methods`
- user_chars: `38317`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 10132, 'completion_tokens': 3417, 'total_tokens': 13549, 'prompt_tokens_details': {'cached_tokens': 256}, 'prompt_cache_hit_tokens': 256, 'prompt_cache_miss_tokens': 9876}`

---

- 新增 `import java.util.Set;` 到文件头。
- 修改 `testConstructor_String_combo`：将 `CharRange[]` 改为 `Set<CharRange>`，`array.length` 改为 `array.size()`，`ArrayUtils.contains` 改为 `array.contains`。
- 修改 `testConstructor_String_comboNegated`：同上。
- 修改 `testConstructor_String_oddCombinations`：同上。
- 修改 `testConstructor_String_oddDash`：同上。
- 修改 `testConstructor_String_oddNegate`：同上。
- 修改 `testConstructor_String_simple`：将 `CharRange[]` 改为 `Set<CharRange>`，`array.length` 改为 `array.size()`，`array[0].toString()` 改为 `array.iterator().next().toString()`。
- 修改 `testContains_Char`：将 `CharRange[]` 改为 `Set<CharRange>`，`array.length` 改为 `array.size()`。
- 修改 `testStatics`：将 `CharRange[]` 改为 `Set<CharRange>`，`array.length` 改为 `array.size()`，`ArrayUtils.contains` 改为 `array.contains`。

```java
// IMPORTS_START
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.lang.reflect.Modifier;
import java.util.Set;

import org.junit.jupiter.api.Test;
// IMPORTS_END

    @Test
    void testConstructor_String_combo() {
        CharSet set;
        Set<CharRange> array;

        set = CharSet.getInstance("abc");
        array = set.getCharRanges();
        assertEquals(3, array.size());
        assertTrue(array.contains(CharRange.is('a')));
        assertTrue(array.contains(CharRange.is('b')));
        assertTrue(array.contains(CharRange.is('c')));

        set = CharSet.getInstance("a-ce-f");
        array = set.getCharRanges();
        assertEquals(2, array.size());
        assertTrue(array.contains(CharRange.isIn('a', 'c')));
        assertTrue(array.contains(CharRange.isIn('e', 'f')));

        set = CharSet.getInstance("ae-f");
        array = set.getCharRanges();
        assertEquals(2, array.size());
        assertTrue(array.contains(CharRange.is('a')));
        assertTrue(array.contains(CharRange.isIn('e', 'f')));

        set = CharSet.getInstance("e-fa");
        array = set.getCharRanges();
        assertEquals(2, array.size());
        assertTrue(array.contains(CharRange.is('a')));
        assertTrue(array.contains(CharRange.isIn('e', 'f')));

        set = CharSet.getInstance("ae-fm-pz");
        array = set.getCharRanges();
        assertEquals(4, array.size());
        assertTrue(array.contains(CharRange.is('a')));
        assertTrue(array.contains(CharRange.isIn('e', 'f')));
        assertTrue(array.contains(CharRange.isIn('m', 'p')));
        assertTrue(array.contains(CharRange.is('z')));
    }

    @Test
    void testConstructor_String_comboNegated() {
        CharSet set;
        Set<CharRange> array;

        set = CharSet.getInstance("^abc");
        array = set.getCharRanges();
        assertEquals(3, array.size());
        assertTrue(array.contains(CharRange.isNot('a')));
        assertTrue(array.contains(CharRange.is('b')));
        assertTrue(array.contains(CharRange.is('c')));

        set = CharSet.getInstance("b^ac");
        array = set.getCharRanges();
        assertEquals(3, array.size());
        assertTrue(array.contains(CharRange.is('b')));
        assertTrue(array.contains(CharRange.isNot('a')));
        assertTrue(array.contains(CharRange.is('c')));

        set = CharSet.getInstance("db^ac");
        array = set.getCharRanges();
        assertEquals(4, array.size());
        assertTrue(array.contains(CharRange.is('d')));
        assertTrue(array.contains(CharRange.is('b')));
        assertTrue(array.contains(CharRange.isNot('a')));
        assertTrue(array.contains(CharRange.is('c')));

        set = CharSet.getInstance("^b^a");
        array = set.getCharRanges();
        assertEquals(2, array.size());
        assertTrue(array.contains(CharRange.isNot('b')));
        assertTrue(array.contains(CharRange.isNot('a')));

        set = CharSet.getInstance("b^a-c^z");
        array = set.getCharRanges();
        assertEquals(3, array.size());
        assertTrue(array.contains(CharRange.isNotIn('a', 'c')));
        assertTrue(array.contains(CharRange.isNot('z')));
        assertTrue(array.contains(CharRange.is('b')));
    }

    @Test
    void testConstructor_String_oddCombinations() {
        CharSet set;
        Set<CharRange> array;

        set = CharSet.getInstance("a-^c");
        array = set.getCharRanges();
        assertTrue(array.contains(CharRange.isIn('a', '^'))); // "a-^"
        assertTrue(array.contains(CharRange.is('c'))); // "c"
        assertFalse(set.contains('b'));
        assertTrue(set.contains('^'));
        assertTrue(set.contains('_')); // between ^ and a
        assertTrue(set.contains('c'));

        set = CharSet.getInstance("^a-^c");
        array = set.getCharRanges();
        assertTrue(array.contains(CharRange.isNotIn('a', '^'))); // "^a-^"
        assertTrue(array.contains(CharRange.is('c'))); // "c"
        assertTrue(set.contains('b'));
        assertFalse(set.contains('^'));
        assertFalse(set.contains('_')); // between ^ and a

        set = CharSet.getInstance("a- ^-- "); //contains everything
        array = set.getCharRanges();
        assertTrue(array.contains(CharRange.isIn('a', ' '))); // "a- "
        assertTrue(array.contains(CharRange.isNotIn('-', ' '))); // "^-- "
        assertTrue(set.contains('#'));
        assertTrue(set.contains('^'));
        assertTrue(set.contains('a'));
        assertTrue(set.contains('*'));
        assertTrue(set.contains('A'));

        set = CharSet.getInstance("^-b");
        array = set.getCharRanges();
        assertTrue(array.contains(CharRange.isIn('^', 'b'))); // "^-b"
        assertTrue(set.contains('b'));
        assertTrue(set.contains('_')); // between ^ and a
        assertFalse(set.contains('A'));
        assertTrue(set.contains('^'));

        set = CharSet.getInstance("b-^");
        array = set.getCharRanges();
        assertTrue(array.contains(CharRange.isIn('^', 'b'))); // "b-^"
        assertTrue(set.contains('b'));
        assertTrue(set.contains('^'));
        assertTrue(set.contains('a')); // between ^ and b
        assertFalse(set.contains('c'));
    }

    @Test
    void testConstructor_String_oddDash() {
        CharSet set;
        Set<CharRange> array;

        set = CharSet.getInstance("-");
        array = set.getCharRanges();
        assertEquals(1, array.size());
        assertTrue(array.contains(CharRange.is('-')));

        set = CharSet.getInstance("--");
        array = set.getCharRanges();
        assertEquals(1, array.size());
        assertTrue(array.contains(CharRange.is('-')));

        set = CharSet.getInstance("---");
        array = set.getCharRanges();
        assertEquals(1, array.size());
        assertTrue(array.contains(CharRange.is('-')));

        set = CharSet.getInstance("----");
        array = set.getCharRanges();
        assertEquals(1, array.size());
        assertTrue(array.contains(CharRange.is('-')));

        set = CharSet.getInstance("-a");
        array = set.getCharRanges();
        assertEquals(2, array.size());
        assertTrue(array.contains(CharRange.is('-')));
        assertTrue(array.contains(CharRange.is('a')));

        set = CharSet.getInstance("a-");
        array = set.getCharRanges();
        assertEquals(2, array.size());
        assertTrue(array.contains(CharRange.is('a')));
        assertTrue(array.contains(CharRange.is('-')));

        set = CharSet.getInstance("a--");
        array = set.getCharRanges();
        assertEquals(1, array.size());
        assertTrue(array.contains(CharRange.isIn('a', '-')));

        set = CharSet.getInstance("--a");
        array = set.getCharRanges();
        assertEquals(1, array.size());
        assertTrue(array.contains(CharRange.isIn('-', 'a')));
    }

    @Test
    void testConstructor_String_oddNegate() {
        CharSet set;
        Set<CharRange> array;
        set = CharSet.getInstance("^");
        array = set.getCharRanges();
        assertEquals(1, array.size());
        assertTrue(array.contains(CharRange.is('^'))); // "^"

        set = CharSet.getInstance("^^");
        array = set.getCharRanges();
        assertEquals(1, array.size());
        assertTrue(array.contains(CharRange.isNot('^'))); // "^^"

        set = CharSet.getInstance("^^^");
        array = set.getCharRanges();
        assertEquals(2, array.size());
        assertTrue(array.contains(CharRange.isNot('^'))); // "^^"
        assertTrue(array.contains(CharRange.is('^'))); // "^"

        set = CharSet.getInstance("^^^^");
        array = set.getCharRanges();
        assertEquals(1, array.size());
        assertTrue(array.contains(CharRange.isNot('^'))); // "^^" x2

        set = CharSet.getInstance("a^");
        array = set.getCharRanges();
        assertEquals(2, array.size());
        assertTrue(array.contains(CharRange.is('a'))); // "a"
        assertTrue(array.contains(CharRange.is('^'))); // "^"

        set = CharSet.getInstance("^a-");
        array = set.getCharRanges();
        assertEquals(2, array.size());
        assertTrue(array.contains(CharRange.isNot('a'))); // "^a"
        assertTrue(array.contains(CharRange.is('-'))); // "-"

        set = CharSet.getInstance("^^-c");
        array = set.getCharRanges();
        assertEquals(1, array.size());
        assertTrue(array.contains(CharRange.isNotIn('^', 'c'))); // "^^-c"

        set = CharSet.getInstance("^c-^");
        array = set.getCharRanges();
        assertEquals(1, array.size());
        assertTrue(array.contains(CharRange.isNotIn('c', '^'))); // "^c-^"

        set = CharSet.getInstance("^c-^d");
        array = set.getCharRanges();
        assertEquals(2, array.size());
        assertTrue(array.contains(CharRange.isNotIn('c', '^'))); // "^c-^"
        assertTrue(array.contains(CharRange.is('d'))); // "d"

        set = CharSet.getInstance("^^-");
        array = set.getCharRanges();
        assertEquals(2, array.size());
        assertTrue(array.contains(CharRange.isNot('^'))); // "^^"
        assertTrue(array.contains(CharRange.is('-'))); // "-"
    }

    @Test
    void testConstructor_String_simple() {
        CharSet set;
        Set<CharRange> array;

        set = CharSet.getInstance((String) null);
        array = set.getCharRanges();
        assertEquals("[]", set.toString());
        assertEquals(0, array.size());

        set = CharSet.getInstance("");
        array = set.getCharRanges();
        assertEquals("[]", set.toString());
        assertEquals(0, array.size());

        set = CharSet.getInstance("a");
        array = set.getCharRanges();
        assertEquals("[a]", set.toString());
        assertEquals(1, array.size());
        assertEquals("a", array.iterator().next().toString());

        set = CharSet.getInstance("^a");
        array = set.getCharRanges();
        assertEquals("[^a]", set.toString());
        assertEquals(1, array.size());
        assertEquals("^a", array.iterator().next().toString());

        set = CharSet.getInstance("a-e");
        array = set.getCharRanges();
        assertEquals("[a-e]", set.toString());
        assertEquals(1, array.size());
        assertEquals("a-e", array.iterator().next().toString());

        set = CharSet.getInstance("^a-e");
        array = set.getCharRanges();
        assertEquals("[^a-e]", set.toString());
        assertEquals(1, array.size());
        assertEquals("^a-e", array.iterator().next().toString());
    }

    @Test
    void testContains_Char() {
        final CharSet btod = CharSet.getInstance("b-d");
        final CharSet dtob = CharSet.getInstance("d-b");
        final CharSet bcd = CharSet.getInstance("bcd");
        final CharSet bd = CharSet.getInstance("bd");
        final CharSet notbtod = CharSet.getInstance("^b-d");

        assertFalse(btod.contains('a'));
        assertTrue(btod.contains('b'));
        assertTrue(btod.contains('c'));
        assertTrue(btod.contains('d'));
        assertFalse(btod.contains('e'));

        assertFalse(bcd.contains('a'));
        assertTrue(bcd.contains('b'));
        assertTrue(bcd.contains('c'));
        assertTrue(bcd.contains('d'));
        assertFalse(bcd.contains('e'));

        assertFalse(bd.contains('a'));
        assertTrue(bd.contains('b'));
        assertFalse(bd.contains('c'));
        assertTrue(bd.contains('d'));
        assertFalse(bd.contains('e'));

        assertTrue(notbtod.contains('a'));
        assertFalse(notbtod.contains('b'));
        assertFalse(notbtod.contains('c'));
        assertFalse(notbtod.contains('d'));
        assertTrue(notbtod.contains('e'));

        assertFalse(dtob.contains('a'));
        assertTrue(dtob.contains('b'));
        assertTrue(dtob.contains('c'));
        assertTrue(dtob.contains('d'));
        assertFalse(dtob.contains('e'));

        final Set<CharRange> array = dtob.getCharRanges();
        assertEquals("[b-d]", dtob.toString());
        assertEquals(1, array.size());
    }

    @Test
    void testStatics() {
        Set<CharRange> array;

        array = CharSet.EMPTY.getCharRanges();
        assertEquals(0, array.size());

        array = CharSet.ASCII_ALPHA.getCharRanges();
        assertEquals(2, array.size());
        assertTrue(array.contains(CharRange.isIn('a', 'z')));
        assertTrue(array.contains(CharRange.isIn('A', 'Z')));

        array = CharSet.ASCII_ALPHA_LOWER.getCharRanges();
        assertEquals(1, array.size());
        assertTrue(array.contains(CharRange.isIn('a', 'z')));

        array = CharSet.ASCII_ALPHA_UPPER.getCharRanges();
        assertEquals(1, array.size());
        assertTrue(array.contains(CharRange.isIn('A', 'Z')));

        array = CharSet.ASCII_NUMERIC.getCharRanges();
        assertEquals(1, array.size());
        assertTrue(array.contains(CharRange.isIn('0', '9')));
    }
```