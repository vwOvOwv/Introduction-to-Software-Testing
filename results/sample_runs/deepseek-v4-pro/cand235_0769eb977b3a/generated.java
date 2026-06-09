// DELETE_TESTS_START
testExtractCauseUnchecked
testHandleCauseUnchecked
// DELETE_TESTS_END

// IMPORTS_START

import org.apache.commons.lang3.concurrent.ConcurrentRuntimeException;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNull;
import static org.junit.Assert.assertSame;
import static org.junit.Assert.fail;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;
import org.junit.Test;

// IMPORTS_END

public class ConcurrentUtilsTest {

    /**
     * Tests extractCause() if the cause is an unchecked exception.
     */
    @Test
    public void testExtractCauseUncheckedException() {
        RuntimeException rex = new RuntimeException("Test");
        try {
            ConcurrentUtils.extractCause(new ExecutionException(rex));
            fail("Runtime exception not thrown!");
        } catch (RuntimeException r) {
            assertEquals("Wrong exception", rex, r);
        }
    }

    /**
     * Tests handleCause() if the cause is an unchecked exception.
     */
    @Test
    public void testHandleCauseUncheckedException() throws ConcurrentException {
        RuntimeException rex = new RuntimeException("Test");
        try {
            ConcurrentUtils.handleCause(new ExecutionException(rex));
            fail("Runtime exception not thrown!");
        } catch (RuntimeException r) {
            assertEquals("Wrong exception", rex, r);
        }
    }
}
