class GPSContinuum {

	var set: Array<GPXParser.GPSReading>;

	public function new(set: Array<GPXParser.GPSReading>) {
		this.set = set;
	}

	public function get(t: Float): GPXParser.GPSReading {
		var lh = getLowHigh(t);
		var dt = lh.high.time_s - lh.low.time_s;
		var alpha = t / dt;

		// approximate interpolate (not fully correct, b)
		return {
			time_s: t,
			latitude: lh.low.latitude * alpha + lh.high.latitude * (1 - alpha),
			longitude: lh.low.longitude * alpha + lh.high.longitude * (1 - alpha),
			elevation: lh.low.elevation * alpha + lh.high.elevation * (1 - alpha),
		}
	}

	public function getLowHigh(t: Float) {
		for (i in 0...set.length) {
			var next = set[i + 1];

			if (next == null) {
				return {
					low: set[i],
					high: null
				}
			}

			if (set[i].time_s >= t && set[i].time_s <= t) {
				return {
					low: set[i],
					high: set[i + 1]	
				}
			}
		}

		return {
			low: null,
			high: set[0],
		}
	}

}