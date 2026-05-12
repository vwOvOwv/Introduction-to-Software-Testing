/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 * https://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */
package org.apache.commons.lang3;

import static org.apache.commons.lang3.LangAssertions.assertIllegalArgumentException;
import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;

/**
 * Tests for primitive double range validators with NaN behavior.
 */
class ValidateDoublesTest extends AbstractLangTest {

    @Nested
    final class ExclusiveBetweenDouble {

        @Nested
        final class WithMessage {

            @Test
            void shouldNotThrowExceptionWhenValueIsBetweenBounds() {
                Validate.exclusiveBetween(0.1, 3.1, 2.1, "MSG");
            }

            @Test
            void shouldThrowIllegalArgumentExceptionWithGivenMessageWhenValueIsNaN() {
                final IllegalArgumentException ex = assertIllegalArgumentException(
                    () -> Validate.exclusiveBetween(0.1, 3.1, Double.NaN, "MSG"));
                assertEquals("MSG", ex.getMessage());
            }

            @Test
            void shouldThrowIllegalArgumentExceptionWithGivenMessageWhenValueIsLowerBound() {
                final IllegalArgumentException ex = assertIllegalArgumentException(
                    () -> Validate.exclusiveBetween(0.1, 3.1, 0.1, "MSG"));
                assertEquals("MSG", ex.getMessage());
            }

            @Test
            void shouldThrowIllegalArgumentExceptionWithGivenMessageWhenValueIsUpperBound() {
                final IllegalArgumentException ex = assertIllegalArgumentException(
                    () -> Validate.exclusiveBetween(0.1, 3.1, 3.1, "MSG"));
                assertEquals("MSG", ex.getMessage());
            }

            @Test
            void shouldThrowIllegalArgumentExceptionWithGivenMessageWhenValueIsAboveUpperBound() {
                final IllegalArgumentException ex = assertIllegalArgumentException(
                    () -> Validate.exclusiveBetween(0.1, 3.1, 4.1, "MSG"));
                assertEquals("MSG", ex.getMessage());
            }

            @Test
            void shouldThrowIllegalArgumentExceptionWithGivenMessageWhenValueIsBelowLowerBound() {
                final IllegalArgumentException ex = assertIllegalArgumentException(
                    () -> Validate.exclusiveBetween(0.1, 3.1, 0.01, "MSG"));
                assertEquals("MSG", ex.getMessage());
            }
        }

        @Nested
        final class WithoutMessage {

            @Test
            void shouldNotThrowExceptionWhenValueIsBetweenBounds() {
                Validate.exclusiveBetween(0.1, 3.1, 2.1);
            }

            @Test
            void shouldThrowIllegalArgumentExceptionWithDefaultMessageWhenValueIsNaN() {
                final IllegalArgumentException ex = assertIllegalArgumentException(
                    () -> Validate.exclusiveBetween(0.1, 3.1, Double.NaN));
                assertEquals("The value NaN is not in the specified exclusive range of 0.1 to 3.1", ex.getMessage());
            }

            @Test
            void shouldThrowIllegalArgumentExceptionWithDefaultMessageWhenValueIsLowerBound() {
                final IllegalArgumentException ex = assertIllegalArgumentException(
                    () -> Validate.exclusiveBetween(0.1, 3.1, 0.1));
                assertEquals("The value 0.1 is not in the specified exclusive range of 0.1 to 3.1", ex.getMessage());
            }

            @Test
            void shouldThrowIllegalArgumentExceptionWithDefaultMessageWhenValueIsUpperBound() {
                final IllegalArgumentException ex = assertIllegalArgumentException(
                    () -> Validate.exclusiveBetween(0.1, 3.1, 3.1));
                assertEquals("The value 3.1 is not in the specified exclusive range of 0.1 to 3.1", ex.getMessage());
            }

            @Test
            void shouldThrowIllegalArgumentExceptionWithDefaultMessageWhenValueIsAboveUpperBound() {
                final IllegalArgumentException ex = assertIllegalArgumentException(
                    () -> Validate.exclusiveBetween(0.1, 3.1, 4.1));
                assertEquals("The value 4.1 is not in the specified exclusive range of 0.1 to 3.1", ex.getMessage());
            }

            @Test
            void shouldThrowIllegalArgumentExceptionWithDefaultMessageWhenValueIsBelowLowerBound() {
                final IllegalArgumentException ex = assertIllegalArgumentException(
                    () -> Validate.exclusiveBetween(0.1, 3.1, 0.01));
                assertEquals("The value 0.01 is not in the specified exclusive range of 0.1 to 3.1", ex.getMessage());
            }
        }
    }

    @Nested
    final class InclusiveBetweenDouble {

        @Nested
        final class WithMessage {

            @Test
            void shouldNotThrowExceptionWhenValueIsBetweenBounds() {
                Validate.inclusiveBetween(0.1, 3.1, 2.1, "MSG");
            }

            @Test
            void shouldNotThrowExceptionWhenValueIsLowerBound() {
                Validate.inclusiveBetween(0.1, 3.1, 0.1, "MSG");
            }

            @Test
            void shouldNotThrowExceptionWhenValueIsUpperBound() {
                Validate.inclusiveBetween(0.1, 3.1, 3.1, "MSG");
            }

            @Test
            void shouldThrowIllegalArgumentExceptionWithGivenMessageWhenValueIsNaN() {
                final IllegalArgumentException ex = assertIllegalArgumentException(
                    () -> Validate.inclusiveBetween(0.1, 3.1, Double.NaN, "MSG"));
                assertEquals("MSG", ex.getMessage());
            }

            @Test
            void shouldThrowIllegalArgumentExceptionWithGivenMessageWhenValueIsAboveUpperBound() {
                final IllegalArgumentException ex = assertIllegalArgumentException(
                    () -> Validate.inclusiveBetween(0.1, 3.1, 4.1, "MSG"));
                assertEquals("MSG", ex.getMessage());
            }

            @Test
            void shouldThrowIllegalArgumentExceptionWithGivenMessageWhenValueIsBelowLowerBound() {
                final IllegalArgumentException ex = assertIllegalArgumentException(
                    () -> Validate.inclusiveBetween(0.1, 3.1, 0.01, "MSG"));
                assertEquals("MSG", ex.getMessage());
            }
        }

        @Nested
        final class WithoutMessage {

            @Test
            void shouldNotThrowExceptionWhenValueIsBetweenBounds() {
                Validate.inclusiveBetween(0.1, 3.1, 2.1);
            }

            @Test
            void shouldNotThrowExceptionWhenValueIsLowerBound() {
                Validate.inclusiveBetween(0.1, 3.1, 0.1);
            }

            @Test
            void shouldNotThrowExceptionWhenValueIsUpperBound() {
                Validate.inclusiveBetween(0.1, 3.1, 3.1);
            }

            @Test
            void shouldThrowIllegalArgumentExceptionWithDefaultMessageWhenValueIsNaN() {
                final IllegalArgumentException ex = assertIllegalArgumentException(
                    () -> Validate.inclusiveBetween(0.1, 3.1, Double.NaN));
                assertEquals("The value NaN is not in the specified inclusive range of 0.1 to 3.1", ex.getMessage());
            }

            @Test
            void shouldThrowIllegalArgumentExceptionWithDefaultMessageWhenValueIsAboveUpperBound() {
                final IllegalArgumentException ex = assertIllegalArgumentException(
                    () -> Validate.inclusiveBetween(0.1, 3.1, 4.1));
                assertEquals("The value 4.1 is not in the specified inclusive range of 0.1 to 3.1", ex.getMessage());
            }

            @Test
            void shouldThrowIllegalArgumentExceptionWithDefaultMessageWhenValueIsBelowLowerBound() {
                final IllegalArgumentException ex = assertIllegalArgumentException(
                    () -> Validate.inclusiveBetween(0.1, 3.1, 0.01));
                assertEquals("The value 0.01 is not in the specified inclusive range of 0.1 to 3.1", ex.getMessage());
            }
        }
    }
}
