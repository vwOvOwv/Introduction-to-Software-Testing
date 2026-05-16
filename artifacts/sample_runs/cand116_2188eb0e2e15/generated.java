import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertSame;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import java.lang.reflect.Constructor;
import java.lang.reflect.Modifier;
import java.util.Collection;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.Set;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
@Nested
        final class WithMessageSupplier {

            @Test
            void shouldNotThrowForTrueExpression() {
                Validate.isTrue(true, () -> "MSG");
            }

            @Test
            void shouldThrowExceptionWithDoubleInsertedIntoTemplateMessageForFalseExpression() {
                final IllegalArgumentException ex = assertThrows(IllegalArgumentException.class,
                    () -> Validate.isTrue(false, () -> String.format("MSG %s %s", "Object 1", "Object 2")));
                assertEquals("MSG Object 1 Object 2", ex.getMessage());
            }
        }
