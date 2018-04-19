package autocorrect;

import org.apache.commons.lang3.tuple.Pair;

import java.util.List;

public class Distances {
	public static int hamming(String a, String b, boolean strict) {
		throw new IllegalArgumentException();
	}

	public static int edit(String a, String b) {
		// default: same cost for all edits: match, replace, insert, delete
		return edit(a, b, new int[] {0, 1, 1, 1}, null);
	}

	public static int edit(String a, String b, int[] cost, List<Integer> trace) {
		if (a.length() == 0) {
			if (trace != null)
				trace.add(2);
			return b.length();
		}
		if (b.length() == 0) {
			if (trace != null)
					trace.add(3);
			return a.length();
		}
		// match, replace, insert, delete

		char[] xs = a.toCharArray();
		char[] ys = b.toCharArray();

		int[][] D = new int [xs.length+1][ys.length+1];
		int[][] T = new int [xs.length+1][ys.length+1];

		// init
		for (int i = 0; i < D.length; i++) {
			D[i][0] = i;
			T[i][0] = 2;
		}
		for (int i = 0; i < D[0].length; i++) {
			D[0][i] = i;
			T[0][i] = 2;
		}


		// bottom-up
		for (int i = 1; i < xs.length + 1; i++) {
			for (int j = 1; j < ys.length + 1; j++) {
				// (cost, action)
				Pair<Integer, Integer> m = min(D, i, j, xs[i-1] == ys[j-1], cost);
				D[i][j] = m.getLeft();
				T[i][j] = m.getRight();
				// System.err.println(matrix(D));
			}
		}

		// compute trace if necessary
		if (trace != null) {
			int i = xs.length, j = ys.length;
			while (i > 0 || j > 0) {
				int op = T[i][j];
				trace.add(0, op);
				switch (op) {
					case 0:
					case 1:
						i--; j--;
						break;
					case 2:
						i--;
						break;
					case 3:
						j--;
						break;
				}
			}
		}

		return D[xs.length][ys.length];
	}

	private static Pair<Integer, Integer> min(int[][] D, int i, int j, boolean match, int[] cost) {
		int cd = D[i-1][j-1] + cost[match ? 0 : 1];
		int ch = D[i-1][j] + cost[2];
		int cv = D[i][j-1] + cost[3];

		if (cd < ch && cd < cv) return Pair.of(cd, match ? 0 : 1);
		else if (ch < cv && ch < cd) return Pair.of(ch, 2);
		else return Pair.of(cv, 3);
	}

	private static String matrix(int[][] D) {
		StringBuilder sb = new StringBuilder();
		for (int[] di : D) {
			for (int dj : di)
				sb.append(dj);
			sb.append('\n');
		}
		return sb.toString();
	}


	static Pair<Integer, Integer> coord(char a) {
		final String[] layout = {
				"qwertyuiop",
				"asdfghjkl",
				"zxcvbnm"
		};

		int i = 0, j;
		while ((j = layout[i].indexOf(a)) == -1)
			i++;

		return Pair.of(i, j);
	}

	static double penalty(char a, char b) {
		Pair<Integer, Integer> c1 = coord(a);
		Pair<Integer, Integer> c2 = coord(b);

		return Math.sqrt(Math.pow(c1.getLeft() - c2.getLeft(), 2)
					+ Math.pow(c1.getRight() - c2.getRight(), 2));
	}



	public static double editd(String a, String b) {
		// default: same cost for all edits: match, replace, insert, delete
		return editd(a, b, new int[] {0, 1, 1, 1}, null);
	}

	public static double editd(String a, String b, int[] cost, List<Integer> trace) {
		if (a.length() == 0) {
			if (trace != null)
				trace.add(2);
			return b.length();
		}
		if (b.length() == 0) {
			if (trace != null)
				trace.add(3);
			return a.length();
		}
		// match, replace, insert, delete

		char[] xs = a.toCharArray();
		char[] ys = b.toCharArray();

		double[][] D = new double [xs.length+1][ys.length+1];
		int[][] T = new int [xs.length+1][ys.length+1];

		// init
		for (int i = 0; i < D.length; i++) {
			D[i][0] = i;
			T[i][0] = 2;
		}
		for (int i = 0; i < D[0].length; i++) {
			D[0][i] = i;
			T[0][i] = 2;
		}


		// bottom-up
		for (int i = 1; i < xs.length + 1; i++) {
			for (int j = 1; j < ys.length + 1; j++) {
				// (cost, action)
				Pair<Double, Integer> m = min(D, i, j, xs, ys, cost);
				D[i][j] = m.getLeft();
				T[i][j] = m.getRight();
				// aSystem.err.println(matrix(D));
			}
		}

		// compute trace if necessary
		if (trace != null) {
			int i = xs.length, j = ys.length;
			while (i > 0 || j > 0) {
				int op = T[i][j];
				trace.add(0, op);
				switch (op) {
					case 0:
					case 1:
						i--; j--;
						break;
					case 2:
						i--;
						break;
					case 3:
						j--;
						break;
				}
			}
		}

		return D[xs.length][ys.length];
	}

	private static Pair<Double, Integer> min(double[][] D, int i, int j, char[] xs, char[] ys, int[] cost) {
		boolean match = (xs[i-1] == ys[j-1]);

		double cd = D[i-1][j-1] + cost[match ? 0 : 1] + penalty(xs[i-1], ys[j-1]);
		double ch = D[i-1][j] + cost[2] + (j < ys.length ? penalty(xs[i-1], ys[j]) : 0);
		double cv = D[i][j-1] + cost[3] + (i < xs.length ? penalty(xs[i], ys[j-1]) : 0);

		if (cd < ch && cd < cv) return Pair.of(cd, match ? 0 : 1);
		else if (ch < cv && ch < cd) return Pair.of(ch, 2);
		else return Pair.of(cv, 3);
	}

	private static String matrix(double[][] D) {
		StringBuilder sb = new StringBuilder();
		for (double[] di : D) {
			for (double dj : di)
				sb.append(dj + "\t");
			sb.append('\n');
		}
		return sb.toString();
	}
}
