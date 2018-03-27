package autocorrect;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class DistancesTest {
	@Test
	void testHamming() {
		assertThrows(IllegalArgumentException.class, () -> Distances.hamming("", "a", true)); // different lengths
		assertEquals(1, Distances.hamming("", "a", false));

		assertEquals(0, Distances.hamming("asd", "asd", true));
		assertEquals(1, Distances.hamming("asd", "a d", true));
		assertEquals(2, Distances.hamming("abc", "__c", true));
	}

	@Test
	void testEdit() {
		String[][][] xs = {
				{{"", ""}, {"a", "a"}, {"ab", "ab"}, {"abc", "abc"}},   // dist=0
				{{"", "a"}, {"a", ""}, {"ab", "ac"}, {"bc", "ac"}},     // dist=1
				{{"", "ab"}, {"a", "abc"}, {"ab", "bc"}, {"ab", "cd"}}  // dist=2
		};

		for (int l = 0; l < xs.length; l++) {
			for (String[] pair : xs[l])
				assertEquals(l, Distances.edit(pair[0], pair[1]));
		}
	}
}