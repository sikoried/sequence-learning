package autocorrect;

import org.apache.commons.lang3.tuple.Pair;
import org.junit.jupiter.api.Test;

import java.util.LinkedList;
import java.util.List;

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

		int[] cost = new int[] {0, 1, 1, 1};
		for (int l = 0; l < xs.length; l++) {
			for (String[] pair : xs[l]) {
				List<Integer> trace = new LinkedList<>();
				int d = Distances.edit(pair[0], pair[1], cost, trace);
				assertEquals(l, d);
				System.err.println(pair[0] + ":" + pair[1] + " = " + d + " " + trace);
			}
		}
	}

	@Test
	void testPenalty() {
		assertEquals(Pair.of(0, 0), Distances.coord('q'));
		assertEquals(Pair.of(0, 1), Distances.coord('w'));
		assertEquals(Pair.of(0, 2), Distances.coord('e'));
		assertEquals(Pair.of(1, 0), Distances.coord('a'));
		assertEquals(Pair.of(2, 2), Distances.coord('c'));

		String a = "asdf";
		String b = "qwer";

		for (int i = 0; i < a.length(); i++)
			System.out.println(Distances.penalty(a.charAt(i), b.charAt(i)));
	}

	@Test
	void testEditd() {
		String[][] xs = {
				{"hans", "haus"},
				{"hans", "hajs"},
				{"hans", "wans"},
				{"hans", "hans"}
		};

		int[] cost = new int[] {0, 1, 1, 1};

		for (String[] pair : xs) {
			List<Integer> trace = new LinkedList<>();
			double d = Distances.editd(pair[0], pair[1], cost, trace);
			System.err.println(pair[0] + ":" + pair[1] + " = " + d + " " + trace);
		}
	}
}