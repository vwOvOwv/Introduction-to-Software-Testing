package org.apache.commons.lang3;


import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;
import org.junit.Test;

/**
 * Tests CharEncoding.
 * 
 * @see CharEncoding
 */
@SuppressWarnings("deprecation")
public class CharEncodingTest  {

    private void assertSupportedEncoding(final String name) {
        assertTrue("Encoding should be supported: " + name, CharEncoding.isSupported(name));
    }

    /**
     * The class can be instantiated.
     */
    @Test
    public void testConstructor() {
        new CharEncoding();
    }

    @Test
    public void testMustBeSupportedJava1_3_1_and_above() {
        this.assertSupportedEncoding(CharEncoding.ISO_8859_1);
        this.assertSupportedEncoding(CharEncoding.US_ASCII);
        this.assertSupportedEncoding(CharEncoding.UTF_16);
        this.assertSupportedEncoding(CharEncoding.UTF_16BE);
        this.assertSupportedEncoding(CharEncoding.UTF_16LE);
        this.assertSupportedEncoding(CharEncoding.UTF_8);
    }

    @Test
    public void testSupported() {
        assertTrue(CharEncoding.isSupported("UTF8"));
        assertTrue(CharEncoding.isSupported("UTF-8"));
        assertTrue(CharEncoding.isSupported("ASCII"));
    }

    @Test
    public void testNotSupported() {
        assertFalse(CharEncoding.isSupported(null));
        assertFalse(CharEncoding.isSupported(""));
        assertFalse(CharEncoding.isSupported(" "));
        assertFalse(CharEncoding.isSupported("\t\r\n"));
        assertFalse(CharEncoding.isSupported("DOESNOTEXIST"));
        assertFalse(CharEncoding.isSupported("this is not a valid encoding name"));
    }
}
