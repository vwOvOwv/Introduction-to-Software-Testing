# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `e05b50e1daa8200ad488a332375200bab132f2ad`
- B: `fbb5d31a581c24e925c442a7754358d2b62a669d`
- test: `src/test/java/org/apache/commons/lang3/ClassUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/ClassUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `75387`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 16348, 'completion_tokens': 276, 'total_tokens': 16624}`

---

- 修改 `testGetClassRawPrimitives`：生产代码现在通过 `namePrimitiveMap` 直接支持 `"void"` 解析为 `void.class`，因此在该测试中新增对应断言；import 无需调整。

```java
    @Test
    public void testGetClassRawPrimitives() throws ClassNotFoundException {
        assertEquals( int.class, ClassUtils.getClass( "int" ) );
        assertEquals( long.class, ClassUtils.getClass( "long" ) );
        assertEquals( short.class, ClassUtils.getClass( "short" ) );
        assertEquals( byte.class, ClassUtils.getClass( "byte" ) );
        assertEquals( char.class, ClassUtils.getClass( "char" ) );
        assertEquals( float.class, ClassUtils.getClass( "float" ) );
        assertEquals( double.class, ClassUtils.getClass( "double" ) );
        assertEquals( boolean.class, ClassUtils.getClass( "boolean" ) );
        assertEquals( void.class, ClassUtils.getClass( "void" ) );
    }
```