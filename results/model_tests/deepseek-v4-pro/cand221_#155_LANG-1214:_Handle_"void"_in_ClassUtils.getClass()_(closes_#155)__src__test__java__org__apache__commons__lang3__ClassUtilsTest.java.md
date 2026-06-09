# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `e05b50e1daa8200ad488a332375200bab132f2ad`
- B: `fbb5d31a581c24e925c442a7754358d2b62a669d`
- test: `src/test/java/org/apache/commons/lang3/ClassUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/ClassUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `75387`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 17311, 'completion_tokens': 1887, 'total_tokens': 19198, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 1627}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 16927}`

---

* 修改 `@Test` 方法 `testGetClassRawPrimitives`：在方法末尾增加 `assertEquals( void.class, ClassUtils.getClass( "void" ) );`，以适应生产代码中通过新 `namePrimitiveMap` 直接支持原始类型名称 `void` 的查找。
* 无需调整 import：`void.class` 对应的 `java.lang.Void` 在隐式导入范围内，现有测试类已可直接使用。
* 无需删除任何测试方法。

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