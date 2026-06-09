// IMPORTS_START

import junit.framework.TestCase;
import org.apache.commons.lang3.text.translate.NumericEntityEscaper;

// IMPORTS_END

/**
 * Unit tests for {@link org.apache.commons.lang3.text.translate.NumericEntityEscaper}.
 */
public class NumericEntityEscaperTest extends TestCase {

    public void testBelow() {
        NumericEntityEscaper nee = NumericEntityEscaper.below('F');

        String input = "ADFGZ";
        String result = nee.translate(input);
        assertEquals("Failed to escape numeric entities via the below method", "&#65;&#68;FGZ", result);
    }

    public void testBetween() {
        NumericEntityEscaper nee = NumericEntityEscaper.between('F', 'L');

        String input = "ADFGZ";
        String result = nee.translate(input);
        assertEquals("Failed to escape numeric entities via the between method", "AD&#70;&#71;Z", result);
    }

    public void testAbove() {
        NumericEntityEscaper nee = NumericEntityEscaper.above('F');

        String input = "ADFGZ";
        String result = nee.translate(input);
        assertEquals("Failed to escape numeric entities via the above method", "ADF&#71;&#90;", result);
    }

    // See LANG-617
    public void testSupplementary() {
        NumericEntityEscaper nee = new NumericEntityEscaper();
        String input = "\uD803\uDC22";
        String expected = "&#68642;";

        String result = nee.translate(input);
        assertEquals("Failed to escape numeric entities supplementary characters", expected, result);

    }
}
