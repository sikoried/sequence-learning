package com.github.sikoried.sl.autocorrect;

import org.junit.jupiter.api.Test;

import java.io.*;

class AutoCorrectSimpleTest {

	@Test
	void testSuggest() {
		AutoCorrectSimple ac = AutoCorrectSimple.fromDummy();

		String[] xs = {"der", "die", "det", "soch", "sichxx"};

		for (String x : xs) {
			System.out.println(x + " => " + ac.suggestA(x, 2, 10));
			System.out.println(x + " => " + ac.suggestB(x, 2, 10, 0.2, 1.0));
			System.out.println(x + " => " + ac.suggestD(x, 2, 10, 0.2, 1.0));
		}
	}

	@Test
	void testSuggestLarge() throws IOException {
		ClassLoader classLoader = AutoCorrectSimple.class.getClassLoader();
		File file = new File(classLoader.getResource("count_1w.txt.zip").getFile());

		AutoCorrectSimple ac = AutoCorrectSimple.fromZippedTextCorpus(file, "count_1w.txt");

		String[] xs = {"soch", "sichxx", "shageshpear", "sheapard"};

		for (String x : xs) {
			System.out.println(x + " => " + ac.suggestA(x, 2, 10));
			System.out.println(x + " => " + ac.suggestB(x, 2, 10, 0.2, 1.0));
			System.out.println(x + " => " + ac.suggestD(x, 2, 10, 1.0, 1.0));  // dist ist wichtiger
		}

		String in = "shagesbeer";
		System.out.println("Simulating suggest-as-typing: " + in);

		for (int i = 1; i < in.length(); ++i) {
			String x = in.substring(0, i+1);
			System.out.println(x + " => " + ac.suggestD(x, 3, 5, 1.0, 1.0));
		}

	}
}