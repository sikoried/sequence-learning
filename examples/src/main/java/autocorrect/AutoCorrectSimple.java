package autocorrect;

import org.apache.commons.lang3.tuple.Pair;
import org.apache.commons.lang3.tuple.Triple;

import java.io.*;
import java.util.*;
import java.util.stream.Collectors;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

public class AutoCorrectSimple {
	private Map<String, Double> logpw;
	public AutoCorrectSimple(Map<String, Double> logpw) {
		this.logpw = logpw;
	}

	public List<Pair<String, Double>> suggest(String x) {
		// return suggestA(x, 2, 10);
		return suggestB(x, 2, 10, 0.2, 1.0);
	}

	/**
	 * Suggest words. Heuristic is that there is exactly one suggestion if there's a lexicon match,
	 * or otherwise first all hits with edit distance 1 ranked by P(w), then all with dist=2 etc.
	 * @url{https://en.wikipedia.org/wiki/Exponential_distribution}
	 * @param x word
	 * @param m max edits
	 * @param n maximum number of suggestions
	 * @return
	 */
	public List<Pair<String, Double>> suggestA(String x, int m, int n) {
		List<Pair<String, Double>> li = new LinkedList<>();

		// exact hit
		if (logpw.containsKey(x)) {
			li.add(Pair.of(x, 0.0));
			return li;
		}

		// compute edit dists, join with freq
		List<Triple<String, Integer, Double>> cands = new LinkedList<>();

		for (Map.Entry<String, Double> e : logpw.entrySet()) {
			if (Math.abs(x.length() - e.getKey().length()) > m)
				continue;
			int ed = Distances.edit(x, e.getKey());
			if (ed <= m)
				cands.add(Triple.of(e.getKey(), ed, e.getValue()));
		}

		// sort by edit, then by freq, limit to n
		return cands.stream()
				.sorted(Comparator.comparingInt(Triple<String, Integer, Double>::getMiddle)
						.thenComparing((t1, t2) -> Double.compare(t2.getRight(), t1.getRight())))
				.map(t -> Pair.of(t.getLeft(), t.getRight()))
				.limit(n)
				.collect(Collectors.toList());
	}

	/**
	 * Suggest words. Heuristic is to model P(x|w)^z P(w) where P(x|w) ~ exp(-lambda*d), d=dist,
	 * and lambda dampens the exponential distribution and z is a weighting factor to balance the two probabilities
	 * We'll apply logarithm, so that the score becomes -z*lambda*d + log(P(w))
	 * @param x word
	 * @param m max edits
	 * @param n max number of suggestions
	 * @param lambda weighting for exponential function (0.2 yields about .5 likelihood for edit distance 2)
	 * @param z weighting factor for P(x|w)
	 * @return
	 */
	public List<Pair<String, Double>> suggestB(String x, int m, int n, double lambda, double z) {
		List<Pair<String, Double>> li = new LinkedList<>();

		// exact hit
		if (logpw.containsKey(x)) {
			li.add(Pair.of(x, 0.0));
			return li;
		}

		// here, we can directly compute the scores:
		for (Map.Entry<String, Double> e : logpw.entrySet()) {
			// discard if too far away
			if (Math.abs(x.length() - e.getKey().length()) > m)
				continue;

			// compute edit distance; discard if too far away
			int ed = Distances.edit(x, e.getKey());
			if (ed > m)
				continue;

			double score = -lambda * z * ed + e.getValue();  // we actually have lop(P(w))
			li.add(Pair.of(e.getKey(), score));
		}

		// sort (log-)likelihood, descending, limit to 15
		return li.stream()
				.sorted((a, b) -> Double.compare(b.getValue(), a.getValue()))
				.limit(n)
				.collect(Collectors.toList());
	}

	public static AutoCorrectSimple fromZippedTextCorpus(File zipFile, String fileName) throws IOException {


		byte[] buffer = new byte[1024];
		ZipInputStream zis = new ZipInputStream(new FileInputStream(zipFile));
		ZipEntry zipEntry = zis.getNextEntry();

		// there should just be a single file
		if (!zipEntry.getName().equals(fileName))
			throw new IOException(fileName + " not first in " + zipFile.getAbsolutePath());

		// read lines
		BufferedReader br = new BufferedReader(new InputStreamReader(zis));

		Map<String, Double> pw = new TreeMap<>();
		String line;
		double sum = 0;
		while ((line = br.readLine()) != null) {
			String[] pair = line.split("\\s+");
			long count = Long.parseLong(pair[1]);
			pw.put(pair[0], Math.log(count));
			sum += count;
		}

		zis.closeEntry();
		zis.close();

		// normalize and log
		sum = Math.log(sum);
		for (Map.Entry<String, Double> e : pw.entrySet()) {
			pw.put(e.getKey(), e.getValue() - sum);
		}

		return new AutoCorrectSimple(pw);
	}

	public static AutoCorrectSimple fromDummy() {
		Map<String, Double> pw = new TreeMap<>();

		String[] mf = {"der", "die", "und", "in", "den", "von", "zu", "das", "mit", "sich", "des", "auf", "für"};

		double norm = Math.log(mf.length);
		for (int i = 0; i < mf.length; i++) {
			pw.put(mf[i], Math.log(mf.length - i) - norm);
		}

		return new AutoCorrectSimple(pw);
	}
}
