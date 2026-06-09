# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `9625891a7bbc0a8b11f7cf9c2b4650775ec8ac53`
- B: `1a002c67f2d3c198411a62165e53b31d6b414aa3`
- test: `src/test/java/org/apache/commons/lang3/RandomStringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/RandomStringUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `18580`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 5113, 'completion_tokens': 1639, 'total_tokens': 6752}`

---

- 修改 `testRandomStringUtils`：针对新增的 `RandomStringUtils.randomGraph(int)` 和 `randomPrint(int)` 增加长度、字符范围与随机性断言。
- 不需要调整 import：新增断言继续使用已有的 `assertEquals` 与 `assertTrue`。

```java
@Test
public void testRandomStringUtils() {
    String r1 = RandomStringUtils.random(50);
    assertEquals("random(50) length", 50, r1.length());
    String r2 = RandomStringUtils.random(50);
    assertEquals("random(50) length", 50, r2.length());
    assertTrue("!r1.equals(r2)", !r1.equals(r2));
    
    r1 = RandomStringUtils.randomAscii(50);
    assertEquals("randomAscii(50) length", 50, r1.length());
    for(int i = 0; i < r1.length(); i++) {
        assertTrue("char between 32 and 127", r1.charAt(i) >= 32 && r1.charAt(i) <= 127);
    }        
    r2 = RandomStringUtils.randomAscii(50);
    assertTrue("!r1.equals(r2)", !r1.equals(r2));

    r1 = RandomStringUtils.randomAlphabetic(50);
    assertEquals("randomAlphabetic(50)", 50, r1.length());
    for(int i = 0; i < r1.length(); i++) {
        assertTrue("r1 contains alphabetic", Character.isLetter(r1.charAt(i)) && !Character.isDigit(r1.charAt(i)));
    }
    r2 = RandomStringUtils.randomAlphabetic(50);
    assertTrue("!r1.equals(r2)", !r1.equals(r2));
    
    r1 = RandomStringUtils.randomAlphanumeric(50);
    assertEquals("randomAlphanumeric(50)", 50, r1.length());
    for(int i = 0; i < r1.length(); i++) {
        assertTrue("r1 contains alphanumeric", Character.isLetterOrDigit(r1.charAt(i)));
    }
    r2 = RandomStringUtils.randomAlphabetic(50);
    assertTrue("!r1.equals(r2)", !r1.equals(r2));
    
    r1 = RandomStringUtils.randomGraph(50);
    assertEquals("randomGraph(50) length", 50, r1.length());
    for(int i = 0; i < r1.length(); i++) {
        assertTrue("char between 33 and 126", r1.charAt(i) >= 33 && r1.charAt(i) <= 126);
    }
    r2 = RandomStringUtils.randomGraph(50);
    assertTrue("!r1.equals(r2)", !r1.equals(r2));
    
    r1 = RandomStringUtils.randomNumeric(50);
    assertEquals("randomNumeric(50)", 50, r1.length());
    for(int i = 0; i < r1.length(); i++) {
        assertTrue("r1 contains numeric", Character.isDigit(r1.charAt(i)) && !Character.isLetter(r1.charAt(i)));
    }
    r2 = RandomStringUtils.randomNumeric(50);
    assertTrue("!r1.equals(r2)", !r1.equals(r2));
    
    r1 = RandomStringUtils.randomPrint(50);
    assertEquals("randomPrint(50) length", 50, r1.length());
    for(int i = 0; i < r1.length(); i++) {
        assertTrue("char between 32 and 126", r1.charAt(i) >= 32 && r1.charAt(i) <= 126);
    }
    r2 = RandomStringUtils.randomPrint(50);
    assertTrue("!r1.equals(r2)", !r1.equals(r2));
    
    String set = "abcdefg";
    r1 = RandomStringUtils.random(50, set);
    assertEquals("random(50, \"abcdefg\")", 50, r1.length());
    for(int i = 0; i < r1.length(); i++) {
        assertTrue("random char in set", set.indexOf(r1.charAt(i)) > -1);
    }
    r2 = RandomStringUtils.random(50, set);
    assertTrue("!r1.equals(r2)", !r1.equals(r2));
    
    r1 = RandomStringUtils.random(50, (String) null);
    assertEquals("random(50) length", 50, r1.length());
    r2 = RandomStringUtils.random(50, (String) null);
    assertEquals("random(50) length", 50, r2.length());
    assertTrue("!r1.equals(r2)", !r1.equals(r2));
    
    set = "stuvwxyz";
    r1 = RandomStringUtils.random(50, set.toCharArray());
    assertEquals("random(50, \"stuvwxyz\")", 50, r1.length());
    for(int i = 0; i < r1.length(); i++) {
        assertTrue("random char in set", set.indexOf(r1.charAt(i)) > -1);
    }
    r2 = RandomStringUtils.random(50, set);
    assertTrue("!r1.equals(r2)", !r1.equals(r2));
    
    r1 = RandomStringUtils.random(50, (char[]) null);
    assertEquals("random(50) length", 50, r1.length());
    r2 = RandomStringUtils.random(50, (char[]) null);
    assertEquals("random(50) length", 50, r2.length());
    assertTrue("!r1.equals(r2)", !r1.equals(r2));

    final long seed = System.currentTimeMillis();
    r1 = RandomStringUtils.random(50,0,0,true,true,null,new Random(seed));
    r2 = RandomStringUtils.random(50,0,0,true,true,null,new Random(seed));
    assertEquals("r1.equals(r2)", r1, r2);

    r1 = RandomStringUtils.random(0);
    assertEquals("random(0).equals(\"\")", "", r1);
}
```