// IMPORTS_START

import static org.junit.Assert.assertEquals;
import java.util.concurrent.atomic.AtomicInteger;
import org.junit.Before;
import org.junit.Test;

// IMPORTS_END

public class AtomicSafeInitializerTest
        extends AbstractConcurrentInitializerTest {
    /** The instance to be tested. */
    private AtomicSafeInitializerTestImpl initializer;

    @Before
    public void setUp() throws Exception {
        initializer = new AtomicSafeInitializerTestImpl();
    }

    /**
     * Returns the initializer to be tested.
     *
     * @return the {@code AtomicSafeInitializer} under test
     */
    @Override
    protected ConcurrentInitializer<Object> createInitializer() {
        return initializer;
    }

    /**
     * Tests that initialize() is called only once.
     *
     * @throws org.apache.commons.lang3.concurrent.ConcurrentException because {@link #testGetConcurrent()} may throw it
     * @throws java.lang.InterruptedException because {@link #testGetConcurrent()} may throw it
     */
    @Test
    public void testNumberOfInitializeInvocations() throws ConcurrentException,
            InterruptedException {
        testGetConcurrent();
        assertEquals("Wrong number of invocations", 1,
                initializer.initCounter.get());
    }

    /**
     * A concrete test implementation of {@code AtomicSafeInitializer}. This
     * implementation also counts the number of invocations of the initialize()
     * method.
     */
    private static class AtomicSafeInitializerTestImpl extends
            AtomicSafeInitializer<Object> {
        /** A counter for initialize() invocations. */
        final AtomicInteger initCounter = new AtomicInteger();

        @Override
        protected Object initialize() throws ConcurrentException {
            initCounter.incrementAndGet();
            return new Object();
        }
    }
}
