package dtw;

import com.github.sikoried.jstk.io.FrameInputStream;
import com.github.sikoried.jstk.util.Distances;
import org.apache.commons.lang3.tuple.Pair;

import java.io.File;
import java.io.IOException;
import java.util.Arrays;
import java.util.Comparator;
import java.util.LinkedList;
import java.util.List;

public class Erkenner {
	public static double distance(double[][] xs, double[][] ys) {
		if (xs.length == 0)
			return Double.MAX_VALUE;

		if (ys.length == 0)
			return Double.MAX_VALUE;

		double[][] D = new double [xs.length][ys.length];

		// init; make it favor "top-left"
		D[0][0] = Distances.euclidean(xs[0], ys[0]);
		for (int i = 1; i < D.length; i++) {
			D[i][0] = Distances.euclidean(xs[i], ys[0]);
		}
		for (int i = 1; i < D[0].length; i++) {
			D[0][i] = Distances.euclidean(xs[0], ys[i]);
		}


		// bottom-up
		for (int i = 1; i < xs.length; i++) {
			for (int j = 1; j < ys.length; j++) {

				double cd = D[i-1][j-1] + Distances.euclidean(xs[i], ys[j]);
				double ch = D[i-1][j] + (j < ys.length-1 ? Distances.euclidean(xs[i], ys[j+1]) : 0);
				double cv = D[i][j-1] + (i < xs.length-1 ? Distances.euclidean(xs[i+1], ys[j]) : 0);

				D[i][j] = min(cd, ch, cv);
			}
		}

		return D[xs.length-1][ys.length-1];
	}

	private static double min(double... d) {
		Arrays.sort(d);
		return d[0];
	}

	public static void main(String[] args) throws IOException {

		String[] samples = {"holzfaeller.ft", "hoschnitzel.ft"};
		double[][][] protos = new double [samples.length][][];

		// read prototype words
		for (int i = 0; i < samples.length; i++) {
			FrameInputStream fis = new FrameInputStream(new File(samples[i]));
			List<double[]> merkmale = new LinkedList<>();
			double[] buf = new double[fis.getFrameSize()];
			while (fis.read(buf))
				merkmale.add(buf.clone());

			protos[i] = merkmale.toArray(new double[merkmale.size()][]);

			fis.close();
		}

		for (int i = 0; i < args.length; i++) {
			FrameInputStream fis = new FrameInputStream(new File(args[i]));
			List<double[]> merkmale = new LinkedList<>();
			double[] buf = new double[fis.getFrameSize()];
			while (fis.read(buf))
				merkmale.add(buf.clone());

			double[][] hyp = merkmale.toArray(new double[merkmale.size()][]);

			// score against all words, sort ascending (it's a distance!)
			List<Pair<String, Double>> scores = new LinkedList<>();
			for (int j = 0; j < protos.length; j++)
				scores.add(Pair.of(samples[j], distance(hyp, protos[j]) / Math.max(hyp.length, protos[j].length)));
			scores.sort(Comparator.comparingDouble(Pair::getRight));

			System.out.println(args[i] + ": " + scores);
			fis.close();
		}
	}
}
